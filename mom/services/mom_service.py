from datetime import datetime
from queue_manager.redis_handler import RedisHandler
from proto.mom import mom_pb2, mom_pb2_grpc
from const.states import states
import json

class MOMServiceServicer(mom_pb2_grpc.MOMServiceServicer):
    def __init__(self):
        self.redis = RedisHandler()
        print("INFO: Redis connection established.")
        print("INFO: MOMService initialized.")
        print("INFO: MOMService is ready to process requests.")

    def SavePendingService(self, request, context):

        print("INFO: Saving pending service request...")

        is_successful, error_message = self.redis.save_pending_request(
            service=request.service,
            client_id=request.client_id,
            task_id=request.task_id,
            payload=request.payload
        )

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

        print("INFO: Retrieving pending service response...")

        is_successful, response, error_message = self.redis.get_response(request.task_id, request.client_id)

        if not is_successful:

            print("ERROR: Failed to retrieve pending service response.")
            print(f"ERROR: {error_message}")

            return mom_pb2.RetrievePendingServiceResponse(
                status=states["2"],
                response="Failed to retrieve task",
                timestamp=datetime.utcnow().isoformat()
            )
        
        print("INFO: Get response works successfully.")
        
        if response:
            is_successful, error_message = self.redis.delete_task(f"response:{request.client_id}:{request.task_id}")
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
        
        else:

            print("INFO: Task not found, the task is still processing.")

            return mom_pb2.RetrievePendingServiceResponse(
                status=states["0"],
                response="Task not found",
                timestamp=datetime.utcnow().isoformat()
            )
        
    def SaveResultService(self, request, context):
        print("INFO: Saving service result...")

        is_successful, error_message = self.redis.save_response(
            task_id=request.task_id,
            client_id=request.client_id,
            response=request.response
        )

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
