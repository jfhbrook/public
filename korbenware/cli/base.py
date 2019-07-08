from functools import wraps

import click
from twisted.internet.defer import ensureDeferred
from twisted.internet.task import react


def async_command(cmd):
    @wraps(cmd)
    def wrapped(*arg, **kwarg):
        return react(lambda reactor: ensureDeferred(
            cmd(reactor, *arg, **kwarg)
        ))

    return wrapped


verbosity = click.option(
    '-v', '--verbose', count=True,
    help="Set the verbosity for the cli logger. More v's means more logs!"
)
