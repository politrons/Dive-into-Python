# Comments in English as requested.
import grpc
from app.protos import user_pb2, user_pb2_grpc

def main() -> None:
    # Connect to the local server using an insecure channel.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.LoginUserStub(channel)
        resp = stub.Login(user_pb2.UserRequest(name="Pablo"))
        print("User info:", resp.user_info)

if __name__ == "__main__":
    main()
