import urllib

import click

from pyxsession.cli.base import async_command
from pyxsession.config import load_config, log_config
from pyxsession.executor import default_executor
from pyxsession.logger import (
    CliObserver, create_logger, publisher
)
from pyxsession.open import ApplicationFinder, exec_key_fields
from pyxsession.urls import UrlRegistry
from pyxsession.xdg.applications import ApplicationsRegistry
from pyxsession.xdg.mime import MimeRegistry


@click.command()
@click.argument('urls_and_or_files', nargs=-1, required=True)
@async_command
async def main(reactor, urls_and_or_files):

    config = load_config()

    log = create_logger()

    publisher.addObserver(CliObserver(config))

    log_config(config)

    applications = ApplicationsRegistry(config)
    mime = MimeRegistry(config, applications)
    urls = UrlRegistry(config, applications)
    finder = ApplicationFinder(urls, mime)

    for url_or_file in urls_and_or_files:
        try:
            app = finder.get_by_url_or_file(url_or_file)
        except OpenError:
            log.failure(
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
