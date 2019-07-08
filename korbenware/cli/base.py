from functools import wraps
from twisted.internet.defer import ensureDeferred
from twisted.internet.task import react


def async_command(cmd):
    @wraps(cmd)
    def wrapped(*arg, **kwarg):
        return react(lambda reactor: ensureDeferred(
            cmd(reactor, *arg, **kwarg)
        ))

    return wrapped
