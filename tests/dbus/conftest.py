import pytest

import attr

from korbenware.dbus import Bool, dbus_attr, Int32, Str
from korbenware.dbus.service import Service


@pytest.fixture
def thing_cls():
    @attr.s
    class Thing:
        string = dbus_attr(Str())

    return Thing


@pytest.fixture
def dbus_service(thing_cls):
    svc = Service("some.namespace")

    a = svc.object("/thing/A")

    @a.method([Str()], Bool())
    def method_one(s):
        assert type(s) == str
        return True

    @a.method([thing_cls], thing_cls)
    def method_two(thing):
        assert isinstance(thing, thing_cls)
        return False

    a.signal("signal_a", Str())
    a.signal("signal_b", thing_cls)

    a.property("property_u", Str(), "pony")
    a.property("property_v", Bool(), True)

    b = svc.object("/thing/B")

    @b.method([thing_cls], Str())
    def method_three(thing):
        assert isinstance(thing, thing_cls)
        return "that's right"

    @b.method([Bool()], Str())
    def method_four(b):
        assert type(s) == bool
        return "that's not it chief"

    b.signal("signal_c", Bool())
    b.signal("signal_d", thing_cls)

    b.property("property_w", Int32(), 12)

    return dict(
        svc=svc,
        a=a,
        b=b,
        method_one=method_one,
        method_two=method_two,
        method_three=method_three,
        method_four=method_four,
    )
