import attr
from pyee import TwistedEventEmitter as EventEmitter
from pyxsession.dbus.tree import insert_into_tree
from pyxsession.dbus.path import split


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

        # TODO: Why is this necessary???
        if not returns_xform.is_field:
            rv = rv[0]
        return returns_xform.load(rv)

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

            insert_into_tree(client_objs, split(obj_path), obj)

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

        for attr_, obj in client_objs.items():
            setattr(client, attr_, obj)

        return client
