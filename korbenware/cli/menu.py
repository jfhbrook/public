import click
import xdg.Menu

from korbenware.cli.base import async_command
from korbenware.cli.urwid.menu import menu_session
from korbenware.config import load_config
from korbenware.executor import default_executor


@click.command()
@async_command
async def main(reactor):
    config = load_config()

    xdg_menu = xdg.Menu.parse(config.menu.filename)

    session = menu_session(xdg_menu)

    desktop_entry = await session.run()

    default_executor.run_xdg_desktop_entry(desktop_entry)
