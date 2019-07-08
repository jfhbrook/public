# -*- coding: utf-8 -*-

from os import path
from setuptools import find_packages, setup

setup(
    name="pyxsession",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description="A little X session manager written in python",
    author="Joshua Holbrook",
    author_email="josh.holbrook@gmail.com",
    url="https://github.com/jfhbrook/pyxsession",
    entry_points=dict(
        console_scripts=[
            'pyxconfig=pyxsession.cli.config:main',
            'pyxmenu=pyxsession.cli.menu:main',
            'pyxopen=pyxsession.cli.open:main'
        ]
    ),
    keywords=[
        "X11", "window manager", "desktop environment", "X session",
        "session manager"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: Linux",
        "Programming Language :: Python :: 3.7",
        "Topic :: Other/Nonlisted Topic"
    ]
)
