# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

import korbenware.dbus.path as dbus_path


@pytest.mark.parametrize(
    "path,expected", [("/foo", "foo"), ("/foo/bar", "bar"), ("/foo/Bar", "Bar")]
)
def test_basename(path, expected):
    assert dbus_path.basename(path) == expected


@pytest.mark.parametrize(
    "path,expected",
    [("/foo", ["foo"]), ("/foo/bar", ["foo", "bar"]), ("/foo/Bar", ["foo", "Bar"])],
)
def test_split(path, expected):
    actual = dbus_path.split(path)

    assert len(actual) == len(expected)
    for i, a in enumerate(actual):
        assert a == expected[i]


@pytest.mark.parametrize(
    "path,expected", [("/foo", "foo"), ("/foo/bar", "foo_bar"), ("/foo/Bar", "foo_Bar")]
)
def test_snaked(path, expected):
    assert dbus_path.snaked(path) == expected
