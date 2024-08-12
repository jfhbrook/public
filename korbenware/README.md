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

You should be able to install Korbenware from my Homebrew tap:

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

Change the background.

### Dependencies

* bash
* fzf
* sway (Linux)
* [viu](https://crates.io/crates/viu)

## kbmenu

A command line application menu launcher, using fzf.

### Dependencies

* bash
* fzf
* System Python 3
* System pyxdg (Linux)

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

# Publishing

The publishing process does the following:

1. Tags the release with [tito](https://github.com/rpm-software-management/tito)
2. Pushes the tag to GitHub
3. Creates a tarball including the scripts, license files and README
4. Creates a GitHub release containing that tarball
5. Generates an updated Homebrew formula
6. Commits and pushes the Homebrew formula
7. Applies the current COPR package configuration
8. Triggers a build of the COPR package

## Dependencies

- `git`, of course
- The `gh` CLI tool
- [exercise-bike](https://npm.im/exercise-bike) - available on my COPR and
  Homebrew tap
- `tito`  - available on Fedora repositories
- [copr-cli](https://developer.fedoraproject.org/deployment/copr/copr-cli.html) -
  available on Fedora repositories
- [coprctl](https://github.com/jfhbrook/public/tree/main/coprctl) - available
  on my COPR
- My [homebrew tap](https://github.com/jfhbrook/homebrew-joshiverse) cloned
  with the `$HOMEBREW_TAP` environment variable set to its path

## Process

First, set up this project on a Fedora machine and install all the
dependencies. Due to the dependencies on `tito` and `copr-cli`, releases can
only be triggered on Fedora. **TODO**: Create a Docker image that can do the
release in a cross-platform manner.

Then, open the `justfile` and update the `VERSION` and `PATCH` variables.
Generally, `PATCH` should be set to `1`, but may be incremented if a package
itself has a bug.

Second, run `just publish`. This should trigger the whole process.

# History

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
[/usr/libexec/sway/volume-helper](https://gitlab.com/fedora/sigs/sway/sway-config-fedora/-/blob/fedora/scripts/sway/volume-helper?ref_type=heads).

### kbscreenshot

Fedora uses a tool called
[grimshot](https://manpages.ubuntu.com/manpages/jammy/man1/grimshot.1.html)
for taking screenshots.

# Licensing

This code is licensed under the Mozilla Public License v2.0. See `COPYING` and
`NOTICE` for details.
