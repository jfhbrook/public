# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

def basename(path):
    return path.split("/")[-1]


def split(path):
    return path[1:].split("/")


def snaked(path):
    return "_".join(split(path))
