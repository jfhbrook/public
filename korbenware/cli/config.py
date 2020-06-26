import click
import crayons
from terminaltables import DoubleTable
from twisted.logger import LogLevel

from korbenware.cli.base import async_command, verbosity
from korbenware.config import load_config, log_config
from korbenware.editor import edit as open_editor
from korbenware.logger import (
    CliObserver, captured, create_logger, greet, publisher
)


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


@main.group()
def base():
    pass


@base.command()
@click.pass_context
def show(ctx):
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
                    table.append([color(section_attr.name), color(attribute.name), color(getattr(section, attribute.name))])
            else:
                for k, v in section.items():
                    table.append([color(section_attr.name), color(k), color(v)])

        print('=== BASE CONFIG: ===')
        print(DoubleTable(table).table)



@base.command()
@click.pass_context
def edit(ctx):
    open_editor(ctx.obj['CONFIG'].meta.config_filename)
