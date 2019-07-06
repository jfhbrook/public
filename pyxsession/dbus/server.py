from asyncio import iscoroutine
import functools

import attr
from twisted.internet.defer import Deferred
from txdbus.objects import DBusObject
from txdbus.interface import DBusInterface, Method, Property, Signal

from pyxsession.dbus.client import Client
from pyxsession.dbus.transformers import MultiTransformer, Transformer
from pyxsession.twisted.util import returns_deferred


@attr.s
class Server:
    connection = attr.ib()
    service = attr.ib()
    bus_name = attr.ib()
    obj_cls = attr.ib()
    obj = attr.ib()

    @classmethod
    async def create(server_cls, connection, service):
        methods = {
            method_name: fn
            for method_name, (args_xform, returns_xform, fn)
            in service.methods.items()
        }
        
        attrs = dict(
            iface=service.iface,
            dbusInterfaces=[service.iface]
        )
       
        for (
            name,
            (args_xform, returns_xform, fn)
        ) in service.methods.items():
            @returns_deferred
            async def proxy_fn(remote_object, *args):
                xformed_args = args_xform.load(args)
                maybe_coro = fn(*xformed_args)

                if iscoroutine(maybe_coro) or isinstance(maybe_coro, Deferred):
                    ret = await maybe_coro
                else:
                    ret = maybe_coro
                return returns_xform.dump(ret)

            attrs[f'dbus_{name}'] = proxy_fn
            proxy_fn.__name__ = f'dbus_{name}'
      
        obj_cls = type(service.name, (DBusObject,), attrs)
        obj = obj_cls(service.object_path)

        connection.exportObject(obj)
        
        bus_name = await connection.requestBusName(service.namespace)

        return server_cls(
            connection,
            service,
            bus_name,
            obj_cls,
            obj
        )
