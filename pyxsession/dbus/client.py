class Client:
    def __init__(self, service, remote_obj):
        self.service = service
        self.remote_obj = remote_obj
        
    async def call(self, method_name, *args):
        args_xform, returns_xform, _ = self.service.methods[method_name]
        xformed_args = args_xform.dump(args)
        rv = await self.remote_obj.callRemote(method_name, *xformed_args)
        return returns_xform.dump(rv)

        return returns_xform.load(
            self.remote_obj.callRemote(method_name, *args_xform.dump(args))
        )
