import click
import xdg.Menu

from korbenware.cli.base import command, pass_context
from korbenware.cli.urwid.menu import menu_session
from korbenware.config import load_config, log_config
from korbenware.executor import BaseExecutor
from korbenware.logger import create_logger


@command(
    help="Display a TUI for the configured XDG app menu",
    hed="Grandmaw Korben's XDG Menu Explorer 🦜",
    subhed='"nice work, pixel birdie!"',
    dek="programmed entirely while unemployed",
)
@pass_context
async def main(ctx, reactor):
    config = ctx.config

    log = create_logger(namespace="korbenware.cli.menu")

    executor = BaseExecutor()

    xdg_menu = xdg.Menu.parse(config.menu.filename)

    session = menu_session(ctx.command.hed, ctx.command.dek, xdg_menu)

    desktop_entry = await session.run()

    if not desktop_entry:
        log.info(
            "Looks like you didn't end up choosing an item from the menu; doing nothing"  # noqa
        )
    else:
        log.info("Opening {name}...", name=desktop_entry.getName())

        executor.run_xdg_desktop_entry(desktop_entry)
