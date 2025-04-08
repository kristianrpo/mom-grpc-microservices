from utils.logger import log_event

def ask_to_continue():
    """
    Prompt the user to decide whether to continue waiting.
    """
    decision = input("Would you like to wait longer? (y/n): ").strip().lower()
    if decision == "y":
        return True
    return False

def notify(client_id, task_id, message):
    """
    Prints a message and logs it with the associated client and task ID.
    """
    print(message)
    log_event(client_id, task_id, message)