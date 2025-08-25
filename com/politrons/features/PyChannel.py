# Comments are in English.

import asyncio
from typing import Generic, TypeVar

T = TypeVar("T")

class PyChannel(Generic[T]):
    """A small channel wrapper over asyncio.Queue."""
    def __init__(self, maxsize: int = 0) -> None:
        # maxsize=0 => unbounded; >0 => bounded (backpressure)
        self._queue: asyncio.Queue[T] = asyncio.Queue(maxsize=maxsize)

    async def send(self, item: T) -> None:
        """Suspend until there's space if bounded."""
        await self._queue.put(item)

    async def receive(self) -> T:
        """Suspend until an item is available."""
        return await self._queue.get()


#  Main
# ---------

async def simple_channel() -> None:
    channel: PyChannel[str] = PyChannel()

    async def producer():
        print(f"Sending data from task {asyncio.current_task().get_name()}")
        await channel.send("Hello world from another coroutine, traveling in a channel")

    async def consumer():
        print(f"Receiving data from task {asyncio.current_task().get_name()}")
        msg = await channel.receive()
        print(f"Data: {msg}")

    # Launch both coroutines concurrently.
    cons = asyncio.create_task(consumer(), name="consumer")
    prod = asyncio.create_task(producer(), name="producer")
    await asyncio.gather(prod, cons)

if __name__ == "__main__":
    asyncio.run(simple_channel())
