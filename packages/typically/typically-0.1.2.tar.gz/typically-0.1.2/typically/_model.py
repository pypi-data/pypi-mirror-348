from __future__ import annotations
import builtins
import orjson
from abc import ABC, abstractmethod
from datetime import datetime
from types import ModuleType
from typing import Any, TypeVar, overload, ClassVar
from typing import Generic, Iterable, TypeVar, Self
from pydantic import BaseModel, ConfigDict, Json, Field
from pydantic_core import core_schema, PydanticSerializationUnexpectedValue
from pydantic.annotated_handlers import (
    GetJsonSchemaHandler,
    GetCoreSchemaHandler,
)
from pydantic.json_schema import JsonSchemaValue


Model = BaseModel


class Documented(Model):
    model_config = ConfigDict(use_attribute_docstrings=True)


class Blob(Model): ...
