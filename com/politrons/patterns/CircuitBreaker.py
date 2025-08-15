# pip install aiohttp aiobreaker
import asyncio
from typing import Any

from aiohttp import web, ClientSession
from aiobreaker import CircuitBreaker
from datetime import timedelta

from aiohttp.web_runner import AppRunner

ENDPOINT = "/hello_circuit_breaker"


# ---- Server: single endpoint; return 500 if {"fail": true} to demo the breaker
async def handler(request: web.Request) -> web.Response:
    data = await (request.json() if request.method == "POST" else asyncio.sleep(0, result={}))
    match (request.method, request.path):
        case ("POST", ENDPOINT):
            if isinstance(data, dict) and data.get("fail"):
                return web.json_response({"error": "boom"}, status=500)
            return web.json_response({"response": data})
        case _:
            return web.json_response({"error": "not found"}, status=404)


async def start_server(host: str = "127.0.0.1", port: int = 0) -> tuple[AppRunner, Any]:
    app = web.Application()
    app.router.add_route("*", ENDPOINT, handler)
    runner = web.AppRunner(app);
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port);
    await site.start()
    real_port = site._server.sockets[0].getsockname()[1]
    return runner, real_port


# ---- Client with circuit breaker
breaker = CircuitBreaker(
    fail_max=3,  # open after 3 consecutive failures
    timeout_duration=timedelta(seconds=5)  # half-open after 5s
)


@breaker  # <-- Circuit breaker wraps the outbound call
async def post_with_circuit_breaker(base_url: str, payload: dict) -> Any:
    """POST to [ENDPOINT] and return parsed JSON."""
    async with ClientSession() as http:
        async with http.post(base_url, json=payload, timeout=3) as r:
            r.raise_for_status()
            return await r.json()


async def main():
    host = "127.0.0.1"
    runner, port = await start_server(host)
    base = f"http://{host}:{port}{ENDPOINT}"

    # A few failing calls to trip the breaker
    for i in range(3):
        try:
            await post_with_circuit_breaker(base, {"fail": True})
        except Exception as e:
            print("failure:", type(e).__name__, str(e))

    # While open, calls are short-circuited immediately
    try:
        await post_with_circuit_breaker(base, {"msg": "should skip"})
    except Exception as e:
        print("circuit open:", type(e).__name__)

    # Wait reset_timeout and succeed (closes breaker)
    await asyncio.sleep(5.2)
    print("success ->", await post_with_circuit_breaker(base, {"hello": "Pablo"}))

    await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
