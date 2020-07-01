import pytest

from korbenware.config import (
    BaseConfig,
    AutostartConfig,
    MenuConfig,
    MimeConfig,
    ApplicationsConfig,
    DBusConfig,
    MetaConfig,
    LoggerConfig,
    FormatConfig,
    ExecutorsConfig,
    ProcessConfig,
    CriticalProcessConfig,
)
from korbenware.dbus.transformers import Transformer
from korbenware.dbus.marshmallow.fields import Str


# TODO: Create a pytest fixture for this
config_loaded = BaseConfig(
    dbus=DBusConfig(namespace="org.jfhbrook.korbenware"),
    autostart=AutostartConfig(
        directories=["/home/josh/.config/autostart", "/etc/xdg/autostart"],
        environment_name="korbenware",
        skip_unparsed=False,
        skip_invalid=False,
    ),
    meta=MetaConfig(config_filename="/home/josh/.config/korbenware/korbenware.toml"),
    menu=MenuConfig(filename="/etc/xdg/menus/arch-applications.menu"),
    mime=MimeConfig(
        cache="/usr/share/applications/mimeinfo.cache", environment="korbenware"
    ),
    applications=ApplicationsConfig(
        directories=["/usr/share/applications"], skip_unparsed=False, skip_invalid=False
    ),
    logger=LoggerConfig(level="debug"),
    format=FormatConfig(pygments_formatter="trac"),
    urls={"https": "firefox.desktop"},
    executors=ExecutorsConfig(
        primary={
            "foo": ProcessConfig(
                exec=["foo", "bar"], monitor=True, restart=False, cleanup=False
            )
        },
        critical={
            "bar": CriticalProcessConfig(
                exec=["baz", "quux"], monitor=True, restart=True, cleanup=False
            )
        },
    ),
)

config_dumped = [
    [
        ["/home/josh/.config/autostart", "/etc/xdg/autostart"],
        "korbenware",
        False,
        False,
    ],
    ["/etc/xdg/menus/arch-applications.menu"],
    ["/usr/share/applications/mimeinfo.cache", "korbenware"],
    [["/usr/share/applications"], False, False],
    {"https": "firefox.desktop"},
]

config_signature = "((asvvv)(v)(vv)(asvv)a{ss})"


@pytest.mark.parametrize(
    "type_,dumped,loaded,sig",
    [
        (Str(), "hello", "hello", "s"),
        (BaseConfig, config_dumped, config_loaded, config_signature),
    ],
)
def test_transformer(type_, dumped, loaded, sig):
    xform = Transformer(type_)
    assert xform.signature() == sig
    assert xform.dump(loaded) == dumped
    assert xform.load(dumped) == loaded
