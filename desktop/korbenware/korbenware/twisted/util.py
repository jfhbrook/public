# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
    def wrapper(*args, **kwargs):
        return ensureDeferred(coro_fn(*args, **kwargs))

    return wrapper


def wait_for_event(ee, event):
    d = Deferred()

    @ee.once(event)
    def fire_deferred(*args, **kwargs):
        data = None
        if args:
            try:
                data = args[0]
            except IndexError:
                pass
        elif kwargs:
            try:
                data = next(iter(kwargs.values()))
            except StopIteration:
                pass
        d.callback(data)

    return d