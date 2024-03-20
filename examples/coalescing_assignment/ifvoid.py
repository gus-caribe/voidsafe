#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from voidsafe import VoidSafe, ifvoid, value
from typing import Optional


class UnsafeInstance:
    unsafeOpt: Optional[str] = None

    def __setattr__(self, __name, __value):
        object.__setattr__(self, __name, __value)


unsafeInst: UnsafeInstance = UnsafeInstance()
unsafeDict: dict = {'unsafeRes': None}


# Note that: 
# - 'unsafeDef' attribute is not defined for 'unsafeInst'
# - 'unsafeOpt' attribute is defined as 'None' for 'unsafeInst'
# - ['unsafeDef'] item is not defined for 'unsafeDict'
# - ['unsafeOpt'] item is defined as 'None' for 'unsafeDict'


# At the point it reaches 'assignment #2', 'assignment #1' had already been done
VoidSafe(unsafeInst).unsafeOpt = ifvoid << "unsafeInst.unsafeOpt assignment #1"
VoidSafe(unsafeInst).unsafeOpt = ifvoid << "unsafeInst.unsafeOpt assignment #2"
print(unsafeInst.unsafeOpt)

# At the point it reaches 'assignment #2', 'assignment #1' had already been done
VoidSafe(unsafeInst).unsafeDef = ifvoid << "unsafeInst.unsafeDef assignment #1"
VoidSafe(unsafeInst).unsafeDef = ifvoid << "unsafeInst.unsafeDef assignment #2"
print(VoidSafe(unsafeInst).unsafeDef >> value)

# At the point it reaches 'assignment #2', 'assignment #1' had already been done
VoidSafe(unsafeDict)['unsafeOpt'] = ifvoid << "unsafeDict['unsafeOpt'] assignment #1"
VoidSafe(unsafeDict)['unsafeOpt'] = ifvoid << "unsafeDict['unsafeOpt'] assignment #2"
print(unsafeDict['unsafeOpt'])

# At the point it reaches 'assignment #2', 'assignment #1' had already been done
VoidSafe(unsafeDict)['unsafeDef'] = ifvoid << "unsafeDict['unsafeDef'] assignment #1"
VoidSafe(unsafeDict)['unsafeDef'] = ifvoid << "unsafeDict['unsafeDef'] assignment #2"
print(VoidSafe(unsafeInst)['unsafeDef'] >> value)
