# sie7e labs filesync professional edition

sie7e filesync (s7sync) is a tool for automatically synchronizing files using
git. it watches any configured git repositories, commits and pushes local
changes automatically, and pulls from upstream regularly. it fits a similar
niche to dropbox or nextcloud, except on top of git.

filesync is cross-platform and (will eventually) work with git bash in windows.

**WARNING:** these docs are for the s7sync I want to develop over the coming
weeks - a lot of this doesn't work yet!

## install

### fedora

```sh
dnf copr add jfhbrook/joshiverse
dnf install s7sync
```

### macos (soon)

```sh
brew tap add jfhbrook/homebrew
brew install s7sync
```

### windows

I will eventually make a windows msi/installer. timeline TBD!

### cargo

```sh
cargo install s7sync
```

## setup

first, add a repository to sie7e filesync. at the command line, run:

```sh
cd path/to/your/repository
s7sync add .
```

or, in the (eventual) GUI, click "add" and choose the folder in the file picker.

## run

### desktop

the fedora package includes an application desktop entry and may be launched
in gui mode through the gnome or kde applications menu.

an eventual windows package will add a shortcut to the start menu. an eventual
homebrew package will hopefully install s7sync as an application.

### command line

to start s7sync on the comand line, run:

```sh
s7sync
```

to start s7sync on the command line in gui mode, run:

```sh
s7sync ui
```

### systemd

the fedora package installs a systemd unit, which will run headless s7sync in
the background:

```sh
systemctl enable s7sync --user
```

### autostart

alternately, use your os's autostart capability to launch s7sync in gui mode.
to enable autostart, run:

```sh
s7sync autostart enable
```

on linux, this will create an xdg autostart desktop file (supported by gnome,
kde and most linux desktop environments). on windows, this will (eventually)
create a relevant shortcut.

to disable autostart (by deleting the desktop file or shortcut), run:

```sh
s7sync autostart disable
```

# license

this code is licensed under the mozilla public license v2.0. see `COPYING` and
`NOTICE` for details.
