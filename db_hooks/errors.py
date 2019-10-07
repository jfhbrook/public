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


class DBHooksError(Exception):
    """
    A generic db_hooks error.
    """


class ConfigNotFoundError(DBHooksError):
    message = "Could not find a configuration in: {}"

    def __init__(self, filename=None, locations=None):
        if filename:
            message = self.message.format(filename)
        elif locations:
            message = self.message.format("; ".join(locations))
        else:
            message = self.message.format("(unknown location)")

        super().__init__(self, message)


class MalformedConfigError(DBHooksError):
    message = "Could not successfully parse the configuration in: {}"

    def __init__(self, filename=None):
        if filename:
            message = self.message.format(filename)
        else:
            message = self.message.format("(unknown location)")

        super().__init__(self, message)


class UnrecognizedCacheImplementationError(DBHooksError):
    message = "Unrecognized cache implementaton {}; must be one of: {}"

    def __init__(self, type, cache_cls_by_name):
        message = self.message.format(type, "; ".join(cache_cls_by_name.keys()))

        super().__init__(self, message)


class CommandNotFoundError(DBHooksError):
    message = "Could not find the command {} in the PATH"

    def __init__(self, cmd):
        super().__init__(self, self.message.format(cmd))


class ClientNotFoundError(CommandNotFoundError):
    pass


class EditorNotFoundError(CommandNotFoundError):
    pass
