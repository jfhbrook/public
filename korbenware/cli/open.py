import click

from korbenware.cli.base import async_command, command
from korbenware.config import load_config, log_config
from korbenware.executor import BaseExecutor
from korbenware.open import ApplicationFinder, exec_key_fields, OpenError
from korbenware.urls import UrlRegistry
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.mime import MimeRegistry


@command(
    help=(
        'Open files and URLs with default and mime-appropriate XDG applications'
    ),
    hed='Korby Jr. The File/Url Opener 🦜',
    subhed='"open up or else!"',
    subsubhed='programmed entirely while eating a spider plant'
)
@click.argument('urls_and_or_files', nargs=-1, required=True)
@click.pass_context
@async_command
async def main(reactor, ctx, urls_and_or_files):

    log = ctx.log
    config = ctx.config
    applications = ApplicationsRegistry(config)
    mime = MimeRegistry(config, applications)
    urls = UrlRegistry(config, applications)
    finder = ApplicationFinder(urls, mime)

    # TODO: dbus executor
    executor = BaseExecutor()

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
            executor.run_xdg_application(
                app,
                exec_key_fields=exec_key_fields(app, url_or_file)
            )
