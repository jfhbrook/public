import click

from korbenware.cli.base import async_command
from korbenware.config import load_config, log_config
from korbenware.executor import default_executor
from korbenware.logger import (
    CliObserver, create_logger, publisher, captured
)
from korbenware.open import ApplicationFinder, exec_key_fields, OpenError
from korbenware.urls import UrlRegistry
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.mime import MimeRegistry


@click.command()
@click.argument('urls_and_or_files', nargs=-1, required=True)
@async_command
async def main(reactor, urls_and_or_files):

    config = load_config()

    log = create_logger(namespace='korbenware.cli.open')

    publisher.addObserver(CliObserver(config))

    hed = 'Korby Jr. The File/Url Opener 🦜'
    subhed = '"open up or else!"'
    attribution = 'programmed entirely while eating a spider plant'
 
    with captured(log):
        log.info('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
        log.info('┃ {hed}                 ┃', hed=hed)
        log.info('┃ {subhed}                              ┃', subhed=subhed)
        log.info('┃ {attribution} ┃', attribution=attribution)
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
