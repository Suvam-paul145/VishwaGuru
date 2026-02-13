from fastapi.testclient import TestClient
import pytest
import hashlib
from backend.main import app
from backend.database import get_db, Base, engine
from backend.models import Issue
from sqlalchemy.orm import Session

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

def test_blockchain_verification_success(client, db_session):
    # Create first issue
    hash1_content = "First issue|Road|"
    hash1 = hashlib.sha256(hash1_content.encode()).hexdigest()

    issue1 = Issue(
        description="First issue",
        category="Road",
        integrity_hash=hash1,
        previous_integrity_hash=""
    )
    db_session.add(issue1)
    db_session.commit()
    db_session.refresh(issue1)

    # Create second issue chained to first
    hash2_content = f"Second issue|Garbage|{hash1}"
    hash2 = hashlib.sha256(hash2_content.encode()).hexdigest()

    issue2 = Issue(
        description="Second issue",
        category="Garbage",
        integrity_hash=hash2,
        previous_integrity_hash=hash1
    )
    db_session.add(issue2)
    db_session.commit()
    db_session.refresh(issue2)

    # Verify first issue
    response = client.get(f"/api/issues/{issue1.id}/blockchain-verify")
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] == True
    assert data["current_hash"] == hash1

    # Verify second issue
    response = client.get(f"/api/issues/{issue2.id}/blockchain-verify")
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] == True
    assert data["current_hash"] == hash2

def test_blockchain_duplicate_creation(client, db_session):
    # 1. Create original issue
    response = client.post(
        "/api/issues",
        data={
            "description": "Original pothole report",
            "category": "Road",
            "latitude": 10.0,
            "longitude": 10.0,
            "user_email": "user1@example.com"
        }
    )
    assert response.status_code == 201
    original_id = response.json()["id"]

    # Get hash of original
    original_issue = db_session.query(Issue).filter(Issue.id == original_id).first()
    original_hash = original_issue.integrity_hash

    # 2. Create duplicate issue
    response = client.post(
        "/api/issues",
        data={
            "description": "Duplicate pothole report",
            "category": "Road",
            "latitude": 10.0001, # Very close
            "longitude": 10.0001,
            "user_email": "user2@example.com"
        }
    )
    assert response.status_code == 201
    assert response.json()["id"] is None
    assert response.json()["linked_issue_id"] == original_id

    # 3. Verify duplicate record exists in DB and is linked in blockchain
    duplicate_issue = db_session.query(Issue).filter(Issue.status == "duplicate").first()
    assert duplicate_issue is not None
    assert duplicate_issue.parent_issue_id == original_id
    assert duplicate_issue.previous_integrity_hash == original_hash

    # 4. Verify integrity of duplicate
    response = client.get(f"/api/issues/{duplicate_issue.id}/blockchain-verify")
    assert response.status_code == 200
    assert response.json()["is_valid"] == True

def test_blockchain_verification_failure(client, db_session):
    # Create issue with tampered hash
    issue = Issue(
        description="Tampered issue",
        category="Road",
        integrity_hash="invalidhash"
    )
    db_session.add(issue)
    db_session.commit()
    db_session.refresh(issue)

    response = client.get(f"/api/issues/{issue.id}/blockchain-verify")
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] == False
    assert data["message"].startswith("Integrity check failed")

def test_upvote_optimization(client, db_session):
    issue = Issue(
        description="Test issue for upvote",
        category="Road",
        upvotes=10
    )
    db_session.add(issue)
    db_session.commit()
    db_session.refresh(issue)

    response = client.post(f"/api/issues/{issue.id}/vote")
    assert response.status_code == 200
    data = response.json()
    assert data["upvotes"] == 11

    # Verify in DB
    db_session.refresh(issue)
    assert issue.upvotes == 11
