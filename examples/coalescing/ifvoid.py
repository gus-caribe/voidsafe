#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from voidsafe import VoidSafe, ifvoid
from voidsafe.unreliable import TAKEN_FOR_GRANTED
from typing import Optional


class UnsafeInstance:
    unsafeOpt: Optional[str] = None
    
    def __setattr__(self, __name, __value):
        object.__setattr__(self, __name, __value)


unsafeInst: UnsafeInstance = UnsafeInstance()
unsafeDict: dict = {'unsafeOpt': None}
unsafeStr: Optional[str] = None

safeStr: str = "always a valid string"

# Hover 'TAKEN_FOR_GRANTED' constant to see its documentation.
if TAKEN_FOR_GRANTED.happens:
    unsafeInst.unsafeOpt = "assignment taken for granted #1"
    unsafeInst.unsafeDef = "assignment taken for granted #2"
    unsafeDict['unsafeOpt'] = "assignment taken for granted #3"
    unsafeDict['unsafeDef'] = "assignment taken for granted #4"
    unsafeStr = "assignment taken for granted #5"


safeStr = VoidSafe(unsafeInst).unsafeOpt << ifvoid >> "TOOK_FOR_GRANTED.doesNotHappen #1"
print(safeStr)

safeStr = VoidSafe(unsafeInst).unsafeDef << ifvoid >> "TOOK_FOR_GRANTED.doesNotHappen #2"
print(safeStr)

safeStr = VoidSafe(unsafeDict)['unsafeOpt'] << ifvoid >> "TOOK_FOR_GRANTED.doesNotHappen #3"
print(safeStr)

safeStr = VoidSafe(unsafeDict)['unsafeDef'] << ifvoid >> "TOOK_FOR_GRANTED.doesNotHappen #4"
print(safeStr)

# Remember the method 'upper()' is not defined for 'None'
safeStr = VoidSafe(unsafeStr).upper() << ifvoid >> "TOOK_FOR_GRANTED.doesNotHappen #5"
print(safeStr)

safeStr = unsafeStr << ifvoid >> "TOOK_FOR_GRANTED.doesNotHappen #6"
print(safeStr)
