# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import click
from txdbus import client as dbus_client

from korbenware.cli.base import command, pass_context
from korbenware.config import load_config, log_config
from korbenware.dbus import Service
from korbenware.logger import JournaldObserver, create_logger, publisher
from korbenware.session import Session
from korbenware.twisted.util import wait_for_event


@command(
    hed="Korben the X Session Manager 🦜",
    subhed="programmed entirely by the windowsill",
    dek="by Korben c2020",
    observer_factory=lambda config, verbosity: JournaldObserver(),
)
@pass_context
async def main(ctx, reactor):
    log_config(ctx.config)

    service = Service.from_config(ctx.config)

    session = Session(reactor, ctx.config)
    session.attach(service)

    dbus_conn = await dbus_client.connect(reactor)

    await service.server(dbus_conn)

    session.start()

    def before_shutdown():
        if session.running:
            session.stop()

    reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)

    exit = wait_for_event(session, "stopped")

    await exit
