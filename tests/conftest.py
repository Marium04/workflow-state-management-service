import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, engine, get_db

# Create a separate session for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create all tables before running tests
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    """FastAPI test client using SQLite in-memory DB."""
    with TestClient(app) as c:
        yield c
