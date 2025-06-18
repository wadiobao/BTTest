import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_demo_rag():
    response = client.post(
        "/chat/demo-rag/",
        data={"prompt": "Test prompt"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "result" in data
    assert isinstance(data["result"], str)

def test_add_file():
    test_file_path = "test.pdf"
    
    try:
        with open(test_file_path, "rb") as f:
            response = client.post(
                "/chat/add/",
                files={"file": ("test.pdf", f, "application/pdf")}
            )
        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert "result" in data
        assert isinstance(data["result"], str)
    finally:
        # Clean up test file if it was created
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_rag_tom_tat():
    response = client.post(
        "/chat/summary/",
        data={"prompt": "Test summary prompt"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "result" in data
    assert isinstance(data["result"], str) 