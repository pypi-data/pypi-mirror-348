from typing import Optional, TypeVar, Union
import os


__version__ = "0.4.1"


T = TypeVar("T")


class _RaiseExceptionSentinel:
    """Sentinel indicating that an exception should be raised."""

    def __repr__(self) -> str:
        return "RAISE"


RAISE = _RaiseExceptionSentinel()


FALSY_STRINGS = {"0", "false", "f", "no", "n"}


class EnvironmentVariableNotSet(Exception):
    def __init__(self, varname: str):
        self.varname: str = varname

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.varname!r})"


def get_int(
    varname: str, default: Union[T, _RaiseExceptionSentinel] = RAISE
) -> Union[T, int]:
    if varname in os.environ:
        return int(os.environ[varname])
    if default is RAISE:
        raise EnvironmentVariableNotSet(varname)
    return default


def get_float(
    varname, default: Union[T, _RaiseExceptionSentinel] = RAISE
) -> Union[T, float]:
    if varname in os.environ:
        return float(os.environ[varname])
    if default is RAISE:
        raise EnvironmentVariableNotSet(varname)
    return default


def get_bool(
    varname,
    default: Union[T, _RaiseExceptionSentinel] = RAISE,
    falsy_strings: Optional[set[str]] = None,
) -> Union[T, bool]:
    if falsy_strings is None:
        falsy_strings = FALSY_STRINGS
    if varname in os.environ:
        return os.environ[varname].lower() not in falsy_strings
    if default is RAISE:
        raise EnvironmentVariableNotSet(varname)
    return default


def get_str(
    varname, default: Union[T, _RaiseExceptionSentinel] = RAISE
) -> Union[T, str]:
    if varname in os.environ:
        return os.environ[varname]
    if default is RAISE:
        raise EnvironmentVariableNotSet(varname)
    return default


__all__ = [
    "EnvironmentVariableNotSet",
    "get_int",
    "get_float",
    "get_bool",
    "get_str",
    "FALSY_STRINGS",
]
