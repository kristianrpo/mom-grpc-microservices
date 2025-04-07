from utils.cli_args import parse_client_args
from utils.client_actions import notify
from services.api_gateway import enqueue_task, list_services
from handlers.response_handler import start_polling
from utils.task_retrieval import get_client_tasks, get_task_result
import sys

def main():
    args = parse_client_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "submit":
        client_id = args.client_id
        service = args.service
        payload = {"a": 5, "b": 10}

        response = enqueue_task(client_id, payload, service)
        task_id = response.get("task_id")
        notify(client_id, task_id, f"📤 Enqueue task with id {task_id} | service: {service} | payload: {payload}")
        start_polling(client_id, task_id)

    elif args.command == "list":
        task_ids = get_client_tasks(args.client_id)
        if not task_ids:
            print(f"No tasks were found for the client '{args.client_id}'.")
        else:
            print(f"Tasks found for client '{args.client_id}':")
            for tid in task_ids:
                print(f"  - {tid}")

    elif args.command == "result":
        result_msg = get_task_result(args.client_id, args.task_id)
        print(result_msg)

    elif args.command == "services":
        services = list_services()
        print("Available services:")
        for service in services:
            print(f"  - {service}")

    else:
        print("Unrecognized command. Use -h to see the available commands.")
        sys.exit(1)

if __name__ == "__main__":
    main()