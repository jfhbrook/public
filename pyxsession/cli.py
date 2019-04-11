import click
from functools import partial, wraps
from pyxsession.config import load_config
from twisted.internet.defer import ensureDeferred
from twisted.internet.task import react


def command_runner(cmd):
    @wraps(cmd)
    def wrapped(*arg, **kwarg):
        def returns_deferred(reactor):
            return ensureDeferred(cmd(*arg, reactor=reactor, **kwarg))

        return react(returns_deferred)

    return wrapped


@click.command()
@command_runner
async def main(reactor):
    # TODO: Anything lmao

    # TODO: Pass any cli parameters in that might override the config
    print(load_config())

    return
