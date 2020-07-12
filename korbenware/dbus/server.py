from asyncio import iscoroutine

import attr
from pyee import TwistedEventEmitter as EventEmitter
from twisted.internet.defer import Deferred, DeferredList
from txdbus.objects import DBusObject, DBusProperty

import korbenware.dbus.path as path
from korbenware.dbus.tree import Node
from korbenware.twisted.util import returns_deferred


class Object(Node, EventEmitter):
    def __init__(self, service_obj, dbus_obj):
        Node.__init__(self)
        EventEmitter.__init__(self)
        self.service_obj = service_obj
        self.iface = service_obj.iface
        self.dbus_obj = dbus_obj

    def _truly_emit(self, name, *args, **kwargs):
        super().emit(name, *args, **kwargs)

    def emit(self, name, *args, **kwargs):
        if name in self.service_obj.signals:
            # Emits that have names shared with signals call emitSignal
            # (which is modified)
            data = args[0]
            xform = self.service_obj.signals[name]
            # (calling _truly_emit is handled by emitSignal)
            self.dbus_obj.emitSignal(name, xform.dump(data))
        else:
            # "Regular" events emit like normal
            self._truly_emit(name, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.dbus_obj, name)


def dbus_obj_factory(obj_path, attrs):
    cls = type(path.basename(obj_path), (DBusObject,), attrs)

    return cls(obj_path)


def dbus_method_factory(name, args_xform, returns_xform, fn):
    @returns_deferred
    async def dbus_method(remote_object, *args):
        xformed_args = args_xform.load(args)
        maybe_coro = fn(*xformed_args)

        if iscoroutine(maybe_coro) or isinstance(maybe_coro, Deferred):
            ret = await maybe_coro
        else:
            ret = maybe_coro

        return returns_xform.dump(ret)

    dbus_method.__name__ = name

    return dbus_method


def emit_signal_proxy_factory(proxy_ee):
    def emitSignal(self, signalName, *args, **kwargs):
        # Allow the proxy ee to handle signals
        proxy_ee.emit("signal", signalName, args)
        # Actually emit the signal
        return DBusObject.emitSignal(self, signalName, *args, **kwargs)

    return emitSignal


@attr.s
class Server(Node):
    connection = attr.ib()
    service = attr.ib()

    @classmethod
    async def create(server_cls, connection, service):
        server = server_cls(connection, service)

        bus_names = []

        def bind_signal_listener(obj, signal_ee):
            signals = obj.service_obj.signals

            # On emitSignal calls, call the object's underlying emitter
            @signal_ee.on("signal")
            def handle_signal(name, args):
                # If this is a known signal, re-hydrate the args
                if name in signals:
                    args = list(args)
                    args[0] = signals[name].load(args[0])
                    args = tuple(args)

                obj._truly_emit(name, *args)

        for obj_path, service_obj in service.items():
            # attributes for our dbus object instance
            obj_attrs = dict(
                iface=service_obj.iface, dbusInterfaces=[service_obj.iface]
            )

            # Collect method callbacks for the dbus object
            for (
                method_name,
                (args_xform, returns_xform, fn),
            ) in service_obj.methods.items():
                attr_name = f"dbus_{method_name}"

                dbus_method = dbus_method_factory(
                    attr_name, args_xform, returns_xform, fn
                )
                obj_attrs[attr_name] = dbus_method

            defaults = dict()

            # Collect dbus properties
            for (prop_name, (xform, default, _)) in service_obj.properties.items():
                obj_attrs[prop_name] = DBusProperty(prop_name)
                defaults[prop_name] = default

            # Intercept signals sent by the server
            signal_ee = EventEmitter()
            obj_attrs["emitSignal"] = emit_signal_proxy_factory(signal_ee)

            # Create a dbus object subclass with our callbacks and properties
            dbus_obj = dbus_obj_factory(obj_path, obj_attrs)

            # Set the default values for our dbus object
            for attr_name, default in defaults.items():
                setattr(dbus_obj, attr_name, default)

            # Construct a server object
            obj = Object(service_obj, dbus_obj)
            bind_signal_listener(obj, signal_ee)
            server.set(obj_path, obj)

            # Grab the iface
            iface = service_obj.iface

            # Store the dbus object on our wrapper object class
            obj.dbus_obj = dbus_obj

            # Export the object on the connection
            connection.exportObject(dbus_obj)

            # Collect the bus name as one we need to request
            bus_names.append(service.namespace)

        # Request all our bus names
        await DeferredList([connection.requestBusName(name) for name in bus_names])

        return server
