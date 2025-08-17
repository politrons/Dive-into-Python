from typing import TypeVar, Generic, Callable

# Define two generic type variables
T = TypeVar("T")  # Input type


class PyIO(Generic[T]):
    def __init__(self, content: T) -> None:
        # Store the content of any type
        self.content = content

    def map(self, func: Callable[[T], T]) -> "PyIO[T]":
        if self.content is None: return self
        return PyIO(func(self.content))

    def flat_map(self, func: Callable[[T], "PyIO[T]"]) -> "PyIO[T]":
        if self.content is None: return self
        return func(self.content)

    def get(self) -> T:
        return self.content

    def get_or_else(self, default:T) -> T:
        if self.content is None:
            return default
        return self.content


if __name__ == "__main__":
    pyio = PyIO[str]("Hello world")
    content = (pyio
               .map(lambda s: s.upper())
               .flat_map(lambda s: PyIO[str](s + "!!!"))
               .get())
    print(content)

    pyio = PyIO[int](10)
    content = (pyio
               .map(lambda s: s + 100)
               .flat_map(lambda s: PyIO[int](s * 2))
               .get())
    print(content)

    pyio = PyIO[str](None)
    content = (pyio
               .map(lambda s: s.upper())
               .flat_map(lambda s: PyIO[str](s + "!!!"))
               .get_or_else("Another world"))
    print(content)