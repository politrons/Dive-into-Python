# Bootstrap import for src/ layout
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from py_quic import PyQuicClient, PyQuicServer

if __name__ == "__main__":
    # Start server with a fluent DSL (no constructor args)
    server = (PyQuicServer()
              .with_host("127.0.0.1")
              .with_port(4433)
              .with_cert("cert.pem")
              .with_key("key.pem")
              .start())

    time.sleep(0.5)  # small grace so the server binds

    # Start client with a fluent DSL
    client = (PyQuicClient()
              .with_host("127.0.0.1")
              .with_port(4433)
              .insecure()  # dev only (self-signed certs)
              .start())

    fut1 = client.send_message("Hello over QUIC!")
    fut2 = client.send_message("How you doing?")
    print(fut1.result())
    print(fut2.result())
    client.close()
