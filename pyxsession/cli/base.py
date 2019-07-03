from functools import wraps
from twisted.internet.defer import Deferred, ensureDeferred
from twisted.internet.task import react
import urwid


def async_command(cmd):
    @wraps(cmd)
    def wrapped(*arg, **kwarg):
        return react(lambda reactor: ensureDeferred(
            cmd(reactor, *arg, **kwarg)
        ))

    return wrapped


def urwid_command(cmd):
    @wraps(cmd)
    @async_command
    async def wrapped(reactor, *arg, **kwarg):
        waiting = Deferred()

        def next_(exc=None):
            if exc:
                waiting.errback(exc)
            else:
                waiting.callback(None)

        agen = cmd(reactor, next_, *arg, **kwarg)

        try:
            while True:
                widget = await agen.__anext__()

                if type(widget) == tuple:
                    widget, loop_kwarg = widget
                else:
                    loop_kwarg = dict()

                loop = urwid.MainLoop(
                    widget,
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
