import pytest

import datetime

import attr

from korbenware.config import (
    BaseConfig,
    ApplicationsConfig,
    AutostartConfig,
    CriticalProcessConfig,
    ExecutorsConfig,
    DBusConfig,
    FormatConfig,
    LoggerConfig,
    MenuConfig,
    MimeConfig,
    MetaConfig,
    ProcessConfig,
)
from korbenware.session import ProcessState, ExecutorState, SessionState
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
                argv=["foo", "bar"],
                monitor=True,
                restart=False,
                cleanup=False,
                env=dict(),
                cwd="",
            )
        },
        critical={
            "bar": CriticalProcessConfig(
                argv=["baz", "quux"],
                monitor=True,
                restart=True,
                cleanup=False,
                env=dict(),
                cwd="",
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
        dict(foo=[["foo", "bar"], True, False, False, {}, ""]),
        dict(bar=[["baz", "quux"], True, True, False, {}, ""]),
    ],
    ["trac"],
    ["debug"],
    ["/etc/xdg/menus/arch-applications.menu"],
    ["/home/josh/.config/korbenware/korbenware.toml"],
    ["/usr/share/applications/mimeinfo.cache", "korbenware"],
    dict(https="firefox.desktop"),
]

config_signature = (
    "((asbb)(assbb)(s)(a{s(asbbba{ss}s)}a{s(asbbba{ss}s)})(s)(s)(s)(s)(ss)a{ss})"
)

executor_empty_loaded = ExecutorState(running=-1, processes=[])

executor_empty_dumped = [-1, []]

executor_some_loaded = ExecutorState(
    running=1, processes=[ProcessState(name="xmonad", state="STOPPED", restart=True)]
)

executor_some_dumped = [1, [["xmonad", "STOPPED", True, -1, -1, -1, -1]]]

executor_signature = "(na(ssbxxxx))"

ages_ago_loaded = datetime.datetime.fromtimestamp(0)
ages_ago_dumped = 0

recently_loaded = datetime.datetime(month=6, day=23, year=2020)
recently_dumped = 1592884800000

session_loaded = SessionState(
    running=False,
    loaded_at=recently_loaded,
    started_at=ages_ago_loaded,
    stopped_at=ages_ago_loaded,
    config=config_loaded,
    critical_executor=executor_empty_loaded,
    primary_executor=executor_some_loaded,
)

session_dumped = [
    False,
    recently_dumped,
    ages_ago_dumped,
    ages_ago_dumped,
    config_dumped,
    executor_empty_dumped,
    executor_some_dumped,
]

session_signature = f"(bxxx{config_signature}{executor_signature}{executor_signature})"


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
        (
            ExecutorState,
            executor_empty_dumped,
            executor_empty_loaded,
            executor_signature,
        ),
        (ExecutorState, executor_some_dumped, executor_some_loaded, executor_signature),
        (SessionState, session_dumped, session_loaded, session_signature),
    ],
)
def test_transformer(type_, dumped, loaded, sig):
    xform = Transformer(type_)
    assert xform.signature() == sig
    assert xform.dump(loaded) == dumped
    assert xform.load(dumped) == loaded
