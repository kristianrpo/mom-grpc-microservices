import grpc
from google.protobuf.json_format import ParseDict
from config.settings import SERVICES

class ServiceClient:
    def __init__(self, service_name):
        self.service_name = service_name
        self.config = SERVICES.get(service_name)
        if not self.config:
            raise ValueError(f"Service '{service_name}' not configured")
        
        self.channel = grpc.insecure_channel(f"{self.config['host']}:{self.config['port']}")
        
        # Importar dinámicamente el stub (ej: calculator_pb2_grpc)
        grpc_module = __import__(
            f"generated.{service_name.lower()}_pb2_grpc",
            fromlist=[self.config["stub"]]
        )
        self.stub = getattr(grpc_module, self.config["stub"])(self.channel)
        self.proto_module = __import__(f"generated.{service_name.lower()}_pb2")

    def call(self, method_name, payload):
        if method_name not in self.config["methods"]:
            raise ValueError(f"Method '{method_name}' not found in {self.service_name}")
        
        # Convertir JSON a protobuf
        request_class = getattr(self.proto_module, self.config["methods"][method_name]["request"])
        request = ParseDict(payload, request_class())
        
        # Llamar al método gRPC
        method = getattr(self.stub, method_name)
        return method(request)