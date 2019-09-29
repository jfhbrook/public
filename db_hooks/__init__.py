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
import os.path
import subprocess

from appdirs import user_data_dir
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
import toml


GLOBAL_CONFIG = os.path.join(user_data_dir("db_hooks", "jfhbrook"), "databases.toml")
LOCAL_CONFIG = os.path.abspath("./.databases.toml")
CONFIG_LOCATIONS = [LOCAL_CONFIG, GLOBAL_CONFIG]


class DBHooksError(Exception):
    pass


class ConfigurationNotFoundError(DBHooksError):
    pass


def load_config_by_filename(filename):
    with open(filename, "r") as f:
        config = toml.load(f)

    return config


def load_config(filename=None):
    if filename:
        return load_config_by_filename(filename)
    for filename in CONFIG_LOCATIONS:
        try:
            return load_config_by_filename(filename)
        except FileNotFoundError:
            pass

    raise ConfigurationNotFoundError(
        "Could not find a configuration in either of the following locations: "
        + "; ".join(CONFIG_LOCATIONS)
    )


def save_config(config, filename=LOCAL_CONFIG):
    with open(filename, "w") as f:
        toml.dump(f, config)


def get_connstring(name, filename=None):
    config = load_config(filename=filename)
    conn_info = config[name]
    kwargs = dict()

    if "password_cmd" in conn_info:
        kwargs["password"] = (
            subprocess.run(
                ["bash", "-c", conn_info["password_cmd"]], capture_output=True
            )
            .stdout.decode("utf8")
            .strip()
        )
    return conn_info["connection"].format(**kwargs)


def get_engine(name, filename=None):
    return create_engine(get_connstring(name, filename=filename))


def get_cli_command(name, filename=None):
    connstring = get_connstring(name, filename=filename)
    url = make_url(connstring)

    if any(
        [url.drivername.startswith(db_type) for db_type in ["postgresql", "redshift"]]
    ):
        argv = ["psql"]
        env = dict()

        for cli_key, conn_key in [
            ("-U", "username"),
            ("-h", "host"),
            ("-p", "port"),
            ("-d", "database"),
        ]:
            if getattr(url, conn_key, None):
                argv.append(cli_key)
                argv.append(str(getattr(url, conn_key)))

        if url.password:
            env["PGPASSWORD"] = url.password

    elif url.drivername.startswith("mysql"):
        argv = ["mysql"]
        env = dict()

        for cli_key, conn_key in [
            ("--user", "username"),
            ("--host", "host"),
            ("--port", "port"),
            ("--password", "password"),
        ]:
            if getattr(url, conn_key, None):
                argv.append(cli_key)
                argv.append(str(getattr(url, conn_key)))

        if url.database:
            argv.append(url.database)

    return argv, env
