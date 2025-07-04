# Josh Holbrook's Public Software

## Hello

This repository contains most of my open source and source-available code.

For my GPL-compatible free software, check out [my GPL-compatible software repository](https://github.com/jfhbrook/public-gpl).

## Contents

### anisotropy

**<https://github.com/jfhbrook/anisotropy>**

This project contains my masters thesis. It is licensed under the Community
Research and Academic Programming License v0 Beta 0.

### coprctl

A bash script, using `copr-cli` and `yq`, to implement an infrastructure-as-code
pattern similar to `kubectl apply`. It is licensed MIT.

### copr-tools

A Docker image, plus some Bash scripts, for running RPM and COPR related tools - including `coprctl` - on other operating systems, namely MacOS.

### crystalfontz

**<https://github.com/jfhbrook/crystalfontz>**

A client library for Crystalfontz LCD displays.

### dbus-iface-markdown

This is a little perl script I used for generating markdown documentation from a live dbus interface. I'm using this in [plusdeck](https://github.com/jfhbrook/plusdeck) to generate documentation for the Dbus interface. This is an alternative to reflecting off the Python objects that captures the true state of the service as seen by Dbus/Systemd.

### dosapp

**<https://github.com/jfhbrook/dosapp>**

A small application for installing and running DOS applications in DOSBox.
It's written in go. License is MIT.

### heos

The `heos` folder contains a simple CLI wrapper that connects to Denon HEOS
devices over Telnet. For further documentation, run `./heos/bin/heos -h`.
License is MIT.

### icons

There are some Windows icons I made in high school, around 2004. License is cc-by-sa-4.0.

### korben

RIP 2010-2022

### korbenware

A collection of scripts I use to glue my Linux desktop and general CLI experience
together. Available under a MPL v2.0 license.

### matanuska

**<https://github.com/jfhbrook/matanuska>**

Matanuska is an ongoing project to implement my own programming language, in
the BASIC family. It's currently written in TypeScript. Matanuska is a major
undertaking, and still needs a lot of work! It's licensed under the MPL v2.0.

#### crafting-interpreters

**<https://github.com/jfhbrook/crafting-interpreters>**

As part of this project, I worked through
[Crafting Interpreters](https://craftinginterpreters.com/) by Robert Nystrom.
It includes my implementation of `clox`, as well as a port of `jlox` to
TypeScript.

### old-memes

old memes is an old-school Node.js anti-framework built around the good parts
of [flatiron](https://github.com/flatiron), a selection of classic [substack](https://github.com/substack) libraries and the few worthwhile
things I personally wrote between roughly 2009 and 2016 - with a targeted
dash of modern conveniences. It's a big project, so see [its README](./old-memes/README.md) for more
details.

#### hoarders

**<https://github.com/jfhbrook/hoarders>**

One of my old modules includes `hoarders`, Node.JS's most complete "utility
grab bag."

### omsxctl

`omsxctl` is a small rust CLI for controlling [openmsx](https://openmsx.org/) over its socket interface.
It can be useful if you're doing retro [MSX](https://en.wikipedia.org/wiki/MSX) game development.

### openscad

These are files I've written for OpenSCAD. So far, these are available under a
MPL v2.0 license.

### Packages

I post packages on a couple of personal registries:

* **COPR:** <https://github.com/jfhbrook/copr>
* **Homebrew:** <https://github.com/jfhbrook/homebrew-joshiverse>

### plusdeck

**<https://github.com/jfhbrook/plusdeck>**

I own a [Plus Deck 2c PC Cassette Deck](https://www.frequencycast.co.uk/plusdeck.html),
which is a casette player in a 5.25" drive bay form factor with rs-232 serial
controls. This project contains library code for interacting with its serial
interface over Python, including a Jupyter interface. It's licensed MIT.

### politics

These are projects I've done for political organizations. For more information,
see [its README](./politics/README.md).

### plusdeck

**<https://github.com/jfhbrook/plusdeck>**

A client library for the Plus Deck 2C Cassette Drive.

### pyee

**<https://github.com/jfhbrook/pyee>**

This is a loose port of the Node.js EventEmitter with special support for
coroutines and concurrent programming. It is licensed under an MIT license.

### pytest-gak

A Pytest plugin and CLI helper for running interactive, prompt-based tests.

### resume

**<https://github.com/jfhbrook/resume>**

This is my resume! This repository contains a .pdf and .docxPDFs version of
my standard 2-page resume.

### templates

**<https://github.com/jfhbrook/templates>**

A small collection of cookiecutter templates, MIT-licensed. These include
templates for Python, Flask, TypeScript, Nest.js, and PowerShell.

### tplinkctl

A simple CLI tool for interacting with my TP-Link home router.

### twisted_ipython

This is a module that makes autoawait work in IPython using Twisted. It is
licened under a BSD 3-clause license with additional restrictions. See
the included NOTICE file for details.

For more information, read [the blog post on dev.to](https://dev.to/jfhbrook/twistedipython-autoawait-in-jupyter-notebooks-with-twisted-lee).
