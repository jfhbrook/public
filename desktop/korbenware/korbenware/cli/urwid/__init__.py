# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from contextlib import contextmanager
from functools import wraps

import attr
import click
from twisted.internet import reactor as reactor_
from twisted.internet.defer import Deferred
import urwid


def on_q(run):
    @wraps(run)
    def run_on_q(key):
        if key in {"q", "Q"}:
            run()

    return run_on_q


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
        loop = urwid.MainLoop(
            self.widget,
            event_loop=urwid.TwistedEventLoop(
                reactor=self.reactor, manage_reactor=False
            ),
            **self.loop_kwarg
        )

        loop.start()

        try:
            return await self.done
        finally:
            loop.stop()
            click.echo()