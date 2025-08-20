from typing import Protocol

# Define a type class (like in Haskell) using Protocol
class TypeClass(Protocol):
    def name(self) -> str: ...

# Example types implementing the "TypeClass" type class
class Float:
    def __init__(self, x: float) -> None:
        self.x = x

    def name(self) -> str:
        return f"Float({self.x})"

class Integer:
    def __init__(self, x: int):
        self.x = x

    def name(self) -> str:
        return f"Integer({self.x})"

class String:
    def __init__(self, x: str):
        self.x = x

    def name(self) -> str:
        return f"String({self.x})"

class Foo:
    def __init__(self, x: str):
        self.x = x

# A generic function that works with anything that has "name"
def print_type(t: TypeClass) -> None:
    print(t.name())


if __name__ == "__main__":
    u = Float(100.0)
    p = Integer(1981)
    s = String("hello")
    print_type(u)
    print_type(p)
    print_type(s)
    # print_type(Foo("")) # Not compiling with mypy

