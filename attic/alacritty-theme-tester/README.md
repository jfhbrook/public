# alacritty-theme-tester

I wanted a way to test out the themes in <https://github.com/jwilm/alacritty/wiki/Color-schemes> quickly. I wrote these scripts to quickly flip through them. This isn't really packaged in a nice way, and it's not very nice to the config, but perhaps this will be helpful to you!

# steps

1. **BACK UP YOUR `~/.config/alacritty/alacritty.yml`!!** This script mangles it hard!! It will get reformatted and lose all comments.
2. Set up your python (recent 3, of course) environment. I'm using conda, so I wrote an `environment.yml` that you're free to use. If you're not using conda (probably), just find a way to get pyyaml in there. Lots of ways to skin this cat.
3. Adjust `base.yml` to your liking. Most likely you can accomplish (1) by copying that file straight to base.yml.
4. Make sure alacritty is running in auto-reload mode. run `alacritty --help` for more info
5. Optionally start build.sh for some inotify action, make sure you have the tools called installed!
6. Edit the `theme_name` variable in `build.py` to match the name before the `.yml` in the `./themes` directory
7. If you didn't start `build.sh`, run `build.py`
8. You should see alacritty abruptly change theme! If you see a big red ERROR, it's because of <https://github.com/jwilm/alacritty/pull/2054>
9. When you're done, put your config back the way it was, minus the new color scheme.

# license

MIT!
