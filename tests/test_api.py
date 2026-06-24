import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "LLM Eval Pipeline API"}

def test_get_models():
    response = client.get("/api/models/list")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0

def test_get_history():
    response = client.get("/api/eval/history")
    assert response.status_code == 200
    assert "history" in response.json()

def test_run_eval_empty_prompt():
    response = client.post("/api/eval/run", json={
        "prompt": "",
        "models": ["claude-sonnet-4-6"],
        "task_type": "general"
    })
    assert response.status_code == 200
    assert response.json()["results"] == []

def test_run_eval_invalid_model():
    response = client.post("/api/eval/run", json={
        "prompt": "테스트",
        "models": ["invalid-model"],
        "task_type": "general"
    })
    assert response.status_code == 400