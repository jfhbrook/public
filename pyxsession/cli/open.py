import click
from pyxsession.cli.base import async_command
from pyxsession.config import load_config
from pyxsession.executor import default_executor
from pyxsession.xdg.applications import ApplicationsDatabase
from pyxsession.xdg.mime import MimeDatabase


# TODO: Custom exception, better naming, move to .xdg.exec_key
# TODO: Detect if url vs file
def _get_field(exec_key, urls_or_files):
    expected_fields = exec_key.expected_fields()

    if 'U' in expected_fields:
        return 'U'
    elif len(urls_or_files) > 1:
        if 'F' in expected_fields:
            return 'F'
        else:
            raise Exception('where are we supposed to put these?')
    else:
        if 'u' in expected_fields:
            return 'u'
        elif 'F' in expected_fields:
            return 'F'
        elif 'f' in expected_fields:
            return 'f'
        else:
            raise Exception('where are we supposed to put this?')


@click.command()
@click.argument('urls_or_files', nargs=-1)
@async_command
async def main(reactor, urls_or_files):
    config = load_config()

    applications = ApplicationsDatabase(config)
    mime = MimeDatabase(config, applications)

    # TODO: Instead of picking the app for the first one, calculate runs
    # of files with the same default and fire multiple starts
    # TODO: Add cli flag and urwid session for flipping through associated
    # non-default applications
    apps = mime.default_by_filename(urls_or_files[0])

    # TODO: try loop that iterates over all listed apps
    app = apps.pop(0)

    field = _get_field(app.executable.exec_key, urls_or_files)
    exec_key_fields = {
        field: urls_or_files
    }

    default_executor.run_xdg_application(
        app,
        exec_key_fields=exec_key_fields
    )
