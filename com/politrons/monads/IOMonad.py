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

    def recover(self, func: Callable[[BaseException], U]) -> "PyIO[U]":
        # If is not failed, propagate the same instance
        if self._error is None: return self
        # Apply the side-effecting function and capture any runtime error
        try:
            return PyIO(func(self._value), None)
        except BaseException as ex:  # Capture *any* runtime error into the pipeline
            return PyIO[U](None, ex)

    def recover_with(self, func: Callable[[BaseException], "PyIO[U]"]) -> "PyIO[U]":
        # If is not failed, propagate the same instance
        if self._error is None: return self
        # Apply the side-effecting function and capture any runtime error
        try:
            return func(self._value)
        except BaseException as ex:  # Capture *any* runtime error into the pipeline
            return PyIO[U](None, ex)

    def on_error(self, func: Callable[[BaseException], None]) -> "PyIO[T]":
        # If already failed, we execute the consumer function provided
        if self._error is not None:
            func(self._error)
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


# ----------------------------- Main ---------------------------------
if __name__ == "__main__":
    # Success path (matches your original behavior)
    pyio = PyIO[str]("Hello world")
    content = (pyio
               .map(lambda s: s.upper())  # side-effect captured if it throws
               .flat_map(lambda s: PyIO[str](s + "!!!"))  # returns PyIO, may fail too
               .get())
    print(content)

    # Another success path with ints
    pyio = PyIO[int](10)
    content = (pyio
               .map(lambda n: n + 100)
               .flat_map(lambda n: PyIO[int](n * 2))
               .get())
    print(content)

    # Starting with None -> behaves like empty success; get_or_else recovers
    pyio = PyIO[str](None)
    content = (pyio
               .map(lambda s: s.upper())  # skipped (value is None)
               .flat_map(lambda s: PyIO[str](s + "!!!"))  # skipped
               .get_or_else("Another world"))
    print(content)

    # Failure injected by a side-effect (division by zero), moved through the pipeline
    pyio = PyIO[int](10)
    content = (pyio
               .map(lambda n: n // 0)  # raises ZeroDivisionError -> captured
               .flat_map(lambda n: PyIO[int](n * 2))  # not executed (failure propagates)
               .on_error(lambda ex: print(f"We have a side-effect because. {ex}"))
               .get_or_else(42))  # recover at the edge
    print(content)

    """
    Failure injected by a side-effect (division by zero), then use [recover] to control side-effect and 
    provide a new success value
    """
    pyio = PyIO[int](100)
    content = (pyio
               .map(lambda n: n // 0)  # raises ZeroDivisionError -> captured
               .recover(lambda ex: 200)  # recover passing a new value
               .map(lambda n: n * 10)
               .get())
    print(content)

    """
    Failure injected by a side-effect (division by zero), then use [recover_with] to control side-effect and 
    provide a new monad success value
    """
    pyio = PyIO[int](1)
    content = (pyio
               .map(lambda n: n // 0)  # raises ZeroDivisionError -> captured
               .recover_with(lambda ex: PyIO[int](10))  # recover passing a new value
               .map(lambda n: n * 10)
               .get())
    print(content)