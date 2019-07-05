class Client:
    def __init__(self, service, remote_obj):
        self.service = service
        self.remote_obj = remote_obj
        
    def call(self, method_name, *args):
        args_xform, returns_xform, fn = self.service.methods[method_name]
        xformed_args = args_xform.dump(args)

        raw_ret = self.remote_obj.callRemote(method_name, xformed_args)

        return returns_xform.load(raw_ret)
