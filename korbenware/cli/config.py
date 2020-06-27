import os.path
from pathlib import Path
from shutil import copy2

import click
import crayons
from pygments import highlight
from pygments.lexers.configs import IniLexer
from pygments.formatters import Terminal256Formatter
from pygments.styles import get_style_by_name
import xdg.BaseDirectory
import xdg.Mime

from korbenware.cli.base import (
    safe_str, color_text_block, command, echo_table, get_color,
    group, pass_context
)
from korbenware.config import load_config
from korbenware.editor import edit as open_editor
from korbenware.logger import create_logger
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.mime import MimeRegistry


def echo_desktop_file(contents, config):
    return click.echo(
        highlight(
            contents,
            IniLexer(),
            Terminal256Formatter(
                style=get_style_by_name(config.format.pygments_formatter)
            )
        )
    )


@group(
    hed="Korben's Cool Petsitter's Configuration Manager 🦜",
    subhed='programmed entirely while Korben was screaming at the neighbors'
)
@pass_context
def main(ctx):
    log = create_logger(namespace='korbenware.cli.config')

    ctx.ensure_object(dict)

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
@pass_context
def show_base_config(ctx):
    config = ctx.config

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

    echo_table(table, title='base config')


@base.command(
    name='edit',
    help='Edit the base config'
)
@pass_context
def edit_base_config(ctx):
    config = ctx.config
    log = ctx.obj['LOGGER']

    config_filename = config.meta.config_filename

    log.info(f'Editing {config_filename}...')

    ctx.defer(lambda: open_editor(config_filename))


@main.group(
    help='Commands related to XDG applications'
)
@click.pass_context
def applications(ctx):
    ctx.obj['APPLICATIONS'] = ApplicationsRegistry(ctx.config)


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
@pass_context
def show_applications(ctx, application):
    config = ctx.config
    log = ctx.obj['LOGGER']
    applications = ctx.obj['APPLICATIONS']

    def common_settings(app):
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

        return color, hidden, no_display


    if application:
        app = applications.entries[application]
        color = crayons.magenta

        color, hidden, no_display = common_settings(app)

        if app.executable.parsed:
            parsed = crayons.green('yes')
        else:
            parsed = color_text_block(
                crayons.yellow,
                app.executable.parse_exc
            )

        if app.executable.validated:
            validated = crayons.green('yes')
        else:
            validated = color_text_block(
                crayons.yellow,
                app.executable.validate_exc
            )

        if app.executable.exec_key_parsed:
            exec_key_parsed = crayons.green('yes')
        else:
            exec_key_parsed = color_text_block(
                crayons.yellow,
                app.executable.exec_key_parse_exc
            )

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

        echo_table(table, title='application')
        click.echo('')
        click.echo('raw file')
        click.echo('----------')
        with open(app.fullpath, 'r') as f:
            echo_desktop_file(f.read(), config)
        click.echo('----------')

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
            color, hidden, no_display = common_settings(app)

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

        click.echo(fmt_table(table, title='applications'))


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
@pass_context
def edit_application(ctx, application, copy):
    config = ctx.config
    log = ctx.obj['LOGGER']
    applications = ctx.obj['APPLICATIONS']

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

    log.info(
        'Opening {file_path} in the editor...',
        file_path=dest_path
    )

    ctx.defer(lambda: open_editor(dest_path))


@main.group(
    help='Commands related to MIME type lookups'
)
def mime():
    pass


@mime.group(
    help='Commands related to file type associations'
)
@pass_context
def associations(ctx):
    config = ctx.config

    applications = ApplicationsRegistry(config)
    mime = MimeRegistry(config, applications)

    ctx.obj['APPLICATIONS'] = applications
    ctx.obj['MIME'] = mime


class MimeType(click.ParamType):
    def convert(self, value, param, ctx):
        if not value:
            return value

        parts = str(value).split('/')

        if len(parts) != 2:
            self.fail(
                f'Invalid mime type {value} - must have the format `{{media}}/{{subtype}}`',
                param,
                ctx
            )
        return xdg.Mime.MIMEtype(parts[0], parts[1])

    def __repr__(self):
        return 'MimeType'


@associations.command(
    name='show',
    help='Show the file type associations recognized by korbenware'
)
@click.option('-t', '--mime-type', type=MimeType(), help='A particular file type to show')
@pass_context
def show_associations(ctx, mime_type):
    mime = ctx.obj['MIME']

    table = [['mime type', 'applications', 'default']]

    if mime_type:
        keys = [mime_type]
    else:
        keys = sorted(
            set(mime.lookup.keys()) | set(mime.defaults.keys()),
            key=str
        )

    for mime_type in keys:
        applications = mime.lookup.get(mime_type, None)
        default = mime.defaults.get(mime_type, None)

        color = get_color()

        table.append([
            color(mime_type),
            color(applications) if applications else crayons.yellow('None'),
            color(default) if default else crayons.yellow('None')
        ])

    echo_table(table, title='associations and defaults')


@mime.group(
    help='Commands related to XDG glob databases'
)
def glob():
    pass


@glob.command(
    name='paths',
    help='Show paths for XDG glob databases'
)
def show_glob_paths():
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

    click.echo(fmt_table(table, title='globs database paths'))


@glob.command(
    name='show',
    help='Show the parsed glob databases'
)
@click.option('-t', '--mime-type', help='A particular file type to show')
def show_glob_database(mime_type):
    xdg.Mime.update_cache()

    table = [['mime type', 'priority', 'pattern', 'flags']]

    for mime_type, rule in sorted(xdg.Mime.globs.allglobs.items(), key=lambda t: str(t[0])):
        color = get_color()
        for priority, glob, flags in sorted(rule, key=lambda t: t[0], reverse=True):
            table.append([
                color(mime_type),
                color(priority),
                color(glob),
                color(flags)
            ])

    click.echo(fmt_table(table, title='glob database'))


@glob.command(
    name='edit',
    help='Edit the highest priority globs database file'
)
@pass_context
def edit_glob_database(ctx):
    f = os.path.join(xdg.BaseDirectory.xdg_data_dirs[0], 'mime', 'globs2')

    log.info('Editing {globs_db_file}', globs_db_file=f)

    ctx.defer(lambda: open_editor(f))


@mime.group(
    help='Commands related to magics'
)
def magic():
    pass


@magic.command(
    name='paths',
    help='Show paths for magic databases'
)
def show_magic_paths():
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

    click.echo(fmt_table(table, title='magic database paths'))


def magic_match_any_repr(self):
    return 'MagicMatchAny([\n    {rules}\n])'.format(
        rules='\n    '.join([str(r) for r in self.rules])
    )


xdg.Mime.MagicMatchAny.__repr__ = magic_match_any_repr


@magic.command(
    name='show'
)
@click.option('-t', '--mime-type', help='A particular file type to show')
def show_magic_database(mime_type):
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

    click.echo(fmt_table(table, title='magic database'))
