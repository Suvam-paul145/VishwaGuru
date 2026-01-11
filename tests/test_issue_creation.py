import asyncio
import os
import shutil
import tempfile
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

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

def test_create_issue():
    # Create a dummy image file
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(b"fake image content")
        tmp_path = tmp.name

    # Mock AI services initialization and action plan generation
    with patch("backend.main.get_ai_services") as mock_get_ai:
        mock_action_plan_service = MagicMock()
        mock_action_plan_service.generate_action_plan.return_value = {
            "whatsapp": "Test Plan",
            "email_subject": "Test Subject",
            "email_body": "Test Body"
        }

        mock_ai_services = MagicMock()
        mock_ai_services.action_plan_service = mock_action_plan_service
        mock_get_ai.return_value = mock_ai_services

        # Use TestClient as context manager to trigger lifespan events
        with TestClient(app) as client:
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
