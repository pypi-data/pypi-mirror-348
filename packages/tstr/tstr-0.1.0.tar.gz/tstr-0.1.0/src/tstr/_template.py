import typing

__all__ = ["Template", "Interpolation", "Conversion", "TEMPLATE_STRING_SUPPORTED"]

type Conversion = typing.Literal["a", "r", "s"]

try:
    from string.templatelib import Interpolation, Template  # type: ignore

    TEMPLATE_STRING_SUPPORTED = True
except Exception:
    # Fallback to compatible implementation if template strings are not supported
    from ._compat import Interpolation, Template

    TEMPLATE_STRING_SUPPORTED = False
