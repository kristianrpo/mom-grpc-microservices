from config.settings import API_URL
import requests

def enqueue_task(client_id, task_id, payload, service):
    """
    Enqueues a task by sending a POST request to the API.
    """
    response = requests.post(f"{API_URL}/api/tasks", json={
        "client_id": client_id,
        "task_id": task_id,
        "service": service,
        "payload": payload
    })
    return response.json()

def check_task_response(client_id, task_id):
    """
    Checks the response for a previously enqueued task by sending a GET request to the API.
    """
    response = requests.get(f"{API_URL}/api/tasks/status/{client_id}/{task_id}")
    return response.json()