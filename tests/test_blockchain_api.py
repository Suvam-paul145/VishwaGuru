from fastapi.testclient import TestClient
import pytest
import hashlib
from backend.main import app
from backend.database import get_db, Base, engine
from backend.models import Issue
from sqlalchemy.orm import Session
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

def test_blockchain_api_chaining(client, db_session):
    # Create first issue via API
    response1 = client.post(
        "/api/issues",
        data={
            "description": "First issue via API",
            "category": "Road",
            "latitude": 19.0760,
            "longitude": 72.8777
        }
    )
    assert response1.status_code == 201
    id1 = response1.json()["id"]

    # Get issue 1 details to get its hash
    issue1 = db_session.query(Issue).filter(Issue.id == id1).first()
    hash1 = issue1.integrity_hash
    assert hash1 is not None
    assert issue1.previous_integrity_hash == ""

    # Verify issue 1
    v_response1 = client.get(f"/api/issues/{id1}/blockchain-verify")
    assert v_response1.status_code == 200
    assert v_response1.json()["is_valid"] == True

    # Create second issue via API
    response2 = client.post(
        "/api/issues",
        data={
            "description": "Second issue via API",
            "category": "Garbage",
            "latitude": 18.5204,
            "longitude": 73.8567
        }
    )
    assert response2.status_code == 201
    id2 = response2.json()["id"]

    # Get issue 2 details
    issue2 = db_session.query(Issue).filter(Issue.id == id2).first()
    assert issue2.previous_integrity_hash == hash1

    # Manually recompute expected hash to verify logic
    lat2_str, lon2_str = f"{18.5204:.7f}", f"{73.8567:.7f}"
    expected_hash2_content = f"Second issue via API|Garbage|{lat2_str}|{lon2_str}|{hash1}"
    expected_hash2 = hashlib.sha256(expected_hash2_content.encode()).hexdigest()
    assert issue2.integrity_hash == expected_hash2

    # Verify issue 2 via API
    v_response2 = client.get(f"/api/issues/{id2}/blockchain-verify")
    assert v_response2.status_code == 200
    assert v_response2.json()["is_valid"] == True
    assert v_response2.json()["current_hash"] == expected_hash2

def test_blockchain_api_tampering(client, db_session):
    # Create an issue
    response = client.post(
        "/api/issues",
        data={
            "description": "Tamper-evident issue",
            "category": "Water",
            "latitude": 19.0,
            "longitude": 72.0
        }
    )
    issue_id = response.json()["id"]

    # Verify it's valid initially
    assert client.get(f"/api/issues/{issue_id}/blockchain-verify").json()["is_valid"] == True

    # Tamper with the data in DB
    db_session.query(Issue).filter(Issue.id == issue_id).update({"description": "Tampered description"})
    db_session.commit()

    # Verify it's now invalid
    v_response = client.get(f"/api/issues/{issue_id}/blockchain-verify")
    assert v_response.json()["is_valid"] == False
    assert "Integrity check failed" in v_response.json()["message"]
