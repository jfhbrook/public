from txdbus.interface import DBusInterface, Method, Property, Signal

from korbenware.dbus.client import Client
from korbenware.dbus.server import Server
from korbenware.dbus.path import basename, split
from korbenware.dbus.transformers import MultiTransformer, Transformer
from korbenware.dbus.tree import Node

property_ = property


class Object(Node):
    def __init__(self, service, obj_path, iface_name=None):
        super().__init__()
        if not iface_name:
            iface_name = f"{basename(obj_path)}Iface"
        self.service = service
        self.obj_path = obj_path
        self.iface_name = iface_name
        self.methods = dict()
        self.properties = dict()
        self.signals = dict()

    def method(self, arguments, returns, method=None, name=None):
        def register_method(fn):
            args_xform = MultiTransformer(arguments)
            returns_xform = Transformer(returns)
            method_name = name or fn.__name__

            self.methods[method_name] = (args_xform, returns_xform, fn)
            return fn

        if method:
            return register_method(method)

        return register_method

    def signal(self, name, type_):
        xform = Transformer(type_)
        self.signals[name] = xform

    def property(self, name, type_, default, **kwargs):
        self.properties[name] = (Transformer(type_), default, kwargs)

    @property_
    def iface(self):
        if hasattr(self, "_iface"):
            iface = self._iface
        else:
            iface_methods = []
            for method_name, (args_xform, returns_xform, fn) in self.methods.items():
                iface_methods.append(
                    Method(
                        method_name,
                        arguments=args_xform.signature(),
                        returns=returns_xform.signature(),
                    )
                )

            iface_properties = []
            for prop_name, (xform, default, kwargs) in self.properties.items():
                iface_properties.append(
                    Property(prop_name, xform.signature(), **kwargs)
                )

            iface_signals = []
            for signal_name, xform in self.signals.items():
                iface_signals.append(Signal(signal_name, xform.signature()))

            iface = DBusInterface(
                f"{self.service.namespace}.{self.iface_name}",
                *(iface_methods + iface_properties + iface_signals),
            )
            self._iface = iface
        return iface


class Service(Node):
    @classmethod
    def from_config(cls, config):
        return cls(config.dbus.namespace)

    def __init__(self, namespace):
        super().__init__()
        self.namespace = namespace

    def object(self, obj_path, iface_name=None):
        obj = Object(self, obj_path, iface_name)

        self.set(obj_path, obj)

        return obj

    def items(self):
        for k, v in super().items():
            if isinstance(v, Object):
                yield k, v

    def keys(self):
        for k, v in self.items():
            yield k

    def values(self):
        for v in super().values():
            if isinstance(v, Object):
                yield v

    async def server(self, connection):
        return await Server.create(connection, self)

    async def client(self, connection):
        return await Client.create(connection, self)
