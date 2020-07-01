import datetime
import typing

import attr
from marshmallow.fields import Field

from korbenware.dbus.service import Service  # noqa
from korbenware.dbus.marshmallow.fields import (
    DBusField,
    Bytes,
    Bool,
    Int16,
    UInt16,
    Int32,
    UInt32,
    Int64,
    UInt64,
    Double,
    Str,
    ObjectPath,
    Signature,
    List,
    Tuple,
    Dict,
    Nested,
    Variant,
    DateTime,
)
from korbenware.dbus.marshmallow.schema import DBUS_FIELD, DBUS_NESTED

__all__ = [
    "Field",
    "Service",
    "DBusField",
    "Bytes",
    "Bool",
    "Int16",
    "UInt16",
    "Int32",
    "UInt32",
    "Int64",
    "UInt64",
    "Double",
    "Str",
    "ObjectPath",
    "Signature",
    "List",
    "Tuple",
    "Nested",
    "Dict",
    "Variant",
    "DateTime",
    "DBUS_FIELD",
    "DBUS_NESTED",
    "dbus_attr",
]


DEFAULTS_FOR_FIELDS = {
    Bool: False,
    Int16: -1,
    UInt16: 0,
    Int32: -1,
    UInt32: 0,
    Int64: -1,
    UInt64: 0,
    Double: -1,
    Str: "",
    List: attr.Factory(list),
    Tuple: attr.Factory(tuple),
    Dict: attr.Factory(dict),
    DateTime: datetime.datetime.fromtimestamp(0),
}


def default_for_field(field):
    if hasattr(field, '__attrs_attrs__'):
        return attr.Factory(field)

    return DEFAULTS_FOR_FIELDS[type(field)]


FIELDS_FOR_DEFAULTS = {
    bool: Bool,
    int: Int64,
    str: Str,
    datetime.datetime: DateTime
}


def field_for_default(default):
    return FIELDS_FOR_DEFAULTS[type(default)]


TYPES_FOR_FIELDS = {
    Bool: bool,
    Int16: int,
    UInt16: int,
    Int32: int,
    UInt32: int,
    Int64: int,
    UInt64: int,
    Double: float,
    Str: str,
    DateTime: datetime.datetime
}


def type_for_field(field):
    if hasattr(field, '__attrs_attrs__'):
        return field
    if hasattr(field, 'cls') and hasattr(field.cls, '__attrs_attrs__'):
        return field.cls

    t = type(field)

    if t == Nested:
        return type_for_field(field.nested)

    if t == List:
        I = type_for_field(field.inner)
        return typing.List[I]

    if t == Dict:
        K = type_for_field(field.key_field)
        V = type_for_field(field.value_field)

        return typing.Dict[K, V]

    # TODO: Iterate through the first few sizes of tuples

    return TYPES_FOR_FIELDS[t]


class DBusAttrSpecificationError(Exception):
    def __init__(self, field, type, default):
        super().__init__(
            'Could not create a DBus attr specification with '
            f'field={field}, type={type}, default={default}'
        )


def dbus_attr(field=None, type=None, default=None, metadata=None, **kwargs):
    try:
        if default is None:
            if field is None:
                raise KeyError('Must either define default or field')
            default = default_for_field(field)
        elif field is None:
            field = field_for_default(default)

        if not type:
            type = type_for_field(field)

    except KeyError as exc:
        raise DBusAttrSpecificationError(field, type, default) from exc

    metadata = metadata or dict()

    if isinstance(field, Field):
        metadata[DBUS_FIELD] = field
    else:
        metadata[DBUS_NESTED] = field

    return attr.ib(type=type, default=default, metadata=metadata, **kwargs)
