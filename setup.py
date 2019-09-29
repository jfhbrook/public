# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name="db_hooks",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description="A simple sqlalchemy connection configuration manager",
    author="Joshua Holbrook",
    author_email="josh.holbrook@gmail.com",
    url="https://github.com/jfhbrook/db_hooks",
    install_requires=["appdirs", "click", "pygments", "sqlalchemy", "toml"],
    entry_points=dict(console_scripts=["db_hooks=db_hooks.cli:main"]),
    keywords=["sqlalchemy", "repl", "jupyter", "database"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: Linux",
        "Programming Language :: Python :: 3.7",
        "Topic :: Other/Nonlisted Topic",
    ],
)
