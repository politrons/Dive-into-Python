from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class UserId:
    # Value-object for user identity
    value: str

    def __post_init__(self):
        v = self.value.strip()
        if not v:
            raise ValueError("UserId cannot be empty")
        object.__setattr__(self, "value", v)

@dataclass(slots=True, frozen=True)
class User:
    # Domain aggregate with immutable design
    id: UserId
    name: str

    def __post_init__(self):
        print(f"User info: {self.id} - {self.name}")

if __name__ == "__main__":
    user_id = UserId("Politrons")
    User(user_id, "Pablo")