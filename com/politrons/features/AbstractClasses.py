from abc import ABC, abstractmethod

class Greeter(ABC):
    """Abstract base class: every subclass must implement hello_world."""

    @abstractmethod
    def hello_world(self) -> None:
        """Print or return a greeting."""
        pass


class EnglishGreeter(Greeter):
    # Concrete implementation of the required method
    def hello_world(self) -> None:
        print("Hello, world!")


class SpanishGreeter(Greeter):
    # Another valid implementation
    def hello_world(self) -> None:
        print("¡Hola, mundo!")


if __name__ == "__main__":
    # Instantiate the concrete greeters
    en = EnglishGreeter()
    es = SpanishGreeter()

    # Call the mandatory method
    en.hello_world()  # -> Hello, world!
    es.hello_world()  # -> ¡Hola, mundo!

    # Uncommenting the following class will raise an error,
    # because it does NOT implement hello_world.
    #
    # class BadGreeter(Greeter):
    #     pass
    #
    # BadGreeter()  # TypeError: Can't instantiate abstract class...
