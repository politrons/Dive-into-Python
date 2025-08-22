# Run: python QuicServer.py --host 0.0.0.0 --port 4433 --cert cert.pem --key key.pem

import argparse

from QuicCore import QuicServer

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=4433)
    ap.add_argument("--cert", default="cert.pem")
    ap.add_argument("--key", default="key.pem")
    args = ap.parse_args()
    server = QuicServer(args.host, args.port, args.cert, args.key)
    server.start()
