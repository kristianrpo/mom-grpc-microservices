from fastapi import FastAPI
from api.routes import api

app = FastAPI()
app.include_router(api.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}