import click
from twisted.logger import LogLevel

from pyxsession.cli.base import async_command
from pyxsession.config import load_config, log_config
from pyxsession.logger import CliObserver, publisher


@click.command()
@async_command
async def main(reactor):
    config = load_config()

    observer = CliObserver(config)
    publisher.addObserver(observer)

    log_config(config, level=LogLevel.info)
