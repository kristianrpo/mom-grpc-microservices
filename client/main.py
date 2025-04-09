from utils.cli_args import parse_client_args
from utils.client_actions import notify
from services.api_gateway import handle_request, list_services
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
        service_name = args.service
        
        if service_name == "CalculatorService":
            payload = {"parameter_a": args.a, "parameter_b": args.b}
        elif service_name == "MultiplicationService":
            payload = {"parameter_a": args.a, "parameter_b": args.b}
        else:
            print(f"Unsupported service: {service_name}")
            sys.exit(1)

        print(client_id, payload, service_name  )
        response = handle_request(client_id, payload, service_name)
        task_id = response.get("task_id")
        notify(client_id, task_id, f"📤 Enqueue task with id {task_id} | service: {service_name} | payload: {payload}")
        interactive = not getattr(args, "background", False)
        start_polling(client_id, task_id, interactive=interactive)

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