# type: ignore

import typing
from string.templatelib import Interpolation, Template

__all__ = ["Template", "Interpolation", "Conversion"]

type Conversion = typing.Literal["a", "r", "s"]
