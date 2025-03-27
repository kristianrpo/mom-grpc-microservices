from datetime import datetime
from utils.obtain_pending_data import obtain_pending_data
from queue_manager.redis_handler import RedisHandler
from proto.mom import mom_pb2, mom_pb2_grpc
from tests.microservice import microservice_pb2, microservice_pb2_grpc
import threading
import json
import grpc
class MOMServiceServicer(mom_pb2_grpc.MOMServiceServicer):
    def __init__(self):
        self.redis = RedisHandler()
        self.pubsub = self.redis.client.pubsub()
        self.pubsub.subscribe("microservices")

        threading.Thread(target=self.listen_to_microservices, daemon=True).start()

    def SavePendingService(self, request, context):
        self.redis.save_pending_request(
            service=request.service,
            client_id=request.client_id,
            task_id=request.task_id,
            payload=request.payload
        )

        return mom_pb2.SavePendingServiceResponse(
            status="pending",
            response="Task queued",
            timestamp=datetime.utcnow().isoformat()
        )
    
    def RetrievePendingService(self, request, context):
        response = self.redis.get_response(request.task_id, request.client_id)
        if response:
            self.redis.delete_task(f"response:{request.client_id}:{request.task_id}")
            return mom_pb2.RetrievePendingServiceResponse(
                status=response["status"],
                response=json.dumps(response["response"]),
                timestamp=response["timestamp"]
            )
        else:
            return mom_pb2.RetrievePendingServiceResponse(
                status="not_found",
                response="Task not found",
                timestamp=datetime.utcnow().isoformat()
            )
        
    def listen_to_microservices(self):
        for message in self.pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                service = data.get("service")
                while(True):
                    task_id, client_id, payload = obtain_pending_data(self.redis, service)
                    if(task_id is None or client_id is None or payload is None):
                        break
                    else:
                        if service == "serviceA":
                            channel = grpc.insecure_channel('localhost:50052')
                            stub = microservice_pb2_grpc.CalculatorServiceStub(channel)
                            payload = json.loads(payload)
                            request = microservice_pb2.SumNumbersParameters(
                                parameter_a=int(payload["a"]),
                                parameter_b=int(payload["b"])
                            )
                            response = stub.SumNumbers(request)
                            self.redis.save_response(task_id, client_id, response.result)
