from contextlib import contextmanager
from functools import wraps

import attr
from twisted.internet import reactor as reactor_
from twisted.internet.defer import Deferred, ensureDeferred
from twisted.internet.task import react
import urwid

from pyxsession.cli.base import async_command


def on_q(run):
    @wraps(run)
    def run_on_q(key):
        if key in {'q', 'Q'}:
            run()


@attr.s
class Session:
    reactor = attr.ib(default=reactor_)
    widget = attr.ib(default=None)
    done = attr.ib(default=attr.Factory(Deferred))
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

    def succeed(self, result=None):
        self.done.callback(result)
    
    @contextmanager
    def capture(self):
        try:
            yield
        except Exception as exc:
            self.fail(exc)

    async def run(self):
        loop_kwarg = dict(**self.loop_kwarg)

        if self.unhandled_input:
            loop_kwarg[
                'unhandled_input'
            ] = self.unhandled_input(
                lambda: self.done.callback(None)
            )

            loop = urwid.MainLoop(
                self.widget,
                event_loop=urwid.TwistedEventLoop(
                    reactor=self.reactor,
                    manage_reactor=False
                ),
                **loop_kwarg
            )

            loop.start()

            try:
                return await self.done
            finally:
                loop.stop()
