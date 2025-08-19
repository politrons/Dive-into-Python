from __future__ import annotations

import collections
from typing import TypeVar, Generic, Callable, Optional

# Define a generic type variable
T = TypeVar("T")
U = TypeVar("U")


class PyFCollection(Generic[T]):

    def __init__(self, content: Optional[collections.Iterable[T]]) -> None:
        self._value: Optional[collections.Iterable[T]] = content if content is None else content
        self._acc = None

    def map(self, func: Callable[[T], U]) -> "PyFCollection[U]":
        map_list = []
        for e in self._value:
            map_list.append(func(e))
        return PyFCollection(map_list)

    def flat_map(self, func: Callable[[T], "PyFCollection[U]"]) -> "PyFCollection[U]":
        map_list = []
        for e in self._value:
            for f in func(e).to_list():
                map_list.append(f)
        return PyFCollection(map_list)

    def filter(self, func: Callable[[T], bool]) -> "PyFCollection[U]":
        filter_list = []
        for e in self._value:
            if func(e):
                filter_list.append(e)
        return PyFCollection(filter_list)

    def find(self, func: Callable[[T], bool]) -> "Optional[U]":
        for e in self._value:
            if func(e):
                return e
        return None

    def exist(self, func: Callable[[T], bool]) -> bool:
        for e in self._value:
            if func(e):
                return True
        return False

    def distinct(self, dis: T) -> "PyFCollection[U]":
        filter_list = []
        for e in self._value:
            if e is not dis:
                filter_list.append(e)
        return PyFCollection(filter_list)

    def fold(self, acc: U, func: Callable[[U, T], U]) -> "PyFCollection[U]":
        self._acc = acc
        for e in self._value:
            acc = acc + func(self._acc, e)
        return PyFCollection(acc)

    def take(self, n: int) -> "PyFCollection[T]":
        return PyFCollection(self._value[:n])

    def drop(self, n: int) -> "PyFCollection[T]":
        return PyFCollection(self._value[n:])

    def slice(self, n:int, m:int) -> "PyFCollection[U]":
        return PyFCollection(self._value[n:m])

    def to_list(self) -> collections.Iterable[T]:
        return self._value


