# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from xdg.BaseDirectory import load_first_config

XDG_RESOURCE = "korbenware"
XDG_CURRENT_DESKTOP = os.environ.get("XDG_CURRENT_DESKTOP", XDG_RESOURCE)


def config_basedir(resource=XDG_RESOURCE):
    return load_first_config(resource)
