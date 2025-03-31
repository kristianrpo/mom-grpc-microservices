from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
import json
import grpc
from clients.mom_client import MOMClient
from config.settings import SERVICES  
from clients.service_client import ServiceClient

router = APIRouter()
mom_client = MOMClient()

class ServiceRequest(BaseModel):
    client_id: str
    service_name: str
    method_name: str
    payload: dict
    time_to_live_seconds: int = 60

@router.post("/request")
async def handle_request(request: ServiceRequest):
    task_id = str(uuid.uuid4())
    
    try:
        client = ServiceClient(request.service_name)
        response = client.call(request.method_name, request.payload)
        
        return {
            "status": "success",
            "task_id": task_id,
            "response": json.loads(response.data),
            "processed_immediately": True
        }
    
    except grpc.RpcError:  # Microservicio no disponible
        mom_response = mom_client.enqueue_task(
            task_id=task_id,
            client_id=request.client_id,
            service_name=request.service_name,
            payload=json.dumps({
                "method": request.method_name,
                "data": request.payload
            }),
            ttl=request.time_to_live_seconds
        )
        return {
            "status": "queued",
            "task_id": task_id,
            "mom_response": {
                "status": mom_response.status,
                "message": mom_response.response
            }
        }
    
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=str(e)) from e  
    
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e)) from e 

@router.get("/task/{task_id}")
async def get_task_status(task_id: str, client_id: str):
    try:
        response = mom_client.check_task(task_id, client_id)
        return {
            "status": response.status,
            "response": response.response,
            "timestamp": response.timestamp
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    

@router.get("/services")
async def list_services():
    """Devuelve todos los servicios y métodos disponibles"""
    return {
        service_name: {
            "methods": list(service_config["methods"].keys())
        }
        for service_name, service_config in SERVICES.items()
    }