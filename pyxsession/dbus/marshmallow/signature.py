from pyxsession.dbus.marshmallow.fields import (
    BASE_FIELDS,
    List, Tuple, Nested, DBusField, Variant
)

STRUCTURE_TYPES = {
    'r': ('(', ')'),
    'e': ('{', '}')
}


def SignatureError(Exception):
    pass


def field_signature(field):
    sig = ''

    if type(field) == List:
        sig += 'a('
        inner = field.container
        sig += field_signature(inner)
        sig += ')'
    elif type(field) == Tuple:
        sig += '('
        for f in field.tuple_fields:
            sig += field_signature(f)
        sig += ')'
    elif type(field) == Nested:
        sig += '('
        inner = field.schema
        sig += schema_signature(inner)
        sig += ')'
    elif type(field) in BASE_FIELDS:
        sig += BASE_FIELDS[type(field)]
    elif type(field) == DBusField:
        base_type = field.dbus_type
        params = field.dbus_type_params
        if params:
            raise NotImplementedError(
                'Nested schemas with custom masks not implemented yet!'
            )
        sig += base_type
    else:
        raise SignatureError(f'Unknown field type {field}')

    return sig


def schema_signature(schema):
    sig = '('
    for name, field in schema.fields.items():
        sig += field_signature(field)
    sig += ')'

    return sig
