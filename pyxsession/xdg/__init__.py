import os
from xdg.BaseDirectory import load_first_config

XDG_RESOURCE = 'pyxsession'
XDG_CURRENT_DESKTOP = os.environ.get('XDG_CURRENT_DESKTOP', XDG_RESOURCE)


def config_basedir(resource=XDG_RESOURCE):
    return load_first_config(resource)
