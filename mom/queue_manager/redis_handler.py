import redis
import os
import json
from datetime import datetime

class RedisHandler:
    def __init__(self):
        # Initialize the Redis connection
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    
    def save_pending_request(self, service, client_id, task_id, time_to_live_seconds, payload):
        """
        Save a task in the queue of the service requested that will be accessed by the microservice when it goes up.
        Args:
            service (str): The name of the service.
            client_id (str): The client ID.
            task_id (str): The task ID.
            time_to_live_seconds (int): Time to live for the task in seconds.
            payload (str): The payload for the task.
        Returns:
            bool: True if the task was saved successfully, False otherwise.
            str: Error message if any.  
        """
        try:
            queue_key= f"queue:{service}"
            value = json.dumps({
                "task_id": task_id,
                "client_id": client_id,
                "service": service,
                "payload": payload,
                "status": "pending",
                "time_to_live_seconds": time_to_live_seconds,
                "created_at": datetime.utcnow().isoformat()
            })
            self.client.rpush(queue_key, value)
            return True,None
        except Exception as e:
            return False, str(e)


    def delete_task(self, task_key):
        """
        Delete a task from the Redis queue.
        Args:
            task_key (str): The key of the task to delete.
        Returns:
            bool: True if the task was deleted successfully, False otherwise.
            str: Error message if any.
        """
        try:
            self.client.delete(task_key)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def save_response(self, task_id, client_id, response, time_to_live_seconds):
        """
        Save the result from the microservice for a given task_id and client_id.
        Args:
            task_id (str): The task ID.
            client_id (str): The client ID.
            response (str): The response from the microservice.
            ttl (int): Time to live for the key in seconds.
        Returns:
            bool: True if the response was saved successfully, False otherwise.
            str: Error message if any.
        """
        try:
            key = f"response:{client_id}:{task_id}"
            value = json.dumps({
                "status": "completed",
                "response": response,
                "timestamp": datetime.utcnow().isoformat()
            })
            self.client.setex(key, time_to_live_seconds, value)
            return True,None
        except Exception as e:
            return False, str(e)

    def get_response(self, task_id, client_id):
        """
        Retrieve the microservice result (when it goes up) for a given task_id and client_id.
        Args:
            task_id (str): The task ID.
            client_id (str): The client ID.
        Returns:
            bool: True if the response was retrieved successfully, False otherwise.
            dict: The response data if found, None otherwise.
            str: Error message if any.
        """
        try:
            key = f"response:{client_id}:{task_id}"
            data = self.client.get(key)
            response = json.loads(data) if data else None
            return True, response, None
        except Exception as e:
            return False, None, str(e) 