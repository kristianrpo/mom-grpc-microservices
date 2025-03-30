import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import grpc
from fastapi import APIRouter
from api.methods import service_pb2, service_pb2_grpc

router = APIRouter()

@router.post("/grpc/say-hello")
async def call_grpc(name: str):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        request = service_pb2.RequestMessage(name=name)
        response = stub.SayHello(request)
    return {"message": response.message}

@router.get("/grpc/test")
async def test_grpc():
    return {"message": "Test gRPC endpoint is working"}