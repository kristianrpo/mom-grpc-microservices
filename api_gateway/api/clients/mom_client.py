import grpc
from api.generated import mom_pb2, mom_pb2_grpc
from api.config.settings import settings

class MOMClient:
    """
    Client for interacting with the MOM (Message Oriented Middleware) service via gRPC.
    """
    def __init__(self):
        self.channel = grpc.insecure_channel(
            f"{settings.MOM_HOST}:{settings.MOM_PORT}")
        self.stub = mom_pb2_grpc.MOMServiceStub(self.channel)

    def enqueue_task(self, task_id, client_id, service_name, payload, ttl):
        """
        Enqueue a task to the MOM system for asynchronous processing.

        Args:
            task_id (str): The unique identifier for the task.
            client_id (str): The identifier of the client requesting the service.
            service_name (str): The name of the service to be called.
            payload (str): The serialized payload to process.
            ttl (int): Time-to-live in seconds for the pending task.

        Returns:
            SavePendingServiceResponse: The response from the MOM service after enqueueing the task.
        """
        request = mom_pb2.SavePendingServiceParameters(
            task_id=task_id,
            client_id=client_id,
            service=service_name,
            time_to_live_seconds=ttl,
            payload=payload
        )
        return self.stub.SavePendingService(request)
    
    def check_task(self, task_id, client_id):
        """
        Check the status of a previously enqueued task in the MOM system.

        Args:
            task_id (str): The unique identifier of the task.
            client_id (str): The identifier of the client who initiated the task.

        Returns:
            RetrievePendingServiceResponse: The response containing the status and result of the task.
        """
        request = mom_pb2.RetrievePendingServiceParameters(
            task_id=task_id,
            client_id=client_id
        )
        return self.stub.RetrievePendingService(request)