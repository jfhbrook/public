from pyxsession.dbus.marshmallow.fields import (
    STRUCTURED_FIELDS,
    BASE_FIELDS,
    DBusField
)

STRUCTURE_TYPES = {
    'r': ('(', ')'),
    'e': ('{', '}')
}


def SignatureError(Exception):
    pass


def field_signature(field):
    sig = ''

    if type(field) in STRUCTURED_FIELDS:
        left, right, accessor = STRUCTURED_FIELDS[field]
        sig += left
        accessed = accessor(field)
        if type(accessed) == list or type(accessed) == tuple:
            for f in accessed:
                sig += schema_signature(f)
        else:
            sig += schema_signature(accessor(field))
        sig += right
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
    sig = ''
    for name, field in schema.fields.items():
        sig += field_signature(field)

    return sig
