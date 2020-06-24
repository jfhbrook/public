import click
from txdbus import client as dbus_client

from korbenware.cli.base import async_command
from korbenware.config import load_config, log_config
from korbenware.dbus import Service
from korbenware.logger import (
    JournaldObserver, create_logger, publisher, captured, greet
)
from korbenware.session import Session
from korbenware.twisted.util import wait_for_event


@click.command()
@async_command
async def main(reactor):
    config = load_config()

    log = create_logger(namespace='korbenware.cli.session')

    publisher.addObserver(JournaldObserver())

    hed = 'Korben the X Session Manager 🦜'
    subhed = 'programmed entirely by the windowsill'
    subsubhed = 'by Korben c2020'

    with captured(log):
        greet(log, hed, subhed, subsubhed)
        log_config(config)

        service = Service.from_config(config)

        session = Session(reactor, config)
        session.attach(service)

        dbus_conn = await dbus_client.connect(reactor)

        await service.server(dbus_conn)

        session.start()

        def before_shutdown():
            if session.running:
                session.stop()

        reactor.addSystemEventTrigger('before', 'shutdown', before_shutdown)

        exit = wait_for_event(session, 'stopped')

        await exit
