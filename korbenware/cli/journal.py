import os

import click

from twisted.logger import LogLevel

from korbenware.config import load_config
from korbenware.cli.base import verbosity
from korbenware.logger import (
    captured, CliObserver, create_logger, greet,
    LEVEL_BY_NAME, publisher, SYSLOG_PRIORITY_BY_LEVEL
)


@click.command(context_settings=dict(ignore_unknown_options=True))
@verbosity
@click.option('-l', '--level')
@click.argument('journald_args', nargs=-1, type=click.UNPROCESSED)
def main(verbose, level, journald_args):

    config = load_config()

    log = create_logger(namespace='korbenware.cli.journal')

    publisher.addObserver(CliObserver(config, verbosity=verbose))

    hed = "Korby Jr's Cool Petsitter's Journald Shimmy-Shim 🦜"
    subhed = "programmed entirely while cursing Lennart Poettering's name"

    argv = None

    with captured(log):
        greet(log, hed, subhed)
        try:
            level = LEVEL_BY_NAME[level] if level else LogLevel.info

            priority = SYSLOG_PRIORITY_BY_LEVEL[level]

            syslog_priority = f'--priority={priority}'

            # TODO: Dynamically look up identifier from config and/or cli arg
            syslog_identifier = f'SYSLOG_IDENTIFIER=korbenware'

            argv = [
                'journalctl',
                syslog_priority,
                syslog_identifier
            ] + list(journald_args)

            log.info('Exec-ing {command}...', command=['journalctl'] + argv)
        except:  # noqa
            argv = None
            raise

    if argv:
        os.execvpe('journalctl', argv, os.environ)
