# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from korbenware.dbus.marshmallow.fields import (
    BASE_FIELDS,
    List,
    Tuple,
    Dict,
    Nested,
    DBusField,
    SerializedField,
)

STRUCTURE_TYPES = {"r": ("(", ")"), "e": ("{", "}")}


def SignatureError(Exception):
    pass


def field_signature(field):
    sig = ""

    if type(field) == List:
        sig += "a"
        inner = field.inner
        sig += field_signature(inner)
    elif type(field) == Tuple:
        sig += "("
        for f in field.tuple_fields:
            sig += field_signature(f)
        sig += ")"
    elif type(field) == Dict:
        sig += "a{"
        sig += field_signature(field.key_field)
        sig += field_signature(field.value_field)
        sig += "}"
    elif type(field) == Nested:
        inner = field.schema
        sig += schema_signature(inner)
    elif isinstance(field, SerializedField):
        sig += BASE_FIELDS[field.field_cls]
    elif type(field) in BASE_FIELDS:
        sig += BASE_FIELDS[type(field)]
    elif type(field) == DBusField:
        base_type = field.dbus_type
        params = field.dbus_type_params
        if params:
            raise NotImplementedError(
                "Nested schemas with custom masks not implemented yet!"
            )
        sig += base_type
    else:
        raise SignatureError(f"Unknown field type {field}")

    return sig


def schema_signature(schema):
    if "wrapped_field" in schema.fields:
        return field_signature(schema.fields["wrapped_field"])

    sig = "("
    for name, field in schema.fields.items():
        sig += field_signature(field)
    sig += ")"

    return sig