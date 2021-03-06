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

    log = create_logger(namespace="korbenware.cli.ctl")


@main.command(help="Log the state of the Korbenware session")
@pass_context
async def get_state(ctx, reactor):
    session = await get_session(ctx, reactor)
    print(await session.get_state())


@main.command(help="Run an application in the session's application executor")
@click.argument("name")
@pass_context
async def run(ctx, reactor, name):
    session = await get_session(ctx, reactor)

    await session.run_xdg_application(name)


@main.command(help="Start an application that has been stopped")
@click.argument("name")
@pass_context
async def start(ctx, reactor, name):
    session = await get_session(ctx, reactor)

    await session.start_xdg_application(name)


@main.command(help="Stop an application that is running")
@click.argument("name")
@pass_context
async def stop(ctx, reactor, name):
    session = await get_session(ctx, reactor)

    await session.stop_xdg_application(name)


@main.command(help="Restart an application or critical process")
@click.argument("name")
@click.option(
    "--critical", is_flag=True, help="Restart a process in the critical executor"
)
@pass_context
async def restart(ctx, reactor, name, critical):
    session = await get_session(ctx, reactor)

    if critical:
        await session.restart_critical_process(name)
    else:
        await session.restart_xdg_application(name)
