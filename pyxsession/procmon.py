# Heavily influenced by https://github.com/twisted/twisted/blob/trunk/src/twisted/runner/procmon.py
# Twisted looks like it's MIT licensed so we should be OK

from twisted.application.service import Service
from twisted.internet import reactor as _reactor
from twisted.internet.error import ProcessExitedAlready
from twisted.internet.protocol import ProcessProtocol as BaseProtocol
from twisted.logger import Logger
from twisted.protocols.basic import LineReceiver

from pyee import TwistedEventEmitter as EventEmitter


class StdioLineReceiver(LineReceiver):
    """
    A LineReceiver used internally to convert binary process output into
    unicode lines.
    """
    delimiter = b'\n'
    name = None

    def lineReceived(self, line):
        try:
            line = line.decode('utf-8')
        except UnicodeDecodeError:
            line = repr(line)

        getattr(self.transport, f'{name}LineReceived')(line)


def _attachRawReceived(cls, pipe):

    def rawReceived(self, data):
        getattr(self, f'{pipe}LineReceiver').dataReceived(data)
        setattr(self, f'_{pipe}Empty', data[-1] == b'\n'

    setattr(cls, f'{pipe}Received', rawReceived)

    return cls


def receivesTextLines(cls):
    """
    A class decorator that interceps calls to outReceived and errReceived,
    uses a StdioLineReceiver to process that output into newline-separated
    unicode, and calls the outLineReceived and errLineReceived methods
    respectively.

    This logic was largely lifted from twisted procmon but modified
    for my own ends (ie not sending both stdout and stderr to a legacy
    logger
    """
    for pipe in ['out', 'err']:
        _attachRawReceived(cls, pipe)

    def initializeLineReceivers(self):
        for pipe in ['out', 'err']:
            receiver = StdioLineReceiver()
            receiver.name = pipe

            setattr(self, f'{pipe}LineReceiver', receiver)

            receiver.makeConnection(self)

    def flushLineReceivers(self):
        for pipe in ['out', 'err']:
            if not getattr(self, f'_{pipe}Empty'):
                getattr(self, f'{pipe}LineReceiver').dataReceived(b'\n')
 

    cls.initializeLineReceivers = initializeLineReceivers

    return cls


# protocols are things that allow reads via callback
@receivesTextLines
class ProcessProtocol(BaseProtocol):
    process = None

    def connectionMade(self):
        self.initializeLineReceivers()

    def outLineReceived(self, line):
        self.process.log('{stream}: {line}', stream='out', line=line)

    def errLineReceived(self, line):
        self.process.log('{stream}: {line}', stream='err', line=line)

    def processEnded(self, status):
        self.flushLineReceivers()

        self.process.emit('exit', status)

        if self.process._forceQuitTimer.active():
            self.process._forceQuitTimer.cancel()
            self.process._forceQuitTimer = None

        # TODO: Implement optional restarts

        self.process._stopService()

class Process(Service, EventEmitter):
    """
    A twisted Service that represents a process that we want to run. A lot
    of the logic is lifted directly from twisted.runner.procmon but modified
    since this is meant to handle the more general case of spawning a process
    that isn't intended to be restarted.
    """

    def __init__(
        self,
        cmd, argv, env=None, path=None,
        uid=None, gid=None,
        killTime=5,
        log=None,
        reactor=_reactor
    ):
        self.reactor = reactor

        self.cmd = cmd
        self.argv = argv
        self.env = env or {}
        self.path = path  # TODO: default this to something "sane"

        self.uid = uid
        self.gid = gid

        self.killTime = killTime

        # TODO: What to do with this log? :)

        self.log = log or Logger()

        self._forceQuitTimer = None

    def startService(self):
        super().startService()

        # TODO: procmon tracks start time, we should track stats too
        # since we'll want to inspect those

        protocol = ProcessProtocol()
        protocol.process = self

        self.protocol = protocol

        self.transport = self._reactor.spawnProcess(
            protocol,
            self.cmd, self.argv,
            env=self.env, path=self.path,
            uid=self.uid, gid=self.gid
        )

    def _stopService(self):
        # Actions that need to get called regardless of whether an exit
        # was initiated by the process or by the user
        super().stopService()

    def _forceQuit(self):
        try:
            self.transport.signalProcess('KILL')
        except ProcessExitedAlready:
            pass

    def stopService(self):
        self._stopService()

        try:
            self.transport.signalProcess('TERM')
        except ProcessExitedAlready:
            pass
        else:
            self._forceQuitTimer = self._reactor.callLater(
                self.killTime,
                self._forceQuit
            )
