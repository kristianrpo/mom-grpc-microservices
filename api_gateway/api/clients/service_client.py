import grpc
from google.protobuf.json_format import ParseDict
from api.config.settings import settings
import re

services = settings.SERVICES

class ServiceClient:
    """
    Generic gRPC client for dynamically interacting with configured services.
    """
    def __init__(self, service_name):
        """
        Initialize the ServiceClient for a specific service.

        Args:
            service_name (str): The name of the service to connect to.

        Raises:
            ValueError: If the service is not configured in settings.
        """
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

    def call(self, method_name, payload):
        """
        Call a method on the service stub with the given payload.

        Args:
            method_name (str): The name of the method to call.
            payload (dict): The payload to send, as a dictionary.

        Returns:
            google.protobuf.message.Message: The response from the gRPC service.
        """
        method_name = list(self.config["methods"].keys())[0]

        request_class = getattr(self.proto_module, self.config["methods"][method_name]["request"])

        request = ParseDict(payload, request_class())
        
        method = getattr(self.stub, method_name)

        return method(request)