import pytest

import attr

from pyxsession.dbus.marshmallow.fields import (
    DBusField, Int32, UInt32, Str, Nested, List, Tuple
)
from pyxsession.dbus.marshmallow.schema import (
    DBusSchema, DBUS_FIELD, DBUS_NESTED,
    from_attrs, from_field,
    SingletonClass, SingletonSchema
)
from pyxsession.dbus.marshmallow.signature import (
    field_signature, schema_signature
)


@attr.s
class NestedTestObj:
    str_field = attr.ib(metadata={DBUS_FIELD: Str()})


@attr.s
class BasicTestObj:
    int_field = attr.ib(metadata={DBUS_FIELD: Int32()})
    uint_field = attr.ib(metadata={DBUS_FIELD: UInt32()})
    str_field = attr.ib(metadata={DBUS_FIELD: Str()})
    nested_field = attr.ib(metadata={DBUS_NESTED: NestedTestObj})

    # TODO: Support nested attrs classes, ie List(NestedTestObj)
    list_field = attr.ib(metadata={DBUS_FIELD: List(Str())})
    tuple_field = attr.ib(metadata={DBUS_FIELD: Tuple((Int32(), Str()))})


class NestedTestSchema(DBusSchema):
    cls = NestedTestObj
    str_field = Str()


class BasicTestSchema(DBusSchema):
    cls = BasicTestObj

    int_field = Int32()
    uint_field = UInt32()
    str_field = Str()
    nested_field = Nested(NestedTestSchema)
    list_field = List(Str())
    tuple_field = Tuple((Int32(), Str()))


basic_test_obj = BasicTestObj(
    int_field=3,
    uint_field=5,
    str_field='foo',
    nested_field=NestedTestObj('bar'),
    list_field=['baz', 'quux'],
    tuple_field=(7, 'moo')
)


basic_test_signature = 'ius(s)a(s)(is)'

basic_test_dump = [3, 5, 'foo', ['bar'], ['baz', 'quux'], (7, 'moo')]


@pytest.mark.parametrize('schema', [
    BasicTestSchema(),
    from_attrs(BasicTestObj)
])
def test_base_schema(schema):
    from_attrs(BasicTestObj)
    assert schema.dump(basic_test_obj) == basic_test_dump
    assert schema.load(basic_test_dump) == basic_test_obj
    assert schema_signature(schema) == basic_test_signature
