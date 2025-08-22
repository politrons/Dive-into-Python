
import asyncio
import ssl
import threading
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol

ALPN = ["echo"]

class QuicServerProtocol(QuicConnectionProtocol):

    def quic_event_received(self, event):
        match event:
            case HandshakeCompleted():
                # Handshake finished; nothing special to do for echo server
                pass

            case StreamDataReceived(stream_id=stream_id, data=data, end_stream=end_stream):
                print("[server] sending data:", data.decode(errors="replace"))
                # Echo the incoming bytes back to the same stream
                self._quic.send_stream_data(
                    stream_id,
                    data,
                    end_stream=end_stream,  # close our side if client closed
                )
                self.transmit()  # Flush pending packets to the network

            case _:
                # Ignore other event types (connection events, datagrams, etc.)
                pass

class QuicClientProtocol(QuicConnectionProtocol):
    """
    Persistent client protocol:
    - Keeps a single bidirectional stream open for the app.
    - Exposes 'ready' event so the outer client can wait until handshake+stream open.
    - Provides 'send_bytes' to push data on the persistent stream.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ready = asyncio.Event()
        self._tx_stream_id: int | None = None

    def quic_event_received(self, event):
        match event:
            case HandshakeCompleted():
                # Open a single long-lived bidirectional stream for app traffic
                self._tx_stream_id = self._quic.get_next_available_stream_id()
                self.ready.set()

            case StreamDataReceived(stream_id=stream_id, data=data, end_stream=end_stream):
                # Avoid printing on hot path; it will throttle throughput.
                # Replace with metrics/counters if you need to observe responses.
                print("[client] got echo:", data.decode(errors="replace"))
                pass
            case _:
                pass

    def send_data(self, message: bytes, *, end_stream: bool = False) -> None:
        """Send bytes on the persistent stream."""
        if self._tx_stream_id is None:
            raise RuntimeError("QUIC stream not ready yet")
        print("[client] sending data:", message.decode(errors="replace"))
        self._quic.send_stream_data(self._tx_stream_id, message, end_stream=end_stream)
        self.transmit()


class QuicServer:
    def __init__( self,host: str,port: int, cert:str, key:str):
        self.host = host
        self.port = port
        self.cert = cert
        self.key = key

    def start(self):
        asyncio.run(self._start_server())

    async def _start_server(self):
        # Configure QUIC server with TLS certificate
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
        # Keep running forever
        await asyncio.Future()

class QuicClient:
    """
    Keep one QUIC connection alive in a background asyncio loop.
    DSL calls send_message() whenever it wants (no busy loop, no reconnects).
    """
    def __init__(self, host: str, port: int, insecure: bool, server_name: str | None):
        self.host = host
        self.port = port
        self.insecure = insecure
        self.server_name = server_name

        # We create a new event loop where to keep the client connection open
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

        self._connect_cm = None
        self._protocol = None

        # Connect once and wait until handshake + stream are ready
        fut = asyncio.run_coroutine_threadsafe(self._async_connect(), self._loop)
        fut.result()  # raises if connect fails

    def _run_loop(self):
        # Dedicated event loop for QUIC IO
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def send_message(self, message: str, *, end_stream: bool = False):
        # Thread-safe: schedule the send in the background loop
        if self._protocol is None:
            raise RuntimeError("Client not connected")
        data = message.encode()
        asyncio.run(self._async_send(data, end_stream=end_stream))

    # ---------- async internals running on the background loop ----------

    async def _async_connect(self):
        cfg = QuicConfiguration(is_client=True, alpn_protocols=ALPN)
        if self.server_name:
            cfg.server_name = self.server_name
        if self.insecure:
            cfg.verify_mode = ssl.CERT_NONE

        # Keep the context manager open as long as the client lives
        self._connect_cm = connect(
            self.host,
            self.port,
            configuration=cfg,
            create_protocol=QuicClientProtocol,
        )
        self._protocol = await self._connect_cm.__aenter__()
        # Wait until protocol signals handshake done and stream opened
        await self._protocol.ready.wait()

    async def _async_send(self, data: bytes, *, end_stream: bool):
        # Use the persistent stream exposed by protocol
        self._protocol.send_data(data, end_stream=end_stream)

