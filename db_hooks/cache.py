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
import logging

from cachetools import LFUCache, LRUCache, RRCache, TTLCache
import cachetools.keys as keys

from db_hooks.errors import UnrecognizedCacheImplementationError

logger = logging.getLogger(__name__)

CACHE_CLS_BY_NAME = {
    cls.__name__: cls for cls in [LFUCache, LRUCache, RRCache, TTLCache]
}


def create_cache(cache_config):
    if cache_config.type not in CACHE_CLS_BY_NAME:
        raise UnrecognizedCacheImplementationError(cache_config.type, CACHE_CLS_BY_NAME)

    logger.info(
        "Creating connection cache of type {}({})...".format(
            cache_config.type, cache_config.kwargs
        )
    )

    cls = CACHE_CLS_BY_NAME[cache_config.type]
    return cls(**cache_config.kwargs)


class CacheManager:
    def __init__(self, key=keys.hashkey, enabled=True):
        self._cache = None
        self._enabled = enabled
        self._key = key

    def set_cache(self, cache):
        logger.info("Cache set to {}.".format(cache))
        self._cache = cache

    def has_cache(self):
        return self._cache is not None

    def clear_cache(self):
        logger.info("Cache has been cleared.")
        self._cache = None

    def disable_cache(self):
        logger.info("Cache has been disabled.")
        self._enabled = False

    def enable_cache(self):
        logger.info("Cache has been enabled.")
        self._enabled = True

    def cached(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if not self._enabled:
                return fn(*args, **kwargs)

            k = self._key(*args, **kwargs)

            if self._cache:
                try:
                    return self._cache[k]
                except KeyError:
                    pass

            v = fn(*args, **kwargs)

            if not self._cache:
                return v

            try:
                self._cache[k] = v
            except ValueError:
                pass

            return v

        return wrapper
