class NumberSearch:
    """Utility helpers related to numeric look-ups."""

    def http_family(self, code: int) -> str:
        """
        Map an HTTP status code to a human-friendly category.
        """
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
    """
    Very small sum-type demo using dataclasses + pattern matching.

    Exposes Cat and Dog dataclasses and a `touch()` method that
    returns the animal's voice.
    """

    from dataclasses import dataclass

    @dataclass
    class Cat:
        voice: str

    @dataclass
    class Dog:
        voice: str

    Animal = Cat | Dog  # type alias for convenience

    def touch(self, animal: Animal) -> str:
        """
        Return the recorded `voice` of a Cat or Dog instance.

        Parameters
        ----------
        animal : AnimalKingdom.Cat | AnimalKingdom.Dog
            Dataclass instance passed by the caller.

        """
        match animal:
            case self.Dog(voice=v):
                return v
            case self.Cat(voice=v):
                return v
        return "What animal is this?"


class LogicInMatchCase:
    """
    Pattern-matching playground for numeric business rules.
    """

    def is_specific_logic(self, seq: list[int]) -> str | bool:
        """
        Evaluate a 3-element integer list against two custom rules.

        Rules
        -----
        1. `[a, b, c]` where `c == a + b`  →  "C equal than B + C"
        2. `[a, b, c]` where `a > (b + c)` →  "A is bigger"

        """
        match seq:
            case [a, b, c] if c == a + b:
                return "C equal than B + C"
            case [a, b, c] if a > (b + c):
                return "A is bigger"
            case _:
                return "No logic detected"


class JsonScan:
    """
    Micro event router that interprets tiny JSON-like dictionaries.
    """

    def route(self, event: dict) -> str:
        """
        Translate an event dict into a log-style message.

        Recognised patterns
        -------------------
        * User login / logout
        * System login
        * Account-info requests (returns entire info payload)
        """
        match event:
            case {"type": "user", "action": "login", "id": uid}:
                return f"Logging in user {uid}"
            case {"type": "user", "action": "logout", "id": uid}:
                return f"Logging out user {uid}"
            case {"type": "system", "action": "login", "id": uid}:
                return f"Logging in system {uid}"
            case {"type": "account_info", **info}:
                return f"User info: {info}"
            case _:
                return "Unrecognized event"


if __name__ == '__main__':
    print(NumberSearch().http_family(404))

    kingdom = AnimalKingdom()
    print(kingdom.touch(AnimalKingdom.Cat("miau")))
    print(kingdom.touch(AnimalKingdom.Dog("warf")))

    logic = LogicInMatchCase()
    print(logic.is_specific_logic([3, 5, 8]))
    print(logic.is_specific_logic([4, 1, 2]))

    scanner = JsonScan()
    print(scanner.route({"type": "user", "action": "login",  "id": 1000}))
    print(scanner.route({"type": "user", "action": "logout", "id": 1000}))
    print(scanner.route({"type": "system", "action": "login", "id": 1000}))
    print(scanner.route({"type": "account_info", "username": "politron", "id": 1000}))
