import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import sys
import os
import httpx

# Ensure backend is in path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.main import app

@pytest.fixture
def client_with_mocked_http_client():
    # Mock the http_client in app.state
    app.state.http_client = AsyncMock(spec=httpx.AsyncClient)

    with TestClient(app) as client:
        # Override the client that was just created by startup
        client.app.state.http_client = AsyncMock(spec=httpx.AsyncClient)
        yield client

@pytest.mark.asyncio
async def test_detect_tree_hazard_endpoint(client_with_mocked_http_client):
    client = client_with_mocked_http_client
    with patch("backend.main.detect_tree_hazard_clip", new_callable=AsyncMock) as mock_detect:
        mock_detect.return_value = [{"label": "fallen tree", "confidence": 0.95, "box": []}]

        files = {"image": ("test.jpg", b"fakeimagebytes", "image/jpeg")}

        response = client.post("/api/detect-tree-hazard", files=files)

        assert response.status_code == 200
        assert response.json()["detections"][0]["label"] == "fallen tree"
        mock_detect.assert_called_once()

@pytest.mark.asyncio
async def test_detect_pest_endpoint(client_with_mocked_http_client):
    client = client_with_mocked_http_client
    with patch("backend.main.detect_pest_clip", new_callable=AsyncMock) as mock_detect:
        mock_detect.return_value = [{"label": "rat", "confidence": 0.95, "box": []}]

        files = {"image": ("test.jpg", b"fakeimagebytes", "image/jpeg")}

        response = client.post("/api/detect-pest", files=files)

        assert response.status_code == 200
        assert response.json()["detections"][0]["label"] == "rat"
        mock_detect.assert_called_once()

@pytest.mark.asyncio
async def test_detect_accessibility_endpoint(client_with_mocked_http_client):
    client = client_with_mocked_http_client

    # Mock the HF service function
    with patch("backend.main.detect_accessibility_clip", new_callable=AsyncMock) as mock_detect:
        mock_detect.return_value = [{"label": "blocked wheelchair ramp", "confidence": 0.95, "box": []}]

        # Create a dummy image
        files = {"image": ("test.jpg", b"fakeimagebytes", "image/jpeg")}

        response = client.post("/api/detect-accessibility", files=files)

        assert response.status_code == 200
        assert response.json()["detections"][0]["label"] == "blocked wheelchair ramp"
        mock_detect.assert_called_once()

@pytest.mark.asyncio
async def test_detect_water_leak_endpoint(client_with_mocked_http_client):
    client = client_with_mocked_http_client
    with patch("backend.main.detect_water_leak_clip", new_callable=AsyncMock) as mock_detect:
        mock_detect.return_value = [{"label": "burst pipe", "confidence": 0.88, "box": []}]

        files = {"image": ("test.jpg", b"fakeimagebytes", "image/jpeg")}

        response = client.post("/api/detect-water-leak", files=files)

        assert response.status_code == 200
        assert response.json()["detections"][0]["label"] == "burst pipe"

@pytest.mark.asyncio
async def test_detect_crowd_endpoint(client_with_mocked_http_client):
    client = client_with_mocked_http_client
    with patch("backend.main.detect_crowd_clip", new_callable=AsyncMock) as mock_detect:
        mock_detect.return_value = [{"label": "dense crowd", "confidence": 0.92, "box": []}]

        files = {"image": ("test.jpg", b"fakeimagebytes", "image/jpeg")}

        response = client.post("/api/detect-crowd", files=files)

        assert response.status_code == 200
        assert response.json()["detections"][0]["label"] == "dense crowd"
