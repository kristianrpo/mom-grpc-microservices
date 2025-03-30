import grpc
from concurrent import futures
import tests.microservice.microservice_pb2 as calculator_pb2
import tests.microservice.microservice_pb2_grpc as calculator_pb2_grpc
import redis
import json
import time
import threading
from datetime import datetime, timedelta
from proto.mom import mom_pb2, mom_pb2_grpc

def sumar(a, b):
    """Función de lógica principal para sumar dos números."""
    return a + b

def response_to_mom(client_id,task_id,time_to_live_seconds,created_at,result):
    channel = grpc.insecure_channel('localhost:50051')
    stub = mom_pb2_grpc.MOMServiceStub(channel)

    response_data = json.dumps({
        "status": "ok",
        "result": result,
        "timestamp": datetime.utcnow().isoformat()
    })

    request = mom_pb2.SaveResultServiceParameters(
        client_id=client_id,
        task_id=task_id,
        time_to_live_seconds=time_to_live_seconds,
        created_at=created_at,
        response=response_data
    )
    response = stub.SaveResultService(request)
    print("📥 MOM Response (Check Task Result):")
    print(f"Status: {response.status}")
    print(f"Response: {response.response}")
    print(f"Timestamp: {response.timestamp}")

class RedisHandler:
    def __init__(self, host="localhost", port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def publish_service_status(self, service_name, is_active=True):
        status_message = {
            "service": service_name,
            "is_active": is_active
        }
        self.client.publish("microservices", json.dumps(status_message))
        print(f"📡 Published service status: {status_message}")

    def pop_next_task(self, service):
        queue_key = f"queue:{service}"
        # Usamos BLPOP para bloquear y esperar una tarea, timeout de 5 seg.
        task = self.client.blpop(queue_key, timeout=5)
        if task:
            # BLPOP devuelve una tupla: (queue_name, valor)
            return task[1]
        return None

class CalculatorService(calculator_pb2_grpc.CalculatorServiceServicer):
    def SumNumbers(self, request, context):
        try:
            a = request.parameter_a
            b = request.parameter_b
            resultado = sumar(a, b)
            result_data = {
                "sum": resultado,
                "status": "ok",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            json_result = json.dumps(result_data)
            print(f"🧮 Responding with JSON: {json_result}")
            return calculator_pb2.SumNumbersResponse(result=json_result)
        except Exception as e:
            error_data = {
                "error": str(e),
                "status": "fail"
            }
            return calculator_pb2.SumNumbersResponse(result=json.dumps(error_data))

def process_tasks(redis_handler):
    """
    Función que procesa tareas pendientes de Redis usando la lógica de sumar.
    Se ejecuta en un hilo separado para no bloquear el servidor gRPC.
    """
    print("🚀 Iniciando el consumidor de tareas de Redis...")
    while True:
        task_json = redis_handler.pop_next_task(service="CalculatorService")
        if task_json:
            try:
                task_data = json.loads(task_json)
                ttl_seconds = task_data.get("time_to_live_seconds")
                created_at = task_data.get("created_at")

                if created_at.endswith('Z'):
                    created_at = created_at[:-1]
                
                dt = datetime.fromisoformat(created_at)
                new_dt = dt + timedelta(seconds=ttl_seconds)

                if datetime.utcnow() > new_dt:
                    print("❌ Task expired, skipping...")
                    continue

                else:
                    payload = json.loads(task_data.get("payload"))
                    print(f"📥 Tarea recibida: {task_data}")
                    a = payload.get("parameter_a")
                    b = payload.get("parameter_b")
                    resultado = sumar(a, b)
                    print(f"🧮 Tarea procesada: {a} + {b} = {resultado}")
                    response_to_mom(task_data.get("client_id"),task_data.get("task_id"),ttl_seconds,created_at,resultado)
            except Exception as e:
                print(f"❌ Error al procesar la tarea: {e}")
        else:
            # Si no hay tarea, se espera unos segundos antes de reintentar.
            print("❌ No tasks found in the queue, esperando...")
            break

def serve():
    redis_handler = RedisHandler()

    # Iniciar el servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServiceServicer_to_server(CalculatorService(), server)
    port = "50052"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"🚀 CalculatorService gRPC server started on port {port}")

    # Publicar estado del servicio en Redis (opcional)
    redis_handler.publish_service_status("CalculatorService", True)

    # Iniciar el consumidor de tareas en un hilo separado
    task_thread = threading.Thread(target=process_tasks, args=(redis_handler,), daemon=True)
    task_thread.start()

    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        print("🛑 Stopping server...")
        server.stop(0)

if __name__ == "__main__":
    serve()
