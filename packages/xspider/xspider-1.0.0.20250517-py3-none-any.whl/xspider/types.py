from inspect import iscoroutine, isgenerator, isasyncgen
from typing import Literal, Any, Self, Final, TypeAlias, TypeVar, TypeGuard, Never, NoReturn, TYPE_CHECKING
from collections.abc import Generator, Iterator, AsyncIterable, AsyncIterator, Callable

T = TypeVar("T")


def is_str(val: Any) -> TypeGuard[str]:
    return isinstance(val, str)


def is_list_of(
        val: list[Any],
        type_: type[T]
) -> TypeGuard[list[T]]:
    return isinstance(val, list) and all(isinstance(x, type_) for x in val)


class TransformTypeError(TypeError):
    pass
