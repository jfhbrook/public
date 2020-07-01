import pytest

import attr

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
from korbenware.dbus import dbus_attr
from korbenware.dbus.transformers import Transformer
from korbenware.dbus.marshmallow.fields import Int32, Str, List


@attr.s
class TestContainerType:
    some_str = dbus_attr(Str())
    some_int32 = dbus_attr(Int32())
    some_list = dbus_attr(List(Str()))


test_container_loaded = TestContainerType(
    some_str="hello", some_int32=42, some_list=["hello"]
)

test_container_dumped = ["hello", 42, ["hello"]]


# TODO: Create a pytest fixture for this
config_loaded = BaseConfig(
    applications=ApplicationsConfig(
        directories=["/usr/share/applications"], skip_unparsed=False, skip_invalid=False
    ),
    autostart=AutostartConfig(
        directories=["/home/josh/.config/autostart", "/etc/xdg/autostart"],
        environment_name="korbenware",
        skip_unparsed=False,
        skip_invalid=False,
    ),
    dbus=DBusConfig(namespace="org.jfhbrook.korbenware"),
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
    format=FormatConfig(pygments_formatter="trac"),
    logger=LoggerConfig(level="debug"),
    meta=MetaConfig(config_filename="/home/josh/.config/korbenware/korbenware.toml"),
    menu=MenuConfig(filename="/etc/xdg/menus/arch-applications.menu"),
    mime=MimeConfig(
        cache="/usr/share/applications/mimeinfo.cache", environment="korbenware"
    ),
    urls={"https": "firefox.desktop"},
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

config_signature = "((asvv)(asvvv)(v)({s(asvvv)})({s(asvvv)})(v)(v)(v)(v)(vv)a{ss})"


@pytest.mark.parametrize(
    "type_,dumped,loaded,sig",
    [
        (Str(), "hello", "hello", "s"),
        (List(Str()), ["hello"], ["hello"], "as"),
        (TestContainerType, test_container_dumped, test_container_loaded, "(sias)"),
        (BaseConfig, config_dumped, config_loaded, config_signature),
    ],
)
def test_transformer(type_, dumped, loaded, sig):
    xform = Transformer(type_)
    assert xform.signature() == sig
    assert xform.dump(loaded) == dumped
    assert xform.load(dumped) == loaded
