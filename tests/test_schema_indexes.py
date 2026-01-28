import pytest
from sqlalchemy import create_engine, inspect
from backend.models import Base, Issue

def test_spatial_indexes_exist():
    # Use in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    indexes = inspector.get_indexes("issues")

    print(f"Found indexes: {indexes}")

    # Check for latitude index
    # Note: SQLite indexes often have auto-generated names, so we check column_names
    lat_index = next((i for i in indexes if i['column_names'] == ['latitude']), None)
    assert lat_index is not None, "Index on latitude column is missing"

    # Check for longitude index
    lon_index = next((i for i in indexes if i['column_names'] == ['longitude']), None)
    assert lon_index is not None, "Index on longitude column is missing"
