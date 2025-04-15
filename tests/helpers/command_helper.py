def build_submit_command(client_id, service_name, a, b):
    """
    Build the command to submit a task to the microservice.
    :param client_id: ID of the client submitting the task
    :param service_name: Name of the service to submit the task to
    :param a: First operand
    :param b: Second operand
    """
    return [
        "python3", "main.py",
        "submit",
        "--client-id", client_id,
        "--service", service_name,
        "--a", str(a),
        "--b", str(b)
    ]
