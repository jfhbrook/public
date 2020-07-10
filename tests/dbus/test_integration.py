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
    rcv_a = Deferred()
    rcv_b = Deferred()
    rcv_c = Deferred()
    rcv_d = Deferred()

    rcv_all = DeferredList([rcv_a, rcv_b, rcv_c, rcv_d])

    @dbus_client.thing.A.on("signal_a")
    def on_signal_a(yes):
        assert yes == "yes"
        rcv_a.callback(None)

    @dbus_client.thing.A.on("signal_b")
    def on_signal_b(thing):
        assert thing == ping
        rcv_b.callback(None)

    @dbus_client.thing.B.on("signal_c")
    def on_signal_c(b):
        assert not b
        rcv_c.callback(None)

    @dbus_client.thing.B.on("signal_d")
    def on_signal_d(thing):
        assert thing == pong
        rcv_d.callback(None)

    dbus_server.thing.A.emit("signal_a", "yes")
    dbus_server.thing.A.emit("signal_b", ping)
    dbus_server.thing.B.emit("signal_c", False)
    dbus_server.thing.B.emit("signal_d", pong)

    await rcv_all.addTimeout(0.1, reactor)

    conn.disconnect()
