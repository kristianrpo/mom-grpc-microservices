import grpc
from concurrent import futures
import tests.microservice.microservice_pb2 as calculator_pb2
import tests.microservice.microservice_pb2_grpc as calculator_pb2_grpc
import redis
import json
import time

class RedisHandler:
    def __init__(self, host="localhost", port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def publish_service_status(self, service_name, is_active=True):
        status_message = {
            "service": service_name,
            "is_active": is_active
        }
        self.client.publish("microservices", json.dumps(status_message))
        print(f"📡 Published service status: {status_message}")

class CalculatorService(calculator_pb2_grpc.CalculatorServiceServicer):
    def SumNumbers(self, request, context):
        try:
            a = request.parameter_a
            b = request.parameter_b
            result_data = {
                "sum": a + b,
                "status": "ok",
                "timestamp": "2025-03-27T15:00:00Z"
            }

            json_result = json.dumps(result_data)
            print(f"🧮 Responding with JSON: {json_result}")
            return calculator_pb2.SumNumbersResponse(result=json_result)

        except Exception as e:
            error_data = {
                "error": str(e),
                "status": "fail"
            }
            return calculator_pb2.SumNumbersResponse(result=json.dumps(error_data))

def serve():
    redis_handler = RedisHandler()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServiceServicer_to_server(CalculatorService(), server)

    port = "50052"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"🚀 CalculatorService gRPC server started on port {port}")
    
    try:
        redis_handler.publish_service_status("serviceA", is_active=True)
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        print("🛑 Stopping server...")
        server.stop(0)

if __name__ == "__main__":
    serve()
