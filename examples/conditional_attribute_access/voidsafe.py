#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from voidsafe import VoidSafe
from voidsafe.unreliable import TAKEN_FOR_GRANTED
from typing import Optional


# ----------------------------------------------
class UnsafeInstance:
    """
    `UnsafeInstance` only serves for the purpose of being used as a generalization
    of any instance that might not hold a value that's required for further operations
    """

    unsafeAttr = "unsafeAttr has been accessed"

    def __getitem__(self, __key) -> str:
        if __key == "unsafeItem":
            return "unsafeItem has been accessed"
        return ""

    def unsafeCall(self) -> str:
        return "unsafeCall has been called"
# ----------------------------------------------


# 'unsafeInst' is initialized as 'None'
unsafeInst: Optional[UnsafeInstance] = None

# Hover 'TAKEN_FOR_GRANTED' constant to see its documentation.
if TAKEN_FOR_GRANTED.happens:
    # 'unsafeInst' gets assigned with a value that will be required
    # to perform further operations
    unsafeInst = UnsafeInstance()

# Now, if you want to secure your application, you'll want to wrap 
# 'unsafeInst' in order to access its 'Potentially Unsafe Resources':
print( VoidSafe(unsafeInst).unsafeAttr )
print( VoidSafe(unsafeInst)['unsafeItem'] )
print( VoidSafe(unsafeInst).unsafeCall() )
