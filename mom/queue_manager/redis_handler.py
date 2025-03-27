import redis
import os
import json
from datetime import datetime

class RedisHandler:
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    
    def save_pending_request(self, service, client_id, task_id, payload, ttl=5000):
        queue_key = f"queue:{service}"
        data_key = f"pending:{service}:{client_id}:{task_id}"
        value = json.dumps({
            "task_id": task_id,
            "client_id": client_id,
            "service": service,
            "payload": payload,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        })
        self.client.setex(data_key, ttl, value)
        self.client.rpush(queue_key, data_key)

    def pop_next_task_key(self, service):
        queue_key = f"queue:{service}"
        return self.client.lpop(queue_key)
    
    def get_task_data(self, task_key):
        data = self.client.get(task_key)
        return json.loads(data) if data else None

    def delete_task(self, task_key):
        self.client.delete(task_key)
    
    def save_response(self, task_id, client_id, response, ttl=5000):
        key = f"response:{client_id}:{task_id}"
        value = json.dumps({
            "status": "completed",
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.client.setex(key, ttl, value)

    def get_response(self, task_id, client_id):
        key = f"response:{client_id}:{task_id}"
        data = self.client.get(key)
        return json.loads(data) if data else None
