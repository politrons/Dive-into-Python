# Types
'''
Python 3 thanks to [typing] library we can have static type
'''
from typing import List

def firstFuncType(arg:str) -> str:
    return arg.upper()

response = firstFuncType("Hello Static type world")
print("This is static type String: %s" % response)

def scale(scalar: float, listFloat: List[float]) -> List[float]:
    return [scalar * num for num in listFloat]

newListFloat = scale(2.0, [1.0, -4.2, 5.4])
print(newListFloat)



