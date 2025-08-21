# Run: python server.py --host 0.0.0.0 --port 4433 --cert cert.pem --key key.pem

import argparse
import asyncio
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, HandshakeCompleted

ALPN = ["echo"]  # Application-Layer Protocol Negotiation label

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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=4433)
    ap.add_argument("--cert", required=True)
    ap.add_argument("--key", required=True)
    args = ap.parse_args()
    asyncio.run(start_server(args.host, args.port, args.cert, args.key))
