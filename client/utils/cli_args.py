import argparse

def parse_client_args():
    parser = argparse.ArgumentParser(
        description='Client for managing tasks (submit, list, and get results)',
        epilog="""\
            Usage examples:

            # List available services
            python main.py services

            # Submit a task in the foreground
            python main.py submit --client-id {client_id} --service {service_name} --a {value1} --b {value2}

            # Submit a task in the background
            nohup python main.py submit --client-id {client_id} --service {service_name} --a {value1} --b {value2} --background &

            # List tasks submitted by a client
            python main.py list {client_id}

            # Get the result of a specific task
            python main.py result {client_id} {task_id}

            Note: Use '&' or 'nohup' if you want to run tasks in the background.
            """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: submit
    submit_parser = subparsers.add_parser("submit", help="Submit a new task")
    submit_parser.add_argument("--client-id", required=True, help="Client ID")
    submit_parser.add_argument("--service", required=True, help="Service name (CalculatorService or MultiplicationService)")
    submit_parser.add_argument("--a", type=float, required=True, help="First operand")
    submit_parser.add_argument("--b", type=float, required=True, help="Second operand")
    submit_parser.add_argument("--background", action="store_true", help="Run in background mode")

    # Subcommand: list
    list_parser = subparsers.add_parser("list", help="List tasks from logs")
    list_parser.add_argument("client_id", help="Client ID")

    # Subcommand: result
    result_parser = subparsers.add_parser("result", help="Get task result")
    result_parser.add_argument("client_id", help="Client ID")
    result_parser.add_argument("task_id", help="Task ID")

    # Subcommand: services
    services_parser = subparsers.add_parser("services", help="List available services")

    return parser, parser.parse_args()