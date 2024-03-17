"""
## VoidSafe
-----------
    \
`VoidSafe` is a library that brings a `void-safe`, `None-aware` approach to
Python3-written scripts and applications. It provides software developers with resources
to apply `null-safe`-like principles to their codebase, guaranteeing that safe
operations can be performed on `potentially unsafe instances [2.1]`, which helps assuring 
that your software will be able to handle many memory-access problems at runtime.  
    \
By being entirely `type-hinted`, this library works well when associated with most
`static type checkers`. When combined with a linter that's capable of predicting `unboud`
or `undefined` variables, this library helps the developer to identify problems with
their code even before running it.  
    \
The inspiration comes from the concept of `Null Safety`, which is adopted by several
programming languages, such as `Dart`, `Kotlin` and `C#`.  
"""

from types import NoneType
from typing import Self, final, Any, Callable, Final, Generic, Optional, Type, TypeVar, Union


_T = TypeVar('_T')
"""
`_T` is the TypeVar used in most of the `Generic` types of this module.
"""


@final
class UndefinedType:
    """
        \
    `UndefinedType` is a `Special Type [1.2]` that's similar to `NoneType` as the first one 
    represents the type of the `Undefined` `Special Constant [1.3]` the same way the second 
    one represents the type of the `None` built-in constant. 

    - Example:

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
    ...
    """

    def __init__(self, _: Callable[[], None]):
        pass

    def __repr__(self) -> str:
        return "Undefined"


@UndefinedType
def Undefined() -> None:
    # docstrings implemented here will have no use
    pass


UNDEFINED: Final[UndefinedType] = Undefined
"""
#### Aliases: `Undefined`
---
    \
`UNDEFINED` is a `Special Constant [1.3]` that's meant to represent an instance's  
resource that hasn't been defined before being accessed, which differs from an 
instance's `Optional` resource that has been defined as `None`.
    \
It is usually obtained from an attempt to getting resources from a `Potentially 
Unsafe Instance [2.1]` that is being checked by the `VoidSafe` `Special Agent [1.4]`.

- Example:

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
...
"""


Undefined.__doc__ = UNDEFINED.__doc__


class _CoalesceAction():
    """
        \
    `_CoalesceAction` creates a wrapper around a value that is supposed to be 
    assigned to a resource, but only if it attends the condition of a coalescing 
    `Infix`.
    
    - Example:

        ```python
        from voidsafe import VoidSafe, ifnone, _CoalesceAction
        
        testDict: dict = {'none': None}
        
        VoidSafe(testDict)['none'] = ifnone << "default value"
        # the previous line can be refactored like the following:
        VoidSafe(testDict)['none'] = _CoalesceAction("default value", [None])
        ```
    ...
    """

    __slots__ = ('_content', '_checkObjects')

    def __init__(self, content: Any, checkObjects: list[Union[NoneType, UndefinedType]]):
        self._content = content
        self._checkObjects = checkObjects


# Those are just meant to be used to address _VoidSafe's _bond tuple
_PARENT: Final[int] = 0
_CHILD: Final[int] = 1


class _VoidSafeTrailing():
    """
        \
    `_VoidSafeTrailing` is a wrapper around a chain of resource accesses starting from a 
    `VoidSafe(foo)` call. 
    
    - Example:

        ```python
        from voidsafe import VoidSafe

        # ---------  From here on, everything is wrapped into a '_VoidSafeTrailing'
        # ---------  v
        VoidSafe(foo).attribute['item'].call()
        ```
    ...
    """

    _latestGetItemKey: Any = Undefined
    _latestGetAttrName: str = ""
    _bond: tuple[Any, Any] = (Undefined, Undefined)

    def __init__(self, parent: Any, child: Any) -> None:
        self._bond = (parent, child)
    
    def _moveForward(self, nextChild: Any) -> None:
        self._bond = (self._bond[_CHILD], nextChild)
    
    def _trySet(self, value: Any) -> bool:
        if self._bond[_PARENT] is None or self._bond[_PARENT] is Undefined:
            return False
        
        try:
            if self._latestGetAttrName != "":
                self._bond[_PARENT].__setattr__(self._latestGetAttrName, value)
                self._bond = (self._bond[_PARENT], self._bond[_PARENT].__getattribute__(self._latestGetAttrName))
                self._latestGetAttrName = ""
            elif self._latestGetItemKey != Undefined:
                self._bond[_PARENT][self._latestGetItemKey] = value # type: ignore
                self._bond = (self._bond[_PARENT], self._bond[_PARENT][self._latestGetItemKey]) # type: ignore
                self._latestGetItemKey = Undefined
            else:
                return False
        except:
            return False
        return True
    
    # self.__name
    def __getattr__(self, __name: str) -> Union[Self, Any]:
        if __name in ['_latestGetItemKey', '_latestGetAttrName', '_bond']:
            return object.__getattribute__(self, __name)
        
        attempt: Any = Undefined

        try:
            attempt = self._bond[_CHILD].__getattribute__(__name)
        finally:
            self._moveForward(attempt)
            self._latestGetAttrName = __name
            self._latestGetItemKey = Undefined
            return self
    
    # self.__name = __value
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in ['_latestGetItemKey', '_latestGetAttrName', '_bond']:
            object.__setattr__(self, __name, __value)
            return
        
        if type(__value) is _CoalesceAction and self._bond[_CHILD] not in __value._checkObjects:
            __value = __value._content
        self._latestGetAttrName = __name
        self._moveForward(__value)
    
    # self[__key]
    def __getitem__(self, __key: Any) -> Self:
        attempt: Any = Undefined

        try:
            attempt = self._bond[_CHILD].__getitem__(__key) # type: ignore
        finally:
            self._moveForward(attempt)
            self._latestGetAttrName = ""
            self._latestGetItemKey = __key
            return self
    
    # self[__key] = __value
    def __setitem__(self, __key: Any, __value: Any) -> None:
        if type(__value) is _CoalesceAction and self._bond[_CHILD] not in __value._checkObjects:
            __value = __value._content
        self._latestGetItemKey = __key
        self._moveForward(__value)
    
    # self(*args, **kwargs)
    def __call__(self, *args, **kwargs) -> Self:
        attempt: Any = Undefined

        try:
            attempt = self._bond[_CHILD](*args, **kwargs) # type: ignore
        finally:
            self._moveForward(attempt)
            self._latestGetAttrName = ""
            self._latestGetItemKey = Undefined
            return self

    # self == __other
    def __eq__(self, __other: Any) -> bool:
        return self._bond[_CHILD] == __other
    
    def __repr__(self) -> str:
        return f"NoneSafe({self._bond[_CHILD]})"


class _VoidSafeLeading():
    """
        \
    `_VoidSafeLeading` is a proxy that grabs the `potentially unsafe instance` being  
    checked by a `VoidSafe(foo)` call (i.e. The root element from a `VoidSafe` operation).
        \
    It is responsible for addressing to the `_VoidSafeTrailing` wrapper any operation that 
    follows.
        \
    This entity had to be created apart from `_VoidSafeTrailing` because at the time it is 
    called, there is no resource being accessed from the checked instance. That means that    
    there is no chance that the protected value is `Undefined` at runtime, so the operations  
    with `ifndef` coalescing `Infix` souldn't be allowed with `_VoidSafeLeading`-protected    
    instances.
    - Example:

        ```python
        from typing import Optional
        from voidsafe import VoidSafe, ifndef

        unsafeStr: Optional[str] = None
        safeStr: str = ""

        #  ---------------------------- Not possible
        #  ---------------------------- v
        safeStr = VoidSafe(unsafeStr) <<ifndef>> "default value"
        ```
    ...
    """

    _check: Any = Undefined

    def __init__(self, check: Any):
        self._check = check
    
    # self.__name
    def __getattr__(self, __name: str) -> Union[_VoidSafeTrailing, Any]:
        if __name == '_check':
            return object.__getattribute__(self, __name)
        
        try:
            return _VoidSafeTrailing(self._check, self._check.__getattribute__(__name))
        except:
            return _VoidSafeTrailing(self._check, Undefined)
    
    # self.__name = __value
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == '_check':
            object.__setattr__(self, __name, __value)
            return
        
        if type(__value) is _CoalesceAction and self._bond[_CHILD] not in __value._checkObjects:
            __value = __value._content
        try:
            self._check.__setattr__(__name, __value)
        except: pass
    
    # self[__key]
    def __getitem__(self, __key: Any) -> _VoidSafeTrailing:
        voidSafe: _VoidSafeTrailing = _VoidSafeTrailing(Undefined, self._check)
        return voidSafe[__key]
    
    #self[__key] = __value
    def __setitem__(self, __key: Any, __value: Any) -> None:
        if type(__value) is _CoalesceAction and self._bond[_CHILD] not in __value._checkObjects:
            __value = __value._content
        try:
            self._check[__key] = __value
        except: pass
    
    # self(*args, **kwargs)
    def __call__(self, *args, **kwargs) -> _VoidSafeTrailing:
        voidSafe: _VoidSafeTrailing = _VoidSafeTrailing(Undefined, self._check)
        return voidSafe(*args, **kwargs)
    
    # self == __other
    def __eq__(self, __other: Any) -> bool:
        return self._check == __other
    
    def __repr__(self) -> str:
        return f"NoneSafe({self._check})"


class _VoidSafeInitiator(Generic[_T]):
    """
        \
    `_VoidSafeInitiator` receives the instance that will be checked and passes it along to 
    the `_VoidSafeLeading` wrapper.
        \
    It is also responsible for "tricking" the linter into interpreting the instance passed 
    to the `check` parameter of its `__call__` method as an instance of the same type passed 
    to the Special Constant `VoidSafe`'s `__getitem__` method (i.e. `VoidSafe[Type]`).
    - Example:

        ```python
        >>> from typing import Optional
        >>> from voidsafe import VoidSafe, value
        >>> 
        >>> unsafeStr: Optional[str] = None
        >>> 
        >>> # --------  '_VoidSafeInitiator[str]' is the result of 'VoidSafe[str]'
        >>> # --------  v
        >>> VoidSafe[str](unsafeStr).upper() >> value
        Undefined
        ```

        Most linters will highlight the `upper` method semantically, even if `unsafeStr` is 
        `None`.
    ...
    """

    def __call__(self, check: Optional[_T]) -> Union[_VoidSafeLeading, _T]:
        """
            \
        The instance passed between these parenthesis will be wrapped into a safe scope
        where every attempt to access, set or call the instance itself or any of its
        resources results in a new wrapper.

        ...
        """
        return _VoidSafeLeading(check)


class _VoidSafeInfix(_VoidSafeInitiator):
    """
        \
    `_VoidSafeInfix` is a class that is used as a decorator for the `VoidSafe` function, 
    resulting on an `instance` that will be further called the `VoidSafe` Special Constant.
        \
    It also works as a proxy, allowing you to use its `__getitem__` to receive a type and  
    pass it along to the `_VoidSafeInitiator`.
    ...
    """

    def __init__(self, _: Callable[[], None]):
        pass
    
    def __getitem__(self, _: Type[_T]) -> _VoidSafeInitiator[_T]:
        """
            \
        The type passed between these brackets will be passed along to the `VoidSafe.__call__`'s
        only parameter, where it's wrapped into an `Optional`. This tells the linter to highlight 
        semantically and suggest all the methods and attributes available for the type passed as 
        argument.

        ...
        """
        return _VoidSafeInitiator[_T]()
    
    def __repr__(self) -> str:
        return "NoneSafe"


@_VoidSafeInfix
def VoidSafe() -> None:
    # docstrings implemented here will have no use
    pass


VOIDSAFE: Final[_VoidSafeInfix] = VoidSafe
"""
#### Aliases: `VoidSafe`
---
    \
`VOIDSAFE` is a `Special Agent [1.4]` that acts as a wrapper, protecting `Potentially   
Unsafe Instances [2.1]` from having their `Potentially Unsafe Resources [2.2]` accessed.
    \
Usually, you can find if an instance/resource is `Potentially Unsafe [2]` by checking   
if its values are into the `Void` `Special Constant [1.3]` provided by the present library.
Type `'VOID'` to see how it's done.
- Example:

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
    >>> VoidSafe(testDict)['probablyNone'].upper() >> value
    Undefined
    >>> 
    >>> potUnsafeResource = VoidSafe(testDict)['probablyNone'] >> value
    >>> 
    >>> # even knowing that 'ptUnsafeResource' is probably set as 'None', you can pass a 
    >>> # type to 'VoidSafe' to tell the linter to highlight and suggest valid methods for 
    >>> # that type (that's what's called 'tricking the linter')
    >>> VoidSafe[str](potUnsafeResource).upper() >> value
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

...
"""

VoidSafe.__doc__ = VOIDSAFE.__doc__


class _ValueInfix():
    """
        \
    `_ValueInfix` is a class that is used as a decorator for the `value` function, resulting  
    on an `instance` that will be further called the `VALUE` `Special Agent [1.4]`.

    ...
    """
    
    _func: Callable[[Any], Any] = lambda _: _


    def __init__(self, func: Callable[[Any], Any]):
        self._func = func
        
    
    # other >> self
    def __rrshift__(self, other: Any) -> Any:
        return self._func(other)
    
    def __repr__(self) -> str:
        return "value"


@_ValueInfix
def value(other: Any) -> Any:
    # docstrings implemented here will have no use

    if type(other) is _VoidSafeTrailing:
        return other._bond[_CHILD]
    if type(other) is _VoidSafeLeading:
        return other._check
    return other


VALUE: Final[_ValueInfix] = value
"""
#### Aliases: `value`
----
    \
`VALUE` is a `Special Agent [1.4]` that allows you to use a `VoidSafe` chain of  
operations with the `>>` operator followed by itself. This works as a getter that  
extracts the value that is being kept by `VoidSafe` or any of its subproducts.
- Example:

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
...
"""

value.__doc__ = VALUE.__doc__


class _VoidInfix:
    """
        \
    `_VoidInfix` is a class that is used as a decorator for the `Void` function, resulting 
    on an `instance` that will be further called the `VOID` Special Constant.

    ...
    """

    _list: list[Union[NoneType, UndefinedType]] = []

    def __init__(self, func: Callable[[], list[Union[NoneType, UndefinedType]]]):
        self._list = func()

    def __contains__(
        self,
        other: Union[NoneType, UndefinedType, _VoidSafeLeading, _VoidSafeTrailing]
    ) -> bool:
        check = other

        if type(other) is _VoidInfix:
            return True
        if type(other) is _VoidSafeLeading:
            check = other._check
        elif type(other) is _VoidSafeTrailing:
            check = other >> value
        
        return check in self._list
    
    def __repr__(self) -> str:
        return "Void"


@_VoidInfix
def Void() -> list[Union[NoneType, UndefinedType]]:
    # docstrings implemented here will have no use
    return [None, Undefined]


VOID: Final[_VoidInfix] = Void
"""
#### Aliases: `value`
----
    \
`VOID` is a `Special Constant [1.3]` that keeps a list containing both `None` built-in  
constant and `Undefined` Special Constant. It can be used to find  if a resource is either 
set as `None` or rather never been set (i.e. `Undefined`).
- Example:

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
...
"""

Void.__doc__ = VOID.__doc__


VoidTypes: Final[tuple[Type, Type]] = (NoneType, UndefinedType)
"""
    \
`VoidTypes` is a `Special Object [1.1]`. It is a Final list that contains both `NoneType` 
and `UndefinedType` types. These are the types used to instantiate a `None` built-in 
constant and an `Undefined` `Special Constant [1.3]`.
- Example:

    ```python
    >>> from voidsafe import VoidTypes, Undefined
    >>> 
    >>> type(None) in VoidTypes
    True
    >>> type(Undefined) in VoidTypes
    True
    ```
...
"""


_LeftType = TypeVar("_LeftType", Any, Any)
"""
`_LeftType` is used to represent an element positioned to the left of a coalescing `Infix`.
"""

class _Coalesce(Generic[_LeftType]):
    """
        \
    `_Coalesce` is the base class of a group of coalescing proxies that sould be instantiated 
    by a coalescing `Infix`.
        \
    It receives an element that's positioned at its left and provides the `>>` operator,   
    allowing to perform coalescing operations. That is done by returning the element at the   
    right of `>>` if the attribute `_checkObjects` contains the element at the left.
    
    ...
    """

    _left: _LeftType
    _checkObjects: list[Union[NoneType, UndefinedType]] = []


    def __init__(self, left: _LeftType) -> None:
        self._left = left
    

    # self >> other
    def __rshift__(self, other: _T) -> _T:
        result = self._left >> value
        
        if type(result) is type(other) and result not in self._checkObjects:
            return result
        
        return other

class _UndefinedCoalesce(_Coalesce[_VoidSafeTrailing]):
    """
        \
    Subtype of `_Coalesce` dedicated to operations being done to a `_VoidSafeTrailing`'s
    protected instance when its value is `UNDEFINED`.

    ...
    """

    _checkTypes: Final[list[UndefinedType]] = [Undefined]


class _NoneCoalesce(_Coalesce[Any]):
    """
        \
    Subtype of `_Coalesce` dedicated to operations being done to any instance when 
    its value is `None`.

    ...
    """

    _checkTypes: Final[list[NoneType]] = [None]


class _VoidCoalesce(_Coalesce[Any]):
    """
        \
    Subtype of `_Coalesce` dedicated to operations being done to any instance when 
    its value is either `None` or a `_VoidSafeTrailing`' when its protected value
    is `Undefined`.

    ...
    """

    _checkTypes: Final[list[Union[NoneType, UndefinedType]]] = Void._list


_CoalesceType = TypeVar(
    "_CoalesceType", 
    _NoneCoalesce, 
    _UndefinedCoalesce, 
    _VoidCoalesce
)
"""
`_CoalesceType` is a generalization for all of the `_Coalesce` class subtypes.
"""

class _IfNdefInfix(object):
    """
        \
    `_IfNdefInfix` is a class that is used as a decorator for the `ifndef` function, 
    resulting on an `instance` that will further be called the `IFNDEF` `Special Operator [1.5]`.

    ...
    """

    __slots__ = ('_func')

    def __init__(self, func: Callable[[_VoidSafeTrailing], _UndefinedCoalesce]):
        self._func: Callable[[_VoidSafeTrailing], _UndefinedCoalesce] = func
    
    # other << self
    def __rlshift__(self, left: _VoidSafeTrailing) -> _UndefinedCoalesce:
        return self._func(left)
    
    # self << other
    def __lshift__(self, right: Any) -> _CoalesceAction:
        return _CoalesceAction(right, [Undefined])
    
    def __repr__(self) -> str:
        return "ifndef"

class _CoalesceInfix(Generic[_CoalesceType]):
    """
        \
    `_CoalesceInfix` is a class that provides a `Generic` parameter that specifies a
    `_Coalesce` type. That allows for creating `TypeAliases` for `_CoalesceInfix` that
    specify which coalescing operation will be done.
        \
    This class and its aliases will be used as decorators for `Special Operators [1.5]`.

    ...
    """

    __slots__ = ('_func')

    def __init__(self, func: Callable[[Any], _CoalesceType]):
        self._func: Callable[[Any], _CoalesceType] = func
    
    # other << self
    def __rlshift__(self, left: Any) -> _CoalesceType:
        return self._func(left)
    
    # self << other
    def __lshift__(self, right: Any) -> _CoalesceAction:
        checkObjects: list[Union[NoneType, UndefinedType]] = []

        if _CoalesceType is _NoneCoalesce:
            checkObjects = [None]
        elif _CoalesceType is _VoidCoalesce:
            checkObjects = Void._list

        return _CoalesceAction(right, checkObjects)

class _IfNoneInfix(_CoalesceInfix[_NoneCoalesce]):
    """
        \
    `_IfNoneInfix` is a class that is used as a decorator for the `ifnone` function, 
    resulting on an `instance` that will further be called the `IFNONE` `Special Operator [1.5]`.

    ...
    """

    def __repr__(self) -> str:
        return "ifnone"


class _IfVoidInfix(_CoalesceInfix[_VoidCoalesce]):
    """
        \
    `_IfVoidInfix` is a class that is used as a decorator for the `ifvoid` function, 
    resulting on an `instance` that will further be called the `IFVOID` `Special Operator [1.5]`.

    ...
    """

    def __repr__(self) -> str:
        return "ifvoid"


@_IfNdefInfix
def ifndef(left: _VoidSafeTrailing) -> _UndefinedCoalesce:
    # docstrings implemented here will have no use
    return _UndefinedCoalesce(left)

IFNDEF: Final[_IfNdefInfix] = ifndef
"""
#### Aliases: `ifndef`
----
    \
`IFNDEF` is a `Special Operator [1.5]` that performs coalescing operations on `Undefined` 
`Potentially Unsafe Resources [2.2]` accessed from instances protected by the `VoidSafe` 
`Special Agent [1.4]`.
- Example:

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
...
"""

@_IfNoneInfix
def ifnone(left: Any) -> _NoneCoalesce:
    # docstrings implemented here will have no use
    return _NoneCoalesce(left)

IFNONE: Final[_IfNoneInfix] = ifnone
"""
#### Aliases: `ifnone`
----
    \
`IFNONE` is a `Special Operator [1.5]` that performs coalescing operations on `None`-assigned \
`Potentially Unsafe Instances [2.1]` and also on `None`-assigned `Potentially Unsafe Resources 
[2.2]`, which are protected by the `VoidSafe` `Special Agent [1.4]`.
- Example:

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
...
"""

@_IfVoidInfix
def ifvoid(left: Any) -> _VoidCoalesce:
    # docstrings implemented here will have no use
    return _VoidCoalesce(left)

IFVOID: Final[_IfVoidInfix] = ifvoid
"""
#### Aliases: `ifvoid`
----
    \
`IFVOID` is a `Special Operator [1.5]` that merges the behavior of `ifndef` and `ifnone`
Special Operators, coalescing both `None`-assigned resources and `Undefined` resources.
- Example:

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
...
"""
