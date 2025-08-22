import ssl
import threading
from collections.abc import Callable
from typing import Self

from aioquic.asyncio import connect, serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived

ALPN = ["echo"]

# ----------------------------- Protocols -----------------------------

# at top
import asyncio


class QuicServerProtocol(QuicConnectionProtocol):
    """
    Server protocol that delegates business logic to an injected handler.

    Handler signature:
        handler(data: bytes, end_stream: bool) -> bytes | bytearray | str | Awaitable[bytes|bytearray|str]
    If the handler returns None, no response is sent for that chunk.
    """

    def __init__(self, *args, handler: Callable[[bytes], bytes] = None, **kwargs):
        super().__init__(*args, **kwargs)
        # Default handler is identity (echo)
        self._handler = handler

    def quic_event_received(self, event):
        match event:
            case HandshakeCompleted():
                pass  # nothing to do
            case StreamDataReceived(stream_id=stream_id, data=data, end_stream=end_stream):
                # Offload to an async task so we can await (async handler or executor)
                asyncio.get_running_loop().create_task(
                    self._apply_handler_and_reply(stream_id, data, end_stream)
                )
            case _:
                pass

    async def _apply_handler_and_reply(self, stream_id: int, data: bytes, end_stream: bool):
        """Apply business handler and send its result back on the same stream."""
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, self._handler, data)

            if result is None:
                return  # no reply for this chunk

            # Normalize to bytes
            if not isinstance(result, (bytes, bytearray)):
                result = str(result).encode()

            # Send reply on same stream; mirror end_stream so client sees closure
            self._quic.send_stream_data(stream_id, bytes(result), end_stream=end_stream)
            self.transmit()

        except Exception as exc:
            # Optional: log/metrics; avoid raising inside protocol callback
            # print(f"[server] handler error: {exc}")
            pass


class QuicClientProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ready = asyncio.Event()
        self._tx_stream_id: int | None = None  # unused with per-request streams, but harmless
        # --- NEW: pending requests by stream_id + per-stream buffers ---
        self._pending: dict[int, asyncio.Future[bytes]] = {}
        self._buffers: dict[int, bytearray] = {}

    def quic_event_received(self, event):
        match event:
            case HandshakeCompleted():
                # Connection is ready; no need to pre-open a stream for this approach
                self.ready.set()

            case StreamDataReceived(stream_id=stream_id, data=data, end_stream=end_stream):
                # Accumulate data per stream until end_stream, then fulfill the matching Future
                buf = self._buffers.setdefault(stream_id, bytearray())
                buf.extend(data)
                if end_stream:
                    fut = self._pending.pop(stream_id, None)
                    body = bytes(buf)
                    self._buffers.pop(stream_id, None)
                    if fut and not fut.done():
                        fut.set_result(body)

            case _:
                pass

    # --- NEW: fire a request on its own bidirectional stream and return a Future[bytes] ---
    def start_request(self, payload: bytes, *, end_stream: bool = True) -> asyncio.Future[bytes]:
        """
        Open a new bidirectional stream, send payload, and return a Future that resolves
        with the echoed response bytes when the server closes the stream.
        Must be called on the connection's event loop.
        """
        loop = asyncio.get_running_loop()
        stream_id = self._quic.get_next_available_stream_id()
        fut: asyncio.Future[bytes] = loop.create_future()
        self._pending[stream_id] = fut
        self._buffers[stream_id] = bytearray()
        self._quic.send_stream_data(stream_id, payload, end_stream=end_stream)
        self.transmit()
        return fut


# ----------------------------- DSL: Server -----------------------------

class PyQuicServer:
    def __init__(self) -> None:
        self.host: str = "127.0.0.1"
        self.port: int = 4433
        self.cert: str = "cert.pem"
        self.key: str = "key.pem"
        self._thread: threading.Thread | None = None
        self._handler = None

    # --- builder methods ---
    def with_handler(self, fn: Callable[[bytes], bytes]) -> Self:
        """Set the business logic handler. If it's CPU/blocking, pass blocking=True."""
        self._handler = fn
        return self

    def with_host(self, host: str) -> Self:
        self.host = host
        return self

    def with_port(self, port: int) -> Self:
        self.port = port
        return self

    def with_cert(self, cert: str) -> Self:
        self.cert = cert
        return self

    def with_key(self, key: str) -> Self:
        self.key = key
        return self

    # ---- lifecycle ----
    def start(self) -> Self:
        # Run the server in its own thread because asyncio.run(...) blocks.
        if self._thread and self._thread.is_alive():
            return self
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    def start_and_wait(self) -> Self:
        asyncio.run(self._start_server())

    def _run(self) -> None:
        asyncio.run(self._start_server())

    async def _start_server(self) -> None:
        cfg = QuicConfiguration(is_client=False, alpn_protocols=ALPN)
        cfg.load_cert_chain(certfile=self.cert, keyfile=self.key)

        # Pass handler into each protocol instance
        await serve(
            self.host,
            self.port,
            configuration=cfg,
            create_protocol=lambda *a, **k: QuicServerProtocol(
                *a,
                handler=self._handler,
                **k
            ),
        )
        print(f"[server] QUIC echo up on {self.host}:{self.port} (ALPN={ALPN})")
        await asyncio.Future()


# ----------------------------- DSL: Client -----------------------------

class PyQuicClient:
    """
    Fluent DSL (builder) for a persistent QUIC client.
    Usage:
        client = (QuicClient()
                    .with_host("127.0.0.1")
                    .with_port(4433)
                    .insecure()                     # for self-signed server certs
                    .start())

        client.send_message("Hello")
        client.close()
    """

    def __init__(self) -> None:
        # Defaults; can be overridden via builder methods
        self.host: str = "127.0.0.1"
        self.port: int = 4433
        self.server_name: str | None = None
        self._insecure: bool = False

        # Runtime fields
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._connect_cm = None
        self._protocol: QuicClientProtocol | None = None

    # ---- builder methods ----
    def with_host(self, host: str) -> Self:
        self.host = host
        return self

    def with_port(self, port: int) -> Self:
        self.port = port
        return self

    def with_server_name(self, server_name: str) -> Self:
        # SNI to validate TLS when not using --insecure
        self.server_name = server_name
        return self

    def insecure(self, value: bool = True) -> Self:
        # Skip certificate verification (DEV ONLY)
        self._insecure = value
        return self

    # ---- lifecycle ----
    def start(self) -> Self:
        if self._loop and self._thread and self._thread.is_alive():
            return self
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        # Connect once and wait until handshake + stream are ready
        fut = asyncio.run_coroutine_threadsafe(self._async_connect(), self._loop)
        fut.result()  # raise if connect fails
        return self

    def close(self) -> None:
        # Minimal/clean close; for dev you could skip and let process exit.
        if not self._loop:
            return

        async def _do_close():
            if self._protocol is not None:
                self._protocol._quic.close(error_code=0)
                self._protocol.transmit()
            if self._connect_cm is not None:
                await self._connect_cm.__aexit__(None, None, None)

        fut = asyncio.run_coroutine_threadsafe(_do_close(), self._loop)
        try:
            fut.result(timeout=2)
        except Exception:
            pass

        self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join(timeout=2)

        self._protocol = None
        self._connect_cm = None
        self._loop = None
        self._thread = None

    def _run_loop(self) -> None:
        assert self._loop is not None
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    # ---- public API ----
    def send_message(self, message: str, *, timeout: float | None = None):
        """
        Send a message over a fresh QUIC stream and return a concurrent.futures.Future[str]
        that resolves with the echoed response. Call .result() to block if needed.
        """
        if not self._loop or not self._protocol:
            raise RuntimeError("Client not started")
        data = message.encode()
        return asyncio.run_coroutine_threadsafe(
            self._async_request(data, timeout=timeout),
            self._loop,
        )

    # ---- internals (async, run in background loop) ----
    async def _async_request(self, data: bytes, *, timeout: float | None) -> str:
        assert self._protocol is not None
        fut_bytes = self._protocol.start_request(data, end_stream=True)  # end stream so server mirrors it
        if timeout is not None:
            body = await asyncio.wait_for(fut_bytes, timeout)
        else:
            body = await fut_bytes
        return body.decode(errors="replace")

    # ---- internals (async, run in background loop) ----
    async def _async_connect(self) -> None:
        cfg = QuicConfiguration(is_client=True, alpn_protocols=ALPN)
        if self.server_name:
            cfg.server_name = self.server_name
        if self._insecure:
            cfg.verify_mode = ssl.CERT_NONE

        self._connect_cm = connect(
            self.host,
            self.port,
            configuration=cfg,
            create_protocol=QuicClientProtocol,
        )
        self._protocol = await self._connect_cm.__aenter__()
        await self._protocol.ready.wait()

    async def _async_send(self, data: bytes, *, end_stream: bool) -> None:
        assert self._protocol is not None
        self._protocol.send_data(data, end_stream=end_stream)
