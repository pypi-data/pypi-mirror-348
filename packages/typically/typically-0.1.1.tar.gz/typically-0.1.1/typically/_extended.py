from __future__ import annotations
from typing import Iterable, SupportsIndex, overload
from typing_extensions import LiteralString
from typically import literal


class estr(str):

    # @property
    # def encoding(self) -> literal.CharacterEncoding: ...

    def isuuid(self, version: literal.UUIDVersion) -> bool: ...

    # def tocase(self, casing: ...): ...

    def dedent(self) -> estr: ...
    def escape(self) -> estr: ...
    def apply(self): ...

    # TODO: regex utils

    @overload
    def replace(
        self: LiteralString,
        old: LiteralString,
        new: LiteralString,
        /,
        count: SupportsIndex = -1,
    ) -> LiteralString: ...
    @overload
    def replace(
        self,
        old: str,
        new: str,
        /,
        count: SupportsIndex = -1,
    ) -> str: ...  # type: ignore[misc]
    @overload
    def replace(self, mapping: dict[str, str]) -> str: ...  # TODO
    def replace(self, *args, **kwargs) -> str:  # type: ignore
        return super().replace(*args, **kwargs)

    def fuzzysearch(
        self, query: str, window: int | None = None, n: int = 1
    ) -> _fuzzy_search_result | list[_fuzzy_search_result]: ...

    @overload
    def cjoin(
        self: LiteralString, iterable: Iterable[LiteralString], /
    ) -> estr: ...
    @overload
    def cjoin(self, iterable: Iterable[str], /) -> estr: ...  # type: ignore[misc]
    def cjoin(
        self: LiteralString | str | estr,
        iterable: Iterable[str] | Iterable[LiteralString],
        /,
        exclude_none: bool = True,
    ) -> estr: ...


# class _estr_slice(str): ...
class _fuzzy_search_result(estr): ...
