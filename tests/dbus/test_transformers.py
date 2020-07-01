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
from korbenware.dbus.marshmallow.fields import Dict, Int32, List, Str


@attr.s
class SimpleContainer:
    some_str = dbus_attr(Str())
    some_int32 = dbus_attr(Int32())
    some_list = dbus_attr(List(Str()))
    some_dict = dbus_attr(Dict(Str(), Int32()))


simple_container_loaded = SimpleContainer(
    some_str="hello", some_int32=42, some_list=["hello"], some_dict=dict(hello=12)
)

simple_container_dumped = ["hello", 42, ["hello"], dict(hello=12)]


@attr.s
class NestedContainer:
    list_of = dbus_attr(List(SimpleContainer))
    dict_of = dbus_attr(Dict(Str(), SimpleContainer))


nested_container_loaded = NestedContainer(
    list_of=[SimpleContainer("hello", 42, ["hello"], dict(hello=12))],
    dict_of={"key": SimpleContainer("hello", 42, ["hello"], dict(hello=12))},
)

nested_container_dumped = [
    [["hello", 42, ["hello"], dict(hello=12)]],
    dict(key=["hello", 42, ["hello"], dict(hello=12)]),
]

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
    menu=MenuConfig(filename="/etc/xdg/menus/arch-applications.menu"),
    meta=MetaConfig(config_filename="/home/josh/.config/korbenware/korbenware.toml"),
    mime=MimeConfig(
        cache="/usr/share/applications/mimeinfo.cache", environment="korbenware"
    ),
    urls={"https": "firefox.desktop"},
)

config_dumped = [
    [["/usr/share/applications"], False, False],
    [
        ["/home/josh/.config/autostart", "/etc/xdg/autostart"],
        "korbenware",
        False,
        False,
    ],
    ["org.jfhbrook.korbenware"],
    [
        dict(foo=[["foo", "bar"], True, False, False]),
        dict(bar=[["baz", "quux"], True, True, False]),
    ],
    ["trac"],
    ["debug"],
    ["/etc/xdg/menus/arch-applications.menu"],
    ["/home/josh/.config/korbenware/korbenware.toml"],
    ["/usr/share/applications/mimeinfo.cache", "korbenware"],
    dict(https="firefox.desktop"),
]

config_signature = "((asbb)(assbb)(s)(a{s(asbbb)}a{s(asbbb)})(s)(s)(s)(s)(ss)a{ss})"


@pytest.mark.parametrize(
    "type_,dumped,loaded,sig",
    [
        (Str(), "hello", "hello", "s"),
        (List(Str()), ["hello"], ["hello"], "as"),
        (Dict(Str(), Int32()), dict(foo=1, bar=2), dict(foo=1, bar=2), "a{si}"),
        (
            SimpleContainer,
            simple_container_dumped,
            simple_container_loaded,
            "(siasa{si})",
        ),
        (
            NestedContainer,
            nested_container_dumped,
            nested_container_loaded,
            "(a(siasa{si})a{s(siasa{si})})",
        ),
        (BaseConfig, config_dumped, config_loaded, config_signature),
    ],
)
def test_transformer(type_, dumped, loaded, sig):
    xform = Transformer(type_)
    assert xform.signature() == sig
    assert xform.dump(loaded) == dumped
    assert xform.load(dumped) == loaded
