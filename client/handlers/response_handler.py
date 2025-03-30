import time
from services.api_gateway import check_task_response
from utils.logger import log_event
from utils.client_actions import ask_to_continue, notify

import time
from services.api_gateway import check_task_response
from utils.client_actions import ask_to_continue, notify

def poll_for_response(client_id, task_id, timeout=30, poll_interval=5):
    """
    Polls the server for the task response until it's completed or timeout is reached.
    """
    start = time.time()
    
    while True:
        elapsed = time.time() - start

        if elapsed > timeout:
            notify(client_id, task_id, "🕐 Timeout reached. No response received.")
            
            if ask_to_continue():
                notify(client_id, task_id, "🔁 Restarting the wait...")
                start = time.time()
                continue
            else:
                notify(client_id, task_id, "🚫 Request canceled by the client.")
                break

        response = check_task_response(client_id, task_id)
        
        if response.get("status") == "completed":
            notify(client_id, task_id, f"✅ Response received: {response}")
            break
        else:
            print("⏳ Waiting for response...")
            time.sleep(poll_interval)