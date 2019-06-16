from functools import wraps


def representable(keys=None):
    if not keys:
        if hasattr(cls, '__attrs_attrs__'):
            keys = [
                attr.name
                for attr in cls.__attrs_attrs__
            ]
        else:
            raise TypeError(
                'Representable classes must either be attrs classes or have '
                'an explicit list of keys!'
            )

    def asdict(self):
        return {
            k: getattr(self, k)
            for k in keys
            if hasattr(self, k)
        }

    def repr_(self):
        return repr(self.as_dict())

    def repr_pretty(self, p, cycle):
        if cycle:
            p.text(f'{self.__class__.__name__}(...)')
        else:
            with p.group(4, f'{self.__class__.__name__}(', ')'):
                p.breakable()
                for i, (k, v) in enumerate(self.asdict().items()):
                    if i:
                        p.text(',')
                        p.breakable()
                    p.text(f'{k}=')
                    p.pretty(v)

    def decorator(cls):
        # Trying to duck type attrs classes, which already have asdict
        # and a solid repr
        if not hasattr(cls, '__attrs_attrs__'):
            setattr(cls, 'asdict', as_dict)
            setattr(cls, '__repr__', repr_)
        setattr(cls, '_repr_pretty_', repr_pretty)
        return cls

    return decorator
