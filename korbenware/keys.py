import attr


def asdict(obj):
    if hasattr(obj.__class__, '__attrs_attrs__'):
        return attr.asdict(obj)
    else:
        return obj.asdict()


class UndictableError(TypeError):
    def __init__(cls):
        super().__init__(
            f'{cls} must be dictable. This functionality can either be '
            'supplied by the @attr.s decorator, the '
            '@korbenware.keys.keys decorator, or manually '
            'implementing the {cls}.asdict method.'
        )


def is_dictable(cls):
    return hasattr(cls, 'asdict') or hasattr(cls, '__attrs_attrs__')


def assert_dictable(cls):
    if not is_dictable(cls):
        raise UndictableError(cls)


def try_asdict(obj, else_=None):
    if is_dictable(obj.__class__):
        return asdict(obj)
    else:
        return else_


def has_keys(cls):
    has_keys = hasattr(cls, '__keys__')
    has_attrs = hasattr(cls, '__attrs_attrs__')
    return has_keys or has_attrs


class UnkeysableError(Exception):
    def __init__(self, cls):
        super().__init__(
            f'{cls} must have keys. This functionality can either be '
            'supplied by the @attr.s decorator or the '
            '@korbenware.keys.keys decorator.'
        )


def assert_keys(cls):
    if not has_keys(cls):
        raise UnkeysableError(cls)


def iter_keys(obj):
    yield from (
        getattr(
            obj, '__keys__',
            [attr.name for attr in getattr(obj, '__attrs_attrs__')]
        )
    )


def iter_values(obj):
    for k in iter_keys(obj):
        yield getattr(obj, k)


def iter_items(obj):
    for k in iter_keys(obj):
        yield (k, getattr(obj, k))


def _default_keys(cls):
    return [
        k
        for k in dir(cls)
        if not k.startswith('_') and not hasattr(getattr(cls, k), '__call__')
    ]


def keys(keys=None):
    __keys__ = keys

    def keys(self):
        yield from self.__keys__

    def values(self):
        for key in self.keys():
            yield getattr(self, key)

    def items(self):
        for key in self.keys():
            yield key, getattr(self, key)

    def asdict(self):
        d = dict()
        for k in self.keys():
            v = getattr(self, k)
            d[k] = try_asdict(v, v)
        return d

    def decorator(cls):
        cls.__keys__ = __keys__ or _default_keys(cls)

        if not hasattr(cls, 'asdict'):
            cls.asdict = asdict

        cls.keys = keys
        cls.__iter__ = keys
        cls.values = values
        cls.items = items

        return cls

    return decorator
