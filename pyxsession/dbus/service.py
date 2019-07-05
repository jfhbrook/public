import functools

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
            
            @functools.wraps(fn)
            def method_proxy(*raw_args):
                return returns_xform.load(fn(*argx_xform.dump(raw_args)))
          
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
            for method_name, (args_sig, returns_sig, fn)
            in self.methods.items()
        }
        
        attrs = dict(
            iface=self.iface,
            dbusInterfaces=[self.iface]
        )
        
        for name, fn in methods.items():
            attrs[f'dbus_{name}'] = returns_deferred(fn)
      
        cls = type(self.name, (DBusObject,), attrs)
        
        connection.exportObject(cls(self.object_path))
        
        return await connection.requestBusName(self.namespace)
      
    async def client(self, connection):
        remote_obj = await connection.getRemoteObject(
            self.namespace, self.object_path, self.iface
        )
        return Client(self, remote_obj)
