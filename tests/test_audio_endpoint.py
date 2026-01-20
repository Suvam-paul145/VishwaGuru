import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from backend.main import app
from backend.database import get_db

def test_detect_audio_endpoint():
    # Use context manager to trigger startup events (lifespan)
    with TestClient(app) as client:
        # Mock the internal service call to avoid hitting external API
        with patch("backend.main.detect_audio_scene", new_callable=AsyncMock) as mock_detect:
            # Simulate a successful detection response
            mock_detect.return_value = [{"label": "dog_bark", "score": 0.95}]

            # Mock file upload
            files = {'audio': ('test.webm', b'fake_audio_bytes', 'audio/webm')}

            response = client.post("/api/detect-audio", files=files)

            assert response.status_code == 200
            data = response.json()
            assert "detections" in data
            assert data["detections"][0]["label"] == "dog_bark"

def test_get_stats():
    # Mock the database session
    mock_db = MagicMock()

    # Mock the query result: List of tuples (category, count)
    # db.query(...).group_by(...).all()
    mock_db.query.return_value.group_by.return_value.all.return_value = [
        ("pothole", 5),
        ("noise", 3),
        (None, 1) # Uncategorized
    ]

    # Override the dependency
    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        # Use context manager for consistency, though get_stats is sync and doesn't need http_client
        with TestClient(app) as client:
            response = client.get("/api/stats")
            assert response.status_code == 200
            data = response.json()

            assert data["total"] == 9
            assert len(data["by_category"]) == 3

            # Check specific values
            categories = {item["category"]: item["count"] for item in data["by_category"]}
            assert categories["pothole"] == 5
            assert categories["noise"] == 3
            assert categories["uncategorized"] == 1

    finally:
        app.dependency_overrides = {}
