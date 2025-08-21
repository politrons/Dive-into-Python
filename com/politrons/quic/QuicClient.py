# Run (self-signed): python client.py --host 127.0.0.1 --port 4433 --insecure
# Or with CA/valid certs: drop --insecure and provide --server-name if needed.

import argparse
import asyncio
import ssl
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived

ALPN = ["echo"]

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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=4433)
    ap.add_argument("--server-name", default=None, help="SNI/hostname for TLS; e.g., 'localhost'")
    ap.add_argument("--insecure", action="store_true", help="Disable TLS verification (self-signed)")
    ap.add_argument("--message", default="Hello over QUIC!")
    args = ap.parse_args()
    asyncio.run(run_client(args.host, args.port, args.insecure, args.server_name, args.message))
