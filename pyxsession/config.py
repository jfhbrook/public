import os.path
import attr
import cattr
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


@attr.s
class AutostartConfig:
    directories = attr.ib(default=XDG_AUTOSTART_DIRS)
    environment_name = attr.ib(default='pyxsession')
    skip_unparsed = attr.ib(default=False)
    skip_invalid = attr.ib(default=False)


@attr.s
class MenuConfig:
    filename = attr.ib(default=None)


@attr.s
class OpenConfig:
    filename = attr.ib(default=None)


@attr.s
class BaseConfig:
    autostart = attr.ib(type=AutostartConfig, default=AutostartConfig())
    menu = attr.ib(type=MenuConfig, default=MenuConfig())
    open = attr.ib(type=OpenConfig, default=OpenConfig())


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

    return cattr.structure(toml_config, BaseConfig)
