#  gRPC “LoginUser” 

## Overview
This project demonstrates a minimal gRPC setup in Python.  
The client sends a simple request with a username, and the server responds with a message confirming that the user has logged in.

---

## Proto definition
The `user.proto` file defines:
- A **package** named `user`.
- A **service** called `LoginUser` with a single RPC method `Login`.
- A **request message** `UserRequest` containing one field: `name`.
- A **response message** `UserResponse` containing one field: `user_info`.

When compiled with `grpcio-tools`, this generates two files:
- `user_pb2.py` → contains the Python classes for the messages (`UserRequest`, `UserResponse`).
- `user_pb2_grpc.py` → contains the client stub (`LoginUserStub`), the server base class (`LoginUserServicer`), and a helper to register the service (`add_LoginUserServicer_to_server`).

---

## Server description
The server:
- Implements the `LoginUserServicer` base class generated from the proto.
- Provides the logic for the `Login` method, building a `UserResponse` using the incoming `UserRequest`.
- Runs a gRPC server, registers the implementation, and listens on a given port (e.g., `50051`).
- Includes an **interceptor** that prints a message whenever an RPC is invoked, then continues execution normally. This allows you to add simple logging or cross-cutting concerns without changing the service logic.

---

## Client description
The client:
- Creates a gRPC channel to the server.
- Uses the generated `LoginUserStub` to access the `Login` RPC method.
- Sends a `UserRequest` with the username and receives a `UserResponse` from the server.
- Prints the `user_info` field from the response.

---

## Run instructions
1. Generate the Python stubs with `grpcio-tools` from the `user.proto`.
2. Start the server process so it listens for incoming requests (with the interceptor attached).
3. Run the client process, which will connect to the server and invoke the `Login` method.
4. The client will print the response message received from the server.

---

## Expected behavior
- **Interceptor:** logs the RPC method name whenever a call is made.
- **Server side:** logs the incoming request showing the user’s name and builds the response.
- **Client side:** prints a response like `User info: Politrons, Pablo logged!`.
