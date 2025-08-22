# QuicCoreTest.py
# Comments are in English (as you asked).

import argparse
import time


def _auto_insecure(host: str, server_name: str | None) -> bool:
    """Enable insecure mode automatically for local dev when no server_name is provided."""
    if server_name:
        # If SNI is explicitly set, do not auto-disable verification
        return False
    h = (host or "").lower()
    return h == "localhost" or h == "::1" or h.startswith("127.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=4433)
    ap.add_argument("--cert", default="cert.pem")
    ap.add_argument("--key", default="key.pem")
    args = ap.parse_args()
    server = QuicServer(args.host, args.port, args.cert, args.key)



    server.start()

    ap.add_argument("--server-name", default=None, help="SNI/hostname for TLS; e.g., 'localhost'")
    ap.add_argument("--insecure", action="store_true", help="Disable TLS verification (self-signed)")
    args = ap.parse_args()

    # If you didn't pass --insecure in PyCharm and you're hitting localhost/127.0.0.1
    # without a server_name, we assume dev mode and turn insecure on automatically.
    effective_insecure = args.insecure or _auto_insecure(args.host, args.server_name)

    client = QuicClient(args.host, args.port, effective_insecure, args.server_name)
    client.send_message("Hello over QUIC!")
    client.send_message("how you doing?")
    time.sleep(10)
