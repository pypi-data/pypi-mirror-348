from __future__ import annotations
import pydantic
from os import PathLike
from pathlib import Path

DirectoryPath = pydantic.DirectoryPath
"""
This is a proxy for `pydantic.DirectoryPath`, which in turn is
just an annotated type for `pathlib.Path`.

It only validates that the path is actually a directory when used
as an attribute in a pydantic model.

Attempting to instantiate it will work but may show in a type error:
`Object of type "Annotated" is not callable`.

It would be used when you need to validate a path is a real directory
path, but only on the instantiation of a pydantic model the path is
an attribute of.
"""

FilePath = pydantic.FilePath
"""
This is a proxy for `pydantic.FilePath`, which in turn is
just an annotated type for `pathlib.Path`.

It only validates that the path is actually a file when used
as an attribute in a pydantic model.

Attempting to instantiate it will work but may show in a type error:
`Object of type "Annotated" is not callable`.

It would be used when you need to validate a path is a real file
path, but only on the instantiation of a pydantic model the path is
an attribute of.
"""

ConvertibleToPath = str | Path
"""
NOTE:
    Not sure what to call this. Would use `PathLike`,
    but already used by `os.PathLike`, and thats an abc,
    so would be confusing.
    
    Ideas:

    - PathLike
    - Pathish
    - ConvertibleToPath

"""


# class RealDirectoryPath(pathlib.Path):
#     def __new__(cls, /, path: Pathish) -> RealDirectoryPath:
#         path = pathlib.Path(path)
#         if not path.is_dir():
#             raise
