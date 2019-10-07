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

from abc import ABC
import os
import shutil

from db_hooks.errors import ClientNotFoundError
from db_hooks.password import PasswordLoader


class Client(ABC):
    bin = None
    options = []
    parameters = []
    env = []

    def __init__(self, config, connection_name):
        self.config = config
        self.connection_name = connection_name
        self.connection_config = config.connections[connection_name]
        self.password_loader = (
            PasswordLoader.from_config(config)
            if self.connection_config.has_password
            else None
        )

    @classmethod
    def from_config(cls, config, connection_name):
        connection_config = config.connections[connection_name]
        return CLIENTS[connection_config.protocol](config, connection_name)

    def get_command(self):
        argv = [self.bin]
        env = dict()

        password = (
            self.password_loader.get_password(self.connection_name)
            if self.connection_config.has_password
            else None
        )

        for cli_key, conn_key in self.options:
            if conn_key == "password":
                conn_val = password
            else:
                conn_val = getattr(self.connection_config, conn_key, None)
            if conn_val:
                argv.append(cli_key)
                argv.append(str(conn_val))

        for conn_key in self.parameters:
            if conn_key == "password":
                parameter = password
            else:
                parameter = getattr(self.connection_config, conn_key, None)
            if parameter:
                argv.append(str(parameter))

        for env_key, conn_key in self.env:
            if conn_key == "password":
                env_val = password
            else:
                env_val = getattr(self.connection_config, conn_key, None)
            if env_val:
                env[env_key] = env_val

        return argv, env

    def exec(self):
        argv, env = self.get_command()

        cmd = argv[0]
        env = dict(os.environ, **env)

        if not shutil.which(cmd):
            raise ClientNotFoundError(cmd)

        if len(argv) > 1:
            os.execvpe(cmd, argv, env)
        else:
            os.execlpe(cmd, env)


class PostgreSQLClient(Client):
    bin = "psql"
    options = [("-U", "username"), ("-h", "host"), ("-p", "port"), ("-d", "database")]
    env = [("PGPASSWORD", "password")]


class MySQLClient(Client):
    bin = "mysql"
    options = [
        ("--user", "username"),
        ("--host", "host"),
        ("--port", "port"),
        ("--password", "password"),
    ]
    parameters = ["database"]


class SqliteClient(Client):
    bin = "sqlite3"
    parameters = ["database"]


CLIENTS = {
    "postgres": PostgreSQLClient,
    "postgresql": PostgreSQLClient,
    "pg": PostgreSQLClient,
    "mysql": MySQLClient,
    "sqlite": SqliteClient,
}
