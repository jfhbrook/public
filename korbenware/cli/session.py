import click

from korbenware.cli.base import async_command
from korbenware.config import load_config, log_config
from korbenware.executor import default_executor
from korbenware.logger import (
    CliObserver, JournaldObserver, create_logger, publisher, captured, greet
)
from korbenware.open import ApplicationFinder, exec_key_fields, OpenError
from korbenware.urls import UrlRegistry
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.mime import MimeRegistry


@click.command()
@async_command
async def main(reactor):

    config = load_config()

    log = create_logger(namespace='korbenware.cli.session')

    publisher.addObserver(JournaldObserver())
    publisher.addObserver(CliObserver(config))

    hed = 'Korben the X Session Manager 🦜'
    subhed = 'programmed entirely by the windowsill'
    subsubhed = 'by Korben'
 
    with captured(log):
        greet(log, hed, subhed, subsubhed)
        log_config(config)

        applications = ApplicationsRegistry(config)
        mime = MimeRegistry(config, applications)
        urls = UrlRegistry(config, applications)
        finder = ApplicationFinder(urls, mime)

        # TODO: Set up executors
        # TODO: Set up dbus service
        # TODO: Set up SIGINT hooks

