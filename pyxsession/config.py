import os.path
import toml
from xdg import BaseDirectory

XDG_RESOURCE = 'pyxsession'


class LoadError(Exception):
    pass


class NoConfigurationFoundError(LoadError):
    def __init__(self):
        super().__init__(
            'No XDG configuration found! Try creating a file '
            'at `$HOME/.config/pyxsession/pyxsession.toml`.'
        )


def load_config():
    basedir = BaseDirectory.load_first_config(XDG_RESOURCE)

    if not basedir:
        # TODO: Can we set a default pyxsession.toml to be nice?
        raise NoConfigurationFoundError()

    filename = os.path.join(basedir, 'pyxsession.toml')

    try:
        f = open(filename, 'r')
    except FileNotFoundError as e:
        raise NoConfigurationFoundError() from e

    with f:
        base_config = toml.load(f)

    # TODO: Process the base config in some way

    return base_config
