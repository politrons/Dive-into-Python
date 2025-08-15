#!/usr/bin/env python3
# Requires: pip install aiohttp
import asyncio
from typing import Any

from aiohttp import web, ClientSession
from aiohttp.web_runner import AppRunner

ENDPOINT = "/echo"  # single allowed URI

# ---------- Server ----------

async def handler(request: web.Request) -> web.Response:
    """Single handler using structural pattern matching for method+path."""
    match (request.method, request.path):
        case ("GET", ENDPOINT):
            # Return a tiny description
            return web.json_response({"endpoint": ENDPOINT, "hint": "POST JSON to echo"})
        case ("POST", ENDPOINT):
            # Try to parse JSON body and echo it back
            try:
                data = await request.json()
            except Exception:
                return web.json_response({"error": "invalid json"}, status=400)
            return web.json_response({"echo": data})
        case _:
            return web.json_response({"error": "not found"}, status=404)

async def start_server(host: str = "127.0.0.1", port: int = 0) -> tuple[AppRunner, Any]:
    """Start aiohttp server on an ephemeral port; return (runner, real_port)."""
    app = web.Application()
    app.router.add_route("*", ENDPOINT, handler)  # route all methods to one handler
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()
    # Discover the actual port if we bound to 0 (private attr but fine for demo)
    real_port = site._server.sockets[0].getsockname()[1]
    return runner, real_port

# ---------- Client ----------

async def client_demo(host: str, port: int) -> None:
    """Hit GET /echo and POST /echo using aiohttp client."""
    base = f"http://{host}:{port}{ENDPOINT}"
    async with ClientSession() as http:
        async with http.get(base) as r:
            print("GET ->", r.status, await r.json())
        async with http.post(base, json={"hello": "Pablo", "nums": [1, 2, 3]}) as r:
            print("POST ->", r.status, await r.json())

# ---------- Main ----------

async def main() -> None:
    host = "127.0.0.1"
    runner, port = await start_server(host)
    print(f"Serving {ENDPOINT} at http://{host}:{port}{ENDPOINT}")
    await asyncio.sleep(0.05)  # tiny pause to ensure server is ready
    await client_demo(host, port)
    await runner.cleanup()
    print("Server closed.")

if __name__ == "__main__":
    asyncio.run(main())
