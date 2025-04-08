import grpc
from google.protobuf.json_format import ParseDict
from api.config.settings import settings

services = settings.SERVICES

class ServiceClient:
    def __init__(self, service_name):
        self.service_name = service_name
        self.config = services.get(service_name)
        if not self.config:
            raise ValueError(f"Service '{service_name}' not configured")
        
        self.channel = grpc.insecure_channel(f"{self.config['host']}:{self.config['port']}")
        
        grpc_module = __import__(
            f"generated.{service_name.lower()}_pb2_grpc",
            fromlist=[self.config["stub"]]
        )
        self.stub = getattr(grpc_module, self.config["stub"])(self.channel)
        self.proto_module = __import__(f"generated.{service_name.lower()}_pb2")

    def call(self, method_name, payload):
        method_name = list(self.config["methods"].keys())[0]

        request_class = getattr(self.proto_module, self.config["methods"][method_name]["request"])
        request = ParseDict(payload, request_class())
        
        method = getattr(self.stub, method_name)
        return method(request)