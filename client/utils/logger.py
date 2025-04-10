from datetime import datetime
import os

def log_event(client_id, task_id, message):
    """
    Logs client events to a file.
    """
    os.makedirs("logs/clients", exist_ok=True)
    log_path = f"logs/clients/{client_id}.log"
    timestamp = datetime.utcnow().isoformat()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{task_id}] {message}\n")