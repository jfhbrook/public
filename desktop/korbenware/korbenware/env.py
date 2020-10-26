# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os.path
import subprocess
import sys


def load_base_env():
    # This is a little hold-my-beer - the goal is to load environment
    # variables from sourced bash files. Turns out that's a little wild.

    # Will luckily inherit our current env and cwd
    process = subprocess.run(
        [
            "bash",
            os.path.join(
                os.path.dirname(__file__), "../bin/korbenware-environment-loader"
            ),
        ],
        check=True,
        capture_output=True,
    )

    env = dict()

    # This output is *hopefully* encoded in this encoding or I'm in a world
    # of hurt...
    encoding = sys.getfilesystemencoding()
    output = process.stdout.decode(encoding)

    for pair in output.split("\n"):
        if pair:  # (blank lines)
            key, val = pair.split("=", 1)
        env[key] = val

    return env


BASE_ENV = load_base_env()


def load_env(extra_vars=None):
    extra_vars = extra_vars or dict()
    env = dict(**BASE_ENV)
    env.update(extra_vars)
    return env
