from datetime import datetime, timedelta
from queue_manager.redis_handler import RedisHandler
from proto.mom import mom_pb2, mom_pb2_grpc
from constants.states import states
import json

class MOMServiceServicer(mom_pb2_grpc.MOMServiceServicer):
    def __init__(self):
        # Initialize the Redis connection
        self.redis = RedisHandler()
        print("INFO: Redis connection established.")
        print("INFO: MOMService initialized.")
        print("INFO: MOMService is ready to process requests.")

    def SavePendingService(self, request, context):
        """
        Save a pending service request to the Redis queue.
        Args:
            request: The request object containing service details.
            context: The gRPC context.
        Returns:
            A response object indicating the status of the operation.
        """

        print("INFO: Saving pending service request...")

        # Save the pending request to Redis queue of the service
        is_successful, error_message = self.redis.save_pending_request(
            service=request.service,
            client_id=request.client_id,
            task_id=request.task_id,
            time_to_live_seconds=request.time_to_live_seconds,
            payload=request.payload
        )

        # Check if the request was saved successfully to respond to the client gRPC
        if not is_successful:

            print("ERROR: Failed to save pending service request.")
            print(f"ERROR: {error_message}")

            return mom_pb2.SavePendingServiceResponse(
                status=states["2"],
                response="Failed to save task",
                timestamp=datetime.utcnow().isoformat()
            )
        
        print("INFO: Pending service request saved.")

        return mom_pb2.SavePendingServiceResponse(
            status=states["1"],
            response="Task queued",
            timestamp=datetime.utcnow().isoformat()
        )
    
    def RetrievePendingService(self, request, context):
        """
        Retrieve the result of the pending service that is created when a service goes up.
        Args:
            request: The request object containing task details.
            context: The gRPC context.
        Returns:
            A response object containing the status and response of the task.
        """

        print("INFO: Retrieving pending service response...")

        # Retrieve the response of the microservice that is saved on Redis
        is_successful, response, error_message = self.redis.get_response(request.task_id, request.client_id)

        # Check if the response was retrieved successfully (including none objects) to respond something to the client gRPC
        if not is_successful:

            print("ERROR: Failed to retrieve pending service response.")
            print(f"ERROR: {error_message}")

            return mom_pb2.RetrievePendingServiceResponse(
                status=states["2"],
                response="Failed to retrieve task",
                timestamp=datetime.utcnow().isoformat()
            )
        
        print("INFO: Get response works successfully.")
        
        # If the response is found, delete the task from Redis to avoid waiting for the ttl of the task and return the response from de microservice
        if response:

            # Delete the task from Redis
            is_successful, error_message = self.redis.delete_task(f"response:{request.client_id}:{request.task_id}")

            # Check if the task was deleted successfully to respond to the client gRPC
            if not is_successful:

                print("ERROR: Failed to delete task.")
                print(f"ERROR: {error_message}")

                return mom_pb2.RetrievePendingServiceResponse(
                    status=states["2"],
                    response="Failed to delete task",
                    timestamp=datetime.utcnow().isoformat()
                )
            
            print("INFO: Task deleted successfully from database to retrieve the response.")

            print(f"INFO: Task found from client id {request.client_id} with task id {request.task_id}, response retrieved.")

            return mom_pb2.RetrievePendingServiceResponse(
                status=response["status"],
                response=json.dumps(response["response"]),
                timestamp=response["timestamp"]
            )
        
        # If the response is not found, it means that the task is still processing 
        else:

            print("INFO: Task not found")

            return mom_pb2.RetrievePendingServiceResponse(
                status=states["0"],
                response="Task not found, the task is still processing or it was deleted because of the time to live",
                timestamp=datetime.utcnow().isoformat()
            )
        
    def SaveResultService(self, request, context):
        """
        Save the result of the microservice to Redis.
        Args:
            request: The request object containing task result details.
            context: The gRPC context.
        Returns:
            A response object indicating the status of the operation.
        """

        print("INFO: Saving service result...")

        # Obtain the creation date from the request
        creation_date_str = request.created_at

        # Check if the string ends with 'Z' and remove it
        if creation_date_str.endswith('Z'):
            creation_date_str = creation_date_str[:-1]

        # Convert the string to a datetime object
        creation_date = datetime.fromisoformat(creation_date_str)

        # Calculate current and expiration dates
        current_date = datetime.utcnow()
        expiration_date = creation_date + timedelta(seconds=int(request.time_to_live_seconds))

        # Check if the request is still available
        time_left = expiration_date - current_date
        if time_left.total_seconds() < 0:
            print("ERROR: The request is not available anymore.")
            return mom_pb2.SaveResultServiceResponse(
                status=states["2"],
                response="Request not available, time to live expired",
                timestamp=datetime.utcnow().isoformat()
            )
    
        print(f"INFO: Time left for the request: {time_left.total_seconds()} seconds")

        # Save the result of the microservice to Redis to retrieve it later
        is_successful, error_message = self.redis.save_response(
            task_id=request.task_id,
            client_id=request.client_id,
            time_to_live_seconds = int(time_left.total_seconds()),
            response=request.response
        )

        # Check if the result was saved successfully to respond to the client gRPC (in this case is the microservice)
        if not is_successful:
            print("ERROR: Failed to save service result when it goes up.")
            print(f"ERROR: {error_message}")

            return mom_pb2.SaveResultServiceResponse(
                status=states["2"],
                response="Failed to save result",
                timestamp=datetime.utcnow().isoformat()
            )

        print("INFO: Service result saved.")

        return mom_pb2.SaveResultServiceResponse(
            status=states["1"],
            response="Response saved",
            timestamp=datetime.utcnow().isoformat()
        )
