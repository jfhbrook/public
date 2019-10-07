# -*- coding: utf-8 -*-
import os.path

from setuptools import find_packages, setup

README_md = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")

with open(README_md, "r") as f:
    long_description = f.read()

setup(
    name="db_hooks",
    version="0.3.0",
    packages=find_packages(),
    include_package_data=True,
    description="A simple sqlalchemy connection configuration manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joshua Holbrook",
    author_email="josh.holbrook@gmail.com",
    url="https://github.com/jfhbrook/db_hooks",
    python_requires=">=3.5",
    install_requires=[
        "appdirs",
        "attrs",
        "cachetools",
        "cattrs",
        "click",
        "pygments",
        "sqlalchemy",
        "toml",
    ],
    entry_points=dict(console_scripts=["db_hooks=db_hooks.cli:main"]),
    keywords=["sqlalchemy", "repl", "jupyter", "database"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
    ],
)
