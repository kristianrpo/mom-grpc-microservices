import time
import grpc
from concurrent import futures
from services.mom_service import MOMServiceServicer
from proto import mom_pb2_grpc

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
mom_pb2_grpc.add_MOMServiceServicer_to_server(
    MOMServiceServicer(), server
)

server.add_insecure_port('[::]:50051')

server.start()
print("🟢 MOM gRPC server is running on port 50051...")

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    print("🛑 Shutting down gRPC server...")
    server.stop(0)