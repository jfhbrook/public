# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import datetime

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
    def __init__(self, cls_or_instance, **kwargs):
        if hasattr(cls_or_instance, "__attrs_attrs__"):
            field = fields.Nested(from_attrs(cls_or_instance))
        else:
            field = cls_or_instance
        super().__init__(field, **kwargs)


class Dict(fields.Dict):
    # TODO: Validate that keys is a base field type
    def __init__(self, keys, values, **kwargs):
        if hasattr(values, "__attrs_attrs__"):
            values = fields.Nested(from_attrs(values))
        super().__init__(keys, values, **kwargs)


Tuple = fields.Tuple
Nested = fields.Nested


class Variant(fields.Field):
    pass


class SerializedField(fields.Field):
    field_cls = None


class DateTime(SerializedField):
    field_cls = Int64

    def _serialize(self, value, attr, obj, **kwargs):
        if not value:
            return 0
        return int(value.timestamp() * 1000)

    def _deserialize(self, value, attr, data, **kwargs):
        if not value:
            value = 0
        return datetime.datetime.fromtimestamp(value / 1000)


BASE_FIELDS = {
    Bytes: "y",
    Bool: "b",
    Int16: "n",
    UInt16: "q",
    Int32: "i",
    UInt32: "u",
    Int64: "x",
    UInt64: "t",
    Double: "d",
    Str: "s",
    ObjectPath: "o",
    Signature: "g",
    Variant: "v",
}
