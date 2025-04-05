from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import time
import random

app = FastAPI()

responses: Dict[str, dict] = {}

class ServiceRequest(BaseModel):
    client_id: str
    task_id: str
    service: str
    payload: dict

@app.post("/api/tasks")
def enqueue_task(request: ServiceRequest):
    """
    Enqueues a task by saving it in the responses dictionary.
    """
    if request.service != "serviceA":
        return {"error": "Service not found"}

    responses[request.task_id] = {
        "status": "pending",
        "response": None,
        "timestamp": None,
        "payload": request.payload
    }

    return {
        "status": "accepted in queue",
        "task_id": request.task_id
    }

@app.get("/api/tasks/status/{client_id}/{task_id}")
def check_task_response(client_id: str, task_id: str):
    """
    Checks the status of a task and simulates a response.
    """
    task = responses.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] == "pending":
        if random.random() < 0.5:
            data = task["payload"]
            a = data.get("a", 0)
            b = data.get("b", 0)

            result = a + b

            task["status"] = "completed"
            task["response"] = {
                "sum": result,
                "timestamp": time.time()
            }

    return {
        "status": task["status"],
        "response": task["response"]
    }