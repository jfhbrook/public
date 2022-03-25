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

import logging
import json
import os
import os.path
from typing import Dict, Optional

from appdirs import user_data_dir
import attr
import cattr
import click
from pygments import highlight
from pygments.lexers import JsonLexer, TOMLLexer
from pygments.formatters import Terminal256Formatter
import toml
from toml.decoder import TomlDecodeError

from db_hooks.errors import ConfigNotFoundError, DBHooksError, MalformedConfigError
from db_hooks.password import PASSWORD_UNSUPPORTED
from db_hooks.pgpass import pg_pass_file

logger = logging.getLogger(__name__)

GLOBAL_CONFIG = os.path.join(user_data_dir("db_hooks", "jfhbrook"), "databases.toml")
LOCAL_CONFIG = os.path.abspath("./.databases.toml")
CONFIG_LOCATIONS = [LOCAL_CONFIG, GLOBAL_CONFIG]


def format_config(config, format="toml", pretty=True):
    config = cattr.unstructure(config)

    if format == "toml":
        config = toml.dumps(config)
        if pretty:
            config = highlight(config, TOMLLexer(), Terminal256Formatter())
    elif format == "json":
        if pretty:
            config = highlight(
                json.dumps(config, indent=2), JsonLexer(), Terminal256Formatter()
            )
        else:
            config = json.dumps(config)
    else:
        raise DBHooksError(f"Unrecognized format {format}!")

    return config


@attr.s
class DatabaseConfig:
    protocol: Optional[str] = attr.ib(default=None)
    username: Optional[str] = attr.ib(default=None)
    has_password: Optional[bool] = attr.ib(default=None)
    host: Optional[str] = attr.ib(default=None)
    port: Optional[int] = attr.ib(default=None)
    database: Optional[str] = attr.ib(default=None)
    password: Optional[str] = attr.ib(default=None)
    password_cmd: Optional[str] = attr.ib(default=None)


@attr.s
class CacheConfig:
    type: str = attr.ib(default="LRUCache")
    kwargs: dict = attr.ib(default=dict(maxsize=512))


@attr.s
class KeyringConfig:
    enable: bool = attr.ib(default=False)
    namespace: str = attr.ib(default="com.jfhbrook.db_hooks")


@attr.s
class PgPassConfig:
    enable: bool = attr.ib(default=False)
    location: bool = attr.ib(default=pg_pass_file())
    ttl: int = attr.ib(default=600)
    clear_backup: bool = attr.ib(default=False)


@attr.s
class Config:
    keyring: KeyringConfig = attr.ib(default=KeyringConfig())
    cache: CacheConfig = attr.ib(default=CacheConfig())
    pgpass: PgPassConfig = attr.ib(default=PgPassConfig())
    connections: Dict[str, DatabaseConfig] = attr.ib(default=dict())
    password_cmd: str = attr.ib(default="zenity --password")
    password_loader: str = attr.ib(default="shlex")

    config_locations = CONFIG_LOCATIONS

    @classmethod
    def structure(cls, unstructured):
        return cattr.structure(unstructured, cls)

    def unstructure(self):
        return cattr.unstructure(self)

    @classmethod
    def from_file(cls, filename):
        logger.info("Loading configuration from {}...".format(filename))
        with open(filename, "r") as f:
            raw = f.read()

        try:
            unstructured = toml.loads(raw)
        except TomlDecodeError as exc:
            raise MalformedConfigError(filename) from exc

        try:
            structured = cls.structure(unstructured)
        except TypeError as exc:
            raise MalformedConfigError(filename) from exc
        structured.raw = raw

        for connection_config in structured.connections.values():
            if connection_config.has_password is None:
                connection_config.has_password = (
                    connection_config.password is not None
                    or connection_config.protocol not in PASSWORD_UNSUPPORTED
                )

        return structured

    @classmethod
    def load_config(cls, filename=None):
        if filename:
            try:
                return cls.from_file(filename)
            except FileNotFoundError as exc:
                raise ConfigNotFoundError(filename=filename) from exc

        for filename in cls.config_locations[:-1]:
            try:
                return cls.from_file(filename)
            except FileNotFoundError:
                logger.info(
                    "Configuration not found at {}. Trying the next location.".format(
                        filename
                    )
                )

        try:
            return cls.from_file(cls.config_locations[-1])
        except FileNotFoundError as exc:
            raise ConfigNotFoundError(locations=cls.config_locations) from exc

    def save(self, filename):
        with open(filename, "w") as f:
            toml.dump(f, self.unstructure())

    def echo(self, format="toml", highlight=True):
        click.echo(format_config(self, format, highlight))

    def echo_property(self, key, format="toml", highlight=True):
        config = self
        root = dict()
        parent = None
        child = root

        for k in key.split("."):
            if type(config) == dict:
                config = config[k]
            else:
                config = getattr(config, k)
            child[k] = dict()
            parent = child
            child = child[k]

        parent[k] = config

        click.echo(format_config(parent, format, highlight))
