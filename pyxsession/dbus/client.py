import attr
from pyee import TwistedEventEmitter as EventEmitter
from pyxsession.dbus.path import split


class Node:
    pass


class Object(EventEmitter):
    def __init__(self, remote_obj, service_obj):
        super().__init__()
        self._emit = self.emit
        self.remote_obj = remote_obj
        self.service_obj = service_obj

    async def call(self, method_name, *args):
        args_xform, returns_xform, _ = self.service_obj.methods[method_name]
        xformed_args = args_xform.dump(args)
        rv = await self.remote_obj.callRemote(method_name, *xformed_args)

        return returns_xform.dump(rv)

        return returns_xform.load(
            self.remote_obj.callRemote(method_name, *args_xform.dump(args))
        )

    async def get_property(self, prop_name):
        xform, default, kwargs = self.service_obj.properties[prop_name]

        rv = await self.remote_obj.callRemote(
            'Get', '', prop_name
        )

        return xform.load(rv)

    async def set_property(self, prop_name, value):
        xform, default, kwargs = self.service_obj.properties[prop_name]

        await self.remote_obj.callRemote(
            'Set', '', prop_name, xform.dump(value)
        )


@attr.s
class Client:
    service = attr.ib()
    remote_objs = attr.ib()

    @classmethod
    async def create(cls, connection, service):
        remote_objs = dict()
        client_objs = dict()

        for obj_path, service_obj in service.objects.items():
            remote_obj = await connection.getRemoteObject(
                service.namespace, obj_path
            )

            remote_objs[obj_path] = remote_obj

            # Generate and attach the client object
            obj = Object(remote_obj, service_obj)

            path_parts = split(obj_path)
            first_part = path_parts.pop(0)
            try:
                last_part = path_parts.pop()
            except IndexError:
                last_part = None

            if last_part:
                this_node = Node()
                client_objs[first_part] = this_node
                for path_part in path_parts:
                    setattr(this_node, path_part, Node())
                    this_node = getattr(this_node, path_part)
                setattr(this_node, last_part, obj)
            else:
                client_objs[first_part] = obj

            def bind(obj):
                async def proxy_fn(*args):
                    return await obj.call(method_name, *args)
                return proxy_fn

            # Add the shim functions for each method
            for method_name in service_obj.methods.keys():

                proxy_fn = bind(obj)
                proxy_fn.__name__ = method_name

                setattr(obj, method_name, proxy_fn)

            # Signals
            for event_name, xform in service_obj.signals.items():
                remote_obj.notifyOnSignal(
                    event_name, lambda d: obj.emit(event_name, xform.load(d))
                )

        client = Client(
            service,
            remote_objs
        )

        for attr, obj in client_objs.items():
            setattr(client, attr, obj)

        return client
