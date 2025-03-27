import grpc
from proto.mom import mom_pb2, mom_pb2_grpc

def enqueue_task():
    channel = grpc.insecure_channel('localhost:50051')
    stub = mom_pb2_grpc.MOMServiceStub(channel)

    request = mom_pb2.SavePendingServiceParameters(
        task_id="task123",
        client_id="client001",
        service="serviceA",
        payload='{"a": 5, "b": 10}'
    )

    response = stub.SavePendingService(request)
    print("📥 MOM Response (Enqueue Task):")
    print(f"Status: {response.status}")
    print(f"Response: {response.response}")
    print(f"Timestamp: {response.timestamp}")


def check_task_response():
    channel = grpc.insecure_channel('localhost:50051')
    stub = mom_pb2_grpc.MOMServiceStub(channel)

    request = mom_pb2.RetrievePendingServiceParameters(
        task_id="task123",
        client_id="client001",
    )

    response = stub.RetrievePendingService(request)
    print("📥 MOM Response (Check Task Result):")
    print(f"Status: {response.status}")
    print(f"Response: {response.response}")
    print(f"Timestamp: {response.timestamp}")


def main_console():
    choice = input("Enter 1 to enqueue task, 2 to check for response: ")
    if choice == "1":
        enqueue_task()
    elif choice == "2":
        check_task_response()
    else:
        print("❌ Invalid option")

if __name__ == '__main__':
    main_console()
