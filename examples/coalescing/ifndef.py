#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from voidsafe import VoidSafe, ifndef
from voidsafe.unreliable import TAKEN_FOR_GRANTED
from typing import Optional


class UnsafeInstance:
    def __setattr__(self, __name, __value):
        object.__setattr__(self, __name, __value)


unsafeInst: UnsafeInstance = UnsafeInstance()
unsafeDict: dict = {}
unsafeStr: Optional[str] = None

safeStr: str = "always a valid string"

# Hover 'TAKEN_FOR_GRANTED' constant to see its documentation.
if TAKEN_FOR_GRANTED.happens:
    unsafeInst.unsafeDef = "assignment taken for granted #1"
    unsafeDict['unsafeDef'] = "assignment taken for granted #2"
    unsafeStr = "assignment taken for granted #3"


safeStr = VoidSafe(unsafeInst).unsafeDef << ifndef >> "TOOK_FOR_GRANTED.doesNotHappen #1"
print(safeStr)

safeStr = VoidSafe(unsafeDict)['unsafeDef'] << ifndef >> "TOOK_FOR_GRANTED.doesNotHappen #2"
print(safeStr)

# Remember the method 'upper()' is not defined for 'None'
safeStr = VoidSafe(unsafeStr).upper() << ifndef >> "TOOK_FOR_GRANTED.doesNotHappen #3"
print(safeStr)
