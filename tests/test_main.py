from fastapi.client import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Notes API is running"}

def test_get_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    assert "notes" in response.json()
