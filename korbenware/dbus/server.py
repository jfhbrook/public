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

    def emit(self, name, data):
        if name not in self.service_obj.signals:
            return

        xform = self.service_obj.signals[name]
        self.dbus_obj.emitSignal(name, xform.dump(data))

        super().emit(self, name, data)

    def on(self, *args, **kwargs):
        raise NotImplementedError(
            "Signals can only be emitted by the server, not received"
        )


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


@attr.s
class Server(Node):
    connection = attr.ib()
    service = attr.ib()

    @classmethod
    async def create(server_cls, connection, service):
        server = server_cls(connection, service)

        bus_names = []

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
            for (prop_name, (xform, default, kwarg)) in service_obj.properties.items():
                obj_attrs[prop_name] = DBusProperty(prop_name)
                defaults[prop_name] = default

            # Create a dbus object subclass with our callbacks and properties
            dbus_obj = dbus_obj_factory(obj_path, obj_attrs)

            # Set the default values for our dbus object
            for attr_name, default in defaults.items():
                setattr(dbus_obj, attr_name, default)

            # Construct a server object
            obj = Object(service_obj, dbus_obj)
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
