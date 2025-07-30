__all__ = [
    "count",
    "ConvertibleToCount",
    "definition",
    "ConvertibleToDefinition",
    "module",
    "ConvertibleToModule",
    "definition",
    "ConvertibleToDefinition",
    "module",
    "ConvertibleToModule",
    "ConvertibleToPath",
    "FilePath",
    "DirectoryPath",
    "Path",
    "PathLike",
    "Model",
    "Documented",
    "Blob",
    "TypedDict",
    "Any",
    "NoReturn",
    "Never",
    "Self",
    "LiteralString",
    "ClassVar",
    "Final",
    "TypeVar",
    "Union",
    "Optional",
    "Literal",
    "TypeAlias",
    "Concatenate",
    "TypeGuard",
    "TypeIs",
    "ForwardRef",
    "overload",
    "cast",
    "of",
]

# * lib types
from ._count import (
    count,
    ConvertibleToCount,
    # BitCount,
    # ByteCount,
)
from ._source import (
    definition,
    ConvertibleToDefinition,
    module,
    ConvertibleToModule,
)

# from ._extended import estr
from ._path import (
    ConvertibleToPath,
    FilePath,
    DirectoryPath,
    Path,
    PathLike,
)
from ._model import Model, Documented, Blob

# * other common types from various standard libs/dependencies

# NOTE: typing_extensions is used over the default `typing` module for
# more compatibility with pydantic for these types
from typing_extensions import (
    TypedDict,  # TODO: add others where pydantic requires typing_extensions type
)

from typing import (
    Any,
    NoReturn,
    Never,
    Self,
    LiteralString,
    ClassVar,
    Final,
    TypeVar,
    Union,
    Optional,
    Literal,
    TypeAlias,
    Concatenate,
    TypeGuard,
    TypeIs,
    ForwardRef,
    overload,
    cast,
    # TODO: add others as needed
)


class of:
    """
    Various type variables. Called `of` so can be used like:

    ```python
    import typically as t

    # t.of.M - as in: "type of M"
    def load(path: t.ConvertibleToPath, model: type[t.of.M]) -> t.of.M:
        ...
    ```
    """

    M = TypeVar("M", bound=Model)
