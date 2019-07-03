import urllib

import click

from pyxsession.cli.base import async_command
from pyxsession.config import load_config
from pyxsession.executor import default_executor
from pyxsession.urls import UrlRegistry
from pyxsession.xdg.applications import ApplicationsRegistry
from pyxsession.xdg.mime import MimeRegistry


def _get_field(exec_key, url_or_file):
    expected_fields = exec_key.expected_fields()

    for potential_field in 'UuFf':
        if potential_field in expected_fields:
            return potential_field
    # TODO: Real exception
    raise Exception('where are we supposed to put this?')


@click.command()
@click.argument('urls_or_files', nargs=-1)
@async_command
async def main(reactor, urls_or_files):
    config = load_config()

    applications = ApplicationsRegistry(config)
    mime = MimeRegistry(config, applications)
    urls = UrlRegistry(config, applications)

    # Loosely inspired by gio
    # TODO: link
    for url_or_file in urls_or_files:
        url_parse = urllib.parse.urlparse(url_or_file)

        # If we can parse out a protocol that's not a file then we need to
        # try to open as a url
        if url_parse.scheme not in {'', 'file'}:
            app = urls.get_application_by_scheme(url_parse.scheme)
        else:
            app = None
            for potential_app in mime.default_by_filename(url_or_file):
                if potential_app.executable.exec_key_parsed:
                    app = potential_app
                    break
                else:
                    # TODO: logging? or delegate to the registries?
                    pass

        if not app:
            # TODO: real exception
            raise Exception('no app found')

        field = _get_field(app.executable.exec_key, url_or_file)
        exec_key_fields = {
            field: url_or_file
        }

        default_executor.run_xdg_application(
            app,
            exec_key_fields=exec_key_fields
        )
