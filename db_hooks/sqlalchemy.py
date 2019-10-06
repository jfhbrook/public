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

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from db_hooks.password import PasswordLoader


SQLALCHEMY_PROTOCOLS = {
    "postgres": "postgresql+psycopg2",
    "postgresql": "postgresql+psycopg2",
    "pg": "postgresql+psycopg2",
    "mysql": "mysql+pymysql",
}


def format_url(connection_config, password):
    url = URL(
        drivername=SQLALCHEMY_PROTOCOLS[connection_config.protocol],
        username=connection_config.username,
        password=password,
        host=connection_config.host,
        port=connection_config.port,
        database=connection_config.database,
    )

    return str(url)


def get_url(config, connection_name):
    connection_config = config.connections[connection_name]

    loader = PasswordLoader.from_config(config)
    password = loader.get_password(connection_name)

    return format_url(connection_config, password)


def build_engine(config, connection_name):
    return create_engine(get_url(config, connection_name))
