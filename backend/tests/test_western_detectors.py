import pytest
import warnings
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock, patch
import io
import sys
import os
from PIL import Image

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from pathlib import Path

# Ensure repository root is importable
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Set environment variable
os.environ['FRONTEND_URL'] = 'http://localhost:5173'

# Mock magic
mock_magic = MagicMock()
mock_magic.from_buffer.return_value = "image/jpeg"
sys.modules['magic'] = mock_magic

# Mock telegram
mock_telegram = MagicMock()
sys.modules['telegram'] = mock_telegram
sys.modules['telegram.ext'] = mock_telegram.ext

# Import app inside patch context to avoid import errors
# We need to mock create_all_ai_services because main.py calls it at startup
with patch("backend.main.create_all_ai_services") as mock_create_ai:
    mock_action = AsyncMock()
    mock_chat = AsyncMock()
    mock_summary = AsyncMock()
    # It returns 3 objects
    mock_create_ai.return_value = (mock_action, mock_chat, mock_summary)
    from backend.main import app

# Fixture for TestClient
@pytest.fixture
def client():
    # We patch the dependency injection get_http_client
    # So that the router uses our mock client
    mock_client = AsyncMock()
    app.dependency_overrides = {} # Reset

    # We need to ensure the router gets this mock client.
    # The router calls `client = get_http_client(request)`.
    # backend.dependencies.get_http_client returns request.app.state.http_client.

    app.state.http_client = mock_client

    with TestClient(app) as c:
        yield c

def create_test_image():
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

def test_detect_public_facilities_damaged(client):
    # Setup mock response
    mock_http_client = client.app.state.http_client
    mock_response = MagicMock()
    mock_response.status_code = 200
    # CLIP response
    mock_response.json.return_value = [
        {"label": "damaged bench", "score": 0.85},
        {"label": "good condition public facility", "score": 0.15}
    ]
    # We need to mock the async post method
    async def async_post(*args, **kwargs):
        return mock_response
    mock_http_client.post = AsyncMock(side_effect=async_post)

    img_bytes = create_test_image()

    response = client.post(
        "/api/detect-public-facilities",
        files={"image": ("bench.jpg", img_bytes, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "detections" in data
    # "damaged bench" is in targets
    assert len(data["detections"]) == 1
    assert data["detections"][0]["label"] == "damaged bench"

def test_detect_public_facilities_safe(client):
    mock_http_client = client.app.state.http_client
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"label": "good condition public facility", "score": 0.90},
        {"label": "damaged bench", "score": 0.10}
    ]
    async def async_post(*args, **kwargs):
        return mock_response
    mock_http_client.post = AsyncMock(side_effect=async_post)

    img_bytes = create_test_image()

    response = client.post(
        "/api/detect-public-facilities",
        files={"image": ("bench.jpg", img_bytes, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    # "good condition public facility" is NOT in targets
    assert len(data["detections"]) == 0

def test_detect_construction_safety_unsafe(client):
    mock_http_client = client.app.state.http_client
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"label": "unsafe construction site", "score": 0.88},
        {"label": "safe construction site", "score": 0.12}
    ]
    async def async_post(*args, **kwargs):
        return mock_response
    mock_http_client.post = AsyncMock(side_effect=async_post)

    img_bytes = create_test_image()

    response = client.post(
        "/api/detect-construction-safety",
        files={"image": ("site.jpg", img_bytes, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["detections"]) == 1
    assert data["detections"][0]["label"] == "unsafe construction site"
