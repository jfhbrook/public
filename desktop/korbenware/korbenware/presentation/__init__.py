# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from korbenware.keys import asdict, assert_dictable


def representable(cls):
    assert_dictable(cls)

    def repr_(self):
        return repr(asdict(self))

    def repr_pretty(self, p, cycle):
        if cycle:
            p.text(f"{self.__class__.__name__}(...)")
        else:
            with p.group(4, f"{self.__class__.__name__}(", ")"):
                p.breakable()
                for i, (k, v) in enumerate(asdict(self).items()):
                    if i:
                        p.text(",")
                        p.breakable()
                    p.text(f"{k}=")
                    p.pretty(v)

    # attrs already has a solid repr
    if not hasattr(cls, "__attrs_attrs__"):
        cls.__repr__ = repr_

    # Proper ipython/jupyter style pretty methods
    cls._repr_pretty_ = repr_pretty

    return cls