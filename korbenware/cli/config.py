import click
from twisted.logger import LogLevel

from korbenware.cli.base import async_command
from korbenware.config import load_config, log_config
from korbenware.logger import CliObserver, publisher


@click.command()
@async_command
async def main(reactor):
    config = load_config()

    observer = CliObserver(config, verbosity=2)
    publisher.addObserver(observer)

    log_config(config)
