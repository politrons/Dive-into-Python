'''
Errors in Python are controlled just like in Java using Exceptions. The most common as in Java to control the effects it's
 using try/catch where we control effects zone of code which are impure so some side effects might exist
'''
def processNumber(n):
    print(n)

list = (1, 2, 3, 4, 5)

for i in range(10):
    try:
        processNumber(list[i])
    except IndexError: # Exception when index cannot be found, and we control calling the function with just 0 value
        processNumber(0)


def customException(arg):
    try:
        arg.upper()
    except Exception:
        print("Error in arg %s" %arg)
    finally: print("Value processed %s" %arg)

customException(0)