import pytest
import pytest_twisted

from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredList
from txdbus import client
from txdbus.error import RemoteError


@pytest_twisted.ensureDeferred
async def test_integration(dbus_service, thing_cls):
    svc = dbus_service["svc"]

    conn = await client.connect(reactor)

    dbus_server = await svc.server(conn)
    assert dbus_server

    dbus_client = await svc.client(conn)
    assert dbus_client

    ping = thing_cls("ping")
    pong = thing_cls("pong")

    # Method calls
    assert await dbus_client.thing.A.method_one("numberwang")
    assert not (await dbus_client.thing.A.method_one("not numberwang"))
    assert (await dbus_client.thing.A.method_two(ping)) == pong

    assert (await dbus_client.thing.B.method_three(ping)) == "that's right"
    assert (await dbus_client.thing.B.method_four(False)) == "that's not it chief"

    # Properties
    s_emit_u = Deferred()
    rcv_u = Deferred()

    @dbus_server.thing.A.on("PropertiesChanged")
    def on_server_property_changed(iface, changed_values, changed_keys):
        assert iface == "some.namespace.AIface"
        assert changed_values["property_u"] == "not pony"
        s_emit_u.callback(None)

    @dbus_client.thing.A.on("PropertiesChanged")
    def on_client_property_changed(iface, changed_values, changed_keys):
        assert iface == "some.namespace.AIface"
        assert changed_values["property_u"] == "not pony"
        rcv_u.callback(None)

    assert (await dbus_client.thing.A.get_property("property_u")) == "pony"
    await dbus_client.thing.A.set_property("property_u", "not pony")
    assert (await dbus_client.thing.A.get_property("property_u")) == "not pony"

    assert (await dbus_client.thing.A.get_property("property_v")) == True
    with pytest.raises(RemoteError):
        await dbus_client.thing.A.set_property("property_v", False)

    assert (await dbus_client.thing.B.get_property("property_w")) == 12
    with pytest.raises(RemoteError):
        await dbus_client.thing.B.set_property("property_w", 22)

    # Signals
    s_emit_a = Deferred()
    rcv_a = Deferred()

    s_emit_b = Deferred()
    rcv_b = Deferred()

    s_emit_c = Deferred()
    rcv_c = Deferred()

    s_emit_d = Deferred()
    rcv_d = Deferred()

    @dbus_server.thing.A.on("signal_a")
    def on_srv_signal_a(yes):
        assert yes == "yes"
        s_emit_a.callback(None)

    @dbus_client.thing.A.on("signal_a")
    def on_signal_a(yes):
        assert yes == "yes"
        rcv_a.callback(None)

    @dbus_server.thing.A.on("signal_b")
    def on_srv_signal_b(thing):
        assert thing == ping
        s_emit_b.callback(None)

    @dbus_client.thing.A.on("signal_b")
    def on_signal_b(thing):
        assert thing == ping
        rcv_b.callback(None)

    @dbus_server.thing.B.on("signal_c")
    def on_srv_signal_c(b):
        assert not b
        s_emit_c.callback(None)

    @dbus_client.thing.B.on("signal_c")
    def on_signal_c(b):
        assert not b
        rcv_c.callback(None)

    @dbus_server.thing.B.on("signal_d")
    def on_srv_signal_d(thing):
        assert thing == pong
        s_emit_d.callback(None)

    @dbus_client.thing.B.on("signal_d")
    def on_signal_d(thing):
        assert thing == pong
        rcv_d.callback(None)

    dbus_server.thing.A.emit("signal_a", "yes")
    dbus_server.thing.A.emit("signal_b", ping)
    dbus_server.thing.B.emit("signal_c", False)
    dbus_server.thing.B.emit("signal_d", pong)

    await s_emit_u.addTimeout(0.1, clock=reactor)
    await rcv_u.addTimeout(0.1, clock=reactor)
    await s_emit_a.addTimeout(0.1, clock=reactor)
    await rcv_a.addTimeout(0.1, clock=reactor)
    await s_emit_b.addTimeout(0.1, clock=reactor)
    await rcv_b.addTimeout(0.1, clock=reactor)
    await s_emit_c.addTimeout(0.1, clock=reactor)
    await rcv_c.addTimeout(0.1, clock=reactor)
    await s_emit_d.addTimeout(0.1, clock=reactor)
    await rcv_d.addTimeout(0.1, clock=reactor)

    conn.disconnect()
