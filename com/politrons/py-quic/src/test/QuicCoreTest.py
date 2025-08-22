import time

from py_quic import PyQuicServer, PyQuicClient


def test_handler(data: bytes) -> bytes:
    return data


if __name__ == "__main__":
    # Start server with a fluent DSL (no constructor args)
    server = (PyQuicServer()
              .with_host("127.0.0.1")
              .with_port(4433)
              .with_cert("cert.pem")
              .with_key("key.pem")
              .with_handler(test_handler)
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


