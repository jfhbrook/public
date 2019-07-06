from asyncio import iscoroutine
import functools

from twisted.internet.defer import Deferred
from txdbus.objects import DBusObject
from txdbus.interface import DBusInterface, Method, Property, Signal

from pyxsession.dbus.client import Client
from pyxsession.dbus.server import Server
from pyxsession.dbus.transformers import MultiTransformer, Transformer
from pyxsession.dbus.path import basename
from pyxsession.twisted.util import returns_deferred


class Object:
    def __init__(self, service, obj_path, iface_name=None):
        if not iface_name:
            iface_name = f'{basename(obj_path)}Iface'
        self.service = service
        self.obj_path = obj_path
        self.iface_name = iface_name
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
                f'{self.service.namespace}.{self.iface_name}',
                *iface_methods.values()
            )
            self._iface = iface
        return iface
 

class Service:
    def __init__(self, namespace):
        self.namespace = namespace
        self.objects = dict()

    def obj(self, obj_path, iface_name=None):
        obj = Object(self, obj_path, iface_name)
        self.objects[obj_path] = obj
        return obj
     
    async def server(self, connection):
        return await Server.create(connection, self)
      
    async def client(self, connection):
        return await Client.create(connection, self)
