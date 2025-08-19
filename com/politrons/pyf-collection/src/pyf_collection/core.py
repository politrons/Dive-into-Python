from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar, Generic, Callable, Optional
from itertools import islice, chain

# Define a generic type variable
T = TypeVar("T")
U = TypeVar("U")

class PyFCollection(Generic[T]):
    def __init__(self, source: Iterable[T]) -> None:
        # just remember the iterable, don't convert to list
        self._it: Iterable[T] = source
        self._acc = None

    def __iter__(self):
        return iter(self._it)

    def __repr__(self) -> str:  # zero side-effects
        return f"<PyFCollection at 0x{id(self):x}>"

    def map(self, fn: Callable[[T], U]) -> "PyFCollection[U]":
        return PyFCollection(fn(x) for x in self._it)

    def filter(self, pred: Callable[[T], bool]) -> "PyFCollection[T]":
        return PyFCollection(x for x in self._it if pred(x))

    def flat_map(self, fn: Callable[[T], Iterable[U]]) -> "PyFCollection[U]":
        return PyFCollection(chain.from_iterable(fn(x) for x in self._it))

    def distinct(self, value: T) -> "PyFCollection[T]":
        return PyFCollection(x for x in self._it if x != value)

    def take(self, n: int) -> "PyFCollection[T]":
        return PyFCollection(islice(self._it, n))

    def find(self, func: Callable[[T], bool]) -> "Optional[U]":
        for e in self._it:
            if func(e):
                return e
        return None

    def exist(self, func: Callable[[T], bool]) -> bool:
        for e in self._it:
            if func(e):
                return True
        return False

    def fold(self, acc: U, func: Callable[[U, T], U]) -> U:
        self._acc = acc
        for e in self._it:
            acc = acc + func(self._acc, e)
        return acc

    def drop(self, n: int) -> "PyFCollection[T]":
        return PyFCollection(self._it[n:])

    def slice(self, n: int, m: int) -> "PyFCollection[U]":
        return PyFCollection(self._it[n:m])

    def to_list(self) -> list[T]:
        return list(self._it)



