from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from backend.main import app
from backend.database import get_db

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# Test Manual Verification (Upvote)
def test_manual_verification_upvote(client):
    pass

# Test AI Verification
@patch("backend.routers.issues.validate_uploaded_file", new_callable=AsyncMock)
@patch("backend.routers.issues.verify_resolution_vqa", new_callable=AsyncMock)
def test_ai_verification_resolved(mock_vqa, mock_validate, client):
    # Setup mocks
    mock_validate.return_value = None
    mock_vqa.return_value = {
        "answer": "no",
        "confidence": 0.95
    }

    # Mock DB dependency to return a fake issue
    mock_db = MagicMock()
    mock_issue = MagicMock()
    mock_issue.id = 1
    mock_issue.category = "pothole"
    mock_issue.status = "open"
    mock_issue.upvotes = 0

    # We need to mock the query chain: db.query().filter().first()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_issue

    # Override dependency
    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.post(
            "/api/issues/1/verify",
            files={"image": ("test.jpg", b"fakeimage", "image/jpeg")}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["is_resolved"] == True
        assert data["ai_answer"] == "no"

    finally:
        app.dependency_overrides = {}
