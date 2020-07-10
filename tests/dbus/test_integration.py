import pytest
import pytest_twisted

from twisted.internet import reactor
from txdbus import client


@pytest_twisted.ensureDeferred
async def test_integration(dbus_service):
    svc = dbus_service["svc"]

    conn = await client.connect(reactor)

    dbus_server = await svc.server(conn)

    dbus_client = await svc.client(conn)

    assert dbus_server

    assert dbus_client

    conn.disconnect()
