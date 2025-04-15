import time
import threading
from services.api_gateway import get_task_status
from utils.client_actions import ask_to_continue, notify

def poll_for_response(client_id, task_id, timeout=30, poll_interval=5, ttl=60, interactive=True):
    """
    Polls the server for the task response until it's completed or TTL/timeout is reached.
    """
    start = time.time()
    timeout_start = start

    while True:
        elapsed = time.time() - start
        timeout_elapsed = time.time() - timeout_start

        if elapsed > ttl:
            notify(client_id, task_id, "🚫 Task canceled after exceeding TTL")
            break

        if timeout_elapsed > timeout:
            if interactive:
                notify(client_id, task_id, "🕐 Timeout reached. No response received.")
                if ask_to_continue():
                    notify(client_id, task_id, "🔁 Continue waiting...")
                    timeout_start = time.time()
                    continue
                else:
                    notify(client_id, task_id, "🚫 Task canceled by user.")
                    break

        response = get_task_status(client_id, task_id)

        if response.get("status") == "completed":
            notify(client_id, task_id, f"✅ Response for task {task_id} received: {response}")
            break
        else:
            print("⏳ Waiting for response...")
            time.sleep(poll_interval)

def start_polling(client_id, task_id, interactive=True):
    """
    Starts a separate thread to poll for the response.
    """
    thread = threading.Thread(target=poll_for_response, args=(client_id, task_id), kwargs={"interactive": interactive})
    thread.start()
    return thread