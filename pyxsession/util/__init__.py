import attr

from pyxsession.util.decorators import representable


@representable
@attr.s(cmp=False)
class Symbol:
    name = attr.ib(default='<symbol>')
