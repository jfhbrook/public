# -*- coding: utf-8 -*-

from os import path
from setuptools import find_packages, setup

README_md = path.join(path.abspath(path.dirname(__file__)), 'README.md')

with open(README_md, 'r') as f:
    long_description = f.read()

setup(
    name="twisted_ipython",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'twisted',
        'crochet',
        'ipython'
    ],
    description="An IPython extension for running twisted code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joshua Holbrook",
    author_email="josh.holbrook@gmail.com",
    url="https://github.com/jfhbrook/twisted_ipython",
    keywords=[
        "IPython", "twisted", "crochet"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Framework :: IPython",
        "Framework :: Twisted"
    ]
)
