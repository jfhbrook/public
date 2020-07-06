import pytest

import attr

from korbenware.dbus import Bool, dbus_attr, Str
from korbenware.dbus.service import Object, Service


@attr.s
class Thing:
    string = dbus_attr(Str())


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
    a.property("property_v", Bool(), True)

    b = srv.get("/thing/B")

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

    b.property("property_w", Thing, Thing(string="#content"))

    assert srv.namespace == "some.namespace"

    assert len(list(srv.keys())) == 2

    assert srv.has("/thing/A")
    assert srv.has("/thing/B")

    assert repr(srv.thing) == "pony"
    assert srv.thing.A is srv.get("/thing/A")
    assert srv.thing.B is srv.get("/thing/B")
