# quic_dsl.py
# Comments are in English.

import asyncio
import ssl
import threading
import time
from typing import Self

from aioquic.asyncio import connect, serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived

ALPN = ["echo"]


# ----------------------------- Protocols -----------------------------

class QuicServerProtocol(QuicConnectionProtocol):
    # Echo server: read on a stream and write back to the same stream.
    def quic_event_received(self, event):
        match event:
            case HandshakeCompleted():
                pass  # nothing special to do on server handshake
            case StreamDataReceived(stream_id=stream_id, data=data, end_stream=end_stream):
                # Avoid heavy prints in production if you care about throughput
                print("[server] got:", data.decode(errors="replace"))
                self._quic.send_stream_data(stream_id, data, end_stream=end_stream)
                self.transmit()
            case _:
                pass


class QuicClientProtocol(QuicConnectionProtocol):
    """
    Persistent client protocol:
    - Opens one long-lived bidirectional stream after handshake.
    - Exposes 'ready' to signal when the stream is available.
    - Provides 'send_data' to push bytes on that persistent stream.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ready = asyncio.Event()
        self._tx_stream_id: int | None = None

    def quic_event_received(self, event):
        match event:
            case HandshakeCompleted():
                # One persistent stream for the DSL traffic
                self._tx_stream_id = self._quic.get_next_available_stream_id()
                self.ready.set()
            case StreamDataReceived(stream_id=stream_id, data=data, end_stream=end_stream):
                # Demo: print echoes; remove for performance
                print("[client] echo:", data.decode(errors="replace"))
            case _:
                pass

    def send_data(self, message: bytes, *, end_stream: bool = False) -> None:
        if self._tx_stream_id is None:
            raise RuntimeError("QUIC stream not ready yet")
        self._quic.send_stream_data(self._tx_stream_id, message, end_stream=end_stream)
        self.transmit()


# ----------------------------- DSL: Server -----------------------------

class QuicServer:
    """
    Fluent DSL (builder) for a QUIC echo server.
    Usage:
        server = (QuicServer()
                    .with_host("127.0.0.1")
                    .with_port(4433)
                    .with_cert("cert.pem")
                    .with_key("key.pem")
                    .start())
    """
    def __init__(self) -> None:
        # Defaults; can be overridden via builder methods
        self.host: str = "127.0.0.1"
        self.port: int = 4433
        self.cert: str = "cert.pem"
        self.key: str = "key.pem"
        self._thread: threading.Thread | None = None

    # ---- builder methods ----
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

        # Start QUIC server (UDP-based)
        await serve(
            self.host,
            self.port,
            configuration=cfg,
            create_protocol=QuicServerProtocol,
        )
        print(f"[server] QUIC echo up on {self.host}:{self.port} (ALPN={ALPN})")
        await asyncio.Future()  # run forever (Ctrl+C or process exit to stop)


# ----------------------------- DSL: Client -----------------------------

class QuicClient:
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
    def send_message(self, message: str, *, end_stream: bool = False) -> None:
        if not self._loop or not self._protocol:
            raise RuntimeError("Client not started")
        data = message.encode()
        fut = asyncio.run_coroutine_threadsafe(self._async_send(data, end_stream=end_stream), self._loop)
        fut.result()  # wait to propagate errors (remove if you want fire-and-forget)

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


# ----------------------------- Demo (optional) -----------------------------

if __name__ == "__main__":
    # Start server with a fluent DSL (no constructor args)
    server = (QuicServer()
              .with_host("127.0.0.1")
              .with_port(4433)
              .with_cert("cert.pem")
              .with_key("key.pem")
              .start())

    time.sleep(0.5)  # small grace so the server binds

    # Start client with a fluent DSL
    client = (QuicClient()
              .with_host("127.0.0.1")
              .with_port(4433)
              .insecure()  # dev only (self-signed certs)
              .start())

    client.send_message("Hello over QUIC!")
    client.send_message("How you doing?")
    time.sleep(2)
    client.close()

