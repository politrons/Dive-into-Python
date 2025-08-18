


if __name__ == "__main__":
    from pyio_effect.core import PyIO

    pyio = PyIO[str]("Hello world")
    content = (pyio
               .map(lambda s: s.upper())  # side-effect captured if it throws
               .flat_map(lambda s: PyIO[str](s + "!!!"))  # returns PyIO, may fail too
               .on_success(lambda s: print("All good mate!"))
               .get())
    print(content)
