import grpc  # Import the gRPC library to handle RPC communication
from proto.mom import mom_pb2, mom_pb2_grpc  # Import generated proto classes for MOM service

def enqueue_task():
    """
    Enqueues a task by sending a request to the MOM service.

    This function creates a gRPC channel to the MOM service running on localhost:50051,
    constructs a request message to save a pending service task, and sends it via the stub.
    The response from the MOM service is printed to the console.
    """
    # Create an insecure channel to connect to the MOM service.
    channel = grpc.insecure_channel('localhost:50051')
    # Create a stub (client) for the MOM service using the generated gRPC classes.
    stub = mom_pb2_grpc.MOMServiceStub(channel)

    # Build the request message with task details.
    request = mom_pb2.SavePendingServiceParameters(
        task_id="task123",
        client_id="client001",
        service="CalculatorService",
        time_to_live_seconds=10,
        payload='{"parameter_a": 5, "parameter_b": 10}'
    )

    # Send the request to the MOM service and capture the response.
    response = stub.SavePendingService(request)

    # Log the response details from the MOM service.
    print("📥 MOM Response (Enqueue Task):")
    print(f"Status: {response.status}")
    print(f"Response: {response.response}")
    print(f"Timestamp: {response.timestamp}")

def check_task_response():
    """
    Checks the response for a previously enqueued task from the MOM service.

    This function creates a gRPC channel to the MOM service running on localhost:50051,
    constructs a request message to retrieve the pending service response, and sends it.
    The retrieved response is printed to the console.
    """
    # Create an insecure channel to connect to the MOM service.
    channel = grpc.insecure_channel('localhost:50051')
    # Create a stub (client) for the MOM service.
    stub = mom_pb2_grpc.MOMServiceStub(channel)

    # Build the request message with task identification details.
    request = mom_pb2.RetrievePendingServiceParameters(
        task_id="task123",
        client_id="client001",
    )

    # Send the request to the MOM service and capture the response.
    response = stub.RetrievePendingService(request)

    # Log the response details from the MOM service.
    print("📥 MOM Response (Check Task Result):")
    print(f"Status: {response.status}")
    print(f"Response: {response.response}")
    print(f"Timestamp: {response.timestamp}")

def main_console():
    """
    Provides a simple console interface to choose between enqueuing a task or checking a task response.

    The user is prompted to enter '1' to enqueue a task or '2' to check for a task response.
    """
    # Prompt the user for input to determine which action to perform.
    choice = input("Enter 1 to enqueue task, 2 to check for response: ")
    if choice == "1":
        enqueue_task() 
    elif choice == "2":
        check_task_response() 
    else:
        print("❌ Invalid option")

if __name__ == '__main__':
    # Run the console interface if this script is executed as the main program.
    main_console()
