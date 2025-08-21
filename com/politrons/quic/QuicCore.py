# Run (self-signed): python client.py --host 127.0.0.1 --port 4433 --insecure
# Or with CA/valid certs: drop --insecure and provide --server-name if needed.

import argparse
import asyncio
import ssl

from aioquic.asyncio import connect
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, HandshakeCompleted

ALPN = ["echo"]

class QuicServerProtocol(QuicConnectionProtocol):

    def quic_event_received(self, event):
        match event:
            case HandshakeCompleted():
                # Handshake finished; nothing special to do for echo server
                pass

            case StreamDataReceived(stream_id=stream_id, data=data, end_stream=end_stream):
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
    # Simple client that sends one message on handshake and prints echo
    def __init__(self, *args, message: bytes, **kwargs):
        super().__init__(*args, **kwargs)
        self._message = message
        self._stream_id = None

    def quic_event_received(self, event):
        match event:
            case HandshakeCompleted():
                # Open a new bidirectional stream and send message
                self._stream_id = self._quic.get_next_available_stream_id()
                self._quic.send_stream_data(self._stream_id, self._message, end_stream=True)
                self.transmit()

            case StreamDataReceived(stream_id=stream_id, data=data, end_stream=end_stream):
                # Print echo from server only if stream matches
                if stream_id == self._stream_id:
                    print("[client] got echo:", data.decode(errors="replace"))
                    # Close the connection politely
                    self._quic.close(error_code=0)
                    self.transmit()
            case _:
                # Ignore other event types
                pass

async def start_server(host: str, port: int, cert: str, key: str):
    # Configure QUIC server with TLS certificate
    cfg = QuicConfiguration(is_client=False, alpn_protocols=ALPN)
    cfg.load_cert_chain(certfile=cert, keyfile=key)

    # Start QUIC server (UDP-based)
    await serve(
        host,
        port,
        configuration=cfg,
        create_protocol=QuicServerProtocol,
    )
    print(f"[server] QUIC echo up on {host}:{port} (ALPN={ALPN})")
    # Keep running forever
    await asyncio.Future()

async def run_client(host: str, port: int, insecure: bool, server_name: str | None, message: str):
    # Configure QUIC client
    cfg = QuicConfiguration(is_client=True, alpn_protocols=ALPN)
    if server_name:
        cfg.server_name = server_name
    if insecure:
        # Disable certificate verification for self-signed testing
        cfg.verify_mode = ssl.CERT_NONE

    # Connect and run protocol
    async with connect(
        host,
        port,
        configuration=cfg,
        create_protocol=lambda *a, **k: QuicClientProtocol(*a, message=message.encode(), **k),
    ):
        # Keep the event loop alive until connection closes
        await asyncio.sleep(1.0)

class QuicServer:
    def __init__( self,host: str,port: int, cert:str, key:str):
        self.host = host
        self.port = port
        self.cert = cert
        self.key = key
        
    def start(self):
        asyncio.run(start_server(self.host, self.port, self.cert, self.key))


class QuicClient:
    def __init__(self, host: str, port: int, insecure: bool, server_name: str):
        self.host = host
        self.port = port
        self.insecure = insecure
        self.server_name = server_name

    def send_message(self, message: str):
        asyncio.run(run_client(self.host, self.port, self.insecure, self.server_name, message))

