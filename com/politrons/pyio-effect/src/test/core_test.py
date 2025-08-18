from __future__ import annotations

from pyio_effect import PyIO

# ----------------------------- Main ---------------------------------
if __name__ == "__main__":
    """
    Success path with [map] and [flat_map]
    """
    pyio = PyIO[str]("Hello world")
    content = (pyio
               .map(lambda s: s.upper())  # side-effect captured if it throws
               .flat_map(lambda s: PyIO[str](s + "!!!"))  # returns PyIO, may fail too
               .on_success(lambda s: print("All good mate!"))
               .get())
    print(content)

    """
    Another success path with [filter]
    """
    pyio = PyIO[int](10)
    content = (pyio
               .map(lambda n: n + 100)
               .filter(lambda n: n > 100)
               .flat_map(lambda n: PyIO[int](n * 2))
               .get())
    print(content)

    """
    Starting with None -> behaves like empty success; [get_or_else] recovers
    """
    pyio = PyIO[str](None)
    content = (pyio
               .map(lambda s: s.upper())  # skipped (value is None)
               .flat_map(lambda s: PyIO[str](s + "!!!"))  # skipped
               .get_or_else("Another world"))
    print(content)

    """
    Failure injected by a side-effect (division by zero), moved through the pipeline
    """
    pyio = PyIO[int](10)
    content = (pyio
               .map(lambda n: n // 0)  # raises ZeroDivisionError -> captured
               .flat_map(lambda n: PyIO[int](n * 2))  # not executed (failure propagates)
               .on_error(lambda ex: print(f"We have a side-effect because. {ex}"))
               .get_or_else(42))  # recover at the edge
    print(content)

    """
    Failure injected by a side-effect (division by zero), then use [recover] to control side-effect and 
    provide a new success value
    """
    pyio = PyIO[int](100)
    content = (pyio
               .map(lambda n: n // 0)  # raises ZeroDivisionError -> captured
               .recover(lambda ex: 200)  # recover passing a new value
               .map(lambda n: n * 10)
               .get())
    print(content)

    """
    Failure injected by a side-effect (division by zero), then use [recover_with] to control side-effect and 
    provide a new monad success value
    """
    pyio = PyIO[int](1)
    content = (pyio
               .map(lambda n: n // 0)  # raises ZeroDivisionError -> captured
               .recover_with(lambda ex: PyIO[int](10))  # recover passing a new value
               .map(lambda n: n * 10)
               .get())
    print(content)

    """
    [when] operator receive two functions, one predicate that is used to filter if the second function passed is executed or not.
    """
    pyio = PyIO[int](15)
    content = (pyio
               .when(lambda n: n > 10, lambda n: n * 100)
               .get())
    print(content)
