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
    lat1, lon1 = 19.0760, 72.8777
    lat1_str, lon1_str = f"{lat1:.7f}", f"{lon1:.7f}"
    hash1_content = f"First issue|Road|{lat1_str}|{lon1_str}|"
    hash1 = hashlib.sha256(hash1_content.encode()).hexdigest()

    issue1 = Issue(
        description="First issue",
        category="Road",
        latitude=lat1,
        longitude=lon1,
        integrity_hash=hash1,
        previous_integrity_hash=""
    )
    db_session.add(issue1)
    db_session.commit()
    db_session.refresh(issue1)

    # Create second issue chained to first
    lat2, lon2 = 18.5204, 73.8567
    lat2_str, lon2_str = f"{lat2:.7f}", f"{lon2:.7f}"
    hash2_content = f"Second issue|Garbage|{lat2_str}|{lon2_str}|{hash1}"
    hash2 = hashlib.sha256(hash2_content.encode()).hexdigest()

    issue2 = Issue(
        description="Second issue",
        category="Garbage",
        latitude=lat2,
        longitude=lon2,
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

def test_blockchain_verification_failure(client, db_session):
    # Create issue with tampered hash
    issue = Issue(
        description="Tampered issue",
        category="Road",
        latitude=19.0,
        longitude=72.0,
        integrity_hash="invalidhash",
        previous_integrity_hash="someprevhash"
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
