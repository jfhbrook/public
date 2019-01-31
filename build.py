import os

from yaml import load, dump

# change theme here
theme_name = 'gruvbox_dark'

with open('./base.yml', 'r') as f:
    base = load(f)

with open('./themes/{}.yml'.format(theme_name), 'r') as f:
    colors = load(f)


base['colors'] = colors['colors']

with open(os.path.expanduser('~/.config/alacritty/alacritty.yml'), 'w') as f:
    dump(base, f)
