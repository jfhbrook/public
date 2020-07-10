import pytest
import pytest_twisted

from unittest.mock import call, Mock

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
def mock_dbus_property_inst():
    return Mock()


@pytest.fixture
def mock_dbus_property_cls(mock_dbus_property_inst, monkeypatch):
    mock = Mock(return_value=mock_dbus_property_inst)

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
    svc = Service("some.namespace")

    a = svc.object("/thing/A")

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

    b = svc.object("/thing/B")

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
        svc=svc,
        a=a,
        b=b,
        method_one=method_one,
        method_two=method_two,
        method_three=method_three,
        method_four=method_four,
    )


@pytest.fixture
def mock_dbus_obj(monkeypatch):
    mock = Mock()

    return mock


@pytest.fixture
def mock_dbus_obj_factory(mock_dbus_obj, monkeypatch):
    mock = Mock(return_value=mock_dbus_obj)

    monkeypatch.setattr("korbenware.dbus.server.dbus_obj_factory", mock)

    return mock


@pytest.fixture
def mock_dbus_method():
    mock = Mock()

    return mock


@pytest.fixture
def mock_dbus_method_factory(mock_dbus_method, monkeypatch):
    mock = Mock(return_value=mock_dbus_method)

    monkeypatch.setattr("korbenware.dbus.server.dbus_method_factory", mock)

    return mock


def dbus_method_factory_call(service_obj, method_name):
    (args_xform, returns_xform, fn) = service_obj.methods[method_name]

    attr_name = f"dbus_{method_name}"
    return call(attr_name, args_xform, returns_xform, fn)


def test_service(dbus_service, hashtag_content, assert_iface):
    svc = dbus_service["svc"]
    a = dbus_service["a"]
    b = dbus_service["b"]
    method_one = dbus_service["method_one"]
    method_two = dbus_service["method_two"]
    method_three = dbus_service["method_three"]
    method_four = dbus_service["method_four"]

    assert svc.namespace == "some.namespace"

    assert svc.has("/thing/A")
    assert svc.has("/thing/B")

    assert svc.thing.A is a
    assert svc.get("/thing/A") is a

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

    assert svc.thing.B is b
    assert svc.get("/thing/B") is b
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
    hashtag_content,
    dbus_service,
    mock_dbus_iface_cls,
    mock_dbus_property_inst,
    mock_dbus_property_cls,
    mock_dbus_object_cls,
    mock_kb_method_cls,
    mock_kb_property_cls,
    mock_kb_signal_cls,
    mock_dbus_obj,
    mock_dbus_obj_factory,
    mock_dbus_method,
    mock_dbus_method_factory,
):
    svc = dbus_service["svc"]
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

    server = await svc.server(mock_connection)

    assert server.connection is mock_connection
    assert server.service is svc

    assert server.has("/thing/A")
    assert server.thing.A is server.get("/thing/A")

    server_a = server.thing.A

    mock_dbus_method_factory.assert_has_calls(
        [
            dbus_method_factory_call(a, "method_one"),
            dbus_method_factory_call(a, "method_two"),
        ]
    )

    assert server_a.service_obj is svc.get("/thing/A")
    assert server_a.iface is svc.get("/thing/A").iface
    assert server_a.dbus_obj is mock_dbus_obj

    mock_dbus_obj_factory.assert_any_call(
        "/thing/A",
        dict(
            iface=a.iface,
            dbusInterfaces=[a.iface],
            dbus_method_one=mock_dbus_method,
            dbus_method_two=mock_dbus_method,
            property_u=mock_dbus_property_inst,
            property_v=mock_dbus_property_inst,
        ),
    )

    assert server_a.dbus_obj.property_u == "pony"
    assert server_a.dbus_obj.property_v == True

    assert server.has("/thing/B")
    assert server.thing.B is server.get("/thing/B")

    server_b = server.thing.B

    assert server_b.service_obj is svc.get("/thing/B")
    assert server_b.iface is svc.get("/thing/B").iface
    assert server_b.dbus_obj is mock_dbus_obj

    mock_dbus_method_factory.assert_has_calls(
        [
            dbus_method_factory_call(b, "method_three"),
            dbus_method_factory_call(b, "method_four"),
        ]
    )

    mock_dbus_obj_factory.assert_any_call(
        "/thing/B",
        dict(
            iface=b.iface,
            dbusInterfaces=[b.iface],
            dbus_method_three=mock_dbus_method,
            dbus_method_four=mock_dbus_method,
            property_w=mock_dbus_property_inst,
        ),
    )

    assert server_b.dbus_obj.property_w is hashtag_content
