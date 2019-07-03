from pyxsession.util import Symbol

DBUS_TYPE = Symbol('DBUS Type')
DBUS_TYPE_PARAMS = Symbol('DBUS Type Parameters')

STRUCTURE_TYPES = {
    'r': ('(', ')'),
    'e': ('{', '}')
}


def dbus_signature(typ):
    """
    class -> dbus signature
    """
    if isinstance(typ, list) or isinstance(typ, tuple):
        return ''.join([
            dbus_signature(subtype)
            for subtype in typ
        ])

    signature = ''

    for attr in typ.__attrs_attrs__:
        if DBUS_TYPE_PARAMS in attr.metadata:
            base_type = attr.metadata[DBUS_TYPE]
            params = attr.metadata[DBUS_TYPE_PARAMS]

            for t in base_type:
                if t in STRUCTURE_TYPES:
                    left, right = STRUCTURE_TYPES[t]
                    signature += left
                    # May either be a list of elements
                    # or a single set
                    if type(params) == list:
                        param = params.pop(0)
                    else:
                        param = params

                    # May be a single string or a tuple
                    if type(param) == str:
                       param = [param]
                    for p in param:
                        if type(p) == str:
                            signature += p
                        else:
                            signature += dbus_signature(p)
                    signature += right
                else:
                   signature += t
        else:
            signature += attr.metadata[DBUS_TYPE]

    return signature


def unstructure(data_structure):
    """
    data structure -> thing txdbus can send
    """
    if isinstance(data_structure, list) or isinstance(data_structure, tuple):
        rv = [
            dbus_marshall(element)
            for element in data_structure
        ]
        return [rv]
    elif isinstance(data_structure, dict):
        return [{k: unstructure(v)[0] for k, v in data_structure.items()}]
    elif hasattr(data_structure.__class__, '__attrs_attrs__'):
        ret = []
        attrs = data_structure.__class__.__attrs_attrs__

        for attr in attrs:
            value = getattr(data_structure, attr.name)
            ret += unstructure(value)
        return ret
    else:
       return [data_structure]


def structure(raw, typ):
    """
    thing dbus will give us -> data structure
    """
    
    if hasattr(typ, '__attrs_attrs__'):
        structured = []
        for unstructured, attr in zip(raw, typ.__attrs_attrs__):
            base_type = attr.metadata[DBUS_TYPE]
            
            pieces = (
                [unstructured]
                if type(unstructured) not in {list, dict}
                else unstructured
            )

            for t, subfield in zip(base_type, pieces):
                if t == 'r':
                    structured.append([
                        structure(subfield)
                        for x in subfield
                    ])
                elif t == 'e':
                    structured.append({
                        structure(k): structure(v)
                        for k, v in subfield.items()
                    })
                else:
                    structured.append(structure(unstructured, base_type))
        return typ(*structured)
    else:
        return raw
