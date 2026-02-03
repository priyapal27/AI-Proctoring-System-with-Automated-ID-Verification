from fastapi.testclient import TestClient
import pytest
from main import app
import os

client = TestClient(app)

def test_read_main_not_found():
    # Verify that a random GET request returns 404 (as we only have POST /detect-id)
    response = client.get("/")
    assert response.status_code == 404

def test_detect_id_no_file():
    # Verify that sending no file returns a validation error
    response = client.post("/detect-id")
    assert response.status_code == 422 # Unprocessable Entity for missing body

def test_database_setup():
    # Check if database setup logic in main.py runs without error
    from database import engine
    from models import Base
    assert Base.metadata.tables["id_records"] is not None
