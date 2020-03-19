from marshmallow import fields

from korbenware.dbus.marshmallow.schema import from_attrs


class DBusField(fields.Field):
    def __init__(self, dbus_type, dbus_type_params=None):
        super().__init__()
        self.dbus_type = dbus_type
        self.dbus_type_params = dbus_type_params


class Bytes(fields.Str):
    pass


Bool = fields.Bool


class _UInt(fields.Integer):
    # TODO: validate inner value >= 0
    pass


class Int16(fields.Integer):
    pass


class UInt16(_UInt):
    pass


class Int32(fields.Integer):
    pass


class UInt32(_UInt):
    pass


class Int64(fields.Integer):
    pass


class UInt64(_UInt):
    pass


class Double(fields.Float):
    pass


Str = fields.Str


class ObjectPath(fields.Str):
    # TODO: Validate as an object path
    pass


class Signature(fields.Str):
    pass


class List(fields.List):
    def __init__(self, field_or_attrs, **kwargs):
        if hasattr(field_or_attrs, '__attrs_attrs__'):
            field = fields.Nested(from_attrs(field_or_attrs))
        else:
            field = field_or_attrs
        super().__init__(field)


Tuple = fields.Tuple
Nested = fields.Nested


class Variant(fields.Field):
    pass


BASE_FIELDS = {
    Bytes: 'y',
    Bool: 'b',
    Int16: 'n',
    UInt16: 'q',
    Int32: 'i',
    UInt32: 'u',
    Int64: 'x',
    UInt64: 't',
    Double: 'd',
    Str: 's',
    ObjectPath: 'o',
    Signature: 'g',
    Variant: 'v'
}
