import urllib

from pyxsession.config import load_config
from pyxsession.executor import default_executor
from pyxsession.urls import UrlRegistry
from pyxsession.xdg.applications import ApplicationsRegistry
from pyxsession.xdg.mime import MimeRegistry


class OpenError(Exception):
    pass


def get_target_field(exec_key, url_or_file):
    expected_fields = exec_key.expected_fields()

    for potential_field in 'UuFf':
        if potential_field in expected_fields:
            return potential_field
    raise OpenError(
        f'Exec key `{exec_key.raw}` needs to contain one of: %U, %u, %F, %f'
    )


def exec_key_fields(application, url_or_file):
    return {
        get_target_field(
            application.executable.exec_key,
            url_or_file
        ): url_or_file
    }


class ApplicationFinder:
    def __init__(self, urls, mime):
        self.urls = urls
        self.mime = mime

    def get_by_url_or_file(self, url_or_file):
        url_parse = urllib.parse.urlparse(url_or_file)

        # If we can parse out a protocol that's not a file then we need to
        # try to open as a url
        if url_parse.scheme not in {'', 'file'}:
            app = self.urls.get_application_by_scheme(url_parse.scheme)
        else:
            app = None
            for potential_app in self.mime.default_by_filename(url_or_file):
                if potential_app.executable.exec_key_parsed:
                    app = potential_app
                    break
                else:
                    # TODO: logging? or delegate to the registries?
                    pass

        if not app:
            raise OpenError(
                f'No suitable application for opening {url_or_file} was found.'
            )

        return app
