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

