from collections import OrderedDict
import attr
from marshmallow import Schema, fields
from marshmallow.schema import SchemaMeta
from marshmallow.decorators import post_dump, pre_load, post_load
from txdbus import client

from pyxsession.util import Symbol


class DBusSchema(Schema, metaclass=SchemaMeta):
    class Meta:
        ordered = True
      
    @post_dump
    def _flatten_attrs_dicts(self, unstructured, many):
        # TODO: What if not dealing with an attrs class?
        # Should dictable use ordered dicts?
        return [
            unstructured[attr.name]
            for attr in self.cls.__attrs_attrs__
        ]
        return unstructured
      
    @pre_load
    def _restructure_flattened_attrs(self, unstructured, many, **kwargs):
        if many:
            return [
                self._restructure_flattened_attrs(self, unstructured, one)
                for one in many
            ]
        return OrderedDict([
            (attr.name, value)
            for attr, value in zip(self.cls.__attrs_attrs__, unstructured)
        ])
    
    @post_load
    def _inflate_flattened_attrs(self, unstructured, many, **kwargs):
        if many:
            return [self.cls(*un) for un in unstructured]
        return self.cls(**unstructured)


DBUS_SCHEMA = Symbol('attrs metadata for generating a dbus schema')


def from_attrs(attrs_cls):
    fields = {
        attr.name: attr.metadata[DBUS_SCHEMA]
        for attr in attrs_cls.__attrs_attrs__
        if DBUS_SCHEMA in attr.metadata
    }

    fields['cls'] = attrs_cls

    return type(f'{attrs_cls.__name__}Schema', (DBusSchema,), fields)
