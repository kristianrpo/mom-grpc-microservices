from fastapi import FastAPI
from api.routes import grpc_client

app = FastAPI()

app.include_router(grpc_client.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
