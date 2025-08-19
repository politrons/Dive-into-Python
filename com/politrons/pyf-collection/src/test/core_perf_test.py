"""
benchmark_pyf_vs_vanilla.py
───────────────────────────
Tiny benchmark: PyFCollection vs. plain-Python comprehensions.

Dataset: 1 000 000 integers
Pipeline:
    1. map        → double each value
    2. filter     → keep multiples of 3
    3. flat_map   → produce (n, -n) for each element
    4. distinct   → drop a single value (-6) so the op does something
    5. take       → keep first 100 items
    6. to_list    → materialise the final result

We use timeit (5 runs) for a rough comparison.
"""

from timeit import timeit
from typing import List

# ---- import your collection implementation -------------------------
from pyf_collection import PyFCollection


# ---------- pipeline using PyFCollection ----------------------------
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


# ---------- pipeline with “vanilla” Python --------------------------
def pipeline_vanilla() -> List[int]:
    data = list(range(1, 1_000_001))

    doubled     = (x * 2 for x in data)                       # map
    multiples   = (x for x in doubled if x % 3 == 0)          # filter
    flatmapped  = (y for x in multiples for y in (x, -x))     # flat-map
    distincted  = (x for x in flatmapped if x != -6)          # distinct
    first_100   = [x for _, x in zip(range(100), distincted)] # take
    return first_100


if __name__ == "__main__":
    vanilla_time = timeit("pipeline_vanilla()", globals=globals(), number=5)
    pyf_time     = timeit("pipeline_pyf()",     globals=globals(), number=5)

    print(f"PyFCollection   → {pyf_time:.3f}s (5 runs)")
    print(f"Vanilla Python  → {vanilla_time:.3f}s (5 runs)")
    print("Sample output  :", pipeline_pyf()[:10])
