# Comments in English as requested.
from pathlib import Path
from grpc_tools import protoc

ROOT = Path(__file__).resolve().parents[1]
PROTO_DIR = ROOT / "src" / "app" / "protos"

def main() -> None:
    # Drive protoc via Python so it's cross-platform and IDE-friendly.
    args = [
        "protoc",                      # dummy argv[0]
        f"-I{PROTO_DIR}",              # include path
        f"--python_out={PROTO_DIR}",   # messages
        f"--grpc_python_out={PROTO_DIR}",  # stubs
        str(PROTO_DIR / "user.proto"),
    ]
    protoc.main(args)
    print("Generated hello_pb2.py and hello_pb2_grpc.py")

if __name__ == "__main__":
    main()
