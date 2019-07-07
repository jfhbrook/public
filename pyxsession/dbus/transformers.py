from marshmallow.fields import Field

from pyxsession.dbus.marshmallow.schema import from_field, from_attrs
from pyxsession.dbus.marshmallow.signature import field_signature, schema_signature


class Transformer:
    def __init__(self, type_):
        if type_ is None:
            self.schema = None
        elif isinstance(type_, Field):
            self.is_field = True
            self.schema = from_field(type_)
        else:
            self.is_field = False
            self.schema = from_attrs(type_)
          
    def signature(self):
        if not self.schema:
            return ''
        return schema_signature(self.schema)
        
    def dump(self, structured):
        if not self.schema:
            return None

        return self.schema.dump(structured)
      
    def load(self, unstructured):
        if not self.schema:
            return None

        return self.schema.load(unstructured)

      
class MultiTransformer(Transformer):
    def __init__(self, types):
        self.transformers = [Transformer(type_) for type_ in types]
        
    def signature(self):
        return ''.join([xform.signature() for xform in self.transformers])
        
    def dump(self, structured):
        return [xform.dump(s) for xform, s in zip(self.transformers, structured)]
      
    def load(self, unstructured):
        return [xform.load(u) for xform, u in zip(self.transformers, unstructured)]
