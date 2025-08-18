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

### Side-Effect Operators

- **`on_success(func)`** - Execute a side-effect function if the PyIO contains a value
- **`on_error(func)`** - Execute a side-effect function if the PyIO contains an error

### Extraction Operators

- **`get()`** - Extract the value (unsafe - throws if there was an error)
- **`get_or_else(default)`** - Extract the value or return default if error/None

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

## Installation

Simply copy the `pyio.py` file to your project directory and import:

```python
from pyio import PyIO
```

## License

This project is open source. See the license file for details.