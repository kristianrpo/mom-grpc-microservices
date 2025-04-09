import grpc
from concurrent import futures
import proto.multiplication_service.multiplication_service_pb2 as multiplication_service_pb2
import proto.multiplication_service.multiplication_service_pb2_grpc as multiplication_service_pb2_grpc
import redis
import json
import time
import threading
from datetime import datetime, timedelta
import sys
import os
from proto.mom import mom_pb2, mom_pb2_grpc
from proto.multiplication_service.multiplication_service_pb2_grpc import MultiplicationServiceServicer

def multiply(a, b):
    """
    Primary logic function to multiply two numbers.
    
    Parameters:
        a (number): The first operand.
        b (number): The second operand.
        
    Returns:
        number: The product of a and b.
    """
    return a * b

def response_to_mom(client_id, task_id, time_to_live_seconds, created_at, result):
    """
    Sends the computed result to the MOM service via gRPC.
    
    Parameters:
        client_id (str): The ID of the client.
        task_id (str): The ID of the task.
        time_to_live_seconds (int): The TTL (in seconds) for the task.
        created_at (str): The creation timestamp of the task in ISO format.
        result (number): The computed result of the task.
    """
    channel = grpc.insecure_channel('localhost:50051')
    stub = mom_pb2_grpc.MOMServiceStub(channel)

    response_data = json.dumps({
        "status": "ok",
        "result": result,
        "timestamp": datetime.utcnow().isoformat()
    })

    request = mom_pb2.SaveResultServiceParameters(
        client_id=client_id,
        task_id=task_id,
        time_to_live_seconds=time_to_live_seconds,
        created_at=created_at,
        response=response_data
    )
    response = stub.SaveResultService(request)
    
    print("📥 MOM Response (Check Task Result):")
    print(f"Status: {response.status}")
    print(f"Response: {response.response}")
    print(f"Timestamp: {response.timestamp}")

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

    def pop_next_task(self, service):
        queue_key = f"queue:{service}"
        task = self.client.blpop(queue_key, timeout=5)
        if task:
            return task[1]
        return None

class MultiplicationService(MultiplicationServiceServicer):
    def MultiplyNumbers(self, request, context):
        try:
            a = request.parameter_a
            b = request.parameter_b
            result = multiply(a, b)
            result_data = {
                "product": result,
                "status": "ok",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            json_result = json.dumps(result_data)
            print(f"🧮 Responding with JSON: {json_result}")
            return multiplication_service_pb2.MultiplyNumbersResponse(result=json_result)
        except Exception as e:
            error_data = {
                "error": str(e),
                "status": "fail"
            }
            return multiplication_service_pb2.MultiplyNumbersResponse(result=json.dumps(error_data))

def process_tasks(redis_handler):
    print("🚀 Starting Redis tasks consumer...")
    while True:
        task_json = redis_handler.pop_next_task(service="MultiplicationService")
        if task_json:
            try:
                task_data = json.loads(task_json)
                
                ttl_seconds = task_data.get("time_to_live_seconds")
                created_at = task_data.get("created_at")

                if created_at.endswith('Z'):
                    created_at = created_at[:-1]
                
                dt = datetime.fromisoformat(created_at)
                expiration_dt = dt + timedelta(seconds=ttl_seconds)

                if datetime.utcnow() > expiration_dt:
                    print("❌ Task expired, skipping...")
                    continue
                else:
                    payload = json.loads(task_data.get("payload"))
                    print(f"📥 Task received: {task_data}")
                    
                    a = payload.get("parameter_a")
                    b = payload.get("parameter_b")
                    result = multiply(a, b)
                    print(f"🧮 Task processed: {a} * {b} = {result}")
                    
                    response_to_mom(
                        client_id=task_data.get("client_id"),
                        task_id=task_data.get("task_id"),
                        time_to_live_seconds=ttl_seconds,
                        created_at=task_data.get("created_at"),
                        result=result
                    )
            except Exception as e:
                print(f"❌ Error processing task: {e}")
        else:
            print("❌ No tasks found in the queue, waiting...")
            time.sleep(2)

def serve():
    redis_handler = RedisHandler()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    multiplication_service_pb2_grpc.add_MultiplicationServiceServicer_to_server(MultiplicationService(), server)
    port = "50053"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"🚀 MultiplicationService gRPC server started on port {port}")

    redis_handler.publish_service_status("MultiplicationService", True)

    task_thread = threading.Thread(target=process_tasks, args=(redis_handler,), daemon=True)
    task_thread.start()

    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        print("🛑 Stopping server...")
        server.stop(0)

if __name__ == "__main__":
    serve() 