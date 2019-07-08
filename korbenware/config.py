import os.path

import attr
import cattr
import toml
from twisted.logger import LogLevel

from korbenware.dbus import DBusField, List, Str, Variant
from korbenware.dbus.marshmallow.schema import DBUS_FIELD, DBUS_NESTED
from korbenware.logger import create_logger
from korbenware.util.decorators import representable
from korbenware.xdg import XDG_CURRENT_DESKTOP, config_basedir
from korbenware.xdg.autostart import XDG_AUTOSTART_DIRS
from korbenware.xdg.applications import XDG_APPLICATIONS_DIRS


class LoadError(Exception):
    pass


class NoConfigurationFoundError(LoadError):
    def __init__(self):
        super().__init__(
            'No XDG configuration found! Try creating a file '
            'at `$HOME/.config/korbenware/korbenware.toml`.'
        )


def config(cls):
    return representable(attr.s(cls))


def subconfig(cls):
    return attr.ib(
        type=cls,
        default=attr.Factory(cls),
        metadata={DBUS_NESTED: cls}
    )


def value(default=None, field=None):
    return attr.ib(default=default, metadata={DBUS_FIELD: field or Variant()})


@config
class AutostartConfig:
    directories = value(XDG_AUTOSTART_DIRS, field=List(Str()))
    environment_name = value(XDG_CURRENT_DESKTOP)
    skip_unparsed = value(False)
    skip_invalid = value(False)


@config
class ApplicationsConfig:
    directories = value(XDG_APPLICATIONS_DIRS, field=List(Str()))
    skip_unparsed = value(False)
    skip_invalid = value(False)


@config
class MenuConfig:
    filename = value()


@config
class MimeConfig:
    cache = value('/usr/share/applications/mimeinfo.cache')
    environment = value(XDG_CURRENT_DESKTOP)


@config
class LoggerConfig:
    level = value('debug')


@config
class MetaConfig:
    config_filename = value('???')


@config
class BaseConfig:
    autostart = subconfig(AutostartConfig)
    meta = subconfig(MetaConfig)
    menu = subconfig(MenuConfig)
    mime = subconfig(MimeConfig)
    applications = subconfig(ApplicationsConfig)
    logger = subconfig(LoggerConfig)
    # TODO: validate
    urls = value(dict(), field=DBusField('a{ss}'))


def load_config():
    basedir = config_basedir()

    if not basedir:
        raise NoConfigurationFoundError()

    filename = os.path.join(basedir, 'korbenware.toml')

    try:
        f = open(filename, 'r')
    except FileNotFoundError as e:
        raise NoConfigurationFoundError() from e

    with f:
        toml_config = toml.load(f)

    structured = cattr.structure(toml_config, BaseConfig)

    structured.meta.config_filename = filename

    return structured


log = create_logger()


def _log_config(path, obj, level):
    for attr_ in obj.__attrs_attrs__:
        if hasattr(attr_.type, '__attrs_attrs__'):
            _log_config(path + [attr_.name], getattr(obj, attr_.name), level)
        else:
            log.emit(
                level,
                'config: {path}={value}',
                path='.'.join(path + [attr_.name]),
                value=getattr(obj, attr_.name)
            )


def log_config(config, level=LogLevel.debug):
    log.emit(
        level,
        'Loaded configuration from {filename}...',
        filename=config.meta.config_filename
    )
    _log_config(['config'], config, level)


def config_dbus_object(service, config):
    obj = service.object('/korbenware/Config')

    @obj.method([], BaseConfig)
    def get_base_config():
        return config

    return obj
