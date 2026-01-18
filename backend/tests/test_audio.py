from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
import pytest
from backend.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        # Manually set the http_client state for the test app
        # This simulates the startup event
        # Note: TestClient runs startup events automatically in context manager
        # but if mock is needed we can patch it.
        yield c

@pytest.mark.asyncio
async def test_transcribe_audio_endpoint(client):
    # Mock the HF service response
    with patch("backend.main.transcribe_audio_clip", new_callable=AsyncMock) as mock_transcribe:
        mock_transcribe.return_value = "This is a test transcription."

        # Create a fake audio file
        file_content = b"fake audio content"

        response = client.post(
            "/api/transcribe-audio",
            files={"audio": ("test.webm", file_content, "audio/webm")}
        )

        assert response.status_code == 200
        assert response.json() == {"text": "This is a test transcription."}

        # Verify mock was called
        mock_transcribe.assert_called_once()

@pytest.mark.asyncio
async def test_transcribe_audio_failure(client):
    # Mock the HF service response returning None (error)
    with patch("backend.main.transcribe_audio_clip", new_callable=AsyncMock) as mock_transcribe:
        mock_transcribe.return_value = None

        file_content = b"fake audio content"

        response = client.post(
            "/api/transcribe-audio",
            files={"audio": ("test.webm", file_content, "audio/webm")}
        )

        assert response.status_code == 200
        assert "error" in response.json()
