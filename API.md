# LibSpecials [1]

## Special Objects [1.1]

### `VoidTypes`

&nbsp;&nbsp;&nbsp;&nbsp; `VoidTypes` is a `Final[list]` that contains both `NoneType` and `UndefinedType` types. These are the types used to instantiate a `None` built-in constant and an `Undefined` **Special Constant** _[1.3]_.

#### **USAGE:**

```python
>>> from voidsafe import VoidTypes, Undefined
>>> 
>>> type(None) in VoidTypes
True
>>> type(Undefined) in VoidTypes
True
```

## Special Types [1.2]

### `UndefinedType`
&nbsp;&nbsp;&nbsp;&nbsp; `UndefinedType` is similar to `NoneType` as the first one represents the type of the `Undefined` **Special Constant** _[1.3]_ the same way the second one represents the type of the `None` built-in constant. 

#### **USAGE:**

```python
>>> from voidsafe import VoidSafe, value
>>> 
>>> emptyDict: dict = {}
>>> 
>>> unsafeResource = VoidSafe(emptyDict)['undefined']
>>> extractedValue = unsafeResource >> value
>>> 
>>> print(extractedValue)
Undefined
>>> type(extractedValue)
UndefinedType
```

## Special Constants [1.3]

### `UNDEFINED`
> **Aliases**: `Undefined`

&nbsp;&nbsp;&nbsp;&nbsp; `UNDEFINED` is meant to represent an instance's resource that hasn't been defined before being accessed, which differs from an instance's `Optional` resource that has been defined as `None`.  

&nbsp;&nbsp;&nbsp;&nbsp; It is usually obtained from an attempt to getting resources from a **Potentially Unsafe Instance** _[2.1]_ that is being checked by the `VoidSafe` **Special Agent** _[1.4]_.

#### **USAGE:**

```python
>>> from typing import Optional
>>> from random import random
>>> from voidsafe import VoidSafe, value
>>> 
>>> class Empty:
...     def __setattr__(self, name, value):
...         object.__setattr__(self, name, value)
... 
>>> emptyInstance = Empty()
>>> 
>>> if random() < 0.01:
...     emptyInstance.doesntExist = "This probably won't happen"
... 
>>> # tying to access a 'Potentially Unsafe Resource [2.2]' ('doesntExist')
>>> print( VoidSafe(emptyObject).doesntExist )
VoidSafe(Undefined)
>>> 
>>> # extracting its value
>>> print( VoidSafe(emptyObject).doesntExist >> value )
Undefined
```

### `VOID`
> **Aliases**: `Void`

&nbsp;&nbsp;&nbsp;&nbsp; `VOID` keeps a list containing both `None` built-in constant and `Undefined` **Special Constant**. It can be used to find if a resource is either set as `None` or rather never been set (i.e. `Undefined`).

#### **USAGE:**

```python
>>> from voidsafe import VoidSafe, Void, value
>>> 
>>> testDict: dict[str, Any] = {}
>>> 
>>> testDict['none'] = None
>>> testDict['filled'] = 'filled'
>>> 
>>> # here's what happens when you try to access a resource
>>> # that has never been defined for an instance using 'VoidSafe'
>>> VoidSafe(testDict)['undefined'] >> value
Undefined
>>> 
>>> # now, we'll check their relationship to 'Void':
>>> 
>>> testDict['none'] in Void
True
>>> testDict['filled'] in Void
False
>>> VoidSafe(testDict)['undefined'] in Void
True
```

## Special Agents [1.4]

### `VOIDSAFE`
> **Aliases**: `VoidSafe`

&nbsp;&nbsp;&nbsp;&nbsp;  `VOIDSAFE` acts as a wrapper, protecting **Potentially Unsafe Instances** _[2.1]_ from having their **Potentially Unsafe Resources** _[2.2]_ accessed.

#### **USAGE:**

```python
>>> from voidsafe import VoidSafe, ifvoid
>>> from typing import Any
>>> from random import random
>>> 
>>> class Empty:
...     def __setattr__(self, __name, __value):
...         object.__setattr__(self, __name, __value)
... 
>>> def foo():
...     return "bar"
...
>>> emptyInstance: Empty = Empty()
>>> testDict: dict[str, Any] = {'probablyNone': None, 'pi': 3.14}
>>> 
>>> if random() < 0.01:
...     testDict['probablyUndefined'] = "This probably won't happen"
...     testDict['probablyNone'] = "Neither will this"
...     emptyInstance.probablyUndefined = "Or this"
...     emptyInstance.probablyNotImplemented = foo
... 
>>> # will return 3.14 in 100 out of 100 attempts:
>>> VoidSafe(testDict)['pi'] >> value 
3.14
>>> # will return "This probably won't happen" in 1 out of 100 attempts:
>>> VoidSafe(testDict)['probablyUndefined'] >> value 
Undefined
>>> # will return "Neither will this" in 1 out of 100 attempts:
>>> VoidSafe(testDict)['probablyNone'] >> value
None
>>> # will return "NEITHER WILL THIS" in 1 out of 100 attempts:
>>> VoidSafe(testDict)['probablyNone'].upper() >> value # 'None' has no 'upper' method
Undefined
>>> 
>>> potUnsafeResource = VoidSafe(testDict)['probablyNone'] >> value
>>> 
>>> # even knowing that 'potUnsafeResource' is probably set as 'None', you can pass a 
>>> # type to 'VoidSafe' to tell the linter to highlight and suggest valid methods for 
>>> # that type (that's what's called 'hacking the linter')
>>> VoidSafe[str](potUnsafeResource).upper() >> value # 'None' has no 'upper' method
Undefined
>>> 
>>> # will return "Or this" in 1 out of 100 attempts:
>>> VoidSafe(emptyInstance).probablyUndefined >> value 
Undefined
>>> # will return "bar" in 1 out of 100 attempts:
>>> VoidSafe(emptyInstance).foo() >> value 
Undefined
>>> 
>>> VoidSafe(testDict)['probablyUndefined'] = ifvoid << 'assignment #1'
>>> VoidSafe(testDict)['probablyNone'] = ifvoid << 'assignment #2'
>>> 
>>> # will return "This probably won't happen" in 1 out of 100 attempts
>>> VoidSafe(testDict)['probablyUndefined']
'assignment #1'
>>> # will return "Neither will this" in 1 out of 100 attempts
>>> VoidSafe(testDict)['probablyNone']
'assignment #2'
```

### `VALUE`
> **Aliases**: `value`

&nbsp;&nbsp;&nbsp;&nbsp;  `VALUE` allows you to use a `VoidSafe` chain of operations with the `>>` operator followed by itself. This works as a getter that extracts the value that is being kept by `VoidSafe` or any of its subproducts.

#### **USAGE:**

```python
>>> from typing import Optional
>>> from voidsafe import VoidSafe, value
>>> 
>>> unsafeStr: Optional[str] = 'content'
>>> 
>>> print( VoidSafe(unsafeStr).upper() >> value )
'CONTENT'
>>> 
>>> # now look what happens when it's set as 'None'
>>> # (which doesn't have a 'upper' method)
>>> unsafeStr = None
>>> 
>>> print( VoidSafe(unsafeStr).upper() >> value )
Undefined
```

## Special Operators [1.5]

### `IFNDEF`
> **Aliases**: `ifndef`

&nbsp;&nbsp;&nbsp;&nbsp; `IFNDEF` performs coalescing operations on `Undefined` **Potentially Unsafe Resources** _[2.2]_ accessed from instances that are being protected by the `VoidSafe` **Special Agent** _[1.4]_.

#### **USAGE:**

```python
>>> from voidsafe import VoidSafe, ifndef
>>> from typing import Any
>>> 
>>> testDict: dict[str, Any] = {'pi': 3.14}
>>> 
>>> # ['pi'] is already defined as 3.14
>>> VoidSafe(testDict)['pi'] << ifndef >> 123
3.14
>>> # now with an item that has never been defined
>>> VoidSafe(testDict)['undefined'] << ifndef >> 'content'
'content'
>>> 
>>> VoidSafe(testDict)['undefined'] = ifndef << 'first assignment'
>>> VoidSafe(testDict)['undefined'] = ifndef << 'second assignment' # not 'Undefined' anymore
>>> 
>>> testDict['undefined']
'first assignment'
```

### `IFNONE`
> **Aliases**: `ifnone`

&nbsp;&nbsp;&nbsp;&nbsp; `IFNONE` performs coalescing operations on `None`-assigned **Potentially Unsafe Instances** _[2.1]_ and also on `None`-assigned **Potentially Unsafe Resources** _[2.2]_, which are protected by the `VoidSafe` **Special Agent** _[1.4]_.

#### **USAGE:**

```python
>>> from voidsafe import VoidSafe, ifnone
>>> from typing import Any
>>> 
>>> testDict: dict[str, Any] = {'none': None, 'pi': 3.14}
>>> 
>>> # ['pi'] is already defined as 3.14
>>> VoidSafe(testDict)['pi'] << ifnone >> 123
3.14
>>> # now with an item that has been defined as 'None'
>>> testDict['none'] << ifnone >> 'content'
'content'
>>> 
>>> VoidSafe(testDict)['none'] = ifnone << 'first assignment'
>>> VoidSafe(testDict)['none'] = ifnone << 'second assignment' # not 'None' anymore
>>> 
>>> testDict['none']
'first assignment'
```

### `IFVOID`
> **Aliases**: `ifvoid`

&nbsp;&nbsp;&nbsp;&nbsp; `IFVOID` merges the behavior of `ifndef` and `ifnone` **Special Operators**, coalescing both `None`-assigned resources and `Undefined` resources.

#### **USAGE:**

```python
>>> from voidsafe import VoidSafe, ifvoid
>>> from typing import Any
>>> 
>>> testDict: dict[str, Any] = {'none': None, 'pi': 3.14}
>>> 
>>> # ['pi'] is already defined as 3.14
>>> VoidSafe(testDict)['pi'] << ifvoid >> 123
3.14
>>> # now with an item that has never been defined
>>> VoidSafe(testDict)['undefined'] << ifvoid >> 'content #1'
'content #1'
>>> # and with an item that has been defined as 'None'
>>> testDict['none'] << ifvoid >> 'content #2'
'content #2'
>>> 
>>> VoidSafe(testDict)['none'] = ifvoid << 'FIRST assignment #1'
>>> VoidSafe(testDict)['none'] = ifvoid << 'SECOND assignment #1' # not 'None' anymore
>>> VoidSafe(testDict)['undefined'] = ifvoid << 'FIRST assignment #2'
>>> VoidSafe(testDict)['undefined'] = ifvoid << 'SECOND assignment #2' # not 'Undefined' anymore
>>> 
>>> testDict['none']
'FIRST assignment #1'
>>> testDict['undefined']
'FIRST assignment #2'
```