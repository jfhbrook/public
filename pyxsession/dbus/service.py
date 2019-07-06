from asyncio import iscoroutine
import functools

from pyee import TwistedEventEmitter as EventEmitter
from twisted.internet.defer import Deferred
from txdbus.objects import DBusObject
from txdbus.interface import DBusInterface, Method, Property, Signal

from pyxsession.dbus.client import Client
from pyxsession.dbus.server import Server
from pyxsession.dbus.transformers import MultiTransformer, Transformer
from pyxsession.dbus.path import basename
from pyxsession.twisted.util import returns_deferred

property_ = property


class Object:
    def __init__(self, service, obj_path, iface_name=None):
        if not iface_name:
            iface_name = f'{basename(obj_path)}Iface'
        self.service = service
        self.obj_path = obj_path
        self.iface_name = iface_name
        self.methods = dict()
        self.properties = dict()
        self.signals = dict()

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

    def signal(self, name, type_):
        xform = Transformer(type_)
        self.signals[name] = xform

    def property(self, name, type_, default, **kwargs):
        self.properties[name] = (Transformer(type_), default, kwargs)

    @property_
    def iface(self):
        if hasattr(self, '_iface'):
            iface = self._iface
        else:
            iface_methods = []
            for method_name, (
                args_xform, returns_xform, fn
            ) in self.methods.items():
                iface_methods.append(Method(
                    method_name,
                    arguments=args_xform.signature(),
                    returns=returns_xform.signature()
                ))

            iface_properties = []
            for prop_name, (xform, default, kwargs) in self.properties.items():
                iface_properties.append(
                    Property(prop_name, xform.signature(), **kwargs)
                )

            iface_signals = []
            for signal_name, xform in self.signals.items():
                iface_signals.append(
                    Signal(signal_name, xform.signature())
                )

            iface = DBusInterface(
                f'{self.service.namespace}.{self.iface_name}',
                *(iface_methods + iface_properties + iface_signals)
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
