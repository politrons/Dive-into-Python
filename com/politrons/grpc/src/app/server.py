from concurrent import futures
import grpc
from app.protos import user_pb2, user_pb2_grpc

class PrintInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        print(f"[Interceptor] RPC called: {handler_call_details.method}")
        return continuation(handler_call_details)

class LoginUserService(user_pb2_grpc.LoginUserServicer):
    def Login(self, request, context):
        print("[Handler] Executing Login method")
        return user_pb2.UserResponse(user_info=f"Politrons, {request.name} logged!")

def main() -> None:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[PrintInterceptor()]  #here we pass our interceptor
    )
    user_pb2_grpc.add_LoginUserServicer_to_server(LoginUserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server listening on :50051")
    server.wait_for_termination()

if __name__ == "__main__":
    main()
