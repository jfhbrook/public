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

from abc import ABC, abstractmethod
import logging
import keyring
from keyring.errors import KeyringError
import shlex
import subprocess

logger = logging.getLogger(__name__)

PASSWORD_UNSUPPORTED = {"sqlite"}


def keyring_service(config, connection_name):
    return "{}.{}".format(config.keyring.namespace, connection_name)


class PasswordLoader(ABC):
    def __init__(self, config):
        self.config = config

    @classmethod
    def from_config(cls, config):
        logger.info(
            "Initializing password loader of type {}...".format(config.password_loader)
        )
        return PASSWORD_LOADERS[config.password_loader](config)

    @classmethod
    def run_command(cls, argv):
        logger.debug("Running {}...".format(argv))
        process = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return process.stdout.decode("utf8").strip()

    @abstractmethod
    def get_argv(self, cmd_str):
        pass

    def get_password(self, connection_name):
        connection_config = self.config.connections[connection_name]
        keyring_pass = None

        if self.config.keyring.enable:
            logger.info("Checking keyring for connection {}...".format(connection_name))
            try:
                keyring_pass = keyring.get_password(
                    keyring_service(self.config, connection_name),
                    connection_config.username or "<no_username>",
                )
            except KeyringError as exc:
                logger.warn(exc)

            if keyring_pass:
                logger.info("Found password in keyring.")
                return keyring_pass

            logger.info("Could not find password in keyring.")
        logger.info("Getting password for connection {}...".format(connection_name))

        if hasattr(self.config, "password_cmd"):
            password_cmd = self.config.password_cmd
        else:
            password_cmd = connection_config.password_cmd

        if not password_cmd:
            return None

        templated = password_cmd.format(name=connection_name)

        argv = self.get_argv(templated)

        keyring_pass = self.run_command(argv)

        if keyring_pass and self.config.keyring.enable:
            logger.info("Saving password to keyring...")
            try:
                keyring.set_password(
                    keyring_service(self.config, connection_name),
                    connection_config.username or "<no_username>",
                    keyring_pass,
                )
            except KeyringError as exc:
                logger.warn(exc)

        return keyring_pass


class ShlexPasswordLoader(PasswordLoader):
    def get_argv(self, cmd_str):
        return shlex.split(cmd_str)


class BashPasswordLoader(PasswordLoader):
    def get_argv(self, cmd_str):
        return ["bash", "-c", cmd_str]


class PowerShellPasswordLoader(PasswordLoader):
    def get_argv(self, cmd_str):
        return ["powershell.exe", "-Command", cmd_str]


PASSWORD_LOADERS = {
    "shlex": ShlexPasswordLoader,
    "bash": BashPasswordLoader,
    "powershell": PowerShellPasswordLoader,
}
