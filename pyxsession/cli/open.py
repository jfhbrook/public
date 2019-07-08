import urllib

import click

from pyxsession.cli.base import async_command
from pyxsession.config import load_config, log_config
from pyxsession.executor import default_executor
from pyxsession.logger import (
    CliObserver, create_logger, publisher, captured
)
from pyxsession.open import ApplicationFinder, exec_key_fields, OpenError
from pyxsession.urls import UrlRegistry
from pyxsession.xdg.applications import ApplicationsRegistry
from pyxsession.xdg.mime import MimeRegistry


@click.command()
@click.argument('urls_and_or_files', nargs=-1, required=True)
@async_command
async def main(reactor, urls_and_or_files):

    config = load_config()

    log = create_logger(namespace='pyxsession.cli.open')

    publisher.addObserver(CliObserver(config))

    with captured(log):
        log.info('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
        log.info('┃ {hed}                 ┃', hed='Korby Jr. The File/Url Opener 🦜')  # noqa
        log.info('┃ {subhed}                              ┃', subhed='"open up or else!"')  # noqa
        log.info('┃ {attribution} ┃', attribution='programmed entirely while eating a spider plant')  # noqa
        log.info('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
        log_config(config)

        applications = ApplicationsRegistry(config)
        mime = MimeRegistry(config, applications)
        urls = UrlRegistry(config, applications)
        finder = ApplicationFinder(urls, mime)

        for url_or_file in urls_and_or_files:
            try:
                app = finder.get_by_url_or_file(url_or_file)
            except OpenError:
                log.error(
                    'Unable to find a suitable application for opening {url_or_file}',  # noqa
                    url_or_file=url_or_file
                )
            else:
                log.info(
                    'Opening {url_or_file} with application {application}...',
                    url_or_file=url_or_file,
                    application=app.filename
                )
                default_executor.run_xdg_application(
                    app,
                    exec_key_fields=exec_key_fields(app, url_or_file)
                )
