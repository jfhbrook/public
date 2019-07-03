import os.path
import attr
import cattr
import toml
from pyxsession.util.decorators import representable
from pyxsession.xdg import XDG_CURRENT_DESKTOP, config_basedir
from pyxsession.xdg.autostart import XDG_AUTOSTART_DIRS
from pyxsession.xdg.applications import XDG_APPLICATIONS_DIRS


class LoadError(Exception):
    pass


class NoConfigurationFoundError(LoadError):
    def __init__(self):
        super().__init__(
            'No XDG configuration found! Try creating a file '
            'at `$HOME/.config/pyxsession/pyxsession.toml`.'
        )


def config(cls):
    return representable(attr.s(cls))


def subconfig(cls):
    return attr.ib(type=cls, default=cls())


def value(default=None):
    return attr.ib(default=default)


@config
class AutostartConfig:
    directories = value(XDG_AUTOSTART_DIRS)
    environment_name = value(XDG_CURRENT_DESKTOP)
    skip_unparsed = value(False)
    skip_invalid = value(False)


@config
class ApplicationsConfig:
    directories = value(XDG_APPLICATIONS_DIRS)
    skip_unparsed = value(False)
    skip_invalid = value(False)


@config
class MenuConfig:
    filename = value()


@config
class OpenConfig:
    filename = value()


@config
class MimeConfig:
    cache = value('/usr/share/applications/mimeinfo.cache')
    environment = value(XDG_CURRENT_DESKTOP)

@config
class BaseConfig:
    autostart = subconfig(AutostartConfig)
    menu = subconfig(MenuConfig)
    open = subconfig(OpenConfig)
    mime = subconfig(MimeConfig)
    applications = subconfig(ApplicationsConfig)
    # TODO: validate
    urls = value(dict())


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
