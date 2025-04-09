import time
import threading
from services.api_gateway import get_task_status
from utils.client_actions import ask_to_continue, notify

def poll_for_response(client_id, task_id, timeout=30, poll_interval=5, max_retries=3, interactive=True):
    """
    Polls the server for the task response until it's completed or timeout is reached.
    """
    start = time.time()
    retries = 0

    while True:
        elapsed = time.time() - start
        retries += 1

        if elapsed > timeout:
            notify(client_id, task_id, "🕐 Timeout reached. No response received.")
            
            if interactive:
                if ask_to_continue():
                    notify(client_id, task_id, "🔁 Restarting the wait...")
                    start = time.time()
                    continue
                else:
                    notify(client_id, task_id, "🚫 Task canceled by user.")
                    break
            
            else:
                if retries < max_retries:
                    notify(client_id, task_id, "🔁 Restarting the wait...")
                    start = time.time()
                    continue
                else:
                    notify(client_id, task_id, "🚫 Max retries reached. Cancelling task.")
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