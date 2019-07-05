from functools import wraps

from twisted.internet import reactor as reactor_
from twisted.internet.defer import Deferred, ensureDeferred


def sleep(n, reactor=None):
    reactor = reactor if reactor else reactor_
    d = Deferred()
    reactor.callLater(n, d.callback, None)
    return d


def returns_deferred(coro_fn):
    @wraps(coro_fn)
    def returns_deferred(*args, **kwargs):
        return ensureDeferred(coro_fn(*args, **kwargs))
