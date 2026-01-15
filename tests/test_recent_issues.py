import sys
import os
import json
from datetime import datetime
import pytest

# Adjust path to import backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import app and dependencies
from main import app, get_db
from database import Base
from models import Issue
from cache import recent_issues_cache

# Setup in-memory DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_recent_issues_caching():
    # Clear cache
    recent_issues_cache.invalidate()

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Add dummy data
    db = TestingSessionLocal()
    issue1 = Issue(
        description="Test Issue 1",
        category="Road",
        status="open",
        created_at=datetime(2023, 1, 1, 12, 0, 0),
        action_plan=json.dumps({"step": "1"})
    )
    db.add(issue1)
    db.commit()
    db.close()

    with TestClient(app) as client:
        # First call - Cache Miss
        response1 = client.get("/api/issues/recent")
        assert response1.status_code == 200
        data1 = response1.json()
        assert len(data1) == 1
        assert data1[0]["description"] == "Test Issue 1"

        # Verify cache is populated
        assert recent_issues_cache.get() is not None

        # Second call - Cache Hit (String format)
        response2 = client.get("/api/issues/recent")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2 == data1
        assert response2.headers["content-type"] == "application/json"

        # Verify robustness with legacy format (List of dicts)
        # Manually inject list into cache
        recent_issues_cache.set([{"id": 999, "description": "Legacy", "category": "Road", "created_at": "2023-01-01T12:00:00", "status": "open", "upvotes": 0}])

        response3 = client.get("/api/issues/recent")
        assert response3.status_code == 200
        data3 = response3.json()
        assert len(data3) == 1
        assert data3[0]["description"] == "Legacy"

if __name__ == "__main__":
    test_recent_issues_caching()
