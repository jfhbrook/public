import click
from pyxsession.cli.base import async_command
from pyxsession.config import load_config


@click.command()
@async_command
async def main(reactor):
    # TODO: Anything lmao

    # TODO: Pass any cli parameters in that might override the config
    print(load_config())

    return
