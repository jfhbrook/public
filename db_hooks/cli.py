# Copyright 2019 Joshua Holbrook. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.
#
# This file is licensed to you under the Apache License,
# Version 2.0 (the "license"); you may not use this file
# except in compliance with the License. You may obtain a
# copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import shutil

import click
from pygments import highlight
from pygments.lexers import TOMLLexer
from pygments.formatters import Terminal256Formatter
import toml

from db_hooks import (
    CONFIG_LOCATIONS, ConfigurationNotFoundError, GLOBAL_CONFIG, LOCAL_CONFIG,
    load_config, get_cli_command
)


@click.group(help="Interact with db_hooks database connections.")
@click.option("--filename", type=click.Path(exists=True), default=None)
@click.option("--system/--no-system", default=None)
@click.pass_context
def main(ctx, filename, system):
    ctx.ensure_object(dict)
    if system is not None:
        if system:
            ctx.obj["CONFIG_FILENAME"] = GLOBAL_CONFIG
        else:
            ctx.obj["CONFIG_FILENAME"] = LOCAL_CONFIG
    else:
        ctx.obj["CONFIG_FILENAME"] = filename


def print_config_for_filename(filename):
    with open(filename, "r") as f:
        click.echo(highlight(f.read(), TOMLLexer(), Terminal256Formatter()))


def print_config(filename=None):
    if filename:
        return print_config_for_filename(filename)
    for filename in CONFIG_LOCATIONS:
        try:
            return print_config_for_filename(filename)
        except FileNotFoundError:
            pass
    raise ConfigurationNotFoundError(
        "Could not find a configuration in either of the following locations: "
        + "; ".join(CONFIG_LOCATIONS)
    )


def print_config_for_database_with_filename(name, filename):
    config = load_config(filename)
    conn_info = config[name]
    click.echo(
        highlight(toml.dumps({name: conn_info}), TOMLLexer(), Terminal256Formatter())
    )


def print_config_for_database(filename=None):
    if filename:
        return print_config_for_database_with_filename(filename)
    for filename in CONFIG_LOCATIONS:
        try:
            return print_config_for_database_with_filename(filename)
        except FileNotFoundError:
            pass
    raise ConfigurationNotFoundError(
        "Could not find a configuration in either of the following locations: "
        + "; ".join(CONFIG_LOCATIONS)
    )

@main.command(help="List available db_hooks database connections.")
@click.option(
    "--name",
    type=str,
    default=None,
    help="Filter to only show info for this connection",
)
@click.pass_context
def list(ctx, name):
    filename = ctx.obj["CONFIG_FILENAME"]

    if name:
        print_config_for_database(name, filename)
    else:
        print_config(filename=filename)


class ClientProgramNotFoundError(Exception):
    pass


@main.command(
    help="Connect to a database using the default cli client for that database."
)
@click.argument("name")
@click.pass_context
def connect(ctx, name):
    filename = ctx.obj["CONFIG_FILENAME"]

    argv, env = get_cli_command(name, filename=filename)

    cmd = argv[0]
    env = dict(os.environ, **env)

    if not shutil.which(cmd):
        raise ClientProgramNotFoundError(f"`Command {cmd} not found.")

    if argv:
        os.execvpe(cmd, argv, env)
    else:
        os.execlpe(cmd, env)
