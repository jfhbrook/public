from functools import wraps


def add_representable_methods(cls, keys):
    def asdict(self):
        return {
            k: getattr(self, k)
            for k in keys
            if hasattr(self, k)
        }

    def repr_(self):
        return repr(self.asdict())

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

    # It should be possible to override this method independently of anything
    if not hasattr(cls, 'asdict'):
        if not keys:
            raise TypeError(
                'keys must be explicitly defined for classes without a '
                'prexisting asdict method'
            )
        cls.asdict = asdict

    # attrs already has a solid repr
    if not hasattr(cls, '__attrs_attrs__'):
        cls.__repr__ = repr_

    # Proper ipython/jupyter style pretty methods
    cls._repr_pretty_ = repr_pretty


def representable(cls=None):
    if hasattr(cls, '__attrs_attrs__'):
        keys = [attr.name for attr in cls.__attrs_attrs__]
        add_representable_methods(cls, keys)
        return cls
    else:
        if cls:
            keys = cls
        else:
            keys = None

        def decorator(cls):
            add_representable_methods(cls, keys)
            return cls

        return decorator

