import pytest
import json
from fastapi.testclient import TestClient
from app import app
import grpc
from httpx import AsyncClient

TEST_CLIENT_ID = "test123"
TEST_TTL = 60
TEST_SERVER_URL = "http://localhost:8000" 

@pytest.fixture
def sync_client():
    return TestClient(app)

def test_request_processing(sync_client):
    """Tests the correct routing to microservices."""
    response = sync_client.post(
        "/request",
        json={
            "client_id": TEST_CLIENT_ID,
            "service_name": "SumService",
            "payload": {"parameterA": 5, "parameterB": 10},
            "time_to_live_seconds": TEST_TTL
        }
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["processed_immediately"] is True
    
    if isinstance(response_data["response"], str):
        response_json = json.loads(response_data["response"])
    else:
        response_json = response_data["response"]
    
    assert response_json["sum"] == 15.0
    assert response_json["status"] == "COMPLETED"

@pytest.mark.asyncio
async def test_failover_to_mom():
    """Tests the failover to MOM when a microservice fails."""
    async with AsyncClient(base_url=TEST_SERVER_URL) as client:
        try:
            response = await client.post(
                "/request",
                json={
                    "client_id": TEST_CLIENT_ID,
                    "service_name": "MultiplicationService", 
                    "payload": {"parameterA": 2, "parameterB": 3},
                    "time_to_live_seconds": TEST_TTL
                }
            )
            assert response.status_code == 200
            assert response.json()["status"] == "queued"
            assert "task_id" in response.json()
        except grpc.RpcError:
            pass

def test_task_retrieval(sync_client):
    """Test retrieving task status"""
    # First create a task
    create_response = sync_client.post(
        "/request",
        json={
            "client_id": TEST_CLIENT_ID,
            "service_name": "SumService",
            "payload": {"parameterA": 5, "parameterB": 10},
            "time_to_live_seconds": TEST_TTL
        }
    )
    task_id = create_response.json()["task_id"]
    
    # Then retrieve it
    retrieve_response = sync_client.get(f"/task/{task_id}", params={"client_id": TEST_CLIENT_ID})
    assert retrieve_response.status_code == 200
    assert "status" in retrieve_response.json()