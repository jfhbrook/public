# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import attr
from pyee import TwistedEventEmitter as EventEmitter
from korbenware.dbus.tree import Node
from korbenware.dbus.path import split


class Object(EventEmitter):
    def __init__(self, remote_obj, service_obj):
        super().__init__()
        self._emit = self.emit
        self.remote_obj = remote_obj
        self.service_obj = service_obj

    async def call(self, method_name, *args):
        args_xform, returns_xform, _ = self.service_obj.methods[method_name]
        xformed_args = args_xform.dump(args)

        rv = await self.remote_obj.callRemote(method_name, *xformed_args)

        # TODO: Why is this necessary???
        if not returns_xform.is_field:
            rv = rv[0]
        return returns_xform.load(rv)

    async def get_property(self, prop_name):
        xform, _, _ = self.service_obj.properties[prop_name]

        rv = await self.remote_obj.callRemote("Get", "", prop_name)

        return xform.load(rv)

    async def set_property(self, prop_name, value):
        xform, _, _ = self.service_obj.properties[prop_name]

        await self.remote_obj.callRemote("Set", "", prop_name, xform.dump(value))


def client_method_factory(obj, method_name):
    async def method(*args):
        return await obj.call(method_name, *args)

    method.__name__ = method_name

    return method


def client_emitter_factory(obj, event_name, xform):
    def callback(data):
        obj.emit(event_name, xform.load(data))

    return callback


def changed_properties_emitter_factory(obj):
    def callback(iface, changed_values, changed_keys):
        obj.emit("PropertiesChanged", iface, changed_values, changed_keys)

    return callback


@attr.s
class Client(Node):
    service = attr.ib()
    remote_objs = attr.ib()

    @classmethod
    async def create(cls, connection, service):
        remote_objs = Node()
        client_objs = dict()

        for obj_path, service_obj in service.items():
            # Collect the remote object
            remote_obj = await connection.getRemoteObject(service.namespace, obj_path)

            remote_objs.set(obj_path, remote_obj)

            # Generate and attach the client object
            obj = Object(remote_obj, service_obj)

            client_objs[obj_path] = obj

            def bind(obj):
                async def proxy_fn(*args):
                    return await obj.call(method_name, *args)

                return proxy_fn

            # Add the shim functions for each method
            for method_name in service_obj.methods.keys():
                client_method = client_method_factory(obj, method_name)
                setattr(obj, method_name, client_method)

            # Signals
            for event_name, xform in service_obj.signals.items():
                remote_obj.notifyOnSignal(
                    event_name, client_emitter_factory(obj, event_name, xform)
                )

            remote_obj.notifyOnSignal(
                "PropertiesChanged", changed_properties_emitter_factory(obj)
            )

        client = Client(service, remote_objs)

        for path, obj in client_objs.items():
            client.set(path, obj)

        return client
