import attr


def dictable(keys):
    def asdict(self):
        return {
            k: getattr(self, k)
            for k in keys
            if hasattr(self, k)
        }

    def decorator(cls):
        cls.asdict = asdict
        return cls

    return decorator


def asdict(obj):
    if hasattr(obj.__class__, '__attrs_attrs__'):
        return attr.asdict(obj)
    else:
        return obj.asdict()


def representable(cls):
    if not (hasattr(cls, 'asdict') or hasattr(cls, '__attrs_attrs__')):
        raise TypeError(
            f'{cls} must be dictable. This functionality can either be '
            'supplied by the @attr.s decorator, the '
            '@pyxsession.util.decorators.dictable decorator, or manually.'
        )

    def repr_(self):
        return repr(asdict(self))

    def repr_pretty(self, p, cycle):
        if cycle:
            p.text(f'{self.__class__.__name__}(...)')
        else:
            with p.group(4, f'{self.__class__.__name__}(', ')'):
                p.breakable()
                for i, (k, v) in enumerate(asdict(self).items()):
                    if i:
                        p.text(',')
                        p.breakable()
                    p.text(f'{k}=')
                    p.pretty(v)

    # attrs already has a solid repr
    if not hasattr(cls, '__attrs_attrs__'):
        cls.__repr__ = repr_

    # Proper ipython/jupyter style pretty methods
    cls._repr_pretty_ = repr_pretty

    return cls
