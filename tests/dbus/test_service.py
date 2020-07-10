import pytest
import pytest_twisted

from unittest.mock import Mock

import attr
from twisted.internet.defer import Deferred
from txdbus.interface import Method, Property, Signal

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


@pytest.fixture
def hashtag_content():
    return Thing(string="#content")


@pytest.fixture
def mock_kb_method_inst(monkeypatch):
    mock = Mock()

    return mock


@pytest.fixture
def mock_kb_method_cls(mock_kb_method_inst, monkeypatch):
    mock_method_cls = Mock(return_value=mock_kb_method_inst)

    monkeypatch.setattr("korbenware.dbus.service.Method", mock_method_cls)

    return mock_method_cls


@pytest.fixture
def mock_kb_property_inst(monkeypatch):
    mock = Mock()

    return mock


@pytest.fixture
def mock_kb_property_cls(mock_kb_property_inst, monkeypatch):
    mock_property_cls = Mock(return_value=mock_kb_property_inst)

    monkeypatch.setattr("korbenware.dbus.service.Property", mock_property_cls)

    return mock_property_cls


@pytest.fixture
def mock_kb_signal_inst(monkeypatch):
    mock = Mock()

    return mock


@pytest.fixture
def mock_kb_signal_cls(mock_kb_signal_inst, monkeypatch):
    mock_signal_cls = Mock(return_value=mock_kb_signal_inst)

    monkeypatch.setattr("korbenware.dbus.service.Signal", mock_signal_cls)

    return mock_signal_cls


@pytest.fixture
def mock_dbus_iface_inst(
    mock_kb_method_inst, mock_kb_property_inst, mock_kb_signal_inst
):
    mock = Mock()

    def side_effect(t):
        def iter():
            for arg in mock.call_args.args:
                if arg == t:
                    yield arg

        return iter

    mock.methods.return_value.__iter__ = Mock(
        side_effect=side_effect(mock_kb_method_inst)
    )

    mock.properties.return_value.__iter__ = Mock(
        side_effect=side_effect(mock_kb_property_inst)
    )

    mock.signals.return_value.__iter__ = Mock(
        side_effect=side_effect(mock_kb_signal_inst)
    )

    return mock


@pytest.fixture
def mock_dbus_iface_cls(mock_dbus_iface_inst, monkeypatch):
    mock_iface_cls = Mock(return_value=mock_dbus_iface_inst)

    monkeypatch.setattr("korbenware.dbus.service.DBusInterface", mock_iface_cls)

    return mock_iface_cls


@pytest.fixture
def mock_dbus_property_cls(monkeypatch):
    mock = Mock()

    monkeypatch.setattr("korbenware.dbus.server.DBusProperty", mock)

    return mock


@pytest.fixture
def mock_dbus_object_cls(monkeypatch):
    mock = Mock()

    monkeypatch.setattr("korbenware.dbus.server.DBusObject", mock)

    return mock


@pytest.fixture
def assert_iface(
    mock_kb_method_inst,
    mock_kb_method_cls,
    mock_kb_property_inst,
    mock_kb_property_cls,
    mock_kb_signal_inst,
    mock_kb_signal_cls,
    mock_dbus_iface_cls,
):
    def asserts(obj, namespace, expected):
        mock_dbus_iface_cls.reset_mock()
        _ = obj.iface

        iface_args = []

        instances = {
            "method": mock_kb_method_inst,
            "property": mock_kb_property_inst,
            "signal": mock_kb_signal_inst,
        }

        classes = {
            "method": mock_kb_method_cls,
            "property": mock_kb_property_cls,
            "signal": mock_kb_signal_cls,
        }

        for type_, args, kwargs in expected:
            classes[type_].assert_any_call(*args, **kwargs)
            iface_args.append(instances[type_])

        mock_dbus_iface_cls.assert_called_once()
        mock_dbus_iface_cls.assert_called_with(namespace, *iface_args)

    return asserts


@pytest.fixture
def dbus_service(hashtag_content):
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

    b.property("property_w", Thing, hashtag_content)

    return dict(
        srv=srv,
        a=a,
        b=b,
        method_one=method_one,
        method_two=method_two,
        method_three=method_three,
        method_four=method_four,
    )


@pytest.fixture
def mock_create_dbus_obj_subcls(monkeypatch):
    mock = Mock()

    monkeypatch.setattr('korbenware.dbus.server.create_dbus_obj_subcls', mock)

    return mock


def test_service(dbus_service, hashtag_content, assert_iface):
    srv = dbus_service["srv"]
    a = dbus_service["a"]
    b = dbus_service["b"]
    method_one = dbus_service["method_one"]
    method_two = dbus_service["method_two"]
    method_three = dbus_service["method_three"]
    method_four = dbus_service["method_four"]

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
    assert_iface(
        a,
        "some.namespace.AIface",
        [
            ("method", ["method_one"], dict(arguments="s", returns="b")),
            ("method", ["method_two"], dict(arguments="(s)", returns="(s)")),
            ("property", ["property_u", "s"], dict()),
            ("property", ["property_v", "b"], dict(foo="bar")),
            ("signal", ["signal_a", "s"], dict()),
            ("signal", ["signal_b", "(s)"], dict()),
        ],
    )

    assert srv.thing.B is b
    assert srv.get("/thing/B") is b
    assert_method(b, "method_three", ("(s)", "s", method_three))
    assert_method(b, "method_four", ("b", "s", method_four))
    assert_signal(b, "signal_c", "b")
    assert_signal(b, "signal_d", "(s)")
    assert_property(b, "property_w", ("(s)", hashtag_content, dict()))
    assert_iface(
        b,
        "some.namespace.BIface",
        [
            ("method", ["method_three"], dict(arguments="(s)", returns="s")),
            ("method", ["method_four"], dict(arguments="b", returns="s")),
            ("property", ["property_w", "(s)"], dict()),
            ("signal", ["signal_c", "b"], dict()),
            ("signal", ["signal_d", "(s)"], dict()),
        ],
    )


@pytest_twisted.ensureDeferred
async def test_server(
    dbus_service,
    mock_dbus_iface_cls,
    mock_dbus_property_cls,
    mock_dbus_object_cls,
    mock_kb_method_cls,
    mock_kb_property_cls,
    mock_kb_signal_cls,
    mock_create_dbus_obj_subcls
):
    srv = dbus_service["srv"]
    a = dbus_service["a"]
    b = dbus_service["b"]
    method_one = dbus_service["method_one"]
    method_two = dbus_service["method_two"]
    method_three = dbus_service["method_three"]
    method_four = dbus_service["method_four"]

    mock_connection = Mock()

    mock_bus = Mock()
    mock_connection.requestBusName.return_value = Deferred()
    mock_connection.requestBusName.return_value.callback(mock_bus)

    server = await srv.server(mock_connection)

    assert server.connection is mock_connection
    assert server.service is srv

    assert server.has("/thing/A")
    assert server.has("/thing/B")
