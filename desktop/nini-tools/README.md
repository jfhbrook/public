# nini-tools

Some stuff I put together for locking/sleeping. Includes a fun wrapper around
physlock and a systemd hook for locking on sleep.

## Dependencies

* cowsay
* fortune
* a bunch of custom fortune files I installed off AUR

You will probably want to modify this project to use your fortune groups of
choice.

## Install

If you're using arch, `makepkg -si` in this directory should work. Otherwise,
it's just a script and a systemd user hook so you can probably open the
`PKGBUILD` and crib off that.

That will install a `lockenate-physlock-wrapper` script, a `nini@` user
service, and a `lockenate` script that wraps manually starting the nini user
service. You can run `systemctl enable "nini@${USER}"` to make the lock script
automatically run when the computer goes to sleep.

I hooked up `sudo lockenate` to a keypress in my window manager and added that
command to my sudoers. Up to you!

## License

A lot of this is cribbed off the Arch wiki and I tbh don't know how that's
licensed. Shrug!