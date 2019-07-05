import pytest

from pyxsession.dbus.transformers import Transformer, MultiTransformer
from pyxsession.dbus.marshmallow.fields import Str


@pytest.mark.parametrize('type_,dumped,loaded,sig', [
    (Str(), 'hello', 'hello', 's')
])
def test_transformer(type_, dumped, loaded, sig):
    xform = Transformer(type_)
    assert xform.dump(loaded) == dumped
    assert xform.load(dumped) == loaded
    assert xform.signature() == sig
