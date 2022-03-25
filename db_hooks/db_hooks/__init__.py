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

from db_hooks.cache import CacheManager, create_cache
from db_hooks.config import Config
from db_hooks.sqlalchemy import build_engine

logger = logging.getLogger(__name__)

cache_manager = CacheManager()


@cache_manager.cached
def get_engine(connection_name, filename=None):
    config = Config.load_config(filename)

    if not cache_manager.has_cache():
        cache_manager.set_cache(create_cache(config.cache))

    return build_engine(config, connection_name)
