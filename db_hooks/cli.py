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


@click.group(help="Interact with db_hooks database connections.")
@click_log.simple_verbosity_option(logger)
@click.option("--filename", type=click.Path(exists=True), default=None)
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
    "--key", type=str, default=None, help="Filter to only show info for this connection"
)
@capture
@pass_config
def show(config, key):
    if key:
        config.echo_property(key)
    else:
        config.echo()


@main.command(
    help="Connect to a database using the default cli client for that database."
)
@click.argument("name")
@capture
@pass_config
def connect(config, name):
    Client.from_config(config, name).exec()


@main.command(help="Edit the global config")
@capture
def edit():
    editor.edit()
