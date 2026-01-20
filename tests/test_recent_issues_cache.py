
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import json
import time
from datetime import datetime
from backend.main import app, get_db
from backend.models import Issue
from backend.cache import recent_issues_cache

# Mock DB dependency
def override_get_db():
    db = MagicMock()
    # Create dummy issues
    issues = []
    for i in range(10):
        issue = Issue(
            id=i,
            description=f"Issue {i}",
            category="Pothole",
            image_path=f"/tmp/img{i}.jpg",
            status="open",
            created_at=datetime.now(),
            user_email="test@example.com",
            upvotes=0,
            latitude=10.0,
            longitude=20.0,
            location="Test Loc",
            action_plan=json.dumps({"whatsapp": "hi"})
        )
        issues.append(issue)

    db.query.return_value.order_by.return_value.limit.return_value.all.return_value = issues
    yield db

app.dependency_overrides[get_db] = override_get_db

def test_get_recent_issues_cache_optimization():
    # Clear cache first
    recent_issues_cache.invalidate()

    with TestClient(app) as client:
        # First call - Cache Miss
        start_time = time.time()
        response = client.get("/api/issues/recent")
        end_time = time.time()
        first_call_time = end_time - start_time

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10
        assert data[0]["description"] == "Issue 0"

        # Verify cache is set (implementation detail: currently it stores list of dicts, we want to change it to str)
        assert recent_issues_cache.get() is not None

        # Second call - Cache Hit
        start_time = time.time()
        response2 = client.get("/api/issues/recent")
        end_time = time.time()
        second_call_time = end_time - start_time

        assert response2.status_code == 200
        assert response2.json() == data

        print(f"First call (Miss): {first_call_time:.6f}s")
        print(f"Second call (Hit): {second_call_time:.6f}s")
