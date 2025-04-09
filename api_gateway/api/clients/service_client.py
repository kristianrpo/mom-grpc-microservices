import grpc
from google.protobuf.json_format import ParseDict
from api.config.settings import settings
import re

services = settings.SERVICES

class ServiceClient:
    def __init__(self, service_name):
        self.service_name = service_name
        self.config = services.get(service_name)
        if not self.config:
            raise ValueError(f"Service '{service_name}' not configured")
        
        self.channel = grpc.insecure_channel(f"{self.config['host']}:{self.config['port']}")
        
        temp_name = re.findall(r'[A-Z][a-z]*', service_name)
        service_name = "_".join(temp_name).lower()

        grpc_module = __import__(

            f"api.generated.{service_name.lower()}_pb2_grpc",
            fromlist=[self.config["stub"]]
        )
        self.stub = getattr(grpc_module, self.config["stub"])(self.channel)
        self.proto_module = __import__(f"api.generated.{service_name.lower()}_pb2",
        fromlist=["*"] )

    def call(self, service_name, payload):
        service_config = services[service_name]

        method_name = next(iter(service_config["methods"]))

        if method_name not in service_config["methods"]:
            raise ValueError(f"Method '{method_name}' not found in service '{service_name}'")

        request_class_name = service_config["methods"][method_name]["request"]
        request_class = getattr(self.proto_module, request_class_name)
        request = ParseDict(payload, request_class())

        method = getattr(self.stub, method_name)

        return method(request)
