import pytest

import attr

from korbenware.dbus import Bool, dbus_attr, Str
from korbenware.dbus.service import Object, Service


@attr.s
class Thing:
    string = dbus_attr(Str())


def assert_method(obj, method, expected):
    (args_xform, return_xform, fn) = obj.methods[method]
    actual = (args_xform.signature(), return_xform.signature(), fn)

    assert actual == expected


def assert_signal(obj, signal, expected):
    assert obj.signals[signal].signature() == expected


def assert_property(obj, property, expected):
    (xform, default, kwargs) = obj.properties[property]

    assert (xform.signature(), default, kwargs) == expected


def test_properties():
    srv = Service("some.namespace")

    a = srv.object("/thing/A")

    @a.method([Str()], Bool())
    def method_one(s):
        assert type(s) == str
        return True

    @a.method([Thing], Thing)
    def method_two(thing):
        assert isinstance(thing, Thing)
        return False

    a.signal("signal_a", Str())
    a.signal("signal_b", Thing)

    a.property("property_u", Str(), "pony")
    a.property("property_v", Bool(), True, foo="bar")

    b = srv.object("/thing/B")

    @b.method([Thing], Str())
    def method_three(thing):
        assert isinstance(thing, Thing)
        return "that's right"

    @b.method([Bool()], Str())
    def method_four(b):
        assert type(s) == bool
        return "that's not it chief"

    b.signal("signal_c", Bool())
    b.signal("signal_d", Thing)

    hashtag_content = Thing(string="#content")

    b.property("property_w", Thing, hashtag_content)

    assert srv.namespace == "some.namespace"

    assert srv.has("/thing/A")
    assert srv.has("/thing/B")

    assert srv.thing.A is a
    assert srv.get("/thing/A") is a
    assert_method(a, "method_one", ("s", "b", method_one))
    assert_method(a, "method_two", ("(s)", "(s)", method_two))
    assert_signal(a, "signal_a", "s")
    assert_signal(a, "signal_b", "(s)")
    assert_property(a, "property_u", ("s", "pony", dict()))
    assert_property(a, "property_v", ("b", True, dict(foo="bar")))

    assert srv.thing.B is b
    assert srv.get("/thing/B") is b
    assert_method(b, "method_three", ("(s)", "s", method_three))
    assert_method(b, "method_four", ("b", "s", method_four))
    assert_signal(b, "signal_c", "b")
    assert_signal(b, "signal_d", "(s)")
    assert_property(b, "property_w", ("(s)", hashtag_content, dict()))
