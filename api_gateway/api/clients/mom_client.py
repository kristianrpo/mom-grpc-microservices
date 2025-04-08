import grpc
from api.generated import mom_pb2, mom_pb2_grpc
from api.config.settings import settings

class MOMClient:
    def __init__(self):
        self.channel = grpc.insecure_channel(
            f"{settings.MOM_HOST}:{settings.MOM_PORT}")
        self.stub = mom_pb2_grpc.MOMServiceStub(self.channel)

    def enqueue_task(self, task_id, client_id, service_name, payload, ttl):
        request = mom_pb2.SavePendingServiceParameters(
            task_id=task_id,
            client_id=client_id,
            service=service_name,
            time_to_live_seconds=ttl,
            payload=payload
        )
        return self.stub.SavePendingService(request)
    
    def check_task(self, task_id, client_id):
        request = mom_pb2.RetrievePendingServiceParameters(
            task_id=task_id,
            client_id=client_id
        )
        return self.stub.RetrievePendingService(request)