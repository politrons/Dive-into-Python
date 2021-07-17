import uuid

import pykka

"""We define the message as the contracts between the client and the actor model"""
C3PO = object()

R2D2 = object()

class Droid(pykka.ThreadingActor):
    """with [pykka] we're able to create Actor model, just like in Akka.
    We just have to create a class that has [pykka.ThreadingActor] as part of the
    class declaration.
    Then we have to implement the [on_receive] function where we expect to receive the message."""

    def __init__(self, name=uuid.uuid4().hex):
        super().__init__()
        self.name = name

    def on_receive(self, message):
        if message is C3PO:
            return f'Hi there!, I´m C3PO human cyborg relations, my register number is {self.name}'
        if message is R2D2:
            return f'Bip, bip bip bip bip {self.name}'


def fire_and_forget_pattern():
    """With this pattern we just send a message to the actor, and we don't expect any response"""
    actor_ref = Droid.start()
    actor_ref.tell(R2D2)

def request_response_pattern():
    """With this pattern, we send a message and we block the call until we receive a response from the
    actor."""
    actor_ref = Droid.start()
    answer = actor_ref.ask(C3PO, block=True)
    print(f"Request-Response:{answer}")

def ask_pattern():
    """With this pattern, we send a message and we receive a [future] with the future response of
    the communication with the actor.
    In order to [await] for the response, we use [get] operator, that block the main thread until
    get the response."""
    actor_ref = Droid.start()
    future = actor_ref.ask(R2D2, block=False)
    print(f"Ask:{future}")
    print(f"Ask:{future.get()}")


def akka_future():
    """With ask pattern and unblock future we can use some operators like [map] to transform values
    or [filter] to filter some values"""
    actor_ref = Droid.start()
    future_1 = actor_ref.ask(C3PO, block=False) \
        .map(lambda res: res.upper())
    future_2 = actor_ref.ask(R2D2, block=False) \
        .filter(lambda res: "bip" in res)
    print(future_1.get(10))
    print(future_2.get(10))


if __name__ == "__main__":
    fire_and_forget_pattern()
    request_response_pattern()
    ask_pattern()
    akka_future()
