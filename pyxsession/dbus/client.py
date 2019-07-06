import attr

from pyxsession.dbus.path import split


class Node:
    pass


@attr.s
class Object:
    remote_obj = attr.ib()
    service_obj = attr.ib()

    async def call(self, method_name, *args):
        args_xform, returns_xform, _ = self.service_obj.methods[method_name]
        xformed_args = args_xform.dump(args)
        rv = await self.remote_obj.callRemote(method_name, *xformed_args)
        return returns_xform.dump(rv)

        return returns_xform.load(
            self.remote_obj.callRemote(method_name, *args_xform.dump(args))
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
            # Set up the iface and generate the remote object
            iface = service_obj.iface

            remote_obj = await connection.getRemoteObject(
                service.namespace, obj_path, iface
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

            # Add the shim functions for each method
            for method_name in service_obj.methods.keys():
                def bind(obj):
                    async def proxy_fn(*args):
                        return await obj.call(method_name, *args)
                    return proxy_fn

                proxy_fn = bind(obj)
                proxy_fn.__name__ = method_name

                setattr(obj, method_name, proxy_fn)

        client = Client(
            service,
            remote_objs
        )

        for attr, obj in client_objs.items():
            setattr(client, attr, obj)

        return client
