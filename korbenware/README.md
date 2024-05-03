# korbenware 🦜

## What

Korbenware is a collection of tools for CLI-driven interaction with your
desktop. They are meant to be paired with [Sway](https://swaywm.org/) in
Linux. They should also, for the most part, work in MacOS.

These scripts need a little help. They used to work, mostly, on my older
Sway/Fedora setup that predates
[Fedora Sway Spin](https://fedoraproject.org/spins/sway/). But I recently
switched to Sway Spin and am in the process of tidying them up.

## Install

### Fedora

You should be able to install Korbenware from COPR:

```bash
sudo dnf copr enable jfhbrook/joshiverse
dnf install korbenware
```

### MacOS

**TODO:** Package korbenware in Homebrew tap. kbconfig, kbopen and kbprev
already work in MacOS. kbbg and kbmenu should work with some love:

- [change background in macos](https://apple.stackexchange.com/questions/40644/how-do-i-change-desktop-background-with-a-terminal-command)
- [detecting platform with python](https://stackoverflow.com/questions/1854/how-to-identify-which-os-python-is-running-on)
- [list all applications](https://www.howtogeek.com/409377/how-to-list-all-applications-on-a-mac/)

Once I create a Formula in my homebrew tap, you should be able to run:

```bash
brew install jfhbrook/joshiverse/korbenware
```

### Other Linux Distros

The scripts in `./bin` should be portable. As long as you have the dependencies
installed, you should be able to
copy them onto your `PATH` and be
set:

```bash
cp ./bin/* ~/.local/bin/
chmod +x ~/.local/bin/kb*
```

## kbconfig

Manage korbenware configs in `~/.config/korbenware/config.ini`.

### Dependencies

* System python3

## kbbg

Change the background (in sway).

### Dependencies

* bash
* fzf
* sway
* [viu](https://crates.io/crates/viu)

## kbmenu

A command line (XDG) application menu launcher, using fzf.

### Dependencies

* bash
* fzf
* System Python 3
* System pyxdg

## kbopen

Open a directory, file or url:

* If a directory, search for the file using fzf
* If one of many whitelisted mime types, open the file using the $EDITOR
* If a URL or non-text file, open with either gio, MacOS open or xdg-open

### Dependencies

* bash
* fzf
* find, grep, sed
* file

## kbprev

Preview files in the terminal, using viu, bat and pdftotext. Used by kbopen.

### Dependencies

* bash
* [bat](https://crates.io/crates/bat) for pretty colors and line numbers
* viu for image preview
* pdftotext for (bad) pdf preview
* cat, if any of these are missing

## Publishing

### COPR

Korbenware uses [tito](https://github.com/rpm-software-management/tito) for
managing COPR releases. To tag, release and build:

1. Open the `justfile` and update the `VERSION` variable
2. Run `just publish`

## What Happened to the Python Korbenware?

A few years ago, I attempted to write a bunch of Linux desktop environment
stuff on top of Python and [Twisted](https://twistedmatrix.com/trac/). It
had a few good tricks, but it ended up being too complex for my needs - and
then my needs changed! It was targeting X11 and xmonad, and I don't use either
anymore.

A lot of ideas from old Korbenware have been copied or ported to these scripts.
A few of them - namely the dbus framework, the session manager and an
inheritance-based composition for XDG helpers - turned out to be bad. Someday
I'll dust off the systemd Twisted logger and the Jupyter UX stuff. I still
have the code, just in my attic.

## What Happened to the Other Tools?

A number of tools were removed from Korbenware because they're no longer
necessary given you're using Fedora Sway Spin and/or its choice of tools:

### kbdesktop

Fedora uses sway-systemd to trigger XDG autostart:

<https://github.com/alebastr/sway-systemd>

### kblock

`kblock` was originally a fun wrapper around
[physlock](https://github.com/xyb3rt/physlock), and was later a wrapper around
swaylock that introduced theming. However, I only have a need for swaylock,
and my swaylock configuration needs are met through swaylock's config file.

### kbnotify

`kbnotify` was glue for various notifications in my sway desktop, such as
volume changes. Fedora solves this in various ways depending on the particular
binding. In the volume case, it uses a script located at
`/usr/libexec/sway/volume-helper`.

### kbscreenshot

Fedora uses a tool called
[grimshot](https://manpages.ubuntu.com/manpages/jammy/man1/grimshot.1.html)
for taking screenshots.

# Licensing

This code is licensed under the Mozilla Public License v2.0. See `COPYING` and
`NOTICE` for details.
