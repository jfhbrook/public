# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import click
from txdbus import client as dbus_client

from korbenware.cli.base import group, pass_context
from korbenware.config import load_config, log_config
from korbenware.dbus import Service
from korbenware.logger import JournaldObserver, create_logger, publisher
from korbenware.session import Session
from korbenware.twisted.util import wait_for_event


# TODO: Refactor groups so that both groups and commands can do
# async actions
async def get_session(ctx, reactor):
    service = Service.from_config(ctx.config)
    Session(reactor, ctx.config).attach(service)

    dbus_conn = await dbus_client.connect(reactor)

    client = await service.client(dbus_conn)
    return client.korbenware.Session


@group(
    help="Send commands to kbsession over DBus",
    hed="Josh the guy that Yells at Korben the X Session Manager All The Time",
    subhed='"Get down from there! I don\'t think so!"',
)
@pass_context
def main(ctx):
    config = ctx.config

    log = create_logger(namespace="korbenware.cli.menu")


@main.command()
@pass_context
async def get_state(ctx, reactor):
    session = await get_session(ctx, reactor)
    print(await session.get_state())
