import attr


def dictable(keys=None):
    if keys:
        def asdict(self):
            return {
                k: getattr(self, k)
                for k in keys
                if hasattr(self, k)
            }
    else:
        def asdict(self):
            d = dict()
            for k in dir(self):
                if not k.startswith('_'):
                    attr = getattr(self, k)
                    if not hasattr(attr, '__call__'):
                        d[k] = attr
            return d

    def decorator(cls):
        cls.asdict = asdict
        return cls

    return decorator


def asdict(obj):
    if hasattr(obj.__class__, '__attrs_attrs__'):
        return attr.asdict(obj)
    else:
        return obj.asdict()
