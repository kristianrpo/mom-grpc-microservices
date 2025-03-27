import redis
import json
from datetime import datetime

class RedisHandler:
    def __init__(self, host="localhost", port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)


def publish_service_status():
    redis_handler = RedisHandler()
    service_name = "serviceA"

    status_message = {
        "service": service_name,
        "is_active": True
    }

    redis_handler.client.publish("microservices", json.dumps(status_message))
    print(f"📡 Published service activation message: {status_message}")

if __name__ == "__main__":
    publish_service_status()
