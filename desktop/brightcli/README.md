# brightcli

A little bash script that adjusts the brightness on my screen, and a udev
rule to make it work. Assumes an `intel_backlight`.

# install/setup

You'll want to read this:

<https://wiki.archlinux.org/index.php/Backlight#ACPI>

This script uses that API with those udev rules.

After that, you'll want to **edit brightcli and backlight.rules** to make sure
they work for *your* backlight.

After that, go ahead and put things where they need to go. If you're using
arch like I am, a `makepkg -si` should suffice.

# usage

* `brightctl up` to bump the brightness
* `brightctl down` to decrease brightness
* `brightctl` to get a reasonable default

I wired these up in xmonad to use my topbar keys. See
[this thing on multimedia keys](https://superuser.com/questions/389737/how-do-you-make-volume-keys-and-mute-key-work-in-xmonad)
for hints, it's largely the same process.

# license

This software is covered by the Mozilla Public License with additional
restrictions. See the COPYING and NOTICE files for details.
