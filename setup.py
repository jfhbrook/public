# -*- coding: utf-8 -*-

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
    scripts=[
        'bin/pyxsession-environment-loader'
    ],
    entry_points=dict(
        console_scripts=[
            'kbconfig=korbenware.cli.config:main',
            'kbmenu=korbenware.cli.menu:main',
            'kbopen=korbenware.cli.open:main'
        ]
    ),
    keywords=[
        "X11", "window manager", "desktop environment", "X session",
        "session manager", "XDG", "dbus"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: Linux",
        "Programming Language :: Python :: 3.7",
        "Topic :: Other/Nonlisted Topic"
    ]
)
