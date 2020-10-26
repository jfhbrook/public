import attr


@attr.s
class Notifier:
    connection = attr.ib()
    remote_obj = attr.ib()

    async def create(connection):
        remote_obj = await connection.getRemoteObject(
            "org.freedesktop.Notifications", "/org/freedesktop/Notifications"
        )

        return Notifier(connection, remote_obj)

    async def notify(
        self,
        appname="",
        replaces=0,
        icon="",
        summary="",
        message="",
        actions=None,
        hints=None,
        timeout=1000,
    ):
        actions = actions or []
        hints = hints or dict()

        return await self.remote_obj.callRemote(
            "Notify", appname, replaces, icon, summary, message, actions, hints, timeout
        )
