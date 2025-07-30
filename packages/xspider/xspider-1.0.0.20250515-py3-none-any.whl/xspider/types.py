from typing import Literal, Any, TypeVar, TypeGuard
from collections.abc import Generator, Iterator

T = TypeVar("T")


def is_list_of(
        val: list[Any],
        type_: type[T]
) -> TypeGuard[list[T]]:
    return all(isinstance(x, type_) for x in val)
