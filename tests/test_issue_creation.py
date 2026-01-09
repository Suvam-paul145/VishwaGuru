import asyncio
import os
import shutil
import tempfile
from fastapi.testclient import TestClient

# Note: This test requires PYTHONPATH=backend to be set to import backend modules
# Run with: PYTHONPATH=backend python tests/test_issue_creation.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app
from models import Base
from database import engine

# Setup test DB
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_issue():
    # Create a valid minimal JPEG image file
    # This is the smallest valid JPEG file format
    jpeg_data = (
        b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        b'\xFF\xDB\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c'
        b'\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c'
        b'\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xFF\xC0\x00\x0b\x08\x00'
        b'\x01\x00\x01\x01\x01\x11\x00\xFF\xC4\x00\x14\x00\x01\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\xFF\xC4\x00\x14\x10\x01\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xDA\x00'
        b'\x08\x01\x01\x00\x00?\x00\x7f\xd9'
    )
    
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(jpeg_data)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            response = client.post(
                "/api/issues",
                data={
                    "description": "Test Issue",
                    "category": "Road",
                    "user_email": "test@example.com"
                },
                files={"image": ("test.jpg", f, "image/jpeg")}
            )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200
        assert response.json()["message"] == "Issue reported successfully"
        assert "action_plan" in response.json()
    finally:
        os.remove(tmp_path)

if __name__ == "__main__":
    test_create_issue()
