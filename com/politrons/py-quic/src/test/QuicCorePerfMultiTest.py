import concurrent.futures
import pathlib
import sys
import time

from py_quic import PyQuicClient, PyQuicServer


def test_handler_1(data: bytes) -> bytes:
    return ((PyQuicClient()
             .with_host("127.0.0.1")
             .with_port(4434)
             .insecure()  # dev only (self-signed certs)
             .start())
            .send_message(data.decode()).result())


def test_handler_2(data: bytes) -> bytes:
    return ((PyQuicClient()
             .with_host("127.0.0.1")
             .with_port(4435)
             .insecure()  # dev only (self-signed certs)
             .start())
            .send_message(data.decode()).result())


def test_handler_3(data: bytes) -> bytes:
    return data.upper()


if __name__ == "__main__":
    # Start server with a fluent DSL (no constructor args)
    (PyQuicServer()
     .with_host("127.0.0.1")
     .with_port(4433)
     .with_cert("cert.pem")
     .with_key("key.pem")
     .with_handler(test_handler_1)
     .start())

    (PyQuicServer()
     .with_host("127.0.0.1")
     .with_port(4434)
     .with_cert("cert.pem")
     .with_key("key.pem")
     .with_handler(test_handler_2)
     .start())

    (PyQuicServer()
     .with_host("127.0.0.1")
     .with_port(4435)
     .with_cert("cert.pem")
     .with_key("key.pem")
     .with_handler(test_handler_3)
     .start())

    time.sleep(0.5)  # small grace so the server binds

    # Start client with a fluent DSL
    client = (PyQuicClient()
              .with_host("127.0.0.1")
              .with_port(4433)
              .insecure()  # dev only (self-signed certs)
              .start())

    futures = []
    start = time.time()
    records = 100
    for i in range(records):
        futures.append(client.send_message("Hello over QUIC!"))

    for result in concurrent.futures.as_completed(futures):
        print(result.result())

    print(f"Request/Response {records} of records, took {time.time() - start} seconds")
    client.close()
