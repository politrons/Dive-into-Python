
def http_family(code: int) -> str:
    """Return the human-friendly category for an HTTP status code."""
    match code:
        case 200 | 201 | 202:
            return "Success (2xx)"
        case 301 | 302 | 307 | 308:
            return "Redirect (3xx)"
        case 400 | 401 | 403 | 404:
            return "Client error (4xx)"
        case _ if 500 <= code < 600:
            return "Server error (5xx)"
        case _:
            return "Unknown / non-standard"

class AnimalKingdom:

    from dataclasses import dataclass

    @dataclass
    class Cat:
        voice: str

    @dataclass
    class Dog:
        voice: str

    Animal = Cat | Dog  # type alias

    def touch(self, animal: Animal) -> str:
        match animal:
            case self.Dog(voice=v):
                return v
            case self.Cat(voice=v):
                return v
        return "What animal is this?"


class LogicInMatchCase:
    def is_fib_triplet(self, seq: list[int]) -> str:
        match seq:
            case [a, b, c] if c == a + b:
                return "C equal than B + C"
            case [a,b,c] if a > (b + c):
                return "A is bigger"
            case _:
                return False


if __name__ == '__main__':
    print(http_family(404))

    animal_kingdom = AnimalKingdom()
    print(animal_kingdom.touch(AnimalKingdom.Cat("miau")))
    print(animal_kingdom.touch(AnimalKingdom.Dog("warf")))

    a = LogicInMatchCase()
    print(a.is_fib_triplet([3, 5, 8]))
    print(a.is_fib_triplet([4, 1, 2]))

