from utils.cli_args import parse_client_args
from utils.client_actions import notify
from services.api_gateway import enqueue_task
from handlers.response_handler import start_polling
from utils.logger import log_event

def main():
    args = parse_client_args()
    client_id = args.client_id
    service = args.service
    payload = {"a": 5, "b": 10}

    response = enqueue_task(client_id, payload, service)
    task_id = response.get("task_id")
    notify(client_id, task_id, f"📤 Enqueue task with id {task_id} | service: {service} | payload: {payload}")

    start_polling(client_id, task_id)

if __name__ == "__main__":
    main()