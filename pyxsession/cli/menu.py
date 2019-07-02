from contextlib import contextmanager
from functools import wraps
import click
from pyxsession.cli.base import urwid_command
from pyxsession.urwid import quit_on_q
from pyxsession.urwid.menu import XDGMenu
from pyxsession.config import load_config
import xdg.Menu


@click.command()
@urwid_command
def main():
    config = load_config()

    xdg_menu = xdg.Menu.parse(config.menu.filename)

    menu = XDGMenu(xdg_menu)

    yield menu.view, dict(unhandled_input=quit_on_q)
