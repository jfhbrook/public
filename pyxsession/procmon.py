"""
Classes for managing processes. Builds on top of twisted.runner.procmon
but includes a number of extensions.

See: https://github.com/twisted/twisted/blob/trunk/src/twisted/runner/procmon.py  # noqa
"""

# Note to self: twisted is MIT licensed.

from enum import Enum
import attr
from pyee import TwistedEventEmitter as EventEmitter
from twisted.logger import Logger
from twisted.runner.procmon import ProcessMonitor as BaseMonitor

from pyxsession.util.decorators import representable

# Hold my beer.
#
# This should hopefully be temporary, since it sounds like they're very much
# open to refactoring this. The refactored version also will support
# separating stdout and stderr.
#
# See: https://twistedmatrix.com/trac/ticket/9657#9657

from twisted.runner.procmon import LoggingProtocol, ProcessProtocol



def patchedLineReceived(self, line):
    try:
        line = line.decode('utf-8')
    except UnicodeDecodeError:
        line = repr(line)

    self.service.log(
        u'[{tag}] {line}',
        tag=self.tag,
        line=line
    )



LoggingProtocol.lineReceived = patchedLineReceived
originalConnectionMade = LoggingProtocol.connectionMade



def patchedConnectionMade(self):
    originalConnectionMade(self)
    self.output.service = self.service



LoggingProtocol.connectionMade = patchedConnectionMade

# OK cool, hand me my beer.



class LifecycleState(Enum):
    """
    The lifecycle state enum of a process monitored by a ProcessMonitor.
    """

    STARTING='STARTING'
    RUNNING='RUNNING'
    QUITTING='QUITTING'
    RESTARTING='RESTARTING'
    STOPPED='STOPPED'


@representable
@attr.s
class ProcessSettings:
    """
    The process management settings for a process.
    """

    restart = attr.ib()
    threshold = attr.ib(default=None)
    killTime = attr.ib(default=None)
    minRestartDelay = attr.ib(default=None)
    maxRestartDelay = attr.ib(default=None)


@representable
@attr.s
class ProcessState:
    """
    The internal state of a process.

    * name: The name of the process
    * state: The lifecycle state of the process
    * settings: The configuration settings used for managing a process.
    """

    name = attr.ib()
    state = attr.ib(default=None)
    settings = attr.ib(default=None)


@representable
class ProcessMonitor(BaseMonitor, EventEmitter):
    """
    A subclass of twisted.runner.procmon#ProcessMonitor. While it implements
    the same interfaces, it also have a number of extensions and behavioral
    changes:

    * Processes can individually be set to restart or, crucially, *not*
      restart - this is the primary use case around the "autostart" freedesktop
      standard. The default is to not restart; it must be explicitly enabled.
    * Processes accept individual arguments for threshold, killTime,
      minRestartDelay and maxRestartDelay. The restart behavior, when enabled,
      is otherwise the same as in twisted.runner.procmon.
    * Emit events as a pyee TwistedEventEmitter for various lifecycle
      behaviors.

    Events:

    * 'startService' - The ProcessMonitor is starting.
    * 'stopService' - The ProcessMonitor is stopping.
    * 'addProcess' - A process is being added.
      - state: ProcessState - The state of the newly-added process.
    * 'removeProcess' - A process is being removed.
      - state: ProcessState - The state of the process at the time of removal.
    * 'startProcess' - A process is being started.
      - state: ProcessState - The state of the process at the time of starting.
    * 'stopProcess' - A process is being stopped.
      - state: ProcessState - The state of the process at the time of it being
        stopped.
    * 'restartProcess' - A process has explicitly been told to restart. This
      event does not fire when a process exits unexpectedly, or is manually
      cycled by calls to stopProcess/startProcess.
      - state: ProcessState - the state of the process at the time of it
        restarting
    * 'connectionLost' - A process has exited.
      - state: ProcessState - the state of the process right before it exited
    * 'forceStop' - A process being stopped timed out and had to be forced to
      stop with a SIGKILL.
      - state: ProcessState - the state of the process being stopped
    """

    restart = False
    log = Logger()


    def __init__(self, log=None, reactor=None):
        if reactor:
            super().__init__(reactor=reactor)
        else:
            super().__init__()

        self.log = log or self.log
        self.settings = dict()
        self.states = dict()


    def isRegistered(self, name):
        """
        Is this process registered?
        """
        return name in self.states


    def assertRegistered(self, name):
        """
        Raises a KeyError if the process isn't registered.
        """
        if not self.isRegistered(name):
            raise KeyError(f'Unrecognized process name: {name}')


    def getState(self, name):
        """
        Fetch and package the internal state of the process. Note that this
        will always return a ProcessState even if the internal state is
        malformed or missing.
        """
        self.assertRegistered(self, name)
        return ProcessState(
            name=name,
            state=self.states.get(name, None),
            settings=self.settings.get(name, None)
        )


    def addProcess(
        self,
        name,
        args,
        *,
        env={}, cwd=None,
        uid=None, gid=None,
        restart=self.restart,
        threshold=self.threshold, killTime=self.killTime,
        minRestartDelay=self.minRestartDelay,
        maxRestartDelay=self.maxRestartDelay
    ):
        """
        Add a new monitored process. If the service is running, start it
        immediately.
        """

        if name in self.states:
            raise KeyError(
                f'Process {name} already exists! Try removing it first.'
            )

        state = ProcessState.STARTING

        settings = ProcessSettings(restart=restart)

        if restart:
            settings.threshold = threshold
            settings.killTime = killTime
            settings.minRestartDelay = minRestartDelay
            settings.maxRestartDelay = maxRestartDelay

        self.state[name] = state
        self.settings[name] = settings

        self.emit('addProcess', self.getState(name))

        super().addProcess(self, name, args, uid, gid, env, cwd)


    def removeProcess(self, name):
        """
        Remove a process. This stops the process and then removes all state
        from the process monitor.

        This currently isn't well-tested and I suspect that code paths
        triggered by stopping the process may cause async race conditions.
        It's therefore recommended that you manually stop processes first,
        before exiting.
        """
        self.emit('removeProcess', self.getState(name))
        super().removeProcess(name)
        del self.settings[name]
        del self.states[name]


    def startService(self):
        """
        Start the service, which starts all the processes.
        """
        self.emit('startService')
        super().startService()


    def stopService(self):
        """
        Stop the service, which stops all the processes.
        """
        self.emit('stopService')
        super().stopService()


    def _isActive(self, name):
        return (
            self.isRegistered(name)
            and
            self.states[name] in {
                ProcessState.RUNNING,
                ProcessState.QUITTING
            }
        )


    def startProcess(self, name):
        """
        Start a process. Updates the state to RUNNING.
        """
        # Unlike in procmon, we track process status in a dict so we
        # should check that to see the state

        self.assertRegistered(self, name)
        if self._isActive(self, name):
            return

        self.emit('startProcess', self.getState(name))

        # Should be smooth sailing - This section is the same as in procmon
        process = self._processes[name]

        proto = LoggingProtocol()
        proto.service = self
        proto.name = name
        self.protocols[name] = proto
        self.timeStarted[name] = self._reactor.seconds()
        self._reactor.spawnProcess(proto, process.args[0], process.args,
                                          uid=process.uid, gid=process.gid,
                                          env=process.env, path=process.cwd)

        # This is new though!
        self.states[name] = ProcessState.RUNNING


    def connectionLost(self, name):
        """
        Called when a monitored process exits. Overrides the base
        ProcessMonitor behavior to use per-process parameters, track state
        for external observation, and by default actually does not restart the
        process.
        """

        priorState = self.states[name]['state']
        settings = self.settings[name]

        self.emit('connectionLost', self.getState(name))

        restartSetting = settings.restart

        # Update our state depending on what it was when the process exited
        if priorState in {ProcessState.STARTING, ProcessState.RUNNING}:
            # We expected the process to be running - we should fall back to
            # our individual settings for restarts
            shouldRestart = restartSetting

            # State should either be RESTARTING or STOPPED
            self.states[name] = (
                ProcessState.RESTARTING
                if shouldRestart
                else ProcessState.STOPPED
            )
        elif priorState == ProcessState.RESTARTING:
            # OK, we're explicitly restarting
            shouldRestart = True
        elif priorState == ProcessState.QUITTING:
            # OK, we're explicitly quitting
            shouldRestart = False
            self.states[name] = ProcessState.STOPPED
        elif priorState == ProcessState.STOPPED:
            # TODO: Warn, this shouldn't happen
            pass

        # This chunk is straight from procmon - this is clearing force
        # quit timeouts
        if name in self.murder:
            if self.murder[name].active():
                self.murder[name].cancel()
            del self.murder[name]

        del self.protocols[name]

        # Pulling in our per-process settings...

        threshold = settings.threshold
        minRestartDelay = settings.minRestartDelay
        maxRestartDelay = settings.maxRestartDelay

        if shouldRestart:
            # This section is also largely copied from procmon
            if self._reactor.seconds() - self.timeStarted[name] < threshold:
                nextDelay = self.delay[name]
                self.delay[name] = min(self.delay[name] * 2, maxRestartDelay)

            else:
                nextDelay = 0
                self.delay[name] = minRestartDelay

            if self.running and name in self._processes:
                self.restart[name] = self._reactor.callLater(
                    nextDelay,
                    self.startProcess,
                    name
                )


    def _forceStopProcess(self, name, proc):
        self.emit('forceStop', self.getState(name))
        super()._forceStopProcess(self, proc)


    def restartProcess(self, name):
        """
        Manually restart a process, regardless of how it's been configured,
        """
        self.states[name] = ProcessState.RESTARTING
        self.emit('restartProcess', self.getState(name))
        self._stopProcess(self, name)


    def stopProcess(self, name):
        """
        Stop a process.
        """
        self.states[name] = ProcessState.STOPPING
        self.emit('stopProcess', self.getState(name))
        self._stopProcess(self, name)


    def _stopProcess(self, name):
        self.assertRegistered(name)

        self.states[name] = ProcessState.STOPPING

        # Same as procmon
        proto = self.protocols.get(name, None)
        if proto is not None:
            proc = proto.transport
            try:
                proc.signalProcess('TERM')
            except error.ProcessExitedAlready:
                pass
            else:
                self.murder[name] = self._reactor.callLater(
                                            self.killTime,
                                            self._forceStopProcess, name, proc)


    def restartAll(self):
        """
        Manually restart all processes, regardless of how they've been configured.
        """
        for name in self._processes:
            self.restartProcess(name)


    def asdict(self):
        return dict(
            running=self.running,
            processes={
                name: self.getState(name)
                for name in self.states
            }
        }
