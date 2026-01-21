import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from backend.main import app

client = TestClient(app)

@pytest.fixture
def mock_hf_service():
    with patch('backend.main.detect_accessibility_clip', new_callable=AsyncMock) as mock_acc, \
         patch('backend.main.detect_crowd_clip', new_callable=AsyncMock) as mock_crowd:
        yield mock_acc, mock_crowd

def test_detect_accessibility(mock_hf_service):
    mock_acc, _ = mock_hf_service
    mock_acc.return_value = [{"label": "blocked wheelchair ramp", "confidence": 0.9}]

    # Create a dummy image file
    files = {'image': ('test.jpg', b'fakeimagebytes', 'image/jpeg')}

    with patch('backend.main.validate_uploaded_file'), \
         patch('backend.main.validate_image_for_processing'), \
         TestClient(app) as client:
             # Also mock initialize_ai_services and bot start in lifespan if needed,
             # but TestClient triggers lifespan which does create_all_ai_services etc.
             # We should probably mock them to speed up tests.
             with patch('backend.main.create_all_ai_services', return_value=(AsyncMock(), AsyncMock(), AsyncMock())), \
                  patch('backend.main.initialize_ai_services'), \
                  patch('backend.main.load_maharashtra_pincode_data'), \
                  patch('backend.main.load_maharashtra_mla_data'), \
                  patch('backend.main.run_bot', new_callable=AsyncMock):
                response = client.post("/api/detect-accessibility", files=files)

    assert response.status_code == 200
    assert response.json() == {"detections": [{"label": "blocked wheelchair ramp", "confidence": 0.9}]}

def test_detect_crowd(mock_hf_service):
    _, mock_crowd = mock_hf_service
    mock_crowd.return_value = [{"label": "crowded", "confidence": 0.8}]

    files = {'image': ('test.jpg', b'fakeimagebytes', 'image/jpeg')}

    with patch('backend.main.validate_uploaded_file'), \
         patch('backend.main.validate_image_for_processing'), \
         TestClient(app) as client:
            with patch('backend.main.create_all_ai_services', return_value=(AsyncMock(), AsyncMock(), AsyncMock())), \
                  patch('backend.main.initialize_ai_services'), \
                  patch('backend.main.load_maharashtra_pincode_data'), \
                  patch('backend.main.load_maharashtra_mla_data'), \
                  patch('backend.main.run_bot', new_callable=AsyncMock):
                response = client.post("/api/detect-crowd", files=files)

    assert response.status_code == 200
    assert response.json() == {"detections": [{"label": "crowded", "confidence": 0.8}]}
