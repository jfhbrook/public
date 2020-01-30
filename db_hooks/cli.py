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

import functools
import os

import click
import click_log

from db_hooks import logger
from db_hooks.client import Client
from db_hooks.config import Config, GLOBAL_CONFIG, LOCAL_CONFIG
import db_hooks.editor as editor
from db_hooks.errors import ConfigNotFoundError

click_log.basic_config(logger)


def capture(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:  # noqa
            logger.exception("FLAGRANT SYSTEM ERROR")
            raise click.Abort()

    return wrapper


def pass_config(fn):
    @functools.wraps(fn)
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        if ctx.obj.get("CONFIG_NOT_FOUND_ERROR"):
            raise ctx.obj["CONFIG_NOT_FOUND_ERROR"]
        return fn(ctx.obj["CONFIG"], *args, **kwargs)

    return wrapper


def autocomplete_config_files(ctx, args, incomplete):
    directory = os.path.dirname(incomplete)
    prefix = os.path.basename(incomplete)

    directory = directory if directory else "."

    try:
        listings = os.listdir(directory)
    except FileNotFoundError:
        return []

    return [
        os.path.join(directory, listing)
        for listing in listings
        if listing.startswith(prefix)
        and os.path.isdir(listing)
        or listing.endswith(".toml")
    ]


def autocomplete_config_key(ctx, args, incomplete):
    try:
        config = Config.load_config()
    except ConfigNotFoundError:
        return []

    known_keys = incomplete.split(".")
    incomplete_key = known_keys.pop()

    for k in known_keys:
        if type(config) == dict:
            config = config[k]
        elif hasattr(config.__class__, "__attrs_attrs__"):
            config = getattr(config, k)
        else:
            return []

    return [
        f"{'.'.join(known_keys)}.{k}" if known_keys else k
        for k in (
            config.keys()
            if type(config) == dict
            else (
                [attr.name for attr in config.__class__.__attrs_attrs__]
                if hasattr(config.__class__, "__attrs_attrs__")
                else []
            )
        )
        if k.startswith(incomplete_key)
    ]


def autocomplete_connection_names(ctx, args, incomplete):
    try:
        config = Config.load_config()
    except ConfigNotFoundError:
        return []

    return [
        connection_name
        for connection_name in config.connections.keys()
        if connection_name.startswith(incomplete)
    ]


@click.group(help="Interact with db_hooks database connections.")
@click_log.simple_verbosity_option(logger)
@click.option(
    "--filename",
    type=click.Path(exists=True),
    default=None,
    autocompletion=autocomplete_config_files,
)
@click.option("--system/--no-system", default=None)
@click.pass_context
@capture
def main(ctx, filename, system):
    ctx.ensure_object(dict)

    if system is not None:
        if system:
            ctx.obj["CONFIG_FILENAME"] = GLOBAL_CONFIG
        else:
            ctx.obj["CONFIG_FILENAME"] = LOCAL_CONFIG
    else:
        ctx.obj["CONFIG_FILENAME"] = filename

    try:
        ctx.obj["CONFIG"] = Config.load_config(ctx.obj["CONFIG_FILENAME"])
    except ConfigNotFoundError as exc:
        ctx.obj["CONFIG"] = None
        ctx.obj["CONFIG_NOT_FOUND_ERROR"] = exc


@main.command(help="Show part or all of the db_hooks configuration")
@click.option(
    "--key",
    type=str,
    default=None,
    help="Filter to only show info for this connection",
    autocompletion=autocomplete_config_key,
)
@click.option("--json/--no-json", default=False, help="Output JSON instead of TOML")
@click.option("--pretty/--no-pretty", default=True, help="Apply syntax highlighting")
@capture
@pass_config
def show(config, key, json, pretty):
    format = "json" if json else "toml"
    if key:
        config.echo_property(key, format, pretty)
    else:
        config.echo(format, pretty)


@main.command(
    help="Connect to a database using the default cli client for that database."
)
@click.argument("name", autocompletion=autocomplete_connection_names)
@capture
@pass_config
def connect(config, name):
    Client.from_config(config, name).exec()


@main.command(help="Edit the global config")
@capture
def edit():
    editor.edit()
