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
- [ ] write something that can assemble a full coherent Configuration based on our base config + the parsed autostart directory
- [ ] build up templates and tooling for rendering `_repr_markdown` representations of the config for inspection in jupyter
- [ ] investigate adding magics to run a non-awaiting result inside crochet's thread in jupyter/ipython
- [ ] write something that can poke at dbus services using xdg rules (should be way easy)
- [ ] make a stub server that can speak dbus query state and soft exit
- [ ] write an api client and tools in jupyter to interact w/ dbus
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
