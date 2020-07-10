from asyncio import iscoroutine

import attr
from pyee import TwistedEventEmitter as EventEmitter
from twisted.internet.defer import Deferred
from txdbus.objects import DBusObject, DBusProperty

import korbenware.dbus.path as path
from korbenware.dbus.tree import Node
from korbenware.twisted.util import returns_deferred


class Object(Node, EventEmitter):
    def __init__(self, service_obj, dbus_obj=None):
        Node.__init__(self)
        EventEmitter.__init__(self)
        self.service_obj = service_obj
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


def create_dbus_obj_subcls(name, attrs):
    return type(name, (DBusObject,), attrs)


@attr.s
class Server(Node):
    connection = attr.ib()
    service = attr.ib()
    bus_names = attr.ib()
    dbus_obj_cls = attr.ib()
    dbus_obj = attr.ib()

    @classmethod
    async def create(server_cls, connection, service):
        bus_names = []
        attrs = dict()
        objects = dict()

        for obj_path, service_obj in service.items():
            obj = Object(service_obj)

            # Attach our object ot the server cls
            objects[obj_path] = obj

            # Generate and add the interface
            iface = service_obj.iface
            attrs["iface"] = iface
            attrs["dbusInterfaces"] = [iface]

            def bind(args_xform, returns_xform, fn):
                @returns_deferred
                async def proxy_fn(remote_object, *args):
                    xformed_args = args_xform.load(args)
                    maybe_coro = fn(*xformed_args)

                    if iscoroutine(maybe_coro) or isinstance(maybe_coro, Deferred):
                        ret = await maybe_coro
                    else:
                        ret = maybe_coro

                    return returns_xform.dump(ret)

                return proxy_fn

            # Add the dbus method callbacks
            for (
                method_name,
                (args_xform, returns_xform, fn),
            ) in service_obj.methods.items():
                key = f"dbus_{method_name}"

                proxy_fn = bind(args_xform, returns_xform, fn)
                attrs[key] = proxy_fn
                proxy_fn.__name__ = key

            defaults = dict()

            # Add dbus properties
            for (prop_name, (xform, default, kwarg)) in service_obj.properties.items():
                attrs[prop_name] = DBusProperty(prop_name)
                defaults[prop_name] = default
            # TODO: This is wrong, there is more than one dbus object, one for each object on the service
            dbus_obj_cls = create_dbus_obj_subcls(path.basename(obj_path), attrs)
            dbus_obj = dbus_obj_cls(obj_path)

            for attr_name, default in defaults.items():
                setattr(dbus_obj, attr_name, default)

            obj.dbus_obj = dbus_obj

            connection.exportObject(dbus_obj)

            bus_names.append(await connection.requestBusName(service.namespace))

        server = server_cls(connection, service, bus_names, dbus_obj_cls, dbus_obj)

        for p, obj in objects.items():
            server.set(p, obj)

        return server
