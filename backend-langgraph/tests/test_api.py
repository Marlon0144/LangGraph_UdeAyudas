from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_invoke_administrativa():
    resp = client.post("/api/invoke", json={"question": "¿Cuál es el horario de atención?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "generation" in data
    assert data["router_decision"] == "ADMINISTRATIVA"

def test_invoke_casual():
    resp = client.post("/api/invoke", json={"question": "Buenos días"})
    assert resp.status_code == 200
    data = resp.json()
    assert "generation" in data
    assert data["router_decision"] == "CASUAL"
