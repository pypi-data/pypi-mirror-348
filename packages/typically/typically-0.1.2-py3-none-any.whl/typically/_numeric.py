# TODO | impl: https://en.wikipedia.org/wiki/List_of_types_of_numbers

from __future__ import annotations
import builtins
import typing
from typing import Generic, TypeVar, Union
from typing_extensions import Self
from ._guard import require
from ._typeshed import ConvertibleToInt, ConvertibleToFloat


class whole(int):
    def __new__(cls, x: ConvertibleToWhole, /) -> Self:
        require.ge(x, 0, "Whole numbers must be greater than or equal to 0.")
        return int.__new__(cls, x)


ConvertibleToWhole = ConvertibleToInt | whole

numeric = Union[
    int,
    float,
    # real,
    # +numpy types
    # +decimal, fraction, etc
]
NT = TypeVar("NT", bound=numeric)


class positive(Generic[NT]):
    # __value: N
    # __type: type[N]
    # def __new__(cls, value: N) -> pos[N]:
    #     return type(value).__new__(type(value), value)
    def __init__(self, value: NT) -> None:
        require.gt(value, 0)
        self.__value = value
        self.__type = type(value)
        raise NotImplementedError("TODO")

    @property
    def type(self) -> type[NT]:
        return self.__type

    @property
    def value(self) -> NT:
        return self.__value


class negative(Generic[NT]): ...


class ordinal: ...


# natural starts at 0, or 1, dependending on what branch of math one is operating in it seems
# ref: https://en.wikipedia.org/wiki/Natural_number
# class natural(int): ...


class cardinal: ...


class nominal: ...
