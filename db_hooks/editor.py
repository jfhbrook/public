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
import os
import os.path
import shlex
import shutil

from db_hooks.config import GLOBAL_CONFIG
from db_hooks.errors import EditorNotFoundError


logger = logging.getLogger(__name__)


def edit():
    dirname = os.path.dirname(GLOBAL_CONFIG)
    logger.debug("Ensuring the path {} exists...".format(dirname))
    os.makedirs(dirname, exist_ok=True)

    argv = shlex.split(shutil.os.environ.get("EDITOR", "vi"))

    editor = argv[0]
    argv.append(GLOBAL_CONFIG)

    if not shutil.which(editor):
        raise EditorNotFoundError(editor)

    logger.debug("execvpe: {}, {}".format(editor, argv))

    os.execvpe(editor, argv, os.environ)
