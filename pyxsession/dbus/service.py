from asyncio import iscoroutine
import functools

from twisted.internet.defer import Deferred
from txdbus.objects import DBusObject
from txdbus.interface import DBusInterface, Method, Property, Signal

from pyxsession.dbus.client import Client
from pyxsession.dbus.transformers import MultiTransformer, Transformer
from pyxsession.twisted.util import returns_deferred


class Service:
    def __init__(self, name, namespace, interface_name):
        self.name = name
        self.namespace = namespace
        self.interface_name = interface_name
        self.object_path = f'/{self.name}'
        self.methods = dict()
        
    def method(self, arguments, returns):
        def register_method(fn):
            args_xform = MultiTransformer(arguments)
            returns_xform = Transformer(returns)
            
            self.methods[fn.__name__] = (
                args_xform,
                returns_xform,
                fn 
            )
            return fn

        return register_method  
      
    @property
    def iface(self):
        if hasattr(self, '_iface'):
            iface = self._iface
        else:
            iface_methods = dict()
            for method_name, (
                args_xform, returns_xform, fn
            ) in self.methods.items():
                iface_methods[method_name] = Method(
                    method_name,
                    arguments=args_xform.signature(),
                    returns=returns_xform.signature()
                )

            iface = DBusInterface(
                f'{self.namespace}.{self.interface_name}',
                *iface_methods.values()
            )
            self._iface = iface
        return iface
      
    async def server(self, connection):
        methods = {
            method_name: fn
            for method_name, (args_xform, returns_xform, fn)
            in self.methods.items()
        }
        
        attrs = dict(
            iface=self.iface,
            dbusInterfaces=[self.iface]
        )

       
        for name, (args_xform, returns_xform, fn) in self.methods.items():
            @returns_deferred
            async def proxy_fn(remote_object, *args):
                xformed_args = args_xform.load(args)
                maybe_coro = fn(*xformed_args)

                if iscoroutine(maybe_coro) or isinstance(maybe_coro, Deferred):
                    ret = await maybe_coro
                else:
                    ret = maybe_coro
                raw_ret = returns_xform.dump(ret)
                return raw_ret
                return returns_xform.dump(await fn(*args_xform.load(args)))

            attrs[f'dbus_{name}'] = proxy_fn
            proxy_fn.__name__ = f'dbus_{name}'
      
        cls = type(self.name, (DBusObject,), attrs)

        connection.exportObject(cls(self.object_path))
        
        return await connection.requestBusName(self.namespace)
      
    async def client(self, connection):
        remote_obj = await connection.getRemoteObject(
            self.namespace, self.object_path, self.iface
        )
        return Client(self, remote_obj)
