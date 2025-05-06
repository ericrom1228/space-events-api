"""Module to set up configurations for tests"""
import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from app.main import app
from app.dependencies import get_database


@pytest.fixture
def app_mock():
    """Fixture to set up app mock"""
    return app


@pytest.fixture
def client():
    """Fixture to set up HTTP test client"""
    return TestClient(app)


@pytest.fixture
async def mock_db():
    """Fixture to set up the connection to the mock mongo"""
    mongo_client = AsyncMongoMockClient()
    db = mongo_client['test_space_events']

    async def override_get_db():
        return db

    app.dependency_overrides[get_database] = override_get_db
    yield db
    app.dependency_overrides.clear()


@pytest.fixture
def sample_event():
    """Fixture for event sample data"""
    return {
        "title": "Test Space Event",
        "description": "This is a test space event",
        "date": "2024-03-14T10:00:00Z",
        "type": "Test",
        "location": "Test Location",
        "tags": ["test", "space"],
        "source": "https://test.com",
        "related_links": ["https://test.com/related"],
        "media": {
            "images": ["https://test.com/image.jpg"],
            "videos": ["https://test.com/video.mp4"]
        }
    }
