import os

import click
from twisted.logger import LogLevel

from korbenware.cli.base import command, pass_context
from korbenware.logger import LEVEL_BY_NAME, SYSLOG_PRIORITY_BY_LEVEL


@command(
    hed="Koren's Luddite Paw-Paw's Journald Shimmy-Shim 🦜",
    subhed="programmed entirely while cursing Lennart Poettering's name",
    context_settings=dict(ignore_unknown_options=True),
    help="A thin wrapper around journalctl for loading korbenware-related journald logs",  # noqa
)
@click.option(
    "-l", "--level", help="Search journald logs at or above this Twisted logger level"
)
@click.argument("journald_args", nargs=-1, type=click.UNPROCESSED)
@pass_context
def main(ctx, level, journald_args):

    argv = None

    level = LEVEL_BY_NAME[level] if level else LogLevel.info

    priority = SYSLOG_PRIORITY_BY_LEVEL[level]

    syslog_priority = f"--priority={priority}"

    # TODO: Dynamically look up identifier from config and/or cli arg
    syslog_identifier = f"SYSLOG_IDENTIFIER=korbenware"

    argv = ["journalctl", syslog_priority, syslog_identifier] + list(journald_args)

    ctx.defer(lambda: os.execvpe("journalctl", argv, os.environ))
