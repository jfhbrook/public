import attr

from pyxsession.dbus import Service
from pyxsession.dbus import (Str, Int32, UInt32, List, DBusField)

service = Service('org.freedesktop.Notifications')

Notifications = service.obj('/org/freedesktop/Notifications')

@Notifications.method([
    Str(),
    UInt32(),
    Str(),
    Str(),
    Str(),
    List(Str()),
    DBusField('a{sv}'),
    Int32()
], UInt32())
def Notify(
    appname,
    replaces,
    icon,
    summary,
    message,
    actions,
    hints,
    timeout
):
    raise NotImplementedError('Use this for a client, silly!')


@attr.s
class Notifier:
    client = attr.ib()

    async def create(connection):
        client = await service.client(connection)

        return Notifier(client)

    async def notify(
        self,
        appname='',
        replaces=0,
        icon='',
        message='',
        summary='',
        actions=None,
        hints=None,
        timeout=1000
    ):
        actions = actions or []
        hints = hints or dict()

        return await self.client.org.freedesktop.Notifications.Notify(
            appname,
            replaces,
            icon,
            summary,
            message,
            actions,
            hints,
            timeout
        )
