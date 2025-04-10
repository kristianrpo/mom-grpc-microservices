import time
import grpc
from concurrent import futures
from services.mom_service import MOMServiceServicer
from proto.mom import mom_pb2_grpc
import os

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
mom_pb2_grpc.add_MOMServiceServicer_to_server(
    MOMServiceServicer(), server
)

port = os.getenv("GRPC_PORT", "50051")

server.add_insecure_port(f'[::]:{port}')

server.start()
print("🟢 MOM gRPC server is running on port 50051...")

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    print("🛑 Shutting down gRPC server...")
    server.stop(0)