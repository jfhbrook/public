from contextlib import contextmanager
from functools import wraps
import click
from pyxsession.cli.urwid import urwid_command, on_q
from pyxsession.cli.urwid.menu import XDGMenu
from pyxsession.config import load_config
import xdg.Menu


@click.command()
@urwid_command
async def main(reactor):
    config = load_config()

    xdg_menu = xdg.Menu.parse(config.menu.filename)

    yield XDGMenu(xdg_menu, unhandled_input=on_q)
