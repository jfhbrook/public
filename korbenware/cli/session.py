import click
import txdbus

from korbenware.cli.base import async_command
from korbenware.config import load_config, log_config
from korbenware.executor import MonitoringExecutor, DBusExecutor
from korbenware.logger import (
    JournaldObserver, create_logger, publisher, captured, greet
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

    hed = 'Korben the X Session Manager 🦜'
    subhed = 'programmed entirely by the windowsill'
    subsubhed = 'by Korben c2019'
 
    with captured(log):
        greet(log, hed, subhed, subsubhed)
        log_config(config)

        applications = ApplicationsRegistry(config)
        mime = MimeRegistry(config, applications)
        urls = UrlRegistry(config, applications)
        finder = ApplicationFinder(urls, mime)

        # For the window manager and maybe the bar
        # critical_executor = MonitoringExecutor(reactor)

        # For everything else
        default_executor = ApplicationExecutor(reactor, applications)

        dbus_executor = DBusExecutor(
            obj_path='/korbenware/executors/DefaultExecutor',
            service=service,
            reactor=reactor,
            underlying=default_executor
        )

        # TODO: Set up SIGINT/exit hooks
        exit = None

        # TODO: Set up lifecycle hooks
        # TODO: Build dbus APIs for inspecting the state of the process

        # Start the world
        default_executor.start()

        dbus_conn = await txdbus.client.connect(reactor)

        await dbus_executor.start_server(dbus_conn)

        # TODO: need to await something
        await exit
