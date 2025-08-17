from concurrent import futures
import grpc
from app.protos import hello_pb2, hello_pb2_grpc

class Greeter(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # Build and return the response message.
        return hello_pb2.HelloReply(message=f"Hello, {request.name}!")

def main() -> None:
    # Start a simple thread-pool gRPC server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:50051")  # Insecure for demo simplicity.
    server.start()
    print("gRPC server listening on :50051")
    server.wait_for_termination()

if __name__ == "__main__":
    main()
