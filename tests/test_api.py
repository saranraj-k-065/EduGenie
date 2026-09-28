from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text

def test_task_validation_rejects_empty_text():
    response = client.post("/api/task", json={"task":"qa","text":"","level":"Beginner"})
    assert response.status_code == 422

def test_invalid_task_rejected():
    response = client.post("/api/task", json={"task":"invalid","text":"Hello","level":"Beginner"})
    assert response.status_code == 422
