import pytest
import httpx
from httpx import AsyncClient
from backend.main import app
from unittest.mock import patch, MagicMock
from PIL import Image
import io

@pytest.mark.asyncio
async def test_detect_traffic_endpoint():
    # Mock the hf_service.detect_traffic_clip
    from unittest.mock import AsyncMock
    with patch("backend.main.detect_traffic_clip", new_callable=AsyncMock) as mock_detect:
        # Configure mock to return a fake detection
        mock_detect.return_value = [
            {"label": "traffic jam", "confidence": 0.95, "box": []}
        ]

        # Create a dummy image
        img = Image.new('RGB', (100, 100), color = 'red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
            files = {'image': ('test.jpg', img_byte_arr, 'image/jpeg')}
            response = await ac.post("/api/detect-traffic", files=files)

        assert response.status_code == 200
        data = response.json()
        assert "detections" in data
        assert len(data["detections"]) == 1
        assert data["detections"][0]["label"] == "traffic jam"
