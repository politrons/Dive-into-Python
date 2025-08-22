# PyQuic - Simple QUIC Client/Server Library

PyQuic is a Python library that provides a simplified, fluent API for building QUIC clients and servers using the `aioquic` library. It abstracts away the complexity of QUIC protocol handling while providing a clean, builder-pattern interface for both client and server implementations.

## Features

- **Fluent Builder API**: Chain configuration methods for clean, readable code
- **Async/Threaded Architecture**: Runs QUIC operations in background threads with asyncio
- **Per-Request Streams**: Each client request uses a fresh bidirectional stream
- **Custom Handler Support**: Pluggable server-side business logic
- **TLS Support**: Built-in certificate handling with optional insecure mode for development
- **Concurrent Requests**: Multiple simultaneous requests supported on the client side

## Architecture

### Server (`PyQuicServer`)

The server uses a handler-based architecture where you provide a function to process incoming data:

```python
def handler(data: bytes) -> bytes:
    # Your business logic here
    return processed_data
```

The server runs in its own daemon thread and uses asyncio internally to handle QUIC events and execute handlers in a thread pool.

### Client (`PyQuicClient`)

The client maintains a persistent QUIC connection and allows you to send multiple concurrent requests. Each request:
- Opens a new bidirectional stream
- Sends data and closes the stream
- Returns a `concurrent.futures.Future` that resolves when the server responds

## Quick Start

### Basic Echo Server and Client

```python
import time
from py_quic import PyQuicClient, PyQuicServer

def echo_handler(data: bytes) -> bytes:
    return data  # Simple echo

# Start server
server = (PyQuicServer()
    .with_host("127.0.0.1")
    .with_port(4433)
    .with_cert("cert.pem")
    .with_key("key.pem")
    .with_handler(echo_handler)
    .start())

time.sleep(0.5)  # Let server bind

# Start client
client = (PyQuicClient()
    .with_host("127.0.0.1")
    .with_port(4433)
    .insecure()  # Skip cert verification for self-signed certs
    .start())

# Send concurrent requests
fut1 = client.send_message("Hello over QUIC!")
fut2 = client.send_message("How you doing?")

print(fut1.result())  # "Hello over QUIC!"
print(fut2.result())  # "How you doing?"

client.close()
```

## API Reference

### PyQuicServer

#### Configuration Methods (Fluent)
- `.with_host(host: str)` - Set server bind address (default: "127.0.0.1")
- `.with_port(port: int)` - Set server port (default: 4433)
- `.with_cert(cert: str)` - Set TLS certificate file path (default: "cert.pem")
- `.with_key(key: str)` - Set TLS private key file path (default: "key.pem")
- `.with_handler(fn: Callable[[bytes], bytes])` - Set request handler function

#### Lifecycle Methods
- `.start()` - Start server in background thread (non-blocking)
- `.start_and_wait()` - Start server and block current thread

#### Handler Function Signature
```python
def handler(data: bytes) -> bytes | bytearray | str | None:
    # Process incoming data
    # Return None to send no response
    # Return str/bytes/bytearray to send back to client
    pass
```

### PyQuicClient

#### Configuration Methods (Fluent)
- `.with_host(host: str)` - Set server address (default: "127.0.0.1")
- `.with_port(port: int)` - Set server port (default: 4433)
- `.with_server_name(server_name: str)` - Set SNI for TLS validation
- `.insecure(value: bool = True)` - Skip certificate verification (dev only)

#### Lifecycle Methods
- `.start()` - Connect to server and start background thread
- `.close()` - Close connection and cleanup resources

#### Request Methods
- `.send_message(message: str, *, timeout: float | None = None)` - Send message and return `Future[str]`

## Advanced Usage

### Custom Processing Handler

```python
import json

def json_processor(data: bytes) -> bytes:
    try:
        # Parse incoming JSON
        request = json.loads(data.decode())
        
        # Process request
        response = {
            "echo": request,
            "timestamp": time.time(),
            "processed": True
        }
        
        # Return JSON response
        return json.dumps(response).encode()
    except Exception as e:
        return json.dumps({"error": str(e)}).encode()

server = (PyQuicServer()
    .with_handler(json_processor)
    .start())
```

### Multiple Concurrent Requests

```python
client = PyQuicClient().with_host("example.com").start()

# Send multiple requests concurrently
futures = []
for i in range(10):
    fut = client.send_message(f"Request {i}")
    futures.append(fut)

# Collect all results
results = [fut.result() for fut in futures]
print(results)

client.close()
```

### With Timeout

```python
try:
    future = client.send_message("Hello", timeout=5.0)
    response = future.result()
    print(f"Response: {response}")
except asyncio.TimeoutError:
    print("Request timed out")
```

## Requirements

- Python 3.10+
- `aioquic` library
- TLS certificates (for production) or use `.insecure()` for development

## TLS Setup

For development, you can generate self-signed certificates:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

Then use `.insecure()` on the client to skip certificate verification.

## Performance

PyQuic achieves high-throughput concurrent request processing by leveraging QUIC's multiplexed streams over a single persistent connection.

### Benchmark Results

- **1,000 concurrent requests** completed in **0.95 seconds** (~1,052 req/sec)
- Single connection with multiplexed bidirectional streams
- Zero head-of-line blocking between concurrent requests
- Memory efficient with per-stream buffers and automatic cleanup

### Key Performance Features

- **Stream Multiplexing**: Each request uses a dedicated bidirectional stream
- **Connection Reuse**: Single QUIC connection handles all concurrent requests  
- **Concurrent Processing**: Server executes handlers in thread pool
- **Low Latency**: Benefits from QUIC's 0-RTT/1-RTT connection establishment
- **Flow Control**: Automatic QUIC-level congestion and flow management

## Protocol Details

- **ALPN**: Uses "echo" as the ALPN protocol identifier
- **Streams**: Each client request uses a new bidirectional stream
- **Flow**: Client sends data + end_stream, server responds + mirrors end_stream
- **Threading**: Server and client run in separate daemon threads with their own asyncio event loops
- **Concurrency**: Multiple streams can be active simultaneously per connection

## Error Handling

- Server handler exceptions are caught and logged (but don't crash the server)
- Client connection failures raise exceptions during `.start()`
- Request timeouts raise `asyncio.TimeoutError`
- Network errors propagate through the `Future.result()` call