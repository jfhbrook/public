from xdg.BaseDirectory import load_first_config

XDG_RESOURCE = 'pyxsession'


def config_basedir(resource=XDG_RESOURCE):
    return load_first_config(resource)
