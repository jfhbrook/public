# -*- coding: utf-8 -*-

from os import path
from setuptools import find_packages, setup

setup(
    name="twisted_ipython",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description="An IPython extension for running twisted code",
    author="Joshua Holbrook",
    author_email="josh.holbrook@gmail.com",
    url="https://github.com/jfhbrook/twisted_ipython",
    keywords=[
        "IPython", "twisted", "crochet"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Framework :: IPython",
        "Framework :: Twisted"
    ]
)
