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
        try:
            queue_key= f"queue:{service}"
            value = json.dumps({
                "task_id": task_id,
                "client_id": client_id,
                "service": service,
                "payload": payload,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat()
            })
            self.client.rpush(queue_key, value)
            return True,None
        except Exception as e:
            return False, str(e)


    def delete_task(self, task_key):
        try:
            self.client.delete(task_key)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def save_response(self, task_id, client_id, response, ttl=5000):
        try:
            key = f"response:{client_id}:{task_id}"
            value = json.dumps({
                "status": "completed",
                "response": response,
                "timestamp": datetime.utcnow().isoformat()
            })
            self.client.setex(key, ttl, value)
            return True,None
        except Exception as e:
            return False, str(e)

    def get_response(self, task_id, client_id):
        try:
            key = f"response:{client_id}:{task_id}"
            data = self.client.get(key)
            response = json.loads(data) if data else None
            return True, response, None
        except Exception as e:
            return False, None, str(e) 