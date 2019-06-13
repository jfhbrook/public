from functools import wraps


def representable(keys):
    # TODO: Default list of keys
    # See: https://stackoverflow.com/questions/1911281/how-do-i-get-list-of-methods-in-a-python-class
    def as_dict(self):
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
                for i, (k, v) in enumerate(self.as_dict().items()):
                    if i:
                        p.text(',')
                        p.breakable()
                    p.text(f'{k}=')
                    p.pretty(v)

    def decorator(cls):
        setattr(cls, 'as_dict', as_dict)
        setattr(cls, '__repr__', repr_)
        setattr(cls, '_repr_pretty_', repr_pretty)
        return cls

    return decorator
