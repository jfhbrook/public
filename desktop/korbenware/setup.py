# -*- coding: utf-8 -*-

# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from setuptools import find_packages, setup

setup(
    name="korbenware",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description="A bunch of Python DIY Linux desktop tools",
    author="Joshua Holbrook",
    author_email="josh.holbrook@gmail.com",
    url="https://github.com/jfhbrook/korbenware",
    scripts=["bin/korbenware-environment-loader"],
    entry_points=dict(
        console_scripts=[
            "kbconfig=korbenware.cli.config:main",
            "kbsession=korbenware.cli.session:main",
            "kbmenu=korbenware.cli.menu:main",
            "kbopen=korbenware.cli.open:main",
            "kbjournal=korbenware.cli.journal:main",
        ]
    ),
    keywords=[
        "X11",
        "window manager",
        "desktop environment",
        "X session",
        "session manager",
        "XDG",
        "dbus",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: Linux",
        "Programming Language :: Python :: 3.7",
        "Topic :: Other/Nonlisted Topic",
    ],
)
