from __future__ import annotations
import warnings
from typing_extensions import SupportsBytes, SupportsIndex
from types import GenericAlias
from typing import (
    Generic,
    Iterable,
    TypeAlias,
    TypeVar,
    Self,
    Literal,
    LiteralString,
    cast,
    get_args,
    Union,
    get_origin,
    Any,
    overload,
)
from pydantic import ValidatorFunctionWrapHandler
from pydantic_core import PydanticSerializationUnexpectedValue
from pydantic_core import core_schema as cs
from pydantic.annotated_handlers import GetCoreSchemaHandler

from ._guard import require, verify, NotEqualError

from ._typeshed import ReadableBuffer
from ._numeric import negative, positive
from ._hidden import LiteralGenericAlias


Nothing = Literal["~"]
NOTHING: Nothing = get_args(Nothing)[0]
# TODO: move to literal module, ensure conformance with mathematical standards
# MathematicalOperation = Literal[
# "addition",
# "subtraction",
# "multiplication",
# "division",
# "exponentation",
# ... etc
# ]
# FIXME: incomplete
MathematicalOperation = Literal["+", "-", "*", "/", "**"]
ComparisonOperation = Literal["==", "!=", ">=", ">", "<=", "<"]
Operation = (
    MathematicalOperation | ComparisonOperation
)  # repl str with comp op

# T = TypeVar("T", bound=LiteralString | Nothing)
T = TypeVar("T", bound=LiteralString)


class DifferentThingsError(NotEqualError, TypeError):
    """Raised when a mathematical operation is run on two different things."""

    def __init__(
        self,
        source: Any,
        target: Any,
        detail: str | None,
        operation: Operation,
        *args: object,
    ) -> None:
        self.operation = operation
        detail = f"The operation '{operation}' cannot be used on counts of different things."
        super().__init__(source, target, detail, *args)


# class AlreadyAThingError(Exception): ...


# class arguments:
#     """Namespace for internal argument normalization functions."""

#     @staticmethod
#     def norm_tuple(): ...


class toolkit:
    @staticmethod
    def validate_same_thing(a: count, b: count, operation: Operation) -> None:
        require.eq(
            source=a.__thing__,
            target=b.__thing__,
            raises=DifferentThingsError,
            operation=operation,
        )


# FIXME: using whole seems to be breaking pydantic atm
# class count(whole, Generic[T]):
class count(int, Generic[T]):
    """
    A count `n` of of a `thing` (widgets, bytes, cities, etc).
    Used in contexts where you want to count a thing and have
    the count for that thing be differentiable from another
    thing being counted. Only for whole numbers, no decimals/floats.

    ### Overview

    ```python
    ```

    ### Details

    What is the purpose? Take this example:

    ```python
    import pydantic

    class LLM(pydantic.BaseModel):
        size_gigabytes: int
        num_parameters: int
        quantization_bits: int

    llm = LLM(size_gigabytes=10, num_parameters=10, quantization_bits=10)

    assert llm.size_gigabytes == llm.num_parameters, "This will pass but shouldn't."
    ```

    The assertion above shouldn't pass because gigabytes are not parameters,
    plus, the information about the fact that the size in gigabytes and
    quantization in bits is only captured in the variable/attribute name.

    The `count` type solves the first issue and partially solves the second
    issue as follows:

    ```python
    import pydantic
    from typing import Literal

    class LLM(pydantic.BaseModel):
        size: count[Literal["gigabyte"]]
        parameters: count[Literal["parameter"]]
        quantization: count[Literal["bit"]]

    llm = LLM(
        size=count(10, "gigabyte"),
        parameters=count((10, "parameter")),
        quantization=count(value=10, thing="bit")),
    )

    assert llm.size != llm.parameters, "This will pass, and should."

    # Note that if you do something like:

    llm = LLM(
        size=count(10, "byte"),
        parameters=count((10, "params")),
        quantization=count(n=10, thing="bits")),
    )

    # your static type checker should catch it, and
    # additionally pydantic will raise an exception
    ```

    Additionally, if you get tired of passing in literals,
    it's straightforward to define your own count types of
    arbitrary things:

    ```python
    TODO
    ```

    If you want to do more detailed unit/quantity
    modeling and conversion, check out: [pint](https://github.com/hgrecco/pint)

    """

    __defined__: bool = False
    # __thing__: T | Nothing = "~"
    __thing__: T

    # :common
    def __str__(self) -> str:
        return f"{super().__str__()} [{self.thing}]"

    def __repr__(self) -> str:
        return f"{super().__repr__()} [{self.thing}]"

    # :constructor
    # ! if the __thing__ is already not none, then passing a new thing should raise an error

    @overload
    def __new__(cls, n: int) -> count[T]:
        """_summary_

        Args:
            n (int): _description_

        Returns:
            count[Nothing]: _description_
        """
        ...

    @overload
    def __new__(cls, n: int, thing: T) -> count[T]:
        """_summary_

        Args:
            n (int): _description_
            thing (T): _description_

        Returns:
            count[T]: _description_
        """
        ...

    @overload
    def __new__(cls, value: ConvertibleToCount) -> count[T]:
        """_summary_

        Args:
            value (ConvertibleToCount): _description_

        Returns:
            count[T]: _description_
        """
        ...

    def __new__(cls, *args, **kwargs) -> count[T]:

        match (len(args), len(kwargs)):
            case (1, 0):
                n = verify.isinstance(args[0], int)
                thing = NOTHING
            case (2, 0):  # count(10, "bit")
                n = verify.isinstance(args[0], int)
                thing = verify.isinstance(args[1], str)
                require.ne(
                    thing,
                    NOTHING,
                    f"'{NOTHING}' is reserved for the absence of a thing and cannot be used here.",
                )
            case _:
                raise NotImplementedError("TODO")
        require.ge(n, 0)
        inst = int.__new__(cls, n)
        inst.__thing__ = cast(T, thing)
        return inst

    @property
    def n(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return int(self)

    @property
    def thing(self) -> T:
        """_summary_

        Returns:
            T: _description_
        """
        return cast(T, self.__thing__)

    @property
    def value(self) -> tuple[int, T]:
        """_summary_

        Returns:
            tuple[int, T]: _description_
        """
        return (self.n, self.thing)

    @classmethod
    def __serialize__(
        cls,
        value: count[T],
        info: cs.SerializationInfo,
    ) -> tuple[int, T] | Self:
        if not isinstance(value, cls):
            raise PydanticSerializationUnexpectedValue(
                f"Expected `{cls}` but got `{type(value)}` with value "
                f"`'{value}'` - serialized value may not be as expected."
            )
        return cast(tuple[int, T], tuple(value))

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[count[T]],
        handler: GetCoreSchemaHandler,
    ) -> cs.CoreSchema:
        def wrapper(
            # TODO: add int - should only be coerced if source is defined count
            value: ConvertibleToCount,
            wrap_handler: ValidatorFunctionWrapHandler,
        ):
            # * source: count | value: count(10, "gram")
            if source is count:
                return count(value)
                # return source.__new__(source, value)
            else:
                internal = count(value)
                if isinstance(
                    source, GenericAlias
                ):  # > count[Literal["gram"]]
                    if get_origin(source) is count:
                        generic_args = get_args(source)  # >(Literal['gram'],)
                        if len(generic_args) != 1:
                            raise TypeError(source)
                        literal_type = generic_args[0]  # > Literal['gram']
                        if not isinstance(literal_type, LiteralGenericAlias):
                            raise TypeError(source)
                        literal_args = get_args(literal_type)  # > ('gram',)
                        if len(literal_args) != 1:
                            raise TypeError(source)
                        if not isinstance(literal_args[0], str):
                            raise TypeError(source)
                        source_thing = literal_args[0]
                        if internal.thing != source_thing:
                            raise TypeError(
                                f"'{internal.thing}' must be '{source_thing}'"
                            )
                        return count(internal.n, cast(T, source_thing))
                    else:
                        raise TypeError(source)
                elif (source.__base__ is count) and (
                    getattr(source, "__defined__")
                ):
                    require.eq(source.__thing__, internal.__thing__)  # type: ignore
                    return source.__new__(source, internal.n)
                else:
                    if (value.__class__.__base__ is count) and (
                        getattr(value.__class__, "__defined__")
                    ):
                        # * handle custom unit
                        # return count(value_n, value_thing)
                        pass
                    else:
                        pass
                        # return count(value_n, value_thing)
                raise NotImplementedError()

        return cs.no_info_wrap_validator_function(
            wrapper,
            schema=cs.tuple_schema(
                [
                    cs.int_schema(
                        ge=0,
                        strict=True,
                    ),
                    cs.str_schema(
                        min_length=0,
                        max_length=1024,
                        strict=True,
                    ),
                ],
                # variadic_item_index=1,
                min_length=2,
                max_length=2,
                strict=True,
            ),
            serialization=cs.plain_serializer_function_ser_schema(
                cls.__serialize__, info_arg=True, when_used="always"
            ),
        )

    @staticmethod
    # def define(thing: T) -> type[count[T]]:
    def define(thing: T):
        """
        Define a new type for counting something.
        """
        # TODO: move main code to sep func

        class count_of_thing(count, Generic[T]):  # type: ignore
            """
            A custom defined count of a thing.
            """

            __defined__ = True
            __thing__: T = thing

            # def __new__(cls, n: int) -> count[T]:
            def __new__(cls, n: int) -> count_of_thing:
                return super().__new__(cls, n, thing)  # type: ignore

        return type("count_of_thing", (count_of_thing,), {})
        # return type(f"count_of_{thing}", (count_of_thing,), {})

    # :operation

    def __add__(self, value: int | count[T], /) -> count[T]:
        if isinstance(value, count):
            toolkit.validate_same_thing(self, value, "+")
            nsum = super().__add__(value.n)
            inst = self.__class__(nsum)
            inst.__thing__ = self.thing
            return inst
        elif isinstance(value, int):
            warnings.warn("count:int operations may be deprecated")
            nsum = super().__add__(value)
            inst = self.__class__(nsum)
            inst.__thing__ = self.thing
            return inst
        else:
            raise TypeError(value)

    def __radd__(self, value: int | count[T], /) -> count[T]:
        return self.__add__(value)

    def __iadd__(self, value: int | count[T], /) -> count[T]:
        return self.__add__(value)

    # TODO: clean up redundant code for unary/binary ops
    def __sub__(self, value: int | count[T], /) -> count[T]:
        if isinstance(value, count):
            toolkit.validate_same_thing(self, value, "-")
            nsum = super().__sub__(value.n)
            inst = self.__class__(nsum)
            inst.__thing__ = self.thing
            return inst
        elif isinstance(value, int):
            warnings.warn("count:int operations may be deprecated")
            nsum = super().__sub__(value)
            inst = self.__class__(nsum)
            inst.__thing__ = self.thing
            return inst
        else:
            raise TypeError(value)

    def __rsub__(self, value: int | count[T], /) -> count[T]:
        return self.__sub__(value)

    def __isub__(self, value: int | count[T], /) -> count[T]:
        return self.__sub__(value)

    def __mul__(self, value: int, /) -> count[T]:  # type: ignore
        """
        *Note that the whole number enforcement is currently broken.*
        Counts are whole numbers, and can only be multiplied by whole numbers.
        Technically, if you have something like:

        ```python
        a = count(10, "meter")
        b = count(10, "meter")
        a * b
        ```

        That would equal something like 'meters squared', but this type
        doesn't do unit conversion, and is for counting arbitrary things
        (meters, widgets, thoughts, colors, notes, caffeine pills, etc);
        because `10 [thoughts] * 10 [thoughts] != 100 [thoughts^2]` (this
        is nonsensical), multiplication only works
        """
        require.isinstance(value, int)
        nsum = super().__mul__(value)
        inst = self.__class__(nsum)
        inst.__thing__ = self.thing
        return inst

    def __rmul__(self, value: int, /) -> count[T]:  # type: ignore
        return self.__mul__(value)

    def __imul__(self, value: int, /) -> count[T]:
        return self.__mul__(value)

    # NOTE: should maybe use __or__ and explicitly return ratio type
    def __truediv__(self, value: count[T], /) -> float:  # type: ignore
        """
        Counts can only be divided by other counts of the same thing,
        which cancels out the count and returns a float that represents
        the ratio between the counts.

        This decision was made so that count values are enforced as whole numbers;
        division is likely to result in non-integer numbers, so while
        technically `10 [gram] / 5 == 2 [gram]` and `10 [g] / 3 == 3.33 [g]`,
        allowing integers would also add cases like `3 [colors] / 2 == 1.5 [colors]`;
        if you had `red, green, blue` and you divided it by `red, green`,
        would this result in `red, gre`? Maybe `red, yellow`? Doesn't make sense.

        """
        require.isinstance(value, count)
        toolkit.validate_same_thing(self, value, "/")
        return self.n / value.n

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, count):
            return False
        return (self.thing == value.thing) and (self.n == value.n)

    def __ne__(self, value: object, /) -> bool:
        return not self.__eq__(value)

    # TODO: can consolidate this code with operator, repetitive
    def __lt__(self, value: count[T], /) -> bool:  # type: ignore
        toolkit.validate_same_thing(self, value, "<")
        return self.n < value.n

    def __le__(self, value: count[T], /) -> bool:  # type: ignore
        """"""
        toolkit.validate_same_thing(self, value, "<=")
        return self.n <= value.n

    def __gt__(self, value: count[T], /) -> bool:  # type: ignore
        """"""
        toolkit.validate_same_thing(self, value, ">")
        return self.n > value.n

    def __ge__(self, value: count[T], /) -> bool:  # type: ignore
        """"""
        toolkit.validate_same_thing(self, value, ">=")
        return self.n >= value.n

    def __float__(self) -> float:
        return super().__float__()

    def __int__(self) -> int:
        return super().__int__()

    def __hash__(self) -> int:
        return hash((self.n, self.thing))

    def __bool__(self) -> bool:
        warnings.warn("unstable")  # repl with decorator
        return self.n != 0

    def __iter__(self):
        for x in (self.n, self.thing):
            yield x

    # TODO.backlog

    def __abs__(self) -> int: ...
    def as_integer_ratio(self) -> tuple[int, Literal[1]]: ...
    @property
    def real(self) -> int: ...
    @property
    def imag(self) -> Literal[0]: ...
    @property
    def numerator(self) -> int: ...
    @property
    def denominator(self) -> Literal[1]: ...
    def conjugate(self) -> int: ...
    def bit_length(self) -> int: ...
    def bit_count(self) -> int: ...
    def to_bytes(
        self,
        length: SupportsIndex = 1,
        byteorder: Literal["little", "big"] = "big",
        *,
        signed: bool = False,
    ) -> bytes: ...
    @classmethod
    def from_bytes(
        cls,
        bytes: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer,
        byteorder: Literal["little", "big"] = "big",
        *,
        signed: bool = False,
    ) -> Self: ...

    def is_integer(self) -> Literal[True]:
        raise NotImplementedError(
            "subclass of integer, but not technically integer - undetermined"
        )

    # def is_whole(self):
    #     raise NotImplementedError("same issue as with integer")

    def is_count(self) -> Literal[True]:
        return True

    def __floordiv__(self, value: int, /) -> int: ...
    def __mod__(self, value: int, /) -> int: ...
    def __divmod__(self, value: int, /) -> tuple[int, int]: ...
    def __rfloordiv__(self, value: int, /) -> int: ...
    def __rtruediv__(self, value: int, /) -> float: ...
    def __rmod__(self, value: int, /) -> int: ...
    def __rdivmod__(self, value: int, /) -> tuple[int, int]: ...
    @overload
    def __pow__(self, x: Literal[0], /) -> Literal[1]: ...  # type: ignore
    @overload
    def __pow__(self, value: Literal[0], mod: None, /) -> Literal[1]: ...
    @overload
    def __pow__(self, value: positive[int], mod: None = None, /) -> int: ...
    @overload
    def __pow__(self, value: negative[int], mod: None = None, /) -> float: ...
    @overload
    def __pow__(self, value: int, mod: None = None, /) -> Any: ...
    @overload
    def __pow__(self, value: int, mod: int, /) -> int: ...  # type: ignore
    def __rpow__(self, value: int, mod: int | None = None, /) -> Any: ...
    def __and__(self, value: int, /) -> int: ...
    def __or__(self, value: int, /) -> int: ...
    def __xor__(self, value: int, /) -> int: ...
    def __lshift__(self, value: int, /) -> int: ...
    def __rshift__(self, value: int, /) -> int: ...
    def __rand__(self, value: int, /) -> int: ...
    def __ror__(self, value: int, /) -> int: ...
    def __rxor__(self, value: int, /) -> int: ...
    def __rlshift__(self, value: int, /) -> int: ...
    def __rrshift__(self, value: int, /) -> int: ...
    def __neg__(self) -> int: ...
    def __pos__(self) -> int: ...
    def __invert__(self) -> int: ...
    def __trunc__(self) -> int: ...
    def __ceil__(self) -> int: ...
    def __floor__(self) -> int: ...
    def __round__(self, ndigits: SupportsIndex = ..., /) -> int: ...
    def __getnewargs__(self) -> tuple[int]: ...
    def __index__(self) -> int: ...


ConvertibleToCount = Union[
    # int,
    # str,
    count[T],
    # tuple[int],
    tuple[int, T],
    # list[int | T],
]
"""Union of all types parsable to `count`."""

# from typing import Literal as L

# ByteCount: type[count[L["byte"]]] = count[L["byte"]].define("byte")
# BitCount = count[L["bit"]].define("bit")
# FooCount: type[count[L["foo"]]] = count.define("foo")

# def f():
#     return BitCount(10)

# def pylance():
#     # test with literal type alias
#     # gram = count[Literal["gram"]]

#     from pydantic import BaseModel

#     class Test(BaseModel):
#         x: BitCount


