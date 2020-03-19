import attr
from marshmallow.fields import Field

from korbenware.dbus.service import Service  # noqa
from korbenware.dbus.marshmallow.schema import from_attrs
from korbenware.dbus.marshmallow.fields import (
    DBusField, Bytes, Bool, Int16, UInt16, Int32, UInt32, Int64, UInt64,
    Double, Str, ObjectPath, Signature, List, Tuple, Nested, Variant
)
from korbenware.dbus.marshmallow.schema import DBUS_FIELD, DBUS_NESTED

__all__ = [
    'Field', 'Service', 'DBusField', 'Bytes', 'Bool', 'Int16', 'UInt16',
    'Int32', 'UInt32', 'Int64', 'UInt64', 'Double', 'Str', 'ObjectPath',
    'Signature', 'List', 'Tuple', 'Nested', 'Variant', 'DBUS_FIELD',
    'DBUS_NESTED', 'dbus_attr', 'from_attrs'
]


def dbus_attr(field=None, metadata=None, **kwargs):
    metadata = metadata or dict()

    if isinstance(field, Field):
        metadata[DBUS_FIELD] = field
    else:
        metadata[DBUS_NESTED] = field

    return attr.ib(metadata=metadata, **kwargs)
