# Types
'''
Python 3 thanks to [typing] library we can have static type
'''
from typing import List


def firstFuncType(arg: str) -> str:
    return arg.upper()


response = firstFuncType("Hello Static type world")
print("This is static type String: %s" % response)


def scale(scalar: float, listFloat: List[float]) -> List[float]:
    return [scalar * num for num in listFloat]


newListFloat = scale(2.0, [1.0, -4.2, 5.4])
print(newListFloat)


def mypy_checker(value: str, bool_val: bool = True):
    """Using command mypy com/politrons/features/StaticType.py it will return the error
    com/politrons/features/StaticType.py:28: error: Argument 2 to "mypy_checker" has incompatible type "str"; expected "bool"
        Found 1 error in 1 file (checked 1 source file)
    """
    print(value.upper())
    print(bool_val)

"""Uncomment to check the error with mypy"""
# mypy_checker("hello mypy checker", "wrong_argument")

