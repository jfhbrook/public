from marshmallow.fields import Field

from pyxsession.dbus.marshmallow.schema import from_field, from_attrs
from pyxsession.dbus.signature import schema_signature


class Transformer:
    def __init__(self, type_):
       if isinstance(type_, Field):
           self.schema = from_field(type_)
       else:
           self.schema = from_attrs(type_)
          
    def signature(self):
        return schema_signature(self.schema)
        
    def dump(self, structured):
       return self.schema.dump(structured)
      
    def load(self, unstructured):
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
