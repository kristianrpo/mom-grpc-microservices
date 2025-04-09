from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
import json
import grpc
import traceback
from api.clients.mom_client import MOMClient
from api.config.settings import settings
from api.clients.service_client import ServiceClient

import logging
logger = logging.getLogger(__name__)

router = APIRouter()
mom_client = MOMClient()
services = settings.SERVICES

class ServiceRequest(BaseModel):
    client_id: str
    service_name: str
    payload: dict
    time_to_live_seconds: int = 60

@router.post("/request")
async def handle_request(request: ServiceRequest):
    task_id = str(uuid.uuid4())
    logger.info(f"Received request: task_id={task_id}, service_name={request.service_name}, client_id={request.client_id}")

    try:
        # Verificar que el servicio exista antes de instanciarlo
        if request.service_name not in services:
            error_message = f"Service '{request.service_name}' not found in configured services."
            logger.error(error_message)
            raise HTTPException(status_code=404, detail=error_message)

        client = ServiceClient(request.service_name)
        logger.info(f"Calling service client for {request.service_name} with payload: {request.payload}")

        response = client.call(request.service_name,request.payload)

        logger.info(f"Immediate response received: {response.result}")

        return {
            "status": "success",
            "task_id": task_id,
            "response": response.result,
            "processed_immediately": True
        }

    except grpc.RpcError as grpc_error:
        logger.warning(f"gRPC error encountered: {grpc_error}")
        mom_response = mom_client.enqueue_task(
            task_id=task_id,
            client_id=request.client_id,
            service_name=request.service_name,
            payload=json.dumps(request.payload),
            ttl=request.time_to_live_seconds
        )
        logger.info(f"Task enqueued to MOM: {mom_response}")

        return {
            "status": "queued",
            "task_id": task_id,
            "mom_response": {
                "status": mom_response.status,
                "message": mom_response.response
            }
        }

    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e

    except Exception as e:
        # Log detallado con traceback
        tb = traceback.format_exc()
        logger.critical(f"Unhandled Exception: {e}\nTraceback:\n{tb}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}") from e

@router.get("/task/{task_id}")
async def get_task_status(task_id: str, client_id: str):
    try:
        logger.info(f"Checking task status for task_id={task_id}, client_id={client_id}")
        response = mom_client.check_task(task_id, client_id)
        return {
            "status": response.status,
            "response": response.response,
            "timestamp": response.timestamp
        }
    except grpc.RpcError as e:
        logger.error(f"gRPC error while checking task: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/services")
async def list_services():
    logger.info("Listing available services")
    if not services:
        logger.error("No services configured in settings")
        raise HTTPException(status_code=500, detail="No services configured")
    return {
        service_name: {
            "methods": list(service_config["methods"].keys())
        }
        for service_name, service_config in services.items()
    }