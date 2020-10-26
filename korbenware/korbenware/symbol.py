import attr

from korbenware.presentation import representable


@representable
@attr.s(eq=False, order=False)
class Symbol:
    name = attr.ib(default="<symbol>")
