import os.path
from pathlib import Path
from shutil import copy2

import click
import crayons
from pygments import highlight
from pygments.lexers.configs import IniLexer
from pygments.formatters import Terminal256Formatter
from pygments.styles import get_style_by_name
from terminaltables import DoubleTable
import xdg.BaseDirectory
import xdg.Mime

from korbenware.cli.base import async_command, verbosity
from korbenware.config import load_config
from korbenware.editor import edit as open_editor
from korbenware.logger import (
    CliObserver, captured, create_logger, greet, publisher
)
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.mime import MimeRegistry


def _safe_str(entity):
    # crayons has a bug where entity.str returns the raw thing (instead of
    # stringifying it) when colors are disabled by the terminal
    return str(entity.__str__())


def _greet(log):
    hed = "Korben's Cool Petsitter's Configuration Manager 🦜"
    subhed = 'programmed entirely while Korben was screaming at the neighbors'
    greet(log, hed, subhed)


class ColorCycler:
    COLORS = ['blue', 'magenta', 'cyan']

    def __init__(self):
        self.i = -1

    def __call__(self):
        self.i += 1
        if self.i >= len(self.COLORS):
            self.i = 0

        crayon = getattr(crayons, self.COLORS[self.i])

        return lambda o: _safe_str(crayon(o))


get_color = ColorCycler()


def fmt_table(table, **kwargs):
    t = DoubleTable([
        [_safe_str(cell) for cell in row]
        for row in table
    ], **kwargs)

    t.inner_row_border = True

    return t.table


def fmt_desktop_file(contents, config):
    return highlight(
        contents,
        IniLexer(),
        Terminal256Formatter(
            style=get_style_by_name(config.format.pygments_formatter)
        )
    )


@click.group()
@verbosity
@click.pass_context
def main(ctx, verbose):
    config = load_config()

    log = create_logger(namespace='krbenware.cli.config')

    publisher.addObserver(CliObserver(config, verbosity=verbose))

    ctx.ensure_object(dict)

    ctx.obj['CONFIG'] = config
    ctx.obj['LOGGER'] = log


@main.group(
    help='Commands related to the base config loaded from korbenware.toml'
)
def base():
    pass


@base.command(
    name='show',
    help='Show the base config'
)
@click.pass_context
def show_base_config(ctx):
    config = ctx.obj['CONFIG']
    log = ctx.obj['LOGGER']

    with captured(log):
        _greet(log)

        table = [['section', 'key', 'value']]

        for section_attr in config.__attrs_attrs__:
            section = getattr(config, section_attr.name)
            color = get_color()
            if hasattr(section, '__attrs_attrs__'):
                for attribute in section.__attrs_attrs__:
                    table.append([
                        color(section_attr.name),
                        color(attribute.name),
                        color(getattr(section, attribute.name))
                    ])
            else:
                for k, v in section.items():
                    table.append([
                        color(section_attr.name),
                        color(k),
                        color(v)
                    ])

        print(fmt_table(table, title='base config'))


@base.command(
    name='edit',
    help='Edit the base config'
)
@click.pass_context
def edit_base_config(ctx):
    config = ctx.obj['CONFIG']
    log = ctx.obj['LOGGER']

    with captured(log):
        _greet(log)

        config_filename = config.meta.config_filename

        log.info(f'Editing {config_filename}...')

    open_editor(config_filename)


@main.group(
    help='Commands related to XDG applications'
)
@click.pass_context
def applications(ctx):
    ctx.obj['APPLICATIONS'] = ApplicationsRegistry(ctx.obj['CONFIG'])


@applications.command(
    name='show',
    help=(
        'Show the XDG applications loaded by Korbenware'
    )
)
@click.option(
    '-a', '--application',
    help='A particular application to show'
)
@click.pass_context
def show_applications(ctx, application):
    config = ctx.obj['CONFIG']
    log = ctx.obj['LOGGER']
    applications = ctx.obj['APPLICATIONS']

    with captured(log):
        _greet(log)

        if application:
            app = applications.entries[application]
            color = crayons.magenta

            if app.executable.is_hidden:
                hidden = crayons.yellow('yes')
                color = crayons.blue
            else:
                hidden = crayons.green('no')

            if app.executable.no_display:
                no_display = crayons.yellow('yes')
                if not app.executable.is_hidden:
                    color = crayons.cyan
            else:
                no_display = crayons.green('no')

            if app.executable.parsed:
                parsed = crayons.green('yes')
            else:
                parsed = '\n'.join([
                    _safe_str(crayons.yellow(line))
                    for line in str(app.executable.parse_exc).split('\n')
                ])

            if app.executable.validated:
                validated = crayons.green('yes')
            else:
                validated = '\n'.join([
                    _safe_str(crayons.yellow(line))
                    for line in str(app.executable.validate_exc).split('\n')
                ])

            if app.executable.exec_key_parsed:
                exec_key_parsed = crayons.green('yes')
            else:
                exec_key_parsed = '\n'.join([
                    _safe_str(crayons.yellow(line))
                    for line in (
                        str(app.executable.exec_key_parse_exc).split('\n')
                    )
                ])

            table = [['key', 'value']]

            for row in [
                ['full path', app.fullpath],
                ['overridden paths', [o.fullpath for o in app.overrides]],
                ['hidden?', hidden],
                ['no display?', no_display],
                ['exec key', app.executable.exec_key.raw],
                ['desktop file parsed?', parsed],
                ['desktop file validated?', validated],
                ['exec key parsed?', exec_key_parsed]
            ]:
                table.append([color(cell) for cell in row])

            print(fmt_table(table, title='application'))
            print('')
            print('raw file')
            print('----------')
            with open(app.fullpath, 'r') as f:
                print(fmt_desktop_file(f.read(), config))
            print('----------')

        else:
            table = [
                [
                    'name',
                    'hidden?',
                    'no display?',
                    'parsed?',
                    'validated?',
                    'exec key parsed?',
                    'exec key'
                ]
            ]

            for app in sorted(applications.entries.values()):

                color = crayons.magenta

                if app.executable.is_hidden:
                    hidden = crayons.yellow('yes')
                    color = crayons.blue
                else:
                    hidden = crayons.green('no')

                if app.executable.no_display:
                    no_display = crayons.yellow('yes')
                    if not app.executable.is_hidden:
                        color = crayons.cyan
                else:
                    no_display = crayons.green('no')

                if app.executable.parsed:
                    parsed = crayons.green('yes')
                else:
                    parsed = crayons.yellow('no')

                if app.executable.validated:
                    validated = crayons.green('yes')
                else:
                    validated = crayons.yellow('no')

                if app.executable.exec_key_parsed:
                    exec_key_parsed = crayons.green('yes')
                else:
                    exec_key_parsed = crayons.yellow('no')

                table.append([
                    color(app.filename),
                    hidden,
                    no_display,
                    parsed,
                    validated,
                    exec_key_parsed,
                    color(app.executable.exec_key.raw)
                ])

            print(fmt_table(table, title='applications'))


class UnresolvedApplicationPathError():
    def __init__(self, src_path, directories):
        super().__init__(
            f"Couldn't generate an edit path for {src_path} in any of: "
            f"{directories.join(', ')}"
        )


@applications.command(
    name='edit',
    help=(
        'Edit an application loaded by Korbenware'
    )
)
@click.option(
    '-a', '--application',
    help='An application to edit',
    required=True
)
@click.option(
    '-c', '--copy/--no-copy',
    help=(
        'Copy the .desktop file to the highest priority search path if it '
        "doesn't already exist there"
    )
)
@click.pass_context
def edit_application(ctx, application, copy):
    config = ctx.obj['CONFIG']
    log = ctx.obj['LOGGER']
    applications = ctx.obj['APPLICATIONS']

    should_edit = True

    with captured(log):
        try:
            _greet(log)

            app = applications.entries[application]

            directories = [
                Path(directory)
                for directory in applications.directories
            ]

            src_path = Path(app.fullpath)

            if copy:
                for directory in directories:
                    try:
                        dest_path = (
                            directories[0]
                            /
                            src_path.relative_to(directory)
                        )
                    except ValueError:
                        continue

                if not dest_path:
                    raise UnresolvedApplicationPathError(src_path, directories)

                if src_path != dest_path:
                    log.info(
                        'Copying {src_path} to {dest_path}...',
                        src_path=src_path,
                        dest_path=dest_path
                    )
                    copy2(src_path, dest_path)
            else:
                dest_path = src_path
        except:  # noqa
            should_edit = False
            raise
        else:
            log.info(
                'Opening {file_path} in the editor...',
                file_path=dest_path
            )

    if should_edit:
        open_editor(dest_path)


@main.group(
    help='Commands related to MIME type lookups'
)
def mime():
    pass



@main.group(
    help='Commands related to file type associations'
)
@click.pass_context
def associations(ctx):
    config = ctx.obj['CONFIG']
    applications = ApplicationsRegistry(ctx.obj['CONFIG'])
    mime = MimeRegistry(config, applications)

    ctx.obj['APPLICATIONS'] = applications
    ctx.obj['MIME'] = mime


@associations.command(
    name='show',
    help='Show the file type associations recognized by korbenware'
)
@click.option('-t', '--mime-type', help='A particular file type to show')
@click.pass_context
def show_associations(ctx, mime_type):
    log = ctx.obj['LOGGER']
    mime = ctx.obj['MIME']

    with captured(log):
        _greet(log)

        table = [['mime type', 'applications', 'default']]

        keys = sorted(set(mime.lookup.keys()) | set(mime.defaults.keys()), key=lambda m: str(m))

        for mimetype in keys:
            applications = mime.lookup.get(mimetype, None)
            default = mime.defaults.get(mimetype, None)

            table.append([
                crayons.magenta(mimetype),
                crayons.magenta(applications) if applications else crayons.yellow('None'),
                crayons.magenta(default) if default else crayons.yellow('None')
            ])

        print(fmt_table(table, title='associations and defaults'))


@mime.group(
    help='Commands related to XDG glob databases'
)
def glob():
    pass


@glob.command(
    name='paths',
    help='Show paths for XDG glob databases'
)
@click.pass_context
def show_glob_paths(ctx):
    log = ctx.obj['LOGGER']

    with captured(log):
        _greet(log)

        table = [['file', 'exists?']]

        for directory in xdg.BaseDirectory.xdg_data_dirs:
            f = os.path.join(directory, 'mime', 'globs2')

            if os.path.isfile(f):
                exists = crayons.green('yes')
            else:
                exists = crayons.yellow('no')

            table.append([
                crayons.magenta(f),
                exists
            ])

        print(fmt_table(table, title='globs database paths'))


@glob.command(
    name='show',
    help='Show the parsed glob databases'
)
@click.pass_context
@click.option('-t', '--mime-type', help='A particular file type to show')
def show_glob_database(ctx, mime_type):
    log = ctx.obj['LOGGER']

    with captured(log):
        _greet(log)
        xdg.Mime.update_cache()

        table = [['mime type', 'priority', 'pattern', 'flags']]

        for mime_type, rule in sorted(xdg.Mime.globs.allglobs.items(), key=lambda t: str(t[0])):
            color = get_color()
            for priority, glob, flags in sorted(associations, key=lambda t: t[0], reverse=True):
                table.append([
                    color(mime_type),
                    color(priority),
                    color(glob),
                    color(flags)
                ])

        print(fmt_table(table, title='glob database'))


@glob.command(
    name='edit',
    help='Edit the highest priority globs database file'
)
@click.pass_context
def edit_glob_database(ctx):
    should_edit = False

    with captured(log):
        _greet(log)

        f = os.path.join(xdg.BaseDirectory.xdg_data_dirs[0], 'mime', 'globs2')

        log.info('Editing {globs_db_file}', globs_db_file=f)

        should_edit = True

    if should_edit:
        open_editor(f)


@mime.group(
    help='Commands related to magics'
)
def magic():
    pass


@magic.command(
    name='paths',
    help='Show paths for magic databases'
)
@click.pass_context
def show_magic_paths(ctx):
    log = ctx.obj['LOGGER']

    with captured(log):
        _greet(log)

        table = [['file', 'exists?']]

        for directory in xdg.BaseDirectory.xdg_data_dirs:
            f = os.path.join(directory, 'mime', 'magic')

            if os.path.isfile(f):
                exists = crayons.green('yes')
            else:
                exists = crayons.yellow('no')

            table.append([
                crayons.magenta(f),
                exists
            ])

        print(fmt_table(table, title='magic database paths'))


def magic_match_any_repr(self):
    return 'MagicMatchAny([\n    {rules}\n])'.format(
        rules='\n    '.join([str(r) for r in self.rules])
    )


xdg.Mime.MagicMatchAny.__repr__ = magic_match_any_repr


@magic.command(
    name='show'
)
@click.pass_context
@click.option('-t', '--mime-type', help='A particular file type to show')
def show_magic_database(ctx, mime_type):
    log = ctx.obj['LOGGER']

    with captured(log):
        _greet(log)
        xdg.Mime.update_cache()

        table = [['mime type', 'priority', 'rule']]

        for mime_type, rules in sorted(xdg.Mime.magic.bytype.items(), key=lambda t: str(t[0])):
            color = get_color()
            for priority, rule in sorted(rules, key=lambda t: t[0], reverse=True):
                table.append([
                    color(mime_type),
                    color(priority),
                    rule
                ])

        print(fmt_table(table, title='magic database'))
