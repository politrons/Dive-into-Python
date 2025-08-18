from __future__ import annotations
from typing import TypeVar, Generic, Callable, Optional, Any

# Define a generic type variable
T = TypeVar("T")
U = TypeVar("U")


class PyIO(Generic[T]):

    def __init__(self, content: Optional[T], error: Optional[BaseException] = None) -> None:
        # Store either a value or an error (never both)
        # This keeps PyIO acting like a Try: Success(value) or Failure(error)
        self._value: Optional[T] = content if error is None else None
        self._error: Optional[BaseException] = error

    def map(self, func: Callable[[T], U]) -> "PyIO[U]":
        # If already failed, propagate the same failure
        # If value is None, treat it like an empty success and propagate None
        if self._error is not None or self._value is None: return self
        # Apply the side-effecting function and capture any runtime error
        try:
            return PyIO(func(self._value))
        except BaseException as ex:  # Capture *any* runtime error into the pipeline
            return PyIO[U](None, ex)

    def flat_map(self, func: Callable[[T], "PyIO[U]"]) -> "PyIO[U]":
        # If already failed, propagate the same failure
        # If value is None, treat it like an empty success and propagate None
        if self._error is not None or self._value is None: return self
        # Run the effectful step; capture thrown errors
        try:
            out = func(self._value)
            # If the returned PyIO is failed, propagate that failure
            if isinstance(out, PyIO) and out._error is not None:
                return PyIO[U](None, out._error)
            return out
        except BaseException as ex:
            return PyIO[U](None, ex)

    def filter(self, func: Callable[[T], bool]) -> "PyIO[T]":
        if self._error is not None or self._value is None: return self
        if func(self._value):
            return self
        return PyIO(None, None)

    def recover(self, func: Callable[[BaseException], U]) -> "PyIO[U]":
        # If is not failed, propagate the same instance
        if self._error is None: return self
        # Apply the side-effecting function and capture any runtime error
        try:
            return PyIO(func(self._error), None)
        except BaseException as ex:  # Capture *any* runtime error into the pipeline
            return PyIO[U](None, ex)

    def recover_with(self, func: Callable[[BaseException], "PyIO[U]"]) -> "PyIO[U]":
        # If is not failed, propagate the same instance
        if self._error is None: return self
        # Apply the side-effecting function and capture any runtime error
        try:
            return func(self._error)
        except BaseException as ex:  # Capture *any* runtime error into the pipeline
            return PyIO[U](None, ex)

    def when(self, predicate: Callable[[T], bool], func: Callable[[T], U]) -> "PyIO[U]":
        if self._error is not None or self._value is None: return self
        # If predicate is true we apply second function
        if predicate(self._value):
            return PyIO[U](func(self._value))
        return self

    def on_error(self, func: Callable[[BaseException], None]) -> "PyIO[T]":
        # If already failed, we execute the consumer function provided
        if self._error is not None:
            try:
                func(self._error)
            except BaseException as ex:
                return PyIO[U](None, ex)
        return self

    def on_success(self, func: Callable[[T], None]) -> "PyIO[T]":
        # If already failed, we execute the consumer function provided
        if self._error is None and self._value is not None:
            try:
                func(self._value)
            except BaseException as ex:
                return PyIO[U](None, ex)
        return self

    def get(self) -> T:
        # Unsafe extract: if there is a captured error, raise it now
        if self._error is not None:
            raise self._error
        return self._value

    def get_or_else(self, default: T) -> T:
        # Safe extract with default if failed or value is None
        if self._error is not None or self._value is None:
            return default
        return self._value


