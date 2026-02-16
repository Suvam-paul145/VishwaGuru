import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.models import Issue

# Setup in-memory DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_get_issue_details(test_db):
    client = TestClient(app)

    # Create a test issue directly in DB
    issue = Issue(
        description="Test Issue for Tracking",
        category="Road",
        status="open",
        latitude=18.5204,
        longitude=73.8567,
        location="Pune"
    )
    test_db.add(issue)
    test_db.commit()
    test_db.refresh(issue)

    # Test GET endpoint
    response = client.get(f"/api/issues/{issue.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == issue.id
    assert data["description"] == "Test Issue for Tracking"
    assert data["status"] == "open"

    # Test 404
    response = client.get("/api/issues/999999")
    assert response.status_code == 404
