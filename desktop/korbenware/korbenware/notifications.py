# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
