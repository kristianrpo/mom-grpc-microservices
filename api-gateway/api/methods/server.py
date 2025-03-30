import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import grpc
from concurrent import futures
import time
from api.methods import service_pb2, service_pb2_grpc

class MyServiceServicer(service_pb2_grpc.MyServiceServicer):
    def SayHello(self, request, context):
        return service_pb2.ResponseMessage(message=f"Hello, {request.name}!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("🚀 gRPC Server running on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
