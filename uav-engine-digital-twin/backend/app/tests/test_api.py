"""
Test API Suite (Section 26).
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_missions_api():
    res = client.get("/api/missions")
    assert res.status_code == 200
    assert len(res.json()) > 0
