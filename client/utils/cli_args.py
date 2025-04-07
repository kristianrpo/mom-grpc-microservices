import argparse

def parse_client_args():
    parser = argparse.ArgumentParser(
        description='Client for managing tasks (submit, list, and get results)',
        epilog="""\
            Usage examples:

            # Submit a task in the foreground (waits for the result)
            python main.py submit --client-id client_001 --service serviceA

            # Submit a task in the background (does not wait for response)
            nohup python main.py submit --client-id client_001 --service serviceA &

            # List tasks submitted by a client
            python main.py list client_001

            # Get the result of a specific task
            python main.py result client_001 1234-abcd-5678

            Note: Use '&' or 'nohup' if you want to run tasks in the background.
            """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command")

    # Subcomando: submit
    submit_parser = subparsers.add_parser("submit", help="Submit a new task")
    submit_parser.add_argument("--client-id", required=True, help="Client ID")
    submit_parser.add_argument("--service", required=True, help="Service name")

    # Subcomando: list
    list_parser = subparsers.add_parser("list", help="List tasks from logs")
    list_parser.add_argument("client_id", help="Client ID")

    # Subcomando: result
    result_parser = subparsers.add_parser("result", help="Get task result")
    result_parser.add_argument("client_id", help="Client ID")
    result_parser.add_argument("task_id", help="Task ID")

    # Subcomando: services
    services_parser = subparsers.add_parser("services", help="List available services")

    return parser.parse_args()