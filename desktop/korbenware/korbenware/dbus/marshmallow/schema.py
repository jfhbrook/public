# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections import OrderedDict

import attr
from marshmallow import Schema
from marshmallow.schema import SchemaMeta
from marshmallow.decorators import pre_dump, post_dump, pre_load, post_load

from marshmallow.fields import Nested
from korbenware.symbol import Symbol


class DBusSchema(Schema, metaclass=SchemaMeta):
    class Meta:
        ordered = True

    @post_dump
    def _flatten_attrs_dicts(self, unstructured, many, **kwargs):
        if many:
            return [self._flatten_attrs_dicts(self, u) for u in unstructured]

        # TODO: What if not dealing with an attrs class?
        return [unstructured[attr.name] for attr in self.cls.__attrs_attrs__]

    @pre_load
    def _restructure_flattened_attrs(self, unstructured, many, **kwargs):
        if many:
            return [
                self._restructure_flattened_attrs(self, unstructured, one)
                for one in many
            ]

        return OrderedDict(
            [
                (attr.name, value)
                for attr, value in zip(self.cls.__attrs_attrs__, unstructured)
            ]
        )

    @post_load
    def _inflate_flattened_attrs(self, unstructured, many, **kwargs):
        if many:
            return [self.cls(*un) for un in unstructured]
        return self.cls(**unstructured)


DBUS_FIELD = Symbol("attrs metadata for generating a dbus schema from a field")
DBUS_NESTED = Symbol(
    "attrs metadata for generating a dbus schema from nested attrs class"
)


@attr.s
class WrappedField:
    wrapped_field = attr.ib()


class WrappedFieldSchema(Schema, metaclass=SchemaMeta):
    class Meta:
        ordered = True

    @pre_dump
    def _wrap_field(self, structured, many, **kwargs):
        if many:
            return [self.cls(s) for s in structured]
        return self.cls(structured)

    @post_dump
    def _flatten_dict(self, unstructured, many, **kwargs):
        if many:
            return [self._extract_field(u) for u in unstructured]
        return unstructured["wrapped_field"]

    @pre_load
    def _dictify_field(self, unstructured, many, **kwargs):
        if many:
            return [self._dictify_field(u) for u in unstructured]

        return dict(wrapped_field=unstructured)

    @post_load
    def _extract_field(self, structured, many, **kwargs):
        if many:
            return [self._extract_field(s) for s in structured]
        return structured["wrapped_field"]


def from_field(field):
    class FieldSchemaClass(WrappedFieldSchema, metaclass=SchemaMeta):
        cls = WrappedField
        wrapped_field = field

    FieldSchemaClass.__name__ = f"{field.__class__.__name__}Schema"

    return FieldSchemaClass()


def from_attrs(attrs_cls):
    class AttrsSchemaMeta(SchemaMeta):
        @classmethod
        def get_declared_fields(mcls, klass, cls_fields, inherited_fields, dict_cls):
            fields = super().get_declared_fields(
                klass, cls_fields, inherited_fields, dict_cls
            )

            for attr_ in attrs_cls.__attrs_attrs__:
                if DBUS_FIELD in attr_.metadata:
                    fields[attr_.name] = attr_.metadata[DBUS_FIELD]
                elif DBUS_NESTED in attr_.metadata:
                    fields[attr_.name] = Nested(from_attrs(attr_.metadata[DBUS_NESTED]))

            return fields

    class AttrsSchemaClass(DBusSchema, metaclass=AttrsSchemaMeta):
        cls = attrs_cls

    AttrsSchemaClass.__name__ = f"{attrs_cls.__name__}Schema"

    return AttrsSchemaClass()