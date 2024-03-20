#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from voidsafe import ifnone
from voidsafe.unreliable import TAKEN_FOR_GRANTED
from typing import Optional


class UnsafeInstance:
    unsafeOpt: Optional[str] = None


unsafeInst: UnsafeInstance = UnsafeInstance()
unsafeDict: dict = {'unsafeOpt': None}
unsafeStr: Optional[str] = None

safeStr: str = "always a valid string"

# Hover 'TAKEN_FOR_GRANTED' constant to see its documentation.
if TAKEN_FOR_GRANTED.happens:
    unsafeInst.unsafeOpt = "assignment taken for granted #1"
    unsafeDict['unsafeOpt'] = "assignment taken for granted #2"
    unsafeStr = "assignment taken for granted #3"


safeStr = unsafeInst.unsafeOpt << ifnone >> "TOOK_FOR_GRANTED.doesNotHappen #1"
print(safeStr)

safeStr = unsafeDict['unsafeOpt'] << ifnone >> "TOOK_FOR_GRANTED.doesNotHappen #2"
print(safeStr)

safeStr = unsafeStr << ifnone >> "TOOK_FOR_GRANTED.doesNotHappen #3"
print(safeStr)
