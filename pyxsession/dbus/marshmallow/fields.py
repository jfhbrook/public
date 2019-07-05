from marshmallow import fields

__all__ = [
    'DBusField', 'Int32', 'UInt32', 'Str', 'Nested', 'List', 'Tuple',
    'Variant', 'BASE_FIELDS'
]


class DBusField(fields.Field):
    def __init__(self, dbus_type, dbus_type_params=None):
        super().__init__()
        self.dbus_type = dbus_type
        self.dbus_type_params = dbus_type_params


class Variant(fields.Field):
    pass

  
class Int32(fields.Integer):
    pass

    
class UInt32(fields.Integer):
    # TODO: Validation around int < 0
    pass

Str = fields.Str

Nested = fields.Nested
List = fields.List
Tuple = fields.Tuple


# TODO: There are a lot of these!!
BASE_FIELDS = {
    Int32: 'i',
    UInt32: 'u',
    Str: 's',
    Variant: 'v'
}
