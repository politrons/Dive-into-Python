# Comments in English as requested.
import grpc
from app.protos import hello_pb2, hello_pb2_grpc

def main() -> None:
    # Connect to the local server using an insecure channel.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        resp = stub.SayHello(hello_pb2.HelloRequest(name="Pablo"))
        print("Server says:", resp.message)

if __name__ == "__main__":
    main()
