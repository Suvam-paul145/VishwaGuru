import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from backend.hf_service import analyze_urgency
from backend.main import app
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_analyze_urgency_mocked():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "labels": ["High Urgency", "Low Urgency"],
            "scores": [0.9, 0.1]
        }
        mock_post.return_value = mock_response

        urgency = await analyze_urgency("There is a massive fire here!")
        assert urgency == "High"

@pytest.mark.asyncio
async def test_analyze_urgency_fallback():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        urgency = await analyze_urgency("Some text")
        assert urgency == "Medium" # Default

def test_create_issue_with_urgency():
    # Mocking dependencies
    with patch("backend.main.analyze_urgency", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = "Critical"

        # We also need to mock DB and Action Plan generation to isolate
        with patch("backend.main.run_in_threadpool", new_callable=AsyncMock) as mock_threadpool, \
             patch("backend.main.generate_action_plan", new_callable=AsyncMock) as mock_plan, \
             patch("backend.main.save_file_blocking"):

            mock_plan.return_value = {"steps": []}

            # Mock DB logic inside threadpool
            async def side_effect(func, *args, **kwargs):
                if func.__name__ == 'save_issue_db':
                     issue = args[1]
                     issue.id = 123
                     # issue.urgency is set in create_issue before calling save_issue_db
                     return issue
                return None
            mock_threadpool.side_effect = side_effect

            with TestClient(app) as client:
                response = client.post("/api/issues", data={
                    "description": "Critical issue description",
                    "category": "road"
                })

                assert response.status_code == 200

                mock_analyze.assert_called_once()
                assert "Critical issue description" in mock_analyze.call_args[0][0]
