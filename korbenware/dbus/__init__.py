import datetime

import attr
from marshmallow.fields import Field

from korbenware.dbus.service import Service  # noqa
from korbenware.dbus.marshmallow.fields import (
    DBusField, Bytes, Bool, Int16, UInt16, Int32, UInt32, Int64, UInt64,
    Double, Str, ObjectPath, Signature, List, Tuple, Nested, Variant,
    DateTime
)
from korbenware.dbus.marshmallow.schema import DBUS_FIELD, DBUS_NESTED

__all__ = [
    'Field', 'Service', 'DBusField', 'Bytes', 'Bool', 'Int16', 'UInt16',
    'Int32', 'UInt32', 'Int64', 'UInt64', 'Double', 'Str', 'ObjectPath',
    'Signature', 'List', 'Tuple', 'Nested', 'Variant', 'DateTime',
    'DBUS_FIELD', 'DBUS_NESTED', 'dbus_attr'
]


SENSIBLE_DEFAULTS = {
    Bool: False,
    Int16: -1,
    UInt16: 0,
    Int32: -1,
    UInt32: 0,
    Int64: -1,
    UInt64: 0,
    Double: -1,
    Str: '',
    List: attr.Factory(list),
    Tuple: attr.Factory(tuple),
    DateTime: datetime.datetime.fromtimestamp(0)
}


def dbus_attr(field=None, metadata=None, default=None, **kwargs):
    if not default:
        default = SENSIBLE_DEFAULTS.get(field, attr.Factory(field))

    metadata = metadata or dict()

    if isinstance(field, Field):
        metadata[DBUS_FIELD] = field
    else:
        metadata[DBUS_NESTED] = field

    return attr.ib(metadata=metadata, default=default, **kwargs)
