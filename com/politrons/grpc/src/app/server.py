# src/app/server.py
# Comments in English as requested.
from concurrent import futures
import grpc
from app.protos import user_pb2, user_pb2_grpc

class LoginUserService(user_pb2_grpc.LoginUserServicer):
    # Must match the RPC name in the .proto: "Login"
    def Login(self, request, context):
        # Build and return the response message.
        print("Login request:", request)
        return user_pb2.UserResponse(user_info=f"Politrons, {request.name} logged!")

def main() -> None:
    # Start a simple thread-pool gRPC server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Register our service implementation with the server.
    user_pb2_grpc.add_LoginUserServicer_to_server(LoginUserService(), server)
    server.add_insecure_port("[::]:50051")  # Insecure for demo simplicity.
    server.start()
    print("gRPC server listening on :50051")
    server.wait_for_termination()

if __name__ == "__main__":
    main()
