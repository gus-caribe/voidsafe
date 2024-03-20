#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from voidsafe import VoidSafe, ifnone
from typing import Optional


class UnsafeInstance:
    unsafeOpt: Optional[str] = None


unsafeInst: UnsafeInstance = UnsafeInstance()
unsafeDict: dict = {'unsafeOpt': None}


# Note that 'unsafeOpt' attribute is defined as 'None' for 'unsafeInst'
# and ['unsafeOpt'] item is defined as 'None' for 'unsafeDict'

# At the point it reaches 'assignment #2', 'assignment #1' had already been done
VoidSafe(unsafeInst).unsafeOpt = ifnone << "unsafeInst.unsafeOpt assignment #1"
VoidSafe(unsafeInst).unsafeOpt = ifnone << "unsafeInst.unsafeOpt assignment #2"
print(unsafeInst.unsafeOpt)

# At the point it reaches 'assignment #2', 'assignment #1' had already been done
VoidSafe(unsafeDict)['unsafeOpt'] = ifnone << "unsafeDict['unsafeOpt'] assignment #1"
VoidSafe(unsafeDict)['unsafeOpt'] = ifnone << "unsafeDict['unsafeOpt'] assignment #2"
print(unsafeDict['unsafeOpt'])
