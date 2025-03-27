def obtain_pending_data(redis_client,service):
    task_key = redis_client.pop_next_task_key(service)
    if task_key:
        task_data = redis_client.get_task_data(task_key)
        if task_data:
            task_id = task_data["task_id"]
            client_id = task_data["client_id"]
            payload = task_data["payload"]
            return task_id, client_id, payload
    return None, None, None

    
