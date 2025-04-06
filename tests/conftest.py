import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from app.main import app
from app.database import get_db

@pytest.fixture
def test_app():
    return app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
async def mock_db():
    client = AsyncMongoMockClient()
    db = client.test_space_events
    
    # Override the dependency
    async def override_get_db():
        return db
    
    app.dependency_overrides[get_db] = override_get_db
    yield db
    app.dependency_overrides.clear()

@pytest.fixture
def sample_event():
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