import concurrent.futures
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from py_quic import PyQuicClient, PyQuicServer

def test_handler(data: bytes) -> bytes:
    return data.upper()

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

    futures = []
    start = time.time()
    records = 1000
    for i in range(records):
        futures.append(client.send_message("Hello over QUIC!"))

    for result in concurrent.futures.as_completed(futures):
        print(result.result())

    print(f"Request/Response {records} of records, took {time.time() - start} seconds")
    client.close()
