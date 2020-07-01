import os.path

import attr
import cattr
import toml
from twisted.logger import LogLevel

from korbenware.dbus import Bool, DBusField, Dict, List, Str, Variant
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
    skip_unparsed = value(False, field=Bool())
    skip_invalid = value(False, field=Bool())


@config
class AutostartConfig:
    directories = value(XDG_AUTOSTART_DIRS, field=List(Str()))
    environment_name = value(XDG_CURRENT_DESKTOP, field=Str())
    skip_unparsed = value(False, field=Bool())
    skip_invalid = value(False, field=Bool())


@config
class DBusConfig:
    namespace = value("org.jfhbrook.korbenware", field=Str())


@config
class FormatConfig:
    pygments_formatter = value("trac", field=Str())


@config
class LoggerConfig:
    level = value("debug", field=Str())


@config
class MenuConfig:
    filename = value(field=Str())


@config
class MetaConfig:
    config_filename = value("???", field=Str())


@config
class MimeConfig:
    cache = value("/usr/share/applications/mimeinfo.cache", field=Str())
    environment = value(XDG_CURRENT_DESKTOP, field=Str())


@config
class ProcessConfig:
    exec = value(attr.Factory(list), field=List(Str()))
    monitor = value(True, field=Bool())
    restart = value(False, field=Bool())
    cleanup = value(False, field=Bool())


@config
class CriticalProcessConfig:
    exec = value(attr.Factory(list), field=List(Str()))
    monitor = value(True, field=Bool())
    restart = value(True, field=Bool())
    cleanup = value(False, field=Bool())


@config
class ExecutorsConfig:
    primary = value(field=Dict(Str(), ProcessConfig))
    critical = value(field=Dict(Str(), CriticalProcessConfig))


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
    urls = value(attr.Factory(dict), field=Dict(Str(), Str()))


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
