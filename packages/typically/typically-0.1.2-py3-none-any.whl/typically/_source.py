from __future__ import annotations
import rpi.v0 as rpi
import inspect
import importlib
from pathlib import Path
from types import ModuleType
from typing import Union, Callable, Any, Self
from pydantic import ValidatorFunctionWrapHandler
from pydantic.annotated_handlers import GetCoreSchemaHandler
from pydantic_core import PydanticSerializationUnexpectedValue
from pydantic_core import core_schema as cs

# TODO: add classvar and model type for web API inputs/payloads that together allow blocking
# of some types for use in apis - eg: definition
# TODO: cover failure cases of inspect.getsource for C/pyo3 modules, or dynamic runtime generated code


class module:
    @staticmethod
    def __validate_str(value: str) -> str:
        value = value.strip()
        if rpi.name_chain.fullmatch(value) is None:
            raise ValueError(
                f"'{value}' does not match pattern r'{rpi.name_chain.pattern}'"
            )
        return value

    @staticmethod
    def __validate_mod(value: ModuleType) -> str:
        return value.__name__

    @staticmethod
    def __validate_value(value: str | ModuleType) -> str:
        if isinstance(value, str):
            return module.__validate_str(value)
        elif isinstance(value, ModuleType):
            return module.__validate_mod(value)
        else:
            raise TypeError(value)

    @staticmethod
    def __init_object(value: str | ModuleType) -> ModuleType | None:
        return None if isinstance(value, str) else value

    def __init__(self, value: str | ModuleType) -> None:
        self.__value = self.__validate_value(value)
        self.__object = self.__init_object(value)

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return self.__str__()

    def reset(self) -> None:
        """Reset cached data."""
        self.__object = None

    @property
    def name(self) -> str:
        return str(self)

    # TODO: review security implications of dynamic import
    @property
    def object(self) -> ModuleType:
        """
        The module object itself.
        """
        if self.__object is None:
            self.__object = importlib.import_module(name=self.name)
        return self.__object

    @property
    def doc(self) -> str:
        """
        The module object docstring.
        """
        return self.object.__doc__ or ""

    @property
    def exists(self) -> bool:
        """
        Whether the module is available in the current environment.
        """
        # return self.value in sys.modules # won't work for relative?
        try:
            _ = self.object
            return True
        except:
            return False

    @property
    def code(self) -> str:
        return inspect.getsource(self.object)

    @property
    def file(self) -> Path | None:
        __file__ = self.object.__file__
        if __file__ is None:
            return None
        # path = Path(__file__).absolute()
        path = Path(__file__).resolve()
        return path

    @property
    def path(self) -> Path | None:
        __path__ = self.object.__path__
        if len(__path__) == 1:
            path = Path(__path__[0]).resolve()
            return path
        else:
            return None

    @staticmethod
    def factory(value: ConvertibleToModule) -> Callable[[], module]:
        return lambda: module(value)

    @classmethod
    def __serialize__(  # type: ignore
        cls,
        value: module,
        info: cs.SerializationInfo,
    ) -> str | Self:
        if not isinstance(value, cls):
            raise PydanticSerializationUnexpectedValue(
                f"Expected `{cls}` but got `{type(value)}` with value `'{value}'` - serialized value may not be as expected."
            )
        if info.mode == "json":
            return str(value)
        return value

    @classmethod
    def __get_pydantic_core_schema__(  # type: ignore
        cls,
        source: type[module],
        handler: GetCoreSchemaHandler,
    ) -> cs.CoreSchema:
        def wrapper(value: Any, wrap_handler: ValidatorFunctionWrapHandler):
            return source(value)

        return cs.no_info_wrap_validator_function(
            wrapper,
            schema=cs.str_schema(
                pattern=rpi.name_chain,
                min_length=1,
                max_length=128,
                strip_whitespace=True,
                strict=True,
            ),
            serialization=cs.plain_serializer_function_ser_schema(
                cls.__serialize__, info_arg=True, when_used="always"
            ),
        )


class definition:
    @staticmethod
    def __validate_str(value: str) -> tuple[str, str]:
        m = rpi.definition_locator.fullmatch(value)
        if m is None:
            raise ValueError(
                f"'{value}' is not in form of '<module>:<object>', "
                f"does not match pattern r'{rpi.definition_locator.pattern}'"
            )
        return (m.group(1), m.group(4))

    @staticmethod
    def __validate_def(value: definition) -> tuple[str, str]:
        return definition.__validate_str(str(value))

    @staticmethod
    def __validate_tuple(value: tuple[str, str]) -> tuple[str, str]:
        if len(value) != 2:
            raise ValueError(value)
        if not all(isinstance(item, str) for item in value):
            raise TypeError(value)
        return definition.__validate_str(":".join(value))

    @staticmethod
    def __validate_value(value: ConvertibleToDefinition) -> tuple[str, str]:
        if isinstance(value, ModuleType):
            raise TypeError(
                f"'{value.__name__}' is a ModuleType, "
                f"'{module.__module__}:{module.__qualname__}' should be used instead"
            )
        else:
            if isinstance(value, str):
                return definition.__validate_str(value)
            elif isinstance(value, definition):
                return definition.__validate_def(value)
            elif isinstance(value, tuple):
                return definition.__validate_tuple(value)
            # FIXME: inspect.isfunction is not reliable, should be replaced
            elif inspect.isfunction(value) or isinstance(value, type):
                return (value.__module__, value.__qualname__)
            else:
                raise TypeError(value)

    @staticmethod
    def __init_object(value: ConvertibleToDefinition) -> object | None:
        return None if isinstance(value, str | tuple | definition) else value

    def __init__(self, value: ConvertibleToDefinition) -> None:
        self.__value = self.__validate_value(value)
        self.__object = self.__init_object(value)

    def __str__(self) -> str:
        return self.locator

    def __bool__(self) -> bool:
        return self.exists

    def __repr__(self) -> str:
        return self.locator

    def reset(self) -> None:
        """Reset cached object."""
        self.__object = None

    @property
    def value(self) -> tuple[str, str]:
        return self.__value

    @property
    def module(self) -> module:
        return module(self.value[0])

    @property
    def exists(self) -> bool:
        """
        Check if the definition exists.
        """
        try:
            _ = self.object
            return True
        except AttributeError:
            return False

    @property
    def name(self) -> str:
        """
        Object qualified name in module.

        Examples:
            - `"urlparse"`
            - `"geohash"`
            - `"definition.locationlocator`
        """
        return self.value[1]

    @property
    def doc(self) -> str | None:
        """
        The definition object docstring.
        """
        return self.object.__doc__

    @property
    def code(self) -> str:
        """Get source code for object."""
        return inspect.getsource(self.object)  # type: ignore

    @property
    def object(self) -> object:
        """
        Get defined object.
        """
        if self.__object is None:
            target = self.module.object
            scopes: list[str] = self.name.split(".")
            while len(scopes):
                name = scopes.pop(0)
                target = getattr(target, name)
            self.__object = target
        return self.__object

    @property
    def type(self) -> type:
        """
        Get object type. Probably will be `function` or `type` (`type` is an instance of itself).
        """
        return type(self.object)

    @property
    def locator(self) -> str:  # ? identity, location, source
        """
        Locator/location: joined name in form of: `<module_name>:<definition_name>`.

        Examples:
            - `"urllib.parse:urlparse"`
            - `"antigravity:geohash"`
            - `"typically.types:definition.locator"` (this property)
        """
        return ":".join(self.value)

    @property
    def cls(self) -> bool:
        """Whether the object is a class."""
        return inspect.isclass(self.object)

    @property
    def fn(self) -> bool:
        """Whether the object is a function."""
        # TODO: replace with reliable inspection func
        return inspect.isfunction(self.object)

    # TODO: add other high level type checks (is instance, is variable?, etc)

    @staticmethod
    def factory(value: ConvertibleToDefinition) -> Callable[[], definition]:
        return lambda: definition(value)

    @classmethod
    def __serialize__(  # type: ignore
        cls,
        value: definition,
        info: cs.SerializationInfo,
    ) -> str | definition:
        if not isinstance(value, cls):
            raise PydanticSerializationUnexpectedValue(
                f"Expected `{cls}` but got `{type(value)}` with value `'{value}'` - serialized value may not be as expected."
            )
        if info.mode == "json":
            return str(value)
        return definition(value)

    @classmethod
    def __get_pydantic_core_schema__(  # type: ignore
        cls,
        source: type[definition],
        handler: GetCoreSchemaHandler,
    ) -> cs.CoreSchema:
        def wrapper(value: Any, wrap_handler: ValidatorFunctionWrapHandler):
            return definition(value)

        return cs.no_info_wrap_validator_function(
            wrapper,
            schema=cs.str_schema(
                pattern=rpi.definition_locator,
                min_length=1,
                max_length=256,
                strip_whitespace=True,
                strict=True,
            ),
            serialization=cs.plain_serializer_function_ser_schema(
                cls.__serialize__,
                info_arg=True,
                when_used="always",
            ),
        )


ConvertibleToDefinition = Union[
    str,
    tuple[str, str],
    definition,
    object,
]
ConvertibleToModule = Union[
    str,
    ModuleType,
]
