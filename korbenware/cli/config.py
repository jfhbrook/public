import click
import crayons
from pygments import highlight
from pygments.lexers.configs import IniLexer
from pygments.formatters import Terminal256Formatter
from pygments.styles import get_style_by_name
from terminaltables import DoubleTable

from korbenware.cli.base import async_command, verbosity
from korbenware.config import load_config
from korbenware.editor import edit as open_editor
from korbenware.logger import (
    CliObserver, captured, create_logger, greet, publisher
)
from korbenware.xdg.applications import ApplicationsRegistry


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

        return lambda o: str(crayon(o))


get_color = ColorCycler()


def fmt_table(table, **kwargs):
    t = DoubleTable([
        [str(cell) for cell in row]
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
    open_editor(ctx.obj['CONFIG'].meta.config_filename)


@main.group(
    help='Commands related to XDG applications'
)
def applications():
    pass


@applications.command(
    name='show',
    help=(
        'Show the applications loaded by Korbenware'
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

    with captured(log):
        _greet(log)

        applications = ApplicationsRegistry(config)

        if application:
            app = applications.entries[application]

            if app.executable.parsed:
                parsed = crayons.green('yes')
            else:
                parsed = '\n'.join([
                    str(crayons.yellow(line))
                    for line in str(app.executable.parse_exc).split('\n')
                ])

            if app.executable.validated:
                validated = crayons.green('yes')
            else:
                validated = '\n'.join([
                    str(crayons.yellow(line))
                    for line in str(app.executable.validate_exc).split('\n')
                ])

            if app.executable.exec_key_parsed:
                exec_key_parsed = crayons.green('yes')
            else:
                exec_key_parsed = '\n'.join([
                    str(crayons.yellow(line))
                    for line in (
                        str(app.executable.exec_key_parse_exc).split('\n')
                    )
                ])

            table = [['key', 'value']]

            for row in [
                ['full path', app.fullpath],
                ['exec key', app.executable.exec_key.raw],
                ['desktop file parsed?', parsed],
                ['desktop file validated?', validated],
                ['exec key parsed?', exec_key_parsed]
            ]:
                color = get_color()
                table.append([color(cell) for cell in row])

            print(fmt_table(table, title='application'))

            print('')
            print('raw file')
            print('----------')
            with open(app.fullpath, 'r') as f:
                print(fmt_desktop_file(f.read(), config))
            print('----------')

        else:
            print(
                fmt_table(
                    [['path']] + [
                        [get_color()(directory)]
                        for directory in applications.directories
                    ],
                    title='directories'
                )
            )

            print('')

            table = [
                [
                    'name',
                    'hidden?',
                    'parsed?',
                    'validated?',
                    'exec key parsed?',
                    'exec key'
                ]
            ]

            for name, app in applications.entries.items():
                color = get_color()

                if app.executable.is_hidden:
                    hidden = crayons.yellow('yes')
                else:
                    hidden = crayons.green('no')

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
                    color(name),
                    hidden,
                    parsed,
                    validated,
                    exec_key_parsed,
                    color(app.executable.exec_key.raw)
                ])

            print(fmt_table(table, title='applications'))
