import asyncio
import random
import threading
import time
import uuid
from asyncio import Future
from typing import Coroutine
import concurrent.futures


async def async_task() -> str:
    time.sleep(1)
    print(threading.current_thread().name)
    return f"Hello Async world {random.randint(1, 100)}"


async def async_await():
    """When we invoke a function that contains the keyword [async] what we receive is a
    [coroutine] when that task is being executed. And in order to obtain the result for
    that computation we have to use [await]"""
    coroutine: Coroutine = async_task()
    print("Waiting for the task to finish....")
    result = await coroutine
    print(f"Async result:{result}")


async def gather():
    """[Gather] operator return a future aggregating results from the given coroutines/futures"""
    coroutine: Future = asyncio.gather(async_task(), async_task(), async_task())
    print("Waiting for the task to finish....")
    result = await coroutine
    print(f"Async result:{result}")


async def composition():
    """To make composition with [coroutines] in Python we have to just pass to another coroutine
    the one created previously in [await] the result in the thread of that coroutine, so then
    we don't have to await the computation to back to the main thread."""
    result = await func3(func2(func1()))
    print(result)


async def func1() -> str:
    return "hello"


async def func2(coroutine: Coroutine) -> str:
    return f"{await coroutine} async"


async def func3(coroutine: Coroutine) -> str:
    return f"{await coroutine} world"


def parallel_feature():
    """Python by default cannot do parallel programing, since the core of how it handle threads is
    not thread-safe. That' why we need to use [concurrent.futures] to allow us use [ProcessPoolExecutor]
    that brings the possibility to use a executor, where each [submit(function)] it will be run in one of your
    available cores."""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(func_parallel),
                   executor.submit(func_parallel),
                   executor.submit(func_parallel),
                   executor.submit(func_parallel),
                   executor.submit(func_parallel),
                   executor.submit(func_parallel),
                   executor.submit(func_parallel),
                   executor.submit(func_parallel)]

    for result in concurrent.futures.as_completed(futures):
        print(result.result())


def func_parallel() -> str:
    print(f"Running in {threading.current_thread().name}")
    time.sleep(2)
    return uuid.uuid4().hex


if __name__ == "__main__":
    """Run the async function"""
    asyncio.run(async_await())
    asyncio.run(gather())
    asyncio.run(composition())
    parallel_feature()
