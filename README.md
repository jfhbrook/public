#### pyxsession

* https://github.com/xmonad/xmonad/issues/77
* https://wiki.lxde.org/en/LXSession#autostart_directories
* https://specifications.freedesktop.org/autostart-spec/autostart-spec-0.5.html
* https://stackoverflow.com/questions/25897836/where-should-i-write-a-user-specific-log-file-to-and-be-xdg-base-directory-comp
* https://pyxdg.readthedocs.io/en/latest/desktopentry.html
* https://specifications.freedesktop.org/desktop-entry-spec/latest/ar01s06.html
* https://github.com/twisted/twisted/blob/twisted-18.9.0/src/twisted/runner/procmon.py#L109
* http://raphael.slinckx.net/blog/documents/dbus-tutorial - tutorial that includes dbus activation

- [x] demo reading a toml config from ~/.config xdg etc
- [x] write something that parses the autostart directory
- [x] write something that can spawn/monitor processes based on twisted's procmon
- [x] patch twisted support into ipython's autoawait
- [x] investigate adding magics to run a non-awaiting result inside crochet's thread in jupyter/ipython
- [x] spin crochet magics out into a separate repo w/ a proper ipython-compatible license
- [x] write an api client and tools in jupyter to interact w/ dbus
- [x] write missing gshell function and spin out into separate repo w/ a proper glib-compatible license
- [x] write executor abstraction for running commands and desktop applications
- [x] write urwid app that will load and display the xdg menu and launch those applications in the background
- [x] write code for loading xdg mime data
- [x] generalize autostart loading code to also work with `xdg.BaseDirectory.load_data_paths('applications')` for the purposes of an applications database to x-ref with mime data
- [x] write code that will load an application database from /usr/share/applications and ~/.local/share/applications and stuff
- [x] make urwid stuff actually work
- [x] POC launcher for default applications
- [x] write dbus marshalling framework
- [ ] now make it support properties and events/signals
- [ ] Make default apps launcher actually good
- [ ] write tooling for editing local desktop entries and mime/defaults data
- [ ] create a dbus service for executing and monitoring programs with queries for state and soft exit
- [ ] clean up obvious spelling/formatting issues with gshell and rename LICENSE to COPYING
- [ ] write code that can take the base config and apply desktop entry overrides at the toml level
- [ ] build up templates and tooling for rendering `_repr_markdown` representations of the config for inspection in nteract
- [ ] write something that can poke at dbus services using xdg rules (should be way easy)
- [ ] write something that can turn that coherent configuration into autostarted processes managed by our procmon and add to server
- [ ] add pyxsession to my xinitrc (manually activate the conda env)
- [ ] write toml thinger for running cron tasks
- [ ] make toml thinger for configuring running the window manager as a special process
- [ ] switch completely to using pyxsession
- [ ] write code that will detect processes w/ open x windows
- [ ] write code in pyxsession that will gracefully attempt to close those processes before doing a hard exit
- [ ] GET LICENSING SORTED OUT!!
- [ ] set up a PKGBUILD in a separate repo that will build and install globally
- [ ] bonus - implement dependencies on top of procmon with a similar technique as in coolbot98 w/ services
