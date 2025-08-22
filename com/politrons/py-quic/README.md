# PyIO - Python Effects System

A lightweight monadic effects system for Python that provides safe error handling and functional composition. PyIO wraps values and exceptions, allowing you to chain operations without explicit error checking at each step.

## Overview

PyIO acts like a `Try` type - it can hold either a successful value or a captured exception. Operations are automatically skipped if a previous step failed, and errors propagate through the chain until handled.

## Core Concept

```python
from pyio import PyIO

# Success case
result = PyIO("hello").map(str.upper).get()  # "HELLO"

# Error case - division by zero is captured and propagated
result = PyIO(10).map(lambda x: x // 0).get_or_else(42)  # 42
```

## Operators

### Transformation Operators

- **`map(func)`** - Transform the value if successful, capture any exceptions thrown by `func`
- **`flat_map(func)`** - Transform with a function that returns a PyIO, flatten the result
- **`filter(predicate)`** - Keep value only if predicate returns True, otherwise become empty

### Recovery Operators

- **`recover(func)`** - Handle errors by providing a recovery function that takes the exception
- **`recover_with(func)`** - Handle errors with a function that returns a PyIO

### Conditional Operators

- **`when(predicate, func)`** - Apply `func` only if `predicate` returns True

### Parallel Processing Operators

- **`on_parallel(func_1, func_2, merge_func, max_workers=None)`** - Run two functions concurrently on the same value, then merge their results using `merge_func`

### Side-Effect Operators

- **`on_success(func)`** - Execute a side-effect function if the PyIO contains a value
- **`on_error(func)`** - Execute a side-effect function if the PyIO contains an error

### State Inspection Operators

- **`is_success()`** - Returns True if the PyIO contains a value and no error
- **`is_error()`** - Returns True if the PyIO contains an error
- **`is_empty()`** - Returns True if the PyIO's value is None

### Extraction Operators

- **`get()`** - Extract the value (unsafe - throws if there was an error)
- **`get_or_else(default)`** - Extract the value or return default if error/None
- **`failed()`** - Extract the captured exception (returns the BaseException)

## Usage Examples

### Basic Chaining
```python
result = (PyIO("hello world")
          .map(str.upper)
          .map(lambda s: s + "!!!")
          .get())  # "HELLO WORLD!!!"
```

### Error Handling
```python
result = (PyIO(10)
          .map(lambda x: x // 0)  # ZeroDivisionError captured
          .recover(lambda ex: 999)  # Recover with default value
          .map(lambda x: x * 2)
          .get())  # 1998
```

### Conditional Processing
```python
result = (PyIO(15)
          .when(lambda n: n > 10, lambda n: n * 100)
          .get())  # 1500
```

### Parallel Processing
```python
import time

def slow_double(x):
    time.sleep(1)
    return x * 2

def slow_square(x):
    time.sleep(1)
    return x ** 2

result = (PyIO(5)
          .on_parallel(
              slow_double,    # 5 * 2 = 10
              slow_square,    # 5 ** 2 = 25
              lambda a, b: a + b,  # 10 + 25 = 35
              max_workers=2
          )
          .get())  # 35 (computed in ~1 second instead of 2)
```

### State Inspection
```python
# Check if computation was successful
pyio_value = PyIO(42).map(lambda x: x * 2)
if pyio_value.is_success():
    print(f"Success: {pyio_value.get()}")

# Check for errors
pyio_error = PyIO(10).map(lambda x: x // 0)
if pyio_error.is_error():
    print(f"Error occurred: {pyio_error.failed()}")

# Check if value is None
empty_pyio = PyIO(None)
if empty_pyio.is_empty():
    print("Value is None")
```

### Side Effects
```python
result = (PyIO("processing data")
          .on_success(lambda msg: print(f"LOG: {msg}"))  # Prints log message
          .map(str.upper)
          .on_success(lambda msg: print(f"RESULT: {msg}"))  # Prints result
          .get())
```

### Error Side Effects
```python
result = (PyIO(10)
          .map(lambda x: x // 0)  # This will fail
          .on_error(lambda ex: print(f"Error logged: {type(ex).__name__}"))
          .recover(lambda ex: 0)
          .get())  # 0
```

## Installation

Simply copy the `pyio.py` file to your project directory and import:

```python
from pyio import PyIO
```

## License

This project is open source. See the license file for details.