#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional
from voidsafe.unreliable import TAKEN_FOR_GRANTED
from voidsafe import VoidSafe


unsafeStr: Optional[str] = None

# Hover 'TAKEN_FOR_GRANTED' constant to see its documentation.
if TAKEN_FOR_GRANTED.happens:
    unsafeStr = "assignment taken for granted #1"

# At this poit, 'unsafeStr' might not be a string (if TAKEN_FOR_GRANTED.doesNotHappen),
# but you can specify '[str]' allowing your linter to suggest the available methods for
# 'str' and highlight them in a semantic manner.
VoidSafe[str](unsafeStr).upper()
