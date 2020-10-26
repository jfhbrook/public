# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import shlex


def edit(path):
    argv = shlex.split(os.environ.get("EDITOR", "vi"))
    cmd = argv[0]
    argv.append(str(path))

    os.execvpe(cmd, argv, os.environ)
