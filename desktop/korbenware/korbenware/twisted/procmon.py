# This code heavily modifies Twisted.runner.procmon and contains substantial
# portions of its code.
#
# Copyright 2020 Josh Holbrook
# Copyright (c) 2001-2020
# Allen Short
# Amber Hawkie Brown
# Andrew Bennetts
# Andy Gayton
# Antoine Pitrou
# Apple Computer, Inc.
# Ashwini Oruganti
# Benjamin Bruheim
# Bob Ippolito
# Canonical Limited
# Christopher Armstrong
# Ciena Corporation
# David Reid
# Divmod Inc.
# Donovan Preston
# Eric Mangold
# Eyal Lotem
# Google Inc.
# Hybrid Logic Ltd.
# Hynek Schlawack
# Itamar Turner-Trauring
# James Knight
# Jason A. Mobarak
# Jean-Paul Calderone
# Jessica McKellar
# Jonathan D. Simms
# Jonathan Jacobs
# Jonathan Lange
# Julian Berman
# Jürgen Hermann
# Kevin Horn
# Kevin Turner
# Laurens Van Houtven
# Mary Gardiner
# Massachusetts Institute of Technology
# Matthew Lefkowitz
# Moshe Zadka
# Paul Swartz
# Pavel Pergamenshchik
# Rackspace, US Inc.
# Ralph Meijer
# Richard Wall
# Sean Riley
# Software Freedom Conservancy
# Tavendo GmbH
# Thijs Triemstra
# Thomas Grainger
# Thomas Herve
# Timothy Allen
# Tom Most
# Tom Prince
# Travis B. Hartwell
#
# and others that have contributed code to the public domain.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Classes for managing processes. Builds on top of twisted.runner.procmon
but includes a number of extensions.

See: https://github.com/twisted/twisted/blob/trunk/src/twisted/runner/procmon.py  # noqa
"""

from enum import Enum
import attr

from pyee import TwistedEventEmitter as EventEmitter
from twisted.internet.error import ProcessExitedAlready
from korbenware.logger import create_logger
from twisted.runner.procmon import ProcessMonitor as BaseMonitor

from korbenware.keys import keys
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable

# Hold my beer.
#
# This should hopefully be temporary, since it sounds like they're very much
# open to refactoring this. The refactored version also will support
# separating stdout and stderr.
#
# See: https://twistedmatrix.com/trac/ticket/9657#9657

from twisted.runner.procmon import LineLogger, LoggingProtocol


def patchedLineReceived(self, line):
    try:
        line = line.decode("utf-8")
    except UnicodeDecodeError:
        line = repr(line)

    self.service.log.info("[{tag}] {line}", tag=self.tag, line=line)


def patchedConnectionMade(self):
    originalConnectionMade(self)
    self.output.service = self.service


if not hasattr(BaseMonitor, "log"):
    LineLogger.lineReceived = patchedLineReceived
    originalConnectionMade = LoggingProtocol.connectionMade

    LoggingProtocol.connectionMade = patchedConnectionMade


# OK cool, hand me my beer.


class LifecycleState(Enum):
    """
    The lifecycle state enum of a process monitored by a ProcessMonitor.
    """

    STARTING = "STARTING"
    RUNNING = "RUNNING"
    RESTARTING = "RESTARTING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


@markdownable
@representable
@attr.s
class ProcessSettings:
    """
    The process management settings for a process.
    """

    restart = attr.ib(default=False)
    cleanup = attr.ib(default=False)
    threshold = attr.ib(default=None)
    killTime = attr.ib(default=None)
    minRestartDelay = attr.ib(default=None)
    maxRestartDelay = attr.ib(default=None)


@markdownable
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


@markdownable
@representable
@keys(["settings", "states"])
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
    * 'serviceStarted' - The ProcessMonitor has stopped and all processes have
      started.
    * 'stopService' - The ProcessMonitor is stopping.
    * 'serviceStopped' - The ProcessMonitor has stopped and all processes have
      exited.
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
    * 'stateChange' - A process's state has changed.
      - state: ProcessState - the new state of the process
    """

    restart = False
    log = create_logger()

    def __init__(self, log=None, reactor=None):
        if reactor:
            BaseMonitor.__init__(self, reactor=reactor)
        else:
            BaseMonitor.__init__(self)

        EventEmitter.__init__(self)

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
            raise KeyError(f"Unrecognized process name: {name}")

    def _setProcessState(self, name, state):
        self.states[name] = state
        self.emit("stateChange", dict(name=name, state=state))

    def getState(self, name):
        """
        Fetch and package the internal state of the process. Note that this
        will always return a ProcessState even if the internal state is
        malformed or missing.
        """
        self.assertRegistered(name)
        return ProcessState(
            name=name,
            state=self.states.get(name, None),
            settings=self.settings.get(name, None),
        )

    def addProcess(
        self,
        name,
        args,
        *,
        env=None,
        cwd=None,
        uid=None,
        gid=None,
        restart=False,
        cleanup=None,
        threshold=None,
        killTime=None,
        minRestartDelay=None,
        maxRestartDelay=None,
    ):
        """
        Add a new monitored process. If the service is running, start it
        immediately.
        """

        env = dict() if env is None else env

        if name in self.states:
            raise KeyError(f"Process {name} already exists! Try removing it first.")

        state = LifecycleState.STOPPED

        settings = ProcessSettings(restart=restart)

        if restart:
            settings.threshold = threshold if threshold is not None else self.threshold
            settings.killTime = killTime if killTime is not None else self.killTime
            settings.minRestartDelay = (
                minRestartDelay if minRestartDelay is not None else self.minRestartDelay
            )
            settings.maxRestartDelay = (
                maxRestartDelay if maxRestartDelay is not None else self.maxRestartDelay
            )
            settings.cleanup = False
        else:
            settings.cleanup = cleanup if cleanup is not None else True

        self._setProcessState(name, state)
        self.settings[name] = settings

        self.emit("addProcess", self.getState(name))

        super().addProcess(name, args, uid, gid, env, cwd)

    def removeProcess(self, name):
        """
        Remove a process. This stops the process and then removes all state
        from the process monitor.

        This currently isn't well-tested and I suspect that code paths
        triggered by stopping the process may cause async race conditions.
        It's therefore recommended that you manually stop processes first,
        before exiting.
        """
        self.emit("removeProcess", self.getState(name))
        super().removeProcess(name)
        del self.settings[name]
        del self.states[name]

    def _allServicesRunning(self):
        return all(state == LifecycleState.RUNNING for state in self.states.values())

    def startService(self):
        """
        Start the service, which starts all the processes.
        """
        self.emit("startService")
        super().startService()

        def maybe_emit(state):
            if self._allServicesRunning():
                self.remove_listener("stateChange", maybe_emit)
                self.emit("serviceStarted")

        if self._allServicesRunning():
            self.emit("serviceStarted")
        else:
            self.on("stateChange", maybe_emit)

    def _allServicesStopped(self):
        return all(state == LifecycleState.STOPPED for state in self.states.values())

    def stopService(self):
        """
        Stop the service, which stops all the processes.
        """
        self.emit("stopService")
        super().stopService()

        def maybe_emit(state):
            if self._allServicesStopped():
                self.emit("serviceStopped")

        if self._allServicesStopped():
            self.emit("serviceStopped")
        else:
            self.on("stateChange", maybe_emit)

    def _isActive(self, name):
        return self.isRegistered(name) and self.states[name] in {
            LifecycleState.RUNNING,
            LifecycleState.STOPPING,
        }

    def _spawnProcess(self, *args, **kwargs):
        return self._reactor.spawnProcess(*args, **kwargs)

    def startProcess(self, name):
        """
        Start a process. Updates the state to RUNNING.
        """
        # Unlike in procmon, we track process status in a dict so we
        # should check that to see the state

        self.assertRegistered(name)
        if self._isActive(name):
            return

        self.emit("startProcess", self.getState(name))

        # Should be smooth sailing - This section is the same as in procmon
        process = self._processes[name]

        proto = LoggingProtocol()
        proto.service = self
        proto.name = name
        self.protocols[name] = proto
        self.timeStarted[name] = self._reactor.seconds()
        self._spawnProcess(
            proto,
            process.args[0],
            process.args,
            uid=process.uid,
            gid=process.gid,
            env=process.env,
            path=process.cwd,
        )

        # This is new though!
        self._setProcessState(name, LifecycleState.RUNNING)

    def connectionLost(self, name):
        """
        Called when a monitored process exits. Overrides the base
        ProcessMonitor behavior to use per-process parameters, track state
        for external observation, and by default actually does not restart the
        process.
        """
        priorState = self.states[name]
        settings = self.settings[name]

        restartSetting = settings.restart

        # Update our state depending on what it was when the process exited
        if priorState in {LifecycleState.STARTING, LifecycleState.RUNNING}:
            # We expected the process to be running - we should fall back to
            # our individual settings for restarts
            shouldRestart = restartSetting

            # State should either be RESTARTING or STOPPED
            self.states[name] = (
                LifecycleState.RESTARTING if shouldRestart else LifecycleState.STOPPED
            )
        elif priorState == LifecycleState.RESTARTING:
            # OK, we're explicitly restarting
            shouldRestart = True
        elif priorState == LifecycleState.STOPPING:
            # OK, we're explicitly quitting
            shouldRestart = False
            self._setProcessState(name, LifecycleState.STOPPED)
        elif priorState == LifecycleState.STOPPED:
            # This shouldn't happen but if it does we *definitely* don't want
            # to restart
            shouldRestart = False

        shouldCleanup = not shouldRestart and settings.cleanup

        self.emit("connectionLost", self.getState(name))

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
                    nextDelay, self.startProcess, name
                )
        elif shouldCleanup:
            # If this is a no-restart yes-cleanup process then remove it
            # on exit
            self.removeProcess(name)

    def _forceStopProcess(self, name, proc):
        self.emit("forceStop", self.getState(name))
        super()._forceStopProcess(proc)

    def hasProcess(self, name):
        """
        Check whether a process is defined with that name.
        """
        return name in self.states

    def restartProcess(self, name):
        """
        Manually restart a process, regardless of how it's been configured.
        """
        self._setProcessState(name, LifecycleState.RESTARTING)
        self.emit("restartProcess", self.getState(name))
        self._stopProcess(self, name)

    def stopProcess(self, name):
        """
        Stop a process.
        """
        self._setProcessState(name, LifecycleState.STOPPING)
        self.emit("stopProcess", self.getState(name))
        self._stopProcess(name)

    def _stopProcess(self, name):
        self.assertRegistered(name)

        self._setProcessState(name, LifecycleState.STOPPING)

        proto = self.protocols.get(name, None)

        if proto is None:
            # If the proto isn't there then the process is definitely already
            # stopped.
            self._setProcessState(name, LifecycleState.STOPPED)
        else:
            # Same as procmon
            proc = proto.transport
            try:
                proc.signalProcess("TERM")
            except ProcessExitedAlready:
                pass
            else:
                self.murder[name] = self._reactor.callLater(
                    self.killTime, self._forceStopProcess, name, proc
                )

    def restartAll(self):
        """
        Manually restart all processes, regardless of how they've been configured.
        """
        for name in self._processes:
            self.restartProcess(name)

    def asdict(self):
        return dict(
            running=self.running,
            processes={name: self.getState(name) for name in self.states},
        )
