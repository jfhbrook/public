from functools import wraps
from twisted.internet.defer import ensureDeferred
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
    def wrapped(*arg, **kwarg):
        gen = cmd(*arg, **kwarg)

        # TODO: As it stands we can only run one urwid loop, since it
        # starts and stops the reactor. It might be possible to start the
        # reactor separately in order to run multiple loops, but for various
        # reasons that seems unlikely.

        if hasattr(gen, '__next__'):
            widget = next(gen)
        else:
            widget = gen

        if type(widget) == tuple:
            widget, loop_kwarg = widget
        else:
            loop_kwarg = dict()

        loop = urwid.MainLoop(
            widget,
            event_loop=urwid.TwistedEventLoop(),
            **loop_kwarg
        )

        loop.run()

        if gen != widget:
            try:
                next(gen)
            except StopIteration:
                pass

    return wrapped
