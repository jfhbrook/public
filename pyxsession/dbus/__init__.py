import attr
from marshmallow.fields import Field

from pyxsession.dbus.service import Service
from pyxsession.dbus.marshmallow.fields import (
    DBusField, Bytes, Bool, Int16, UInt16, Int32, Int64, UInt64, Double,
    Str, ObjectPath, Signature, List, Tuple, Nested, Variant
)
from pyxsession.dbus.marshmallow.schema import DBUS_FIELD, DBUS_NESTED

type_ = type
def dbus_attr(type=None, attr_type=None, metadata=None, **kwargs):
    metadata = metadata or dict()

    if isinstance(type, Field):
        metadata[DBUS_FIELD] = type
    else:
        metadata[DBUS_NESTED] = type

    return attr.ib(type=attr_type, metadata=metadata, **kwargs)
