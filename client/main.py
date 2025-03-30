from utils.cli_args import parse_client_args
from utils.client_actions import notify
from services.api_gateway import enqueue_task
from handlers.response_handler import poll_for_response
from utils.logger import log_event
import uuid

def main():
    args = parse_client_args()
    client_id = args.client_id
    service = args.service
    task_id = str(uuid.uuid4())
    payload = {"a": 5, "b": 10}

    response = enqueue_task(client_id, task_id, payload, service)
    notify(client_id, task_id, f"📤 Enqueue task: {response}")

    poll_for_response(client_id, task_id)

if __name__ == "__main__":
    main()