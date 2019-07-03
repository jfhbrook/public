from contextlib import contextmanager
from functools import wraps

import click
import xdg.Menu

from pyxsession.cli.urwid import urwid_command, on_q
from pyxsession.cli.urwid.menu import XDGMenu
from pyxsession.config import load_config
from pyxsession.executor import default_executor


@click.command()
@urwid_command
async def main(reactor):
    config = load_config()

    xdg_menu = xdg.Menu.parse(config.menu.filename)

    session = XDGMenu(xdg_menu, unhandled_input=on_q)

    yield session

    desktop_entry = await session.done

    default_executor.run_xdg_desktop_entry(desktop_entry)
