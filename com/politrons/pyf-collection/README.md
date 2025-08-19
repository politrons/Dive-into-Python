# PyF Collection

A Python library that brings functional programming collection operations to Python, inspired by monadic operations from languages like Scala and Haskell.

## Installation

```bash
pip install pyf-collection
```

## Overview

PyFCollection is a generic collection wrapper that provides a fluent API for functional programming operations on iterables. It allows you to chain operations like `map`, `filter`, `fold`, and more in a clean, readable way.

## Quick Start

```python
from pyf_collection import PyFCollection

# Create a collection
numbers = PyFCollection([1, 2, 3, 4, 5])

# Chain operations
result = (numbers
    .map(lambda x: x * 2)
    .filter(lambda x: x > 4)
    .to_list())

print(list(result))  # [6, 8, 10]
```

## API Reference

### Constructor

#### `PyFCollection(content: Optional[collections.Iterable[T]])`

Creates a new PyFCollection instance.

```python
# From a list
collection = PyFCollection([1, 2, 3])

# From any iterable
collection = PyFCollection(range(5))

# Empty collection
collection = PyFCollection(None)
```

### Transformation Operations

#### `map(func: Callable[[T], U]) -> PyFCollection[U]`

Transforms each element in the collection using the provided function.

```python
numbers = PyFCollection([1, 2, 3])
doubled = numbers.map(lambda x: x * 2)
print(list(doubled.to_list()))  # [2, 4, 6]

# Transform to different type
words = PyFCollection(["hello", "world"])
lengths = words.map(len)
print(list(lengths.to_list()))  # [5, 5]
```

#### `flat_map(func: Callable[[T], PyFCollection[U]]) -> PyFCollection[U]`

Maps each element to a PyFCollection and flattens the results.

```python
words = PyFCollection(["hello", "world"])
chars = words.flat_map(lambda word: PyFCollection(list(word)))
print(list(chars.to_list()))  # ['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd']

# Expand numbers
numbers = PyFCollection([1, 2, 3])
expanded = numbers.flat_map(lambda x: PyFCollection([x, x * 10]))
print(list(expanded.to_list()))  # [1, 10, 2, 20, 3, 30]
```

### Filtering Operations

#### `filter(func: Callable[[T], bool]) -> PyFCollection[T]`

Keeps only elements that satisfy the predicate function.

```python
numbers = PyFCollection([1, 2, 3, 4, 5, 6])
evens = numbers.filter(lambda x: x % 2 == 0)
print(list(evens.to_list()))  # [2, 4, 6]
```

#### `distinct(dis: T) -> PyFCollection[T]`

Removes all occurrences of the specified element.

```python
numbers = PyFCollection([1, 2, 2, 3, 2, 4])
without_twos = numbers.distinct(2)
print(list(without_twos.to_list()))  # [1, 3, 4]
```

### Search Operations

#### `find(func: Callable[[T], bool]) -> Optional[T]`

Returns the first element that satisfies the predicate, or None if not found.

```python
numbers = PyFCollection([1, 2, 3, 4, 5])
first_even = numbers.find(lambda x: x % 2 == 0)
print(first_even)  # 2

not_found = numbers.find(lambda x: x > 10)
print(not_found)  # None
```

#### `exist(func: Callable[[T], bool]) -> bool`

Returns True if any element satisfies the predicate.

```python
numbers = PyFCollection([1, 2, 3, 4, 5])
has_even = numbers.exist(lambda x: x % 2 == 0)
print(has_even)  # True

has_large = numbers.exist(lambda x: x > 10)
print(has_large)  # False
```

### Aggregation Operations

#### `fold(acc: U, func: Callable[[U, T], U]) -> PyFCollection[U]`

Reduces the collection to a single value using an accumulator function.

```python
numbers = PyFCollection([1, 2, 3, 4])
sum_result = numbers.fold(0, lambda acc, x: acc + x)
print(list(sum_result.to_list()))  # [10]

# String concatenation
words = PyFCollection(["Hello", " ", "World"])
sentence = words.fold("", lambda acc, x: acc + x)
print(list(sentence.to_list()))  # ["Hello World"]
```

### Slicing Operations

#### `take(n: int) -> PyFCollection[T]`

Returns a new collection with the first n elements.

```python
numbers = PyFCollection([1, 2, 3, 4, 5])
first_three = numbers.take(3)
print(list(first_three.to_list()))  # [1, 2, 3]
```

#### `drop(n: int) -> PyFCollection[T]`

Returns a new collection without the first n elements.

```python
numbers = PyFCollection([1, 2, 3, 4, 5])
without_first_two = numbers.drop(2)
print(list(without_first_two.to_list()))  # [3, 4, 5]
```

#### `slice(n: int, m: int) -> PyFCollection[T]`

Returns elements from index n to m (exclusive).

```python
numbers = PyFCollection([0, 1, 2, 3, 4, 5])
middle = numbers.slice(2, 4)
print(list(middle.to_list()))  # [2, 3]
```

### Output Operations

#### `to_list() -> collections.Iterable[T]`

Converts the collection back to its underlying iterable.

```python
collection = PyFCollection([1, 2, 3])
result = collection.to_list()
print(list(result))  # [1, 2, 3]
```

## Chaining Operations

All operations return a new PyFCollection, allowing for fluent method chaining:

```python
result = (PyFCollection([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    .filter(lambda x: x % 2 == 0)      # [2, 4, 6, 8, 10]
    .map(lambda x: x * x)              # [4, 16, 36, 64, 100]
    .take(3)                           # [4, 16, 36]
    .map(lambda x: f"Value: {x}")      # ["Value: 4", "Value: 16", "Value: 36"]
    .to_list())

print(list(result))  # ["Value: 4", "Value: 16", "Value: 36"]
```

## Type Safety

PyFCollection is fully typed using Python's type hints and generics, providing excellent IDE support and type checking:

```python
from typing import List

# Type inference works correctly
numbers: PyFCollection[int] = PyFCollection([1, 2, 3])
strings: PyFCollection[str] = numbers.map(str)  # PyFCollection[str]
```

## Requirements

- Python >= 3.9
- typing support for generics

## License

MIT License

## Author

Pablo Picouto Garcia

## Contributing

Contributions are welcome! Please visit the [GitHub repository](https://github.com/politrons/Dive-into-Python) for more information.

## Issues

Report issues at: https://github.com/politrons/Dive-into-Python/issues