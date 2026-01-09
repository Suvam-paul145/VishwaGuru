
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from backend.main import app
import sys

# Mock sys.modules to prevent double import issues if any
# This is a precaution based on memory guidelines
if 'backend.main' not in sys.modules:
    import backend.main

client = TestClient(app)

@pytest.mark.asyncio
async def test_detect_blocked_road_endpoint():
    # Mock the detection function
    with patch("backend.main.detect_blocked_road_clip", new_callable=AsyncMock) as mock_detect:
        # Mock Image.open to avoid actual file processing issues
        with patch("PIL.Image.open") as mock_open:
            mock_open.return_value = MagicMock()

            # Setup the mock return value
            mock_detect.return_value = [
                {"label": "blocked road", "confidence": 0.95, "box": []}
            ]

            # Create a dummy image file
            files = {'image': ('test.jpg', b'fake_image_bytes', 'image/jpeg')}

            response = client.post("/api/detect-blocked-road", files=files)

            assert response.status_code == 200
            data = response.json()
            assert "detections" in data
            assert len(data["detections"]) == 1
            assert data["detections"][0]["label"] == "blocked road"
            assert data["detections"][0]["confidence"] == 0.95

@pytest.mark.asyncio
async def test_detect_blocked_road_no_detection():
    # Mock the detection function
    with patch("backend.main.detect_blocked_road_clip", new_callable=AsyncMock) as mock_detect:
         with patch("PIL.Image.open") as mock_open:
            mock_open.return_value = MagicMock()

            # Setup the mock return value (empty list)
            mock_detect.return_value = []

            files = {'image': ('test.jpg', b'fake_image_bytes', 'image/jpeg')}

            response = client.post("/api/detect-blocked-road", files=files)

            assert response.status_code == 200
            data = response.json()
            assert "detections" in data
            assert len(data["detections"]) == 0
