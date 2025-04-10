import grpc
from concurrent import futures
import proto.sum_service.sum_service_pb2 as sum_service_pb2
import proto.sum_service.sum_service_pb2_grpc as sum_service_pb2_grpc
import redis
import json
import time
import threading
from datetime import datetime, timedelta
import sys
import os
from proto.mom import mom_pb2, mom_pb2_grpc
from proto.sum_service.sum_service_pb2_grpc import SumServiceServicer
from constants.states import states

def sumar(a, b):
    """
    Primary logic function to sum two numbers.
    
    Parameters:
        a (number): The first operand.
        b (number): The second operand.
        
    Returns:
        number: The sum of a and b.
    """
    return a + b

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

    # Create an insecure gRPC channel to the MOM service running on localhost port 50051.
    channel = grpc.insecure_channel(os.getenv("INSECURE_CHANNEL_MOM", "localhost:50051"))

    # Create a stub (client) for the MOM service.
    stub = mom_pb2_grpc.MOMServiceStub(channel)

    # Prepare the response data as a JSON-encoded string.
    response_data = json.dumps({
        "status": states["1"],
        "result": result,
        "timestamp": datetime.utcnow().isoformat()
    })

    # Create the request message using the defined proto message.
    request = mom_pb2.SaveResultServiceParameters(
        client_id=client_id,
        task_id=task_id,
        time_to_live_seconds=time_to_live_seconds,
        created_at=created_at,
        response=response_data
    )
    # Send the request to the MOM service and receive the response.
    response = stub.SaveResultService(request)
    
    # Print the MOM service's response for logging/verification.
    print("📥 MOM Response (Check Task Result):")
    print(f"Status: {response.status}")
    print(f"Response: {response.response}")
    print(f"Timestamp: {response.timestamp}")

class RedisHandler:
    """
    Helper class to interact with Redis.
    """
    def __init__(self, host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379))):
        # Initialize the Redis client with host, port, and enable string decoding.
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def publish_service_status(self, service_name, is_active=True):
        """
        Publishes the service status to a Redis channel.
        
        Parameters:
            service_name (str): The name of the service.
            is_active (bool): The active status of the service.
        """
        # Create a status message as a dictionary.
        status_message = {
            "service": service_name,
            "is_active": is_active
        }
        # Publish the JSON-encoded status message to the "microservices" channel.
        self.client.publish("microservices", json.dumps(status_message))
        print(f"📡 Published service status: {status_message}")

    def pop_next_task(self, service):
        """
        Pops the next task from the Redis queue using BLPOP.
        
        Parameters:
            service (str): The service name, used to construct the queue key.
            
        Returns:
            str or None: The task data as a string if available, otherwise None.
        """
        queue_key = f"queue:{service}"
        # Use BLPOP to block and wait for a task (with a 5-second timeout).
        task = self.client.blpop(queue_key, timeout=5)
        if task:
            # BLPOP returns a tuple: (queue_key, task_value)
            return task[1]
        return None

class SumService(SumServiceServicer):
    """
    gRPC service implementation for the SumService.
    """
    def SumNumbers(self, request, context):
        """
        Sums two numbers provided in the request and returns the result in JSON format.
        
        Parameters:
            request: The gRPC request object containing 'parameter_a' and 'parameter_b'.
            context: The gRPC context.
            
        Returns:
            SumNumbersResponse: The response message containing the result in JSON.
        """
        try:
            # Extract the parameters from the gRPC request.
            a = request.parameter_a
            b = request.parameter_b
            # Compute the sum using the helper function.
            result = sumar(a, b)
            # Prepare the result data as a dictionary.
            result_data = {
                "status": states["1"],
                "sum": result,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            # Convert the dictionary to a JSON string.
            json_result = json.dumps(result_data)
            print(f"🧮 Responding with JSON: {json_result}")
            # Return the response message.
            return sum_service_pb2.SumNumbersResponse(result=json_result)
        except Exception as e:
            # If an error occurs, prepare an error response.
            error_data = {
                "error": str(e),
                "status": "fail"
            }
            return sum_service_pb2.SumNumbersResponse(result=json.dumps(error_data))

def process_tasks(redis_handler):
    """
    Processes pending tasks from Redis using the summing logic.
    This function runs in a separate thread so as not to block the gRPC server.
    
    Parameters:
        redis_handler (RedisHandler): An instance to interact with Redis.
    """
    print("🚀 Starting Redis tasks consumer...")
    while True:
        # Retrieve the next task from the Redis queue.
        task_json = redis_handler.pop_next_task(service="SumService")
        if task_json:
            try:
                # Decode the task JSON to a Python dictionary.
                task_data = json.loads(task_json)
                
                # Retrieve TTL and created_at values from the task data.
                ttl_seconds = task_data.get("time_to_live_seconds")
                created_at = task_data.get("created_at")

                # If the created_at string ends with 'Z', remove it (indicates UTC).
                if created_at.endswith('Z'):
                    created_at = created_at[:-1]
                
                # Convert the created_at string to a datetime object.
                dt = datetime.fromisoformat(created_at)
                # Calculate the expiration datetime by adding the TTL.
                expiration_dt = dt + timedelta(seconds=ttl_seconds)

                # Check if the current UTC time is past the expiration time.
                if datetime.utcnow() > expiration_dt:
                    print("❌ Task expired, skipping...")
                    continue
                else:
                    # Decode the nested payload JSON.
                    payload = json.loads(task_data.get("payload"))
                    print(f"📥 Task received: {task_data}")
                    
                    # Extract parameters from the payload.
                    a = payload.get("parameter_a")
                    b = payload.get("parameter_b")
                    # Compute the result using the sum function.
                    result = sumar(a, b)
                    print(f"🧮 Task processed: {a} + {b} = {result}")
                    
                    # Send the computed result to the MOM service.
                    response_to_mom(
                        client_id=task_data.get("client_id"),
                        task_id=task_data.get("task_id"),
                        time_to_live_seconds=ttl_seconds,
                        created_at=task_data.get("created_at"),
                        result=result
                    )
            except Exception as e:
                # Log any exceptions that occur during task processing.
                print(f"❌ Error processing task: {e}")
        else:
            # If no task is available
            print("❌ No tasks found in the queue, waiting...")
            break

def serve():
    """
    Starts the SumService gRPC server and the Redis tasks consumer.
    """
    # Create an instance of RedisHandler to interact with Redis.
    redis_handler = RedisHandler()

    # Initialize the gRPC server with a thread pool of 10 workers.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add the SumService to the gRPC server.
    sum_service_pb2_grpc.add_SumServiceServicer_to_server(SumService(), server)
    port = os.getenv("GRPC_PORT", "50052")  # Define the port for the gRPC server.
    server.add_insecure_port(f"[::]:{port}")
    # Start the gRPC server.
    server.start()
    print(f"🚀 SumService gRPC server started on port {port}")

    # Optionally, publish the service status to Redis.
    redis_handler.publish_service_status("SumService", True)

    # Start the Redis task consumer in a separate daemon thread.
    task_thread = threading.Thread(target=process_tasks, args=(redis_handler,), daemon=True)
    task_thread.start()

    try:
        # Keep the main thread alive indefinitely.
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        # On a keyboard interrupt (Ctrl+C), gracefully stop the server.
        print("🛑 Stopping server...")
        server.stop(0)

if __name__ == "__main__":
    serve()
