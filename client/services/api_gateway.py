from config.settings import API_URL
import requests

def enqueue_task(client_id, payload, service_name, ttl=60):
    """
    Enqueues a task by sending a POST request to the API.
    """
    response = requests.post(f"{API_URL}/request", json={
        "client_id": client_id,
        "service_name": service_name,
        "payload": payload,
        "time_to_live_seconds": ttl
    })
    response.raise_for_status()
    return response.json()

def check_task_response(client_id, task_id):
    """
    Checks the response for a previously enqueued task.
    """
    response = requests.get(f"{API_URL}/task/{task_id}", params={
        "client_id": client_id
    })
    response.raise_for_status()
    return response.json()

def list_services():
    """
    Retrieves a list of available services and their methods.
    """
    response = requests.get(f"{API_URL}/services")
    response.raise_for_status()
    return response.json()