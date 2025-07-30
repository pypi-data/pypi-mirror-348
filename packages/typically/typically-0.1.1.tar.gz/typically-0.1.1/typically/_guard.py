import builtins
from typing import TypeVar, Any

T = TypeVar("T")
V = TypeVar("V")
KT = TypeVar("KT")

collection = set[T] | list[T] | tuple[T, ...]
ordered = list[T] | tuple[T, ...]


def coerce(f): ...


class utils:
    """local utility functions"""

    # TODO: replace/move
    @staticmethod
    def emsg(msg: str, detail: str | None) -> str:
        """concat msg + detail"""
        return msg if msg is None else msg + f". {detail}"


class check:  # ? compare, condition
    """Returns bools"""

    @staticmethod
    def haskeys(value: dict[KT, Any], keys: set[KT]) -> bool: ...


class verify:  # ? verify, validate
    """Returns validated type"""

    @staticmethod
    def isinstance(value: V, expected: type[V]) -> V:
        """

        Args:
            value (object): _description_
            expected (type): _description_

        Raises:
            TypeError: _description_
        """
        # NOTE: clip value to avoid console overflow
        value_str_clip = str(value)
        value_str_clip: str = (
            value_str_clip
            if len(value_str_clip) < 128
            else f"{value_str_clip[:128]}..."
        )
        value_cls_name: str = value.__class__.__qualname__
        exp_cls_name: str = expected.__qualname__
        if not builtins.isinstance(value, expected):
            raise TypeError(
                f"Expected '{exp_cls_name}' but received '{value_cls_name}' with value '{value_str_clip}'"
            )
        return value

    @staticmethod
    def issubclass():
        raise NotImplementedError()


# TODO: have o1 go through and add other extra utils


class IsEqualError(ValueError):
    def __init__(
        self,
        source: Any,
        target: Any,
        detail: str | None = None,
        *args: builtins.object,
    ) -> None:
        self.source = source
        self.target = target
        self.detail = detail
        # msg = utils.emsg(f"'{source}' cannot be equal to '{target}'", detail)
        msg = utils.emsg(f"'{source}' is equal to '{target}'", detail)
        super().__init__(msg, *args)


class NotEqualError(ValueError):
    def __init__(
        self,
        source: Any,
        target: Any,
        detail: str | None = None,
        *args: builtins.object,
    ) -> None:
        self.source = source
        self.target = target
        self.detail = detail
        msg = utils.emsg(f"'{source}' does not equal '{target}'", detail)
        super().__init__(msg, *args)


class NotGreaterThanOrEqualToError(ValueError):
    def __init__(
        self,
        source: Any,
        target: Any,
        detail: str | None = None,
        *args: builtins.object,
    ) -> None:
        self.source = source
        self.target = target
        self.detail = detail
        msg = utils.emsg(
            f"'{source}' is not greater than or equal to '{target}'", detail
        )
        super().__init__(msg, *args)


class NotGreaterThanError(ValueError):
    def __init__(
        self,
        source: Any,
        target: Any,
        detail: str | None = None,
        *args: builtins.object,
    ) -> None:
        self.source = source
        self.target = target
        self.detail = detail
        msg = utils.emsg(f"'{source}' is not greater than '{target}'", detail)
        super().__init__(msg, *args)


class param:
    """
    Guarding parameters/attributes.
    """

    ...


class require:
    """Returns none, raises if false"""

    @staticmethod
    def eq(
        source: Any,
        target: Any,
        detail: str | None = None,
        raises: type[NotEqualError] = NotEqualError,
        *args,
        **kwargs,
    ) -> None:
        # if not (source == target):
        # if source != target:
        #     raise raises(source, target, detail, *args, **kwargs)
        if source == target:
            return
        raise raises(source, target, detail, *args, **kwargs)

    @staticmethod
    def ne(
        source: Any,
        target: Any,
        detail: str | None = None,
        raises: type[IsEqualError] = IsEqualError,
        *args,
        **kwargs,
    ) -> None:
        # if not (source != target):
        # if source == target:
        #     raise raises(source, target, detail, *args, **kwargs)
        if source != target:
            return
        raise raises(source, target, detail, *args, **kwargs)

    @staticmethod
    def ge(
        source: Any,
        target: Any,
        detail: str | None = None,
        raises: type[
            NotGreaterThanOrEqualToError
        ] = NotGreaterThanOrEqualToError,
        *args,
        **kwargs,
    ) -> None:
        if source >= target:
            return
        raise raises(source, target, detail, *args, **kwargs)

    @staticmethod
    def gt(
        source: Any,
        target: Any,
        detail: str | None = None,
        raises: type[NotGreaterThanError] = NotGreaterThanError,
        *args,
        **kwargs,
    ) -> None:
        if source > target:
            return
        raise raises(source, target, detail, *args, **kwargs)

    @staticmethod
    def lt(): ...
    @staticmethod
    def le(): ...

    @staticmethod
    def notinstance(
        source: object,
        target: type,
        detail: str | None = None,
    ) -> None:
        # stype: str = source.__class__.__qualname__
        ttype: str = target.__qualname__
        if builtins.isinstance(source, target):
            raise TypeError(f"'{source}' cannot be an instance of '{ttype}'")

    # TODO: make sure this can handle generics, unions, literal, etc
    @staticmethod
    def isinstance(
        source: object,
        target: type,
        detail: str | None = None,
        raises: type[ValueError] = ValueError,
    ) -> None:
        ttype: str = target.__qualname__
        if not builtins.isinstance(source, target):
            # raise TypeError(
            #     f"Expected '{ttype}' but received '{stype}' with value '{value_str_clip}'"
            # )
            raise TypeError(f"'{source}' must be an instance of '{ttype}'")

    # @staticmethod
    # def contains(
    #     domain: collection[T], member: T
    # ) -> None:  # ? co & nc for negated? - would be consistent
    #     """
    #     Whether the domain of items contains the item in question.
    #     """
    #     # future: for single item, diff from 'has' which maybe should do set intersection?
    #     # future: expand to sequences? would need to figure out order, eg: contains("hello world", "hello") vs contains("hello world", "hw")
    #     if member not in domain:
    #         msg = f"'{member}' must be a member of '{domain}'"
    #         raise ValueError()

    # @staticmethod
    # def has():
    #     """same as 'hasall'"""
    #     ...

    # @staticmethod
    # def hasone(): ...

    # @staticmethod
    # def hasnone(): ...  # ? hasnt (hasn't, has not, somewhat medieval)

    # @staticmethod
    # def hassome(): ...

    # @staticmethod
    # def hasall(): ...

    # @staticmethod
    # def hasany() -> None: ...

    # @staticmethod
    # def notin(
    #     value: Any,
    #     forbidden: collection[Any],
    #     detail: str | None = None,
    # ) -> None:
    #     if value in forbidden:
    #         msg = utils.comd(
    #             f"Value '{value}' must not be a member of '{forbidden}'",
    #             detail,
    #         )
    #         raise ValueError(msg)

    # @staticmethod
    # def isin(): ...

    # @staticmethod
    # def istype(): ...

    # @staticmethod
    # def issubclass():
    #     raise NotImplementedError()

    # @staticmethod
    # def haskeys(value: dict[KT, Any], keys: set[KT]) -> None: ...
