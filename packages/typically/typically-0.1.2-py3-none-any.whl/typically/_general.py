from __future__ import annotations
import re
import inspect
import importlib
from decimal import Decimal, DecimalTuple, Context
from types import ModuleType as module
from typing import (
    Any,
    Generic,
    TypeVar,
    overload,
    get_args,
    TypeVar,
    Self,
    ClassVar,
    cast,
    Callable,
)
from typing_extensions import LiteralString
from pydantic import ValidatorFunctionWrapHandler
from pydantic_core import core_schema, PydanticSerializationUnexpectedValue
from pydantic.annotated_handlers import GetCoreSchemaHandler

# TODO: split into submodules once type interdependency graph is clearer
# TODO: may be useful to split numeric into scalar/vector modules
# TODO: reimplement fractions.Fraction + reciprocal prop

T = TypeVar("T")
P = TypeVar("P")
CT = TypeVar("CT", covariant=True)


ordered = list[T] | tuple[T, ...]


class pair(tuple[T, T]):
    @classmethod
    def __new_args__(cls, *args) -> pair[T]:
        match len(args):
            case 1:
                arg = args[0]
                if len(arg) == 2:
                    return tuple.__new__(cls, arg)
                else:
                    raise TypeError(
                        f"'{cls.__name__}' expects 2 args or an iterable of length 2, but received length {len(arg)}: '{arg}'",
                    )
            case 2:
                return tuple.__new__(cls, args)
            case _:
                raise TypeError(args)

    @classmethod
    def __new_kwargs__(cls, **kwargs) -> pair[T]:
        # FIXME
        keys = set(kwargs.keys())
        if keys == {"value"}:
            return cls.__new_args__(*kwargs["value"])
        elif keys == {"a", "b"}:
            return cls.__new_args__(kwargs["a"], kwargs["b"])
        else:
            raise TypeError(f"Invalid keyword arguments: {kwargs}")

    @overload
    def __new__(cls, value: pair[T] | tuple[T, T] | list[T]) -> pair[T]: ...
    @overload
    def __new__(cls, a: T, b: T) -> pair[T]: ...
    def __new__(cls, *args, **kwargs) -> pair[T]:
        if len(args):
            return cls.__new_args__(*args)
        elif len(kwargs):
            return cls.__new_kwargs__(**kwargs)
        else:
            raise TypeError(
                f"{cls.__name__} expects a pair of two items, or an iterable of length 2",
                args,
                kwargs,
            )

    def __hash__(self) -> int:
        return hash((self.a, self.b))

    @property
    def a(self) -> T:
        return self[0]

    @property
    def b(self) -> T:
        return self[1]

    @classmethod
    def __serialize__(
        cls,
        value: pair[T],
        info: core_schema.SerializationInfo,
    ) -> tuple[T, ...] | Self:
        if not isinstance(value, cls):
            raise PydanticSerializationUnexpectedValue(
                f"Expected `{cls}` but got `{type(value)}` with value `'{value}'` - serialized value may not be as expected."
            )
        if info.mode == "json":
            return tuple(value)
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[pair[T]],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        def wrapper(value: Any, wrap_handler: ValidatorFunctionWrapHandler):
            generic_param_types: tuple[type, ...] = get_args(source)
            match len(generic_param_types):
                case 0:
                    return source.__new__(source, value)
                case 1:
                    generic_type: type = generic_param_types[0]
                    new_value = list()
                    for item in value:
                        if isinstance(item, generic_type):
                            new_value.append(item)
                        else:
                            try:
                                new_value.append(generic_type(item))
                            except ValueError:
                                raise TypeError(
                                    f"Could not coerce value '{item}' to type '{generic_type.__name__}'"
                                )
                    return source.__new__(source, value.__class__(new_value))
                case _:
                    raise TypeError(
                        f"'pair' can only have one generic type, but has: '{generic_param_types}'"
                    )

        return core_schema.no_info_wrap_validator_function(
            wrapper,
            schema=core_schema.tuple_schema(
                [core_schema.any_schema(), core_schema.any_schema()],
                variadic_item_index=1,
                min_length=2,
                max_length=2,
                strict=True,
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls.__serialize__, info_arg=True, when_used="always"
            ),
        )


# TODO: real needs pydantic schema impl.
# TODO: reimplement in rust
# TODO: add precision/precise number of significant figures
# TODO: optimize, lot of bloat
# ? real, precise, decimal
class decimal(Decimal):
    """
    Same as decimal but with greater interoperability across other numeric types.

    NOTE: `float` to `str` cast
        Instantiating `Decimal(3.14)` yields the decimal:

        `Decimal('3.140000000000000124344978758017532527446746826171875')`

        This is probably because even though `Decimal` has arbitrary precision,
        the float passed in doesn't. As such input floats are converted to strings
        before being passed to the constructor.

    NOTE: Infinity
        ```python
        x = Decimal(0) / Decimal('inf')
        ```

        In the code above, `x == Decimal('0E-1000026')`.
        Accordingly infinity has just been blocked from being a valid value.
        May re-evaluate later.
    """

    # TODO: test with numpy/sympy types, make sure this works w/ array, sparse matrices, etc

    # * core methods

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__str__()})"

    def __hash__(self) -> int:
        return super().__hash__()

    def __copy__(self) -> decimal:
        return decimal(super().__copy__())

    def __deepcopy__(self, memo: Any) -> decimal:
        return decimal(super().__deepcopy__(memo))

    # * constructors

    def __new__(
        cls,
        value: Realish,
        context: Context | None = None,
    ) -> decimal:
        if isinstance(value, float):
            value = str(value)
        lstr = str(value).lower()
        if "inf" in lstr:
            raise TypeError(f"'{cls.__name__}' does not allow infinite value")
        if "nan" in lstr:
            raise TypeError(f"'{cls.__name__}' does not allow nan values")
        return Decimal.__new__(cls, value=value, context=context)

    @classmethod
    def from_numeric(cls, value: Numeric) -> decimal:
        if isinstance(value, str):
            raise TypeError(f"{type(value)}: '{value}'")
        return cls(value)

    @classmethod
    def from_float(cls, f: float) -> Self:
        return cls(str(f))

    # * type conversion

    def __bool__(self) -> bool:
        return super().__bool__()

    def __float__(self) -> float:
        return super().__float__()

    def __int__(self) -> int:
        return super().__int__()

    def __complex__(self) -> complex:
        return super().__complex__()

    @property
    def decimal(self) -> Decimal:
        return Decimal(self)

    def as_integer_ratio(
        self,
    ) -> tuple[int, int]: ...  # TODO: replace with ratio / pair[int]

    # * formatting

    def to_eng_string(self, context: Context | None = None) -> str:
        return super().to_eng_string(context=context)

    def __format__(
        self, specifier: str, context: Context | None = None
    ) -> str:
        return super().__format__(specifier, context)

    # * comparison

    def __eq__(self, value: object) -> bool:  # type: ignore
        if not isinstance(value, Numeric):
            return False
        return super().__eq__(decimal.from_numeric(value))

    def __ne__(self, value: object) -> bool:  # type: ignore
        if not isinstance(value, Numeric):
            return True
        return super().__ne__(decimal.from_numeric(value))

    def __ge__(self, value: Numeric) -> bool:  # type: ignore
        return super().__ge__(decimal.from_numeric(value))

    def __gt__(self, value: Numeric) -> bool:  # type: ignore
        return super().__gt__(decimal.from_numeric(value))

    def __le__(self, value: Numeric) -> bool:  # type: ignore
        return super().__le__(decimal.from_numeric(value))

    def __lt__(self, value: Numeric) -> bool:  # type: ignore
        return super().__lt__(decimal.from_numeric(value))

    # * sign

    def __abs__(self) -> decimal:
        return decimal(super().__abs__())

    def __neg__(self) -> decimal:
        return decimal(super().__neg__())

    def __pos__(self) -> decimal:
        return decimal(super().__pos__())

    # * addition

    def __add__(self, value: Numeric) -> decimal:
        return decimal(super().__add__(decimal.from_numeric(value)))

    def __radd__(self, value: Numeric) -> decimal:
        return decimal(super().__radd__(decimal.from_numeric(value)))

    # * subtraction

    def __sub__(self, value: Numeric) -> decimal:
        return decimal(super().__sub__(decimal.from_numeric(value)))

    def __rsub__(self, value: Numeric) -> decimal:
        return decimal(super().__rsub__(decimal.from_numeric(value)))

    # * multiplication

    def __mul__(self, value: Numeric) -> decimal:
        return decimal(super().__mul__(decimal.from_numeric(value)))

    def __rmul__(self, value: Numeric) -> decimal:
        return decimal(super().__rmul__(decimal.from_numeric(value)))

    # * division

    def __truediv__(self, value: Numeric) -> decimal:
        return decimal(super().__truediv__(decimal.from_numeric(value)))

    def __rtruediv__(self, value: Numeric) -> decimal:
        return decimal(super().__rtruediv__(decimal.from_numeric(value)))

    def __floordiv__(self, value: Numeric) -> decimal:
        return decimal(super().__floordiv__(decimal.from_numeric(value)))

    def __rfloordiv__(self, value: Numeric) -> decimal:
        return decimal(super().__rfloordiv__(decimal.from_numeric(value)))

    # * modulo

    def __mod__(self, value: Numeric) -> decimal:
        return decimal(super().__mod__(decimal.from_numeric(value)))

    def __rmod__(self, value: Numeric) -> decimal:
        return decimal(super().__rmod__(decimal.from_numeric(value)))

    def __divmod__(self, value: Numeric) -> tuple[decimal, decimal]:
        dt = super().__divmod__(decimal.from_numeric(value))
        return (decimal(dt[0]), decimal(dt[1]))

    def __rdivmod__(self, value: Numeric) -> tuple[Decimal, Decimal]:
        raise NotImplementedError()

    # * exponentation / logarithms

    def __pow__(self, value: Numeric, mod: Numeric | None = None) -> decimal:
        mod = decimal(mod).decimal if mod else None
        return decimal(
            super().__pow__(decimal.from_numeric(value).decimal, mod)
        )

    def __rpow__(self, value: Numeric, mod: Context | None = None) -> decimal:
        return decimal(
            super().__rpow__(decimal.from_numeric(value).decimal, mod)
        )

    def exp(self, context: Context | None = None) -> decimal:
        return decimal(super().exp(context))

    def sqrt(self, context: Context | None = None) -> decimal:
        return decimal(super().sqrt(context))

    def ln(self, context: Context | None = None) -> decimal:
        return decimal(super().ln(context))

    def log10(self, context: Context | None = None) -> decimal:
        return decimal(super().log10(context))

    def logb(self, context: Context | None = None) -> decimal:
        return decimal(super().logb(context))

    # * rounding

    def __round__(self, ndigits: int = 0) -> decimal:  # type: ignore
        return decimal(super().__round__(ndigits))

    def __floor__(self) -> int:
        return super().__floor__()

    def __ceil__(self) -> int:
        return super().__ceil__()

    # * stats
    def max(self, other: Numeric, context: Context | None = None) -> decimal:
        return decimal(super().max(decimal(other).decimal, context))

    def min(self, other: Numeric, context: Context | None = None) -> decimal:
        return decimal(super().min(decimal(other).decimal, context))

    # TODO
    @property
    def real(self) -> Self: ...
    @property
    def imag(self) -> decimal: ...
    def __trunc__(self) -> int: ...
    def conjugate(self) -> decimal: ...
    def remainder_near(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def normalize(self, context: Context | None = None) -> decimal: ...
    def fma(
        self, other: Numeric, third: Numeric, context: Context | None = None
    ) -> decimal: ...
    def quantize(
        self,
        exp: Numeric,
        rounding: str | None = None,
        context: Context | None = None,
    ) -> decimal: ...
    def same_quantum(
        self, other: Numeric, context: Context | None = None
    ) -> bool: ...
    def to_integral_exact(
        self, rounding: str | None = None, context: Context | None = None
    ) -> decimal: ...
    def to_integral_value(
        self, rounding: str | None = None, context: Context | None = None
    ) -> decimal: ...
    def to_integral(
        self, rounding: str | None = None, context: Context | None = None
    ) -> decimal: ...
    def adjusted(self) -> int: ...
    def canonical(self) -> decimal: ...
    def compare_signal(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def compare_total(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def compare_total_mag(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def copy_abs(self) -> decimal: ...
    def copy_negate(self) -> decimal: ...
    def copy_sign(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def is_canonical(self) -> bool: ...
    def is_finite(self) -> bool: ...
    def is_infinite(self) -> bool: ...
    def is_nan(self) -> bool: ...
    def is_normal(self, context: Context | None = None) -> bool: ...
    def is_qnan(self) -> bool: ...
    def is_signed(self) -> bool: ...
    def is_snan(self) -> bool: ...
    def is_subnormal(self, context: Context | None = None) -> bool: ...
    def is_zero(self) -> bool: ...
    def logical_and(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def logical_invert(self, context: Context | None = None) -> decimal: ...
    def logical_or(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def logical_xor(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def max_mag(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def min_mag(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def next_minus(self, context: Context | None = None) -> decimal: ...
    def next_plus(self, context: Context | None = None) -> decimal: ...
    def next_toward(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def number_class(self, context: Context | None = None) -> str: ...
    def radix(self) -> decimal: ...
    def rotate(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def scaleb(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def shift(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def __reduce__(self) -> tuple[type[Self], tuple[str]]: ...
    def as_tuple(self) -> DecimalTuple: ...


Numeric = int | float | Decimal | decimal  # | Fraction | Rational
Realish = Numeric | str

N = TypeVar("N", bound=Numeric)

from typing import Generic, TypeVar, Self, Literal
from enum import Enum

U = TypeVar("U", bound=LiteralString)

# U = TypeVar("U")

# # TODO: count of type T with prefix P - Generic[T, P]
# class count(int, Generic[U]):
#     __unit: U
#     __type: type[U]

#     @property
#     def unit(self) -> U:
#         return self.__unit

#     @property
#     def type(self) -> type[U]:
#         if self.__type is str:
#             return Literal[self.__unit] # type: ignore
#         raise
#         # return self.__type

#     def __new__(cls, value: int, unit: U, t: type[U] | None = None) -> count[U]:
#         inst = super(count, cls).__new__(cls, value)
#         inst.__unit = unit
#         inst.__type = t if t else type(unit)
#         return inst

#     def __repr__(self) -> str:
#         # return f"{super().__repr__()} [{self.__type.__name__}:{self.__unit}]"
#         return f"{super().__repr__()} [{self.__unit}]"

#     def __eq__(self, other) -> bool: ...

# U = TypeVar("U", bound=LiteralString)

# class _count(int, Generic[U]):
#     __unit: U

#     def __repr__(self) -> str:
#         return f"{super().__repr__()} [{self.__unit}]"

#     def __iter__(self):
#         for k, v in dict(value=int(self), unit=self.unit).items():
#             yield k, v

#     def __new__(cls, value: int, unit: U) -> count[U]:
#         inst = super(count, cls).__new__(cls, value)
#         inst.__unit = unit
#         return inst

#     @property
#     def unit(self) -> U:
#         return self.__unit

#     @unit.setter
#     def unit(self, u: U) -> None:
#         ...


class even(int): ...


class odd(int): ...


class natural(int): ...


# ? positive, pos
class positive(Generic[N]): ...


# ? negative, neg
class negative(Generic[N]): ...


class ratio(pair[int]): ...


# 2d point default?
class point2(pair[decimal]): ...


# TODO: should be float pair option iff importance(speed) > importance(accuracy)
# class point(pair[real]):
#     """
#     n-dim point
#     """
#     ...


class fpoint(pair[float]): ...


class ndpoint(tuple[decimal, ...]):
    @property
    def dimensions(self) -> positive[int]: ...
