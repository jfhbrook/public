from asyncio import iscoroutine
import functools

import attr
from twisted.internet.defer import Deferred
from txdbus.objects import DBusObject, dbusMethod
from txdbus.interface import DBusInterface, Method, Property, Signal

from pyxsession.dbus.client import Client
import pyxsession.dbus.path as path
import pyxsession.dbus.namespace as namespace
from pyxsession.dbus.transformers import MultiTransformer, Transformer
from pyxsession.twisted.util import returns_deferred


class Node:
    pass


class Object:
    pass


@attr.s
class Server:
    connection = attr.ib()
    service = attr.ib()
    bus_name = attr.ib()
    dbus_obj_cls = attr.ib()
    dbus_obj = attr.ib()

    @classmethod
    async def create(server_cls, connection, service):
        attrs = dict()

        dbus_objs = dict()
        objects = dict()
        bus_names = []

        for obj_path, service_obj in service.objects.items():
            path_parts = path.split(obj_path)
            first_part = path_parts.pop(0)
            try:
                last_part = path_parts.pop()
            except IndexError:
                last_part = None

            obj = Object()

            # Attach our object ot the server cls
            if last_part:
                this_node = Node()
                objects[first_part] = this_node
                for path_part in path_parts:
                    setattr(this_node, path_part, Node())
                    this_node = getattr(this_node, path_part)
                setattr(this_node, last_part, obj)
            else:
                objects[first_part] = obj

            # Generate and add the interface
            iface = service_obj.iface
            attrs['iface'] = iface
            attrs['dbusInterfaces'] = [iface]

            # Add the dbus method callbacks
            for (
                method_name,
                (args_xform, returns_xform, fn)
            ) in service_obj.methods.items():
                @returns_deferred
                async def proxy_fn(remote_object, *args):
                    xformed_args = args_xform.load(args)
                    maybe_coro = fn(*xformed_args)

                    if iscoroutine(maybe_coro) or isinstance(maybe_coro, Deferred):
                        ret = await maybe_coro
                    else:
                        ret = maybe_coro
                    return returns_xform.dump(ret)

                key = f'dbus_{method_name}'

                attrs[key] = proxy_fn
                proxy_fn.__name__ = key

            dbus_obj_cls = type(path.basename(obj_path), (DBusObject,), attrs)
            dbus_obj = dbus_obj_cls(obj_path)
            dbus_objs[obj_path] = dbus_obj

            obj.dbus_obj = dbus_obj

            connection.exportObject(dbus_obj)
        
            bus_names.append(await connection.requestBusName(service.namespace))

        server = server_cls(
            connection,
            service,
            bus_names,
            dbus_obj_cls,
            dbus_obj
        )

        for attr, obj in objects.items():
            setattr(server, attr, obj)

        return server
