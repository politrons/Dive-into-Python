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


## Performance

PyFCollection is designed to be performant while maintaining readability. Benchmarks show it can even outperform equivalent vanilla Python implementations in complex pipelines.

### Benchmark Results

A comprehensive benchmark comparing PyFCollection against vanilla Python comprehensions shows impressive performance:

**Test Setup:**
- Dataset: 1,000,000 integers
- Pipeline operations:
  1. `map` → double each value
  2. `filter` → keep multiples of 3
  3. `flat_map` → produce (n, -n) for each element
  4. `distinct` → drop a single value (-6)
  5. `take` → keep first 100 items
  6. `to_list` → materialize the final result

**Results:**
```
PyFCollection   → 0.187s (5 runs)
Vanilla Python  → 0.235s (5 runs)
Sample output   : [6, 12, -12, 18, -18, 24, -24, 30, -30, 36]
```

PyFCollection demonstrates **~20% better performance** than equivalent vanilla Python code, while providing significantly more readable and maintainable code.

### Benchmark Code

```python
from timeit import timeit
from typing import List
from pyf_collection import PyFCollection

def pipeline_pyf() -> List[int]:
    data = list(range(1, 1_000_001))
    
    result = (
        PyFCollection(data)
        .map(lambda x: x * 2)
        .filter(lambda x: x % 3 == 0)
        .flat_map(lambda x: PyFCollection([x, -x]))
        .distinct(-6)
        .take(100)
        .to_list()
    )
    return result

def pipeline_vanilla() -> List[int]:
    data = list(range(1, 1_000_001))
    
    doubled     = (x * 2 for x in data)                       # map
    multiples   = (x for x in doubled if x % 3 == 0)          # filter
    flatmapped  = (y for x in multiples for y in (x, -x))     # flat-map
    distincted  = (x for x in flatmapped if x != -6)          # distinct
    first_100   = [x for *, x in zip(range(100), distincted)] # take
    return first_100

# Run benchmark
vanilla_time = timeit("pipeline_vanilla()", globals=globals(), number=5)
pyf_time     = timeit("pipeline_pyf()",     globals=globals(), number=5)

print(f"PyFCollection   → {pyf_time:.3f}s (5 runs)")
print(f"Vanilla Python  → {vanilla_time:.3f}s (5 runs)")
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