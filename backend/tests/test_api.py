import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    assert client.get("/health").status_code == 200

def test_list_ipos():
    r = client.get("/api/v1/ipos")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
