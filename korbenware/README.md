# korbenware 🦜

## What

Korbenware is a collection of bash scripts intended for desktop usage. Some of
them will work in MacOS, but some of them are Linux only and a few of them
depend on [sway](https://swaywm.org/).

They're pretty messy right now and *wildly* inconsistent, but I'm using them
on my Fedora Thinkpad running Sway, and a handful of them on MacOS as well.

## Install

You can copy the scripts in `./bin` wherever you like! Someday I'll make
package manifests, but that day's not today.

## kbconfig

Manage korbenware configs in `~/.config/korbenware/config.ini`.

### Dependencies

* System python3

## kbbg

Change the background in sway.

### Dependencies

* bash
* fzf
* swaymsg
* [viu](https://crates.io/crates/viu)

## kbdesktop

Basic interaction with .desktop files for both the
[XDG application menu](https://specifications.freedesktop.org/menu-spec/menu-spec-latest.html)
and [XDG autostart](https://specifications.freedesktop.org/autostart-spec/0.5/ar01s02.html).

### Dependencies

* System python3
* System [pyxdg](https://www.freedesktop.org/wiki/Software/pyxdg/)

## kblock

A screen locking script. Works with swaylock and *probably* works with
[physlock](https://github.com/muennich/physlock).

### Dependencies

* bash
* Either swaylock or physlock
* If using swaylock, cowsay and fortune-mod
* `kbconfig`

## kbmenu

A command line XDG application menu launcher, using fzf.

### Dependencies

* bash
* fzf
* System Python 3
* System pyxdg

## kbnotify

A collection of XDG notifications for things like volume/mute, screenshots, battery
status.

To hook up the battery, you can set up some [udev](https://wiki.archlinux.org/title/udev)
rules. Adopting the strategy used in [Ventto/batify](https://github.com/Ventto/batify)
gets you a file like this:

```
ACTION=="change", KERNEL=="BAT0", \
SUBSYSTEM=="power_supply", \
ATTR{status}=="Discharging", \
ATTR{capacity}=="[0-9]", \
IMPORT{program}="/usr/bin/xpub", \
RUN+="/bin/su $env{XUSER} -c '/usr/bin/kbnotify battery-critical $attr{capacity}'"

ACTION=="change", KERNEL=="BAT0", \
SUBSYSTEM=="power_supply", \
ATTR{status}=="Discharging", \
ATTR{capacity}=="1[0-5]", \
IMPORT{program}="/usr/bin/xpub", \
RUN+="/bin/su $env{XUSER} -c '/usr/bin/kbnotify battery-low $attr{capacity}'"

SUBSYSTEM=="power_supply", ACTION=="change", \
ENV{POWER_SUPPLY_ONLINE}=="0", ENV{POWER}="off", \
OPTIONS+="last_rule", \
IMPORT{program}="/usr/bin/xpub", \
RUN+="/bin/su $env{XUSER} -c '/usr/bin/kbnotify unplugged'"

SUBSYSTEM=="power_supply", ACTION=="change", \
ENV{POWER_SUPPLY_ONLINE}=="1", ENV{POWER}="on", \
OPTIONS+="last_rule", \
IMPORT{program}="/usr/bin/xpub", \
RUN+="/bin/su $env{XUSER} -c '/usr/bin/kbnotify plugged-in'"
```

For volume notifications, you can call kbnotify after using a different tool
(such as pactl) to adjust the volume. For example, I have something like
this in my sway config:

```
bindsym XF86AudioRaiseVolume exec bash -c 'pactl set-sink-volume @DEFAULT_SINK@ +5% && kbnotify volume-up'
bindsym XF86AudioLowerVolume exec bash -c 'pactl set-sink-volume @DEFAULT_SINK@ -5% && kbnotify volume-down'
bindsym XF86AudioMute exec bash -c 'pactl set-sink-mute @DEFAULT_SINK@ toggle && kbnotify toggle-mute'
b
```

For more, look at kbscreenshot.

### Dependencies

* bash
* notify-send
* pactl (volume hooks)

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

## kbscreenshot

A thin wrapper around [grim](https://github.com/emersion/grim), [slurp](https://github.com/emersion/slurp) and [wl-copy](https://github.com/bugaevc/wl-clipboard). Prints
the created file to output, or `CLIPBOARD` if sent to the clipboard.

kbnotify knows what to do with the output of kbscreenshot, so you can plumb
them together pretty easy. For example, in sway:

```
bindsym Print exec bash -c 'kbnotify screenshot "$(kbscreenshot)"
bindsym Shift+Print exec bash -c 'kbnotify screenshot "$(kbscreenshot --select)"
bindsym $mod+Print exec bash -c 'kbnotify screenshot "$(kbscreenshot --clipboard)"
bindsym $mod+Shift+Print exec bash -c 'kbnotify screenshot "$(kbscreenshot --select --clipboard)"
```

### Dependencies

* bash
* grim
* slurp
* wl-copy

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

# Licensing

This code is licensed under the Mozilla Public License v2.0. See `COPYING` and
`NOTICE` for details.
