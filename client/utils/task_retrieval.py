import os
import re
from datetime import datetime
import ast

def get_client_tasks(client_id):
    """
    Retrieves all tasks from the client's log file.
    """
    log_path = f"logs/clients/{client_id}.log"
    tasks = {}

    if not os.path.exists(log_path):
        return []

    with open(log_path, "r") as f:
        for line in f:
            match = re.search(r'\[\d{4}-\d{2}-\d{2}.*?\] \[(.*?)\] 📤 Enqueue task with id .*? \| service: (.*?) \| payload: (.*)', line)
            if match:
                task_id = match.group(1)
                service = match.group(2).strip()
                try:
                    payload = ast.literal_eval(match.group(3).strip())
                except Exception:
                    payload = match.group(3).strip()

                tasks[task_id] = {
                    "task_id": task_id,
                    "service": service,
                    "payload": payload
                }

    return list(tasks.values())

def get_task_result(client_id, task_id):
    """
    Searches for the result of a specific task in the client's log file.
    """
    log_path = f"logs/clients/{client_id}.log"
    if not os.path.exists(log_path):
        return f"Client log not found '{client_id}'."

    enqueue_info = None
    result_info = None

    with open(log_path, "r") as f:
        for line in f:
            if task_id in line:
                if "Enqueue task with id" in line:
                    match = re.match(r".*service: (.*?) \| payload: (.*)", line)
                    if match:
                        service = match.group(1).strip()
                        try:
                            payload = ast.literal_eval(match.group(2).strip())
                        except Exception:
                            payload = match.group(2).strip()
                        enqueue_info = {"service": service, "payload": payload}

                elif "Response for task" in line and "received" in line:
                    match = re.match(r"\[(.*?)\].*received: (.*)", line)
                    if match:
                        try:
                            result = ast.literal_eval(match.group(2).strip())
                        except Exception:
                            result = match.group(2).strip()
                        result_info = {
                            "timestamp": datetime.fromisoformat(match.group(1)),
                            "result": result
                        }

    if result_info:
        service = enqueue_info["service"] if enqueue_info else "unknown"
        payload = enqueue_info["payload"] if enqueue_info else "unknown"
        return (
            f"The task {task_id} that called the service '{service}' with arguments {payload} "
            f"returned the result: {result_info['result']}"
        )
    else:
        return f"No result was found for task {task_id}."

