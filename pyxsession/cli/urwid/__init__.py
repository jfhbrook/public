from contextlib import contextmanager
from functools import wraps

import attr
from twisted.internet.defer import Deferred, ensureDeferred
from twisted.internet.task import react
import urwid

from pyxsession.twisted.util import as_deferred
from pyxsession.cli.base import async_command


def on_q(run):
    @wraps(run)
    def run_on_q(key):
        if key in {'q', 'Q'}:
            run()


_bail = Deferred()


@_bail.addErrback
def _sad(exc=None):
    print(exc)
    sys.exit(1)


@_bail.addCallback
def _happy(result=None):
    sys.exit(0)


@attr.s
class Session:
    widget = attr.ib(default=None)
    done = attr.ib(default=_bail)
    unhandled_input = attr.ib(default=None)
    loop_kwarg = attr.ib(default=dict())

    def catch(self, fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                self.fail(exc)
            else:
                return result

        return wrapped

    def fail(self, exc):
        self.done.errback(exc)

    def succeed(self):
        self.done.callback(None)
    
    @contextmanager
    def capture(self):
        try:
            yield
        except Exception as exc:
            self.fail(exc)


def urwid_command(cmd):
    @wraps(cmd)
    @async_command
    async def wrapped(reactor, *arg, **kwarg):
        waiting = Deferred()

        agen = cmd(reactor, *arg, **kwarg)

        try:
            while True:
                session = await agen.__anext__()

                session.done = waiting

                loop_kwarg = dict(**session.loop_kwarg)

                if session.unhandled_input:
                    loop_kwarg[
                        'unhandled_input'
                    ] = session.unhandled_input(
                        lambda: session.done.callback(None)
                    )

                loop = urwid.MainLoop(
                    session.widget,
                    event_loop=urwid.TwistedEventLoop(
                        reactor=reactor,
                        manage_reactor=False
                    ),
                    **loop_kwarg
                )

                loop.start()

                try:
                    await waiting
                finally:
                    loop.stop()
                    waiting = Deferred()

        except StopAsyncIteration:
            pass

    return wrapped
