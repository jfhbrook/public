import os.path
from typing import Dict

import attr
import cattr
import toml
from twisted.logger import LogLevel

from korbenware.dbus import DBusField, List, Str, Variant
from korbenware.dbus.marshmallow.schema import DBUS_FIELD, DBUS_NESTED
from korbenware.logger import create_logger
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable
from korbenware.xdg import XDG_CURRENT_DESKTOP, config_basedir
from korbenware.xdg.autostart import XDG_AUTOSTART_DIRS
from korbenware.xdg.applications import XDG_APPLICATIONS_DIRS


class LoadError(Exception):
    pass


class NoConfigurationFoundError(LoadError):
    def __init__(self):
        super().__init__(
            "No XDG configuration found! Try creating a file "
            "at `$HOME/.config/korbenware/korbenware.toml`."
        )


def config(cls):
    return markdownable(representable(attr.s(cls)))


def subconfig(cls):
    return attr.ib(type=cls, default=attr.Factory(cls), metadata={DBUS_NESTED: cls})


def value(default=None, field=None):
    return attr.ib(default=default, metadata={DBUS_FIELD: field or Variant()})


@config
class ApplicationsConfig:
    directories = value(XDG_APPLICATIONS_DIRS, field=List(Str()))
    skip_unparsed = value(False)
    skip_invalid = value(False)


@config
class AutostartConfig:
    directories = value(XDG_AUTOSTART_DIRS, field=List(Str()))
    environment_name = value(XDG_CURRENT_DESKTOP)
    skip_unparsed = value(False)
    skip_invalid = value(False)


@config
class DBusConfig:
    namespace = value("org.jfhbrook.korbenware")


@config
class FormatConfig:
    pygments_formatter = value("trac")


@config
class LoggerConfig:
    level = value("debug")


@config
class MenuConfig:
    filename = value()


@config
class MetaConfig:
    config_filename = value("???")


@config
class MimeConfig:
    cache = value("/usr/share/applications/mimeinfo.cache")
    environment = value(XDG_CURRENT_DESKTOP)


@config
class ProcessConfig:
    exec = value(attr.Factory(list))
    monitor = value(True)
    restart = value(False)
    cleanup = value(False)


@config
class CriticalProcessConfig:
    exec = value(attr.Factory(list))
    monitor = value(True)
    restart = value(True)
    cleanup = value(False)


@config
class ExecutorsConfig:
    primary = attr.ib(type=Dict[str, ProcessConfig], default=attr.Factory(dict))
    critical = attr.ib(
        type=Dict[str, CriticalProcessConfig], default=attr.Factory(dict)
    )


@config
class BaseConfig:
    applications = subconfig(ApplicationsConfig)
    autostart = subconfig(AutostartConfig)
    dbus = subconfig(DBusConfig)
    executors = subconfig(ExecutorsConfig)
    format = subconfig(FormatConfig)
    logger = subconfig(LoggerConfig)
    menu = subconfig(MenuConfig)
    meta = subconfig(MetaConfig)
    mime = subconfig(MimeConfig)
    urls = value(dict(), field=DBusField("a{ss}"))


def load_config():
    basedir = config_basedir()

    if not basedir:
        raise NoConfigurationFoundError()

    filename = os.path.join(basedir, "korbenware.toml")

    try:
        f = open(filename, "r")
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
        if hasattr(attr_.type, "__attrs_attrs__"):
            _log_config(path + [attr_.name], getattr(obj, attr_.name), level)
        else:
            log.emit(
                level,
                "config: {path}={value}",
                path=".".join(path + [attr_.name]),
                value=getattr(obj, attr_.name),
            )


def log_config(config, level=LogLevel.debug):
    log.emit(
        level,
        "Loaded configuration from {filename}...",
        filename=config.meta.config_filename,
    )
    _log_config(["config"], config, level)
