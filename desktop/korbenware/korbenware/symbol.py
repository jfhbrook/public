# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import attr

from korbenware.presentation import representable


@representable
@attr.s(eq=False, order=False)
class Symbol:
    name = attr.ib(default="<symbol>")
