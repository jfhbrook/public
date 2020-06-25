import click
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
    greet(hed, subhed)


@click.group()
@verbosity
@click.pass_context
def main(ctx, verbose):
    config = load_config()

    log = create_logger(namespace='krbenware.cli.config')

    publisher.addObserver(CliObserver(config, verbosity=verbose + 1))

    ctx.ensure_object(dict)

    ctx.obj['CONFIG'] = config
    ctx.obj['LOGGER'] = log


@main.group()
def base():
    pass


@base.command()
@click.pass_context
def show(ctx):
    log = ctx.obj['LOGGER']

    with captured(log):
        greet()

        log_config(ctx.obj['CONFIG'], LogLevel.info)


@base.command()
@click.pass_context
def edit(ctx):
    open_editor(ctx.obj['CONFIG'].meta.config_filename)
