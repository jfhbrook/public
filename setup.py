# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

long_description = """
twisted_ipython
===============

An `IPython <https://ipython.org/>`__ extension that uses
`crochet <https://github.com/itamarst/crochet>`__ to enable running
`Twisted <https://twistedmatrix.com/trac/>`__ in IPython and
`Jupyter <https://jupyter.org/>`__ notebooks.

For more information, check out the
`README <https://github.com/jfhbrook/twisted_ipython/blob/master/README.ipynb>`__.
"""  # noqa

setup(
    name="twisted_ipython",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'twisted',
        'crochet',
        'ipython'
    ],
    description="An IPython extension for running twisted code",
    long_description=long_description,
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
