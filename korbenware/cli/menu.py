import click
import xdg.Menu

from korbenware.cli.base import async_command
from korbenware.cli.urwid.menu import menu_session
from korbenware.config import load_config, log_config
from korbenware.executor import default_executor
from korbenware.logger import (
    CliObserver, create_logger, greet, publisher, captured
)


@click.command()
@async_command
async def main(reactor):
    config = load_config()

    log = create_logger(namespace='korbenware.cli.menu')

    publisher.addObserver(CliObserver(config))

    hed = "Grandmaw Korben's XDG Menu Explorer 🦜"
    subhed = '"nice work, pixel birdie!"'
    subsubhed = 'programmed entirely while unemployed'

    with captured(log):
        greet(log, hed, subhed, subsubhed)
        log_config(config)

        xdg_menu = xdg.Menu.parse(config.menu.filename)

        session = menu_session(hed, subsubhed, xdg_menu)

        desktop_entry = await session.run()

        if not desktop_entry:
            log.info(
                "Looks like you didn't end up choosing an item from the menu; doing nothing"  # noqa
            )
        else:
            default_executor.run_xdg_desktop_entry(desktop_entry)
