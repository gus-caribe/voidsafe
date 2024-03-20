#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from voidsafe import VoidSafe, ifndef, value


class UnsafeInstance:
    def __setattr__(self, __name, __value):
        object.__setattr__(self, __name, __value)


unsafeInst: UnsafeInstance = UnsafeInstance()
unsafeDict: dict = {}


# Note that 'unsafeDef' attribute is not defined for 'unsafeInst'
# and ['unsafeDef'] item is not defined for 'unsafeDict'

# At the point it reaches 'assignment #2', 'assignment #1' had already been done
VoidSafe(unsafeInst).unsafeDef = ifndef << "unsafeInst.unsafeDef assignment #1"
VoidSafe(unsafeInst).unsafeDef = ifndef << "unsafeInst.unsafeDef assignment #2"
print(VoidSafe(unsafeInst).unsafeDef >> value)

# At the point it reaches 'assignment #2', 'assignment #1' had already been done
VoidSafe(unsafeDict)['unsafeDef'] = ifndef << "unsafeDict['unsafeDef'] assignment #1"
VoidSafe(unsafeDict)['unsafeDef'] = ifndef << "unsafeDict['unsafeDef'] assignment #2"
print(VoidSafe(unsafeInst)['unsafeDef'] >> value)
