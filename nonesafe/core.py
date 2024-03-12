'''
    ## VoidSafe

    \t `VoidSafe` is a library that brings a `void-safe`, `None-aware` approach to            \
    Python3-written scripts and applications. It provides software developers with resources  \
    to apply `null-safe-like` principles to their codebase, guaranteeing that `safe`          \
    operations can be performed on `potentially unsafe` instances, which helps assuring that  \
    your software will be able to handle many memory-access problems at runtime.

    \t By being entirely `type-hinted`, this library works well when associated with most     \
    `static type checkers`. When combined with a linter that's capable of predicting `unboud` \
    or `undefined` variables, this library helps the developer to identify problems with      \
    their code even before running it.

    \t The inspiration comes from the concept of `Null Safety`, which is adopted by several   \
    programming languages, such as `Dart`, `Kotlin` and `C#`.
    ...

    ------------------------------------------------------------------------------------------
    ## `Special Constants`

    \t A `Special Constant` is used to perform crucial tasks or to represent values that \
    serve for the good usage of this library. What do we expect from a special constant  \
    syntax and semantic highlighting?

    - A `special color` that highlights the instance, making it easy to distinguish it 
    from ordinary instances;
    - A `docstring` that describes what the instance is supposed to perform or represent;
    - A `syntax` that doesn't pollute your code.

    \t Unfortunately, we couldn't find a way to declare, instantiate or decorate this    \
    library's resources in a way that the available linters could provide the            \
    developers with all of what's mentioned above. That said, we opted to provide two    \
    ways of using special constants:

    - `ThisWay` \\
    This is done by `class-decorating` a function with the special constant's type class.
    The result is an `instance` of that class (i.e. the Special Constant).

        - PROS:

            - Some linters will highlight it with the same color used to highlight       \
            `functions` and `methods`. That little hack allows for `distinguishing` it   \
            from ordinary instances;

            - It allows for declaring it with `UpperCamelCase` syntax, which tends to    \
            be "cleaner" than the the second way to use it.
        
        - CONS:

            - Most linters will either:
            
            1. (correctly) Interpret it as an instance but then highlight it as an       \
            `ordinary variable`; 

            2. Misinterpret what role the decorator should perform and then lose the     \
            reference to the instance's docstring, which `wipes the docstring` that      \
            should be shown on the tooltip of the IDE.

    - `THISWAY` \\
    This is done by declaring a Final-typed `constant` and assignining to it the value 
    holded by the instance described above.

        - PROS:

            - By declaring it with `UPPERCASE` syntax, which configures a constant in    \
            Python, most linters will highlight it with the color that's reserved for    \
            constants, which helps `distiguishing` it from other instances;

            - Because it's a regular constant definition, the `docstring` attached to    \
            its assignment will be correctly addressed by most of the available linters. \
            That way, the developer will be able to see a docstring explaining the       \
            Special Constant's usage.
        
        - CONS:

            - Python doesn't support defining an UpperCamelCase declaration as constant. \
            The only constants that can contain this syntax are the built-in ones, such  \
            as `None`, `True`, `False` and a few others. That's is a shame, because      \
            the `Undefined` Special Constant from the present library resides in the     \
            same semantic level as the `None` built-in constant, and it performs a       \
            similar role. This nature of the language results in the following           \
            implications: 
            
            1. It forces you to declare the Special Constant with an `UPPERCASE` syntax;

            2. That form of declaration tends to `pollute` your code as it "screams"     \
            the constant's name, especially if the constant is used frequently.
    ...
'''

from types import NoneType
from typing import Self, final, Any, Callable, Final, Generic, Optional, Type, TypeVar, Union


_T = TypeVar('_T')
'''
    `_T` is the TypeVar used in most of the `Generic` types of this module.
'''


@final
class UndefinedType:
    '''
        \t `UndefinedType` is similar to `types.NoneType` as the first one represents the    \
        type of the `Undefined` Special Constant the same way the second one represents the  \
        type of the `None` built-in constant. 

        - Example:

            ```python
            >>> type(None)
            NoneType

            >>> type(Undefined)
            UndefinedType
            ```
        ...

        -----
        ##### Min. API Version: `0.1.0`
    '''

    def __init__(self, _: Callable[[], None]):
        pass

    def __repr__(self) -> str:
        return "UndefinedType()"
    
    def __str__(self) -> str:
        return "Undefined"


@UndefinedType
def Undefined() -> None:
    # docstrings implemented here will have no use
    pass


UNDEFINED: Final[UndefinedType] = Undefined
'''
    ##### ‣ Aliases: `Undefined`
    ---

    \t `UNDEFINED` is a `Special Constant` that's meant to represent an instance's        \
    resource that hasn't been defined before being accessed, which differs from an        \
    instance's `Optional` resource that has been defined as `None`.

    \t It is usually obtained from an attempt to getting resources from a `potentially    \
    unsafe` instance that is being checked by a `_VoidSafe` wrapper.

    - Example:

        ```python
        >>> from typing import Optional
        >>> from random import random
        >>> from voidsafe import VoidSafe, value
        >>> 
        >>> class EmptyClass:
        ...     def __setattr__(self, name, value):
        ...         object.__setattr__(self, name, value)
        ... 
        >>> emptyInstance = EmptyClass()
        >>> 
        >>> if random() < 0.01:
        ...     emptyInstance.doesntExist = "This probably won't happen"
        ... 
        >>> # tying to access a potentially unsafe resource
        >>> print( VoidSafe(emptyObject).doesntExist )
        _VoidSafe(Undefined)
        >>> 
        >>> # extracting its value
        >>> print( VoidSafe(emptyObject).doesntExist >> value )
        Undefined
        ```
    ...

    -----
    ##### Min. API Version: `0.1.0`
'''


Undefined.__doc__ = UNDEFINED.__doc__


class _CoalesceAction():
    '''
        \t `_CoalesceAction` creates a wrapper around a value that is supposed to be \
        assigned to a resource, but only if it attends the condition of a coalescing \
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
        
        -----
        ##### Min. API Version: `0.1.0`
    '''

    __slots__ = ('_content', '_checkObjects')

    def __init__(self, content: Any, checkObjects: list[Union[NoneType, UndefinedType]]):
        self._content = content
        self._checkObjects = checkObjects


# Those are just meant to be used to address _VoidSafe's _bond tuple
_PARENT: Final[int] = 0
_CHILD: Final[int] = 1


class _VoidSafeTrailing():
    '''
        \t `_VoidSafeTrailing` is a wrapper around a chain of resource accesses starting from a   \
        `VoidSafe(foo)` call. 
        
        - Example:

            ```python
            from voidsafe import VoidSafe

            # ---------  From here on, everything is wrapped into a '_VoidSafeTrailing'
            # ---------  v
            VoidSafe(foo).attribute['item'].call()
            ```
        ...
        
        -----
        ##### Min. API Version: `0.1.0`
    '''

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


class _VoidSafeLeading():
    '''
        \t `_VoidSafeLeading` is a proxy that grabs the `potentially unsafe instance` being       \
        checked by a `VoidSafe(foo)` call (i.e. The root element from a `VoidSafe` operation).

        \t It is responsible for addressing to the `_VoidSafeTrailing` wrapper any operation that \
        follows.

        \t This entity had to be created apart from `_VoidSafeTrailing` because at the time it is \
        called, there is no resource being accessed from the checked instance. That means that    \
        there is no chance that the protected value is `Undefined` at runtime, so the operations  \
        with `ifndef` coalescing `Infix` souldn't be allowed with `_VoidSafeLeading`-protected    \
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
        
        -----
        ##### Min. API Version: `0.1.0`
    '''

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


class _VoidSafeInitiator(Generic[_T]):
    '''
        \t `_VoidSafeInitiator` receives the instance that will be checked and passes it along to \
        the `_VoidSafeLeading` wrapper.

        \t It is also responsible for "tricking" the linter into interpreting the instance passed \
        to the `check` parameter of its `__call__` method as an instance of the same type passed  \
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
        
        -----
        ##### Min. API Version: `0.1.0`
    '''

    def __call__(self, check: Optional[_T]) -> Union[_VoidSafeLeading, _T]:
        return _VoidSafeLeading(check)


class _VoidSafeInfix(_VoidSafeInitiator):
    '''
        \t `_VoidSafeInfix` is a class that is used as a decorator for the `VoidSafe` function,   \
        resulting on an `instance` that will be further called the `VoidSafe` Special Constant.

        \t It also works as a proxy, allowing you to use its `__getitem__` to receive a type and  \
        pass it along to the `_VoidSafeInitiator`.
        ...
        
        -----
        ##### Min. API Version: `0.1.0`
    '''

    def __init__(self, _: Callable[[], None]):
        pass
    
    def __getitem__(self, _: Type[_T]) -> _VoidSafeInitiator[_T]:
        return _VoidSafeInitiator[_T]()


@_VoidSafeInfix
def VoidSafe() -> None:
    # docstrings implemented here will have no use
    pass


VOIDSAFE: Final[_VoidSafeInfix] = VoidSafe
'''
    ##### ‣ Aliases: `VoidSafe`
    ---

    ### ‣ VOIDSAFE

    \t `VOIDSAFE` is a `Special Constant` that acts as a wrapper protecting `potentially \
    unsafe instances` from having their `potentially unsafe resources` accessed.
    ...

    #### ‣ Potentially Unsafe Instances:

    \t `Potentially unsafe instances` are those that might be keeping a value that is    \
    not expected for a certain operation (like getting `None` when you expect a `str`).
    - Example:

        ```python
        >>> from typing import Optional
        >>> from random import random
        >>> 
        >>> unsafeStr: Optional[str] = None
        >>> 
        >>> if random() < 0.01:
        ...     unsafeStr = "This probably won't happen"
        ...
        >>> # 'unsafeStr' holds 'None' as its value
        >>> print( unsafeStr.upper() )
        AttributeError: 'NoneType' object has no attribute 'upper'
        ```
    ...

    #### ‣ Potentially Unsafe Resources

    \t `Potentially unsafe resources` of an instance refers to the instance's            \
    `.attributes`, `[items]` and `calls()` that hold `None` as their value OR the ones   \
    that haven't been `defined` at the moment they are being accessed.
    - Example:

        ```python
        >>> from typing import Optional
        >>> from random import random
        >>> 
        >>> class EmptyClass:
        ...     def __setattr__(self, name, value):
        ...         object.__setattr__(self, name, value)
        ... 
        >>> emptyInstance = EmptyClass()
        >>> 
        >>> if random() < 0.01:
        ...     emptyInstance.unsafeStr = "This probably won't happen"
        ... 
        >>> # 'unsafeStr' hasn't been defined for 'emptyInstance'
        >>> print( emptyInstance.unsafeStr )
        AttributeError: 'EmptyClass' object has no attribute 'unsafeStr'
        ```
    ...

    \t Usually, you can find if an instance/resource is potentially unsafe by checking   \
    if their values are into the `VOID` Special Constant provided by the present library.\
    Type `'VOID'` to see its usage.
    ...
    
    -----
    ##### Min. API Version: `0.1.0`
'''


class _ValueInfix():
    '''
        `_ValueInfix` is a class that is used as a decorator for the `value` function, resulting  \
        on an `instance` that will be further called the `VALUE` Special Constant.
        ...
        
        -----
        ##### Min. API Version: `0.1.0`
    '''
    
    _func: Callable[[Any], Any] = lambda _: _


    def __init__(self, func: Callable[[Any], Any]):
        self._func = func
        
    
    # other >> self
    def __rrshift__(self, other: Any) -> Any:
        return self._func(other)


@_ValueInfix
def value(other: Any) -> Any:
    # docstrings implemented here will have no use

    if type(other) is _VoidSafeTrailing:
        return other._bond[_CHILD]
    if type(other) is _VoidSafeLeading:
        return other._check
    return other


VALUE: Final[_ValueInfix] = value
'''
    ##### ‣ Aliases: `value`
    ----

    \t `VALUE` is a `Special Constant` that allows you to use a `VoidSafe` chain of           \
    operations with the `>>` operator followed by `value`. This works as a getter that        \
    extracts the value that is being kept by `VoidSafe` or any of its subproducts.
    - Example:

        ```python
        >>> from typing import Optional
        >>> from voidsafe import VoidSafe, value
        >>> 
        >>> unsafeStr: Optional[str] = "content"
        >>> print( VoidSafe(unsafeStr).upper() >> value )
        CONTENT
        ```
    ...
    
    -----
    ##### Min. API Version: `0.1.0`
'''


class _VoidInfix:
    '''
        \t `_VoidInfix` is a class that is used as a decorator for the `Void` function, resulting \
        on an `instance` that will be further called the `VOID` Special Constant.
        ...
        
        -----
        ##### Min. API Version: `0.1.0`
    '''
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


@_VoidInfix
def Void() -> list[Union[NoneType, UndefinedType]]:
    # docstrings implemented here will have no use
    return [None, Undefined]


VOID: Final[_VoidInfix] = Void
'''
    ##### ‣ Aliases: `value`
    ----

    \t `VOID` is a `Special Constant` that keeps a list containing both `None` built-in  \
    constant and `UNDEFINED` Special Constant.

    \t It can be used to find out if a resource is either set as `None` or rather never  \
    been set (i.e. `UNDEFINED`).
    - Example:

        ```python
        >>> from voidsafe import VoidSafe, Void, value
        >>> 
        >>> testDict: dict[str, Any] = {}
        >>> 
        >>> testDict['none'] = None
        >>> testDict['filled'] = 'filled'
        >>> 
        >>> # Here's what happens when you try to access a resource
        >>> # that has never been defined for an instance using 'VoidSafe'
        >>> VoidSafe(testDict)['undefined'] >> value
        Undefined
        >>> 
        >>> # Now, we'll check their relationship to 'Void'
        >>> 
        >>> testDict['none'] in Void
        True
        >>> testDict['filled'] in Void
        False
        >>> VoidSafe(testDict)['undefined'] in Void
        True
        ```
    ...
    
    -----
    ##### Min. API Version: `0.1.0`
'''


VoidTypes: Final[tuple[Type, Type]] = (NoneType, UndefinedType)
'''
    \t `VoidTypes` is a Final list that contains both `NoneType` and `UndefinedType` types.   \
    These are the types used to instantiate a `None` built-in constant and an `UNDEFINED`     \
    Special Constant.
    ...
    
    -----
    ##### Min. API Version: `0.1.0`
'''


_LeftType = TypeVar("_LeftType", Any, Any)
'''
    `_LeftType` is used to represent an element positioned to the left of a coalescing
    `Infix`.
    ...
    
    -----
    ##### Min. API Version: `0.1.0`
'''

class _Coalesce(Generic[_LeftType]):
    '''
        \t `_Coalesce` is the base class of a group of coalescing proxies that sould be           \
        instantiated by a coalescing `Infix`.

        \t It receives an element that's positioned at its left and provides the `>>` operator,   \
        allowing to perform coalescing operations. That is done by returning the element at the   \
        right of `>>` if the attribute `_checkObjects` contains the element at the left.
        ...
        
        -----
        ##### Min. API Version: `0.1.0`
    '''

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
    _checkTypes: Final[list[UndefinedType]] = [Undefined]


class _NoneCoalesce(_Coalesce[Any]):
    _checkTypes: Final[list[NoneType]] = [None]


class _VoidCoalesce(_Coalesce[Any]):
    _checkTypes: Final[list[Union[NoneType, UndefinedType]]] = Void._list


_CoalesceType = TypeVar(
    "_CoalesceType", 
    _NoneCoalesce, 
    _UndefinedCoalesce, 
    _VoidCoalesce
)

class _IfNdefInfix(object):
    __slots__ = ('_func')

    def __init__(self, func: Callable[[_VoidSafeTrailing], _UndefinedCoalesce]):
        self._func: Callable[[_VoidSafeTrailing], _UndefinedCoalesce] = func
    
    # other << self
    def __rlshift__(self, left: _VoidSafeTrailing) -> _UndefinedCoalesce:
        return self._func(left)
    
    # self << other
    def __lshift__(self, right: Any) -> _CoalesceAction:
        return _CoalesceAction(right, [Undefined])

class _CoalesceInfix(Generic[_CoalesceType]):
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

_IfNoneInfix = _CoalesceInfix[_NoneCoalesce]
_IfVoidInfix = _CoalesceInfix[_VoidCoalesce]


@_IfNdefInfix
def ifndef(left: _VoidSafeTrailing) -> _UndefinedCoalesce:
    # docstrings implemented here will have no use
    return _UndefinedCoalesce(left)

IFNDEF: Final[_IfNdefInfix] = ifndef

@_IfNoneInfix
def ifnone(left: Any) -> _NoneCoalesce:
    # docstrings implemented here will have no use
    return _NoneCoalesce(left)

IFNONE: Final[_IfNoneInfix] = ifnone

@_IfVoidInfix
def ifvoid(left: Any) -> _VoidCoalesce:
    # docstrings implemented here will have no use
    return _VoidCoalesce(left)

IFVOID: Final[_IfVoidInfix] = ifvoid











