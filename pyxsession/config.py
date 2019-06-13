import os.path
import toml
from pyxsession.xdg import XDG_AUTOSTART_DIRS, config_basedir


class LoadError(Exception):
    pass


class NoConfigurationFoundError(LoadError):
    def __init__(self):
        super().__init__(
            'No XDG configuration found! Try creating a file '
            'at `$HOME/.config/pyxsession/pyxsession.toml`.'
        )


BASE_CONFIG = dict(
    autostart=dict(
        directories=XDG_AUTOSTART_DIRS,
        environment_name='pyxsession',
        skip_unparsed=False,
        skip_invalid=False
    )
)


def load_config():
    basedir = config_basedir()

    if not basedir:
        raise NoConfigurationFoundError()

    filename = os.path.join(basedir, 'pyxsession.toml')

    try:
        f = open(filename, 'r')
    except FileNotFoundError as e:
        raise NoConfigurationFoundError() from e

    with f:
        toml_config = toml.load(f)

    config = {}

    for section, section_base_config in BASE_CONFIG.items():
        config[section] = dict()
        for k, v in section_base_config.items():
            if section in toml_config and k in toml_config[section]:
                config[section][k] = toml_config[section][k]
            else:
                config[section][k] = v

    return config
