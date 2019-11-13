import functools


class DBusMethod:
    def __init__(self, argv_types, rv_type):
        self.argv_types = argv_types
        self.rv_type = rv_type

    def client_method(self, fn):
        self.client_fn = fn
        return fn

    def server_method(self, fn):
        self.server_fn = fn
        return fn


def dbus_method(argv_types, rv_type):
    method = DBusMethod(argv_types, rv_type)

    def decorator(fn):
        method.client_method(fn)
        return method

    return decorator


def dbus_proxy(cls):
    def client_side_method(method_obj):
        """Generates the client-side entry point method"""

        @functools.wraps(method_obj.client_fn)
        def wrapped(self, *args, **kwargs):
            return method_obj.client_fn(
                getattr(self.remote_obj, method_obj.client_fn.__name__),
                *args, **kwargs
            )

        return wrapped

    def server_side_method(method_obj):
        """Generates the server-side entry point method"""

        @functools.wraps(method_obj.client_fn)
        def wrapped(self, *args, **kwargs):
            return method_obj.client_fn(self.server_fn, *args, **kwargs)

    def server_stub(method_obj):
        """Generates a stub for server implementation methods on the client"""
        @functools.wraps(method_obj.server_fn)
        def wrapped(self, *args, **kwargs):
            raise NotImplementedError(
                f'{method_obj.server_fn.__name__} is only implemented on the server!'  # noqa
            )
        return wrapped

    def remote_method(method_obj):
        """Generates the API method exposed over dbus"""

        @functools.wraps(method_obj.server_fn)
        def wrapped(self, *args):
            return getattr(
                self.remote_obj, method_obj.client_fn.__name__
            )(*args)

        return wrapped

    def mount(self, *, service, obj_path):
        self.service = service
        self.object = service.obj(obj_path)
        self.__dbus_methods__ = [
            method for method in dir(self) if isinstance(method, DBusMethod)
        ]

        for method_obj in self.__dbus_methods__:
            # Register the method on our object to call the server fn and
            # use the client fn name - necessary for both the client and the
            # server
            self.object.method(
                method_obj.argv_types, method_obj.rv_type,
                method_obj.server_fn,
                method_obj.client_fn.__name__
            )

    async def client_connect(self, connection):
        self.client = await self.service.client(connection)
        self.remote_obj = self.client.remote_obs[self.obj_path]
        return self.client

    def mount_client(self, *, service, obj_path):
        self.mount(service=service, obj_path=obj_path)
        for method_obj in self.__dbus_methods__:
            # Set the main method to proxy the remote call
            setattr(
                self, method_obj.client_fn.__name__,
                client_side_method(method_obj)
            )

            # Stub out the server-side method so we can't accidentally call it
            # on the client
            setattr(
                self, method_obj.server_fn.__name__,
                server_stub(method_obj)
            )

        self.connect = client_connect

    async def server_connect(self, connection):
        self.server = await self.service.server(connection)
        return self.server

    def mount_server(self, *, service, obj_path, connection, underlying):
        self.mount(service=service, obj_path=obj_path)
        self.underlying = underlying

        for method_obj in self.__dbus_methods__:
            # Set the main method on the server to just naively call itself
            # without using the remote
            setattr(
                self, method_obj.client_fn.__name__,
                server_side_method(self.remote_obj)
            )

        self.connect = server_connect

    cls.mount = mount
    cls.mount_client = mount_client
    cls.mount_server = mount_server

    return cls
