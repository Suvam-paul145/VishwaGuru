import pytest
import math
from backend.spatial_utils import get_bounding_box
from fastapi.testclient import TestClient
from backend.main import app
from backend.models import Issue
from backend.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_get_bounding_box_logic():
    # Mumbai coordinates
    lat = 19.0760
    lon = 72.8777
    radius = 1000.0 # 1km

    min_lat, max_lat, min_lon, max_lon = get_bounding_box(lat, lon, radius)

    # 1 degree lat is approx 111km -> 1km is approx 0.009 degrees
    expected_delta_lat = 1000 / 111320.0
    assert abs((max_lat - lat) - expected_delta_lat) < 0.0001
    assert abs((lat - min_lat) - expected_delta_lat) < 0.0001

    assert min_lat < lat < max_lat
    assert min_lon < lon < max_lon

def test_get_nearby_issues_spatial_filtering(client, db_session):
    # Center point (Mumbai)
    center_lat = 19.0760
    center_lon = 72.8777

    # Issue 1: Very close (10m away)
    issue_close = Issue(
        description="Close issue",
        category="Road",
        status="open",
        latitude=center_lat + 0.00009, # approx 10m north
        longitude=center_lon,
        reference_id="ref_close"
    )
    db_session.add(issue_close)

    # Issue 2: Inside bounding box (approx 330m away)
    # 0.003 deg is approx 334m
    issue_medium = Issue(
        description="Medium issue",
        category="Road",
        status="open",
        latitude=center_lat + 0.003,
        longitude=center_lon,
        reference_id="ref_medium"
    )
    db_session.add(issue_medium)

    # Issue 3: Far away (Pune, approx 150km away)
    issue_far = Issue(
        description="Far issue",
        category="Road",
        status="open",
        latitude=18.5204,
        longitude=73.8567,
        reference_id="ref_far"
    )
    db_session.add(issue_far)

    db_session.commit()

    # Test 1: Small radius (should only find close issue)
    response = client.get(
        "/api/issues/nearby",
        params={
            "latitude": center_lat,
            "longitude": center_lon,
            "radius": 100.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    ids = [i['id'] for i in data]
    assert issue_close.id in ids
    assert issue_medium.id not in ids
    assert issue_far.id not in ids

    # Test 2: Medium radius (should find close and medium)
    # Max allowed radius is 500m
    response = client.get(
        "/api/issues/nearby",
        params={
            "latitude": center_lat,
            "longitude": center_lon,
            "radius": 400.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    ids = [i['id'] for i in data]
    assert issue_close.id in ids
    assert issue_medium.id in ids
    assert issue_far.id not in ids
