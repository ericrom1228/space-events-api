"""Test events module."""
import pytest
from fastapi import status
from bson import ObjectId


@pytest.mark.asyncio
async def test_create_event(client, mock_db, sample_event):
    """Test creating an event"""
    assert await mock_db['events'].count_documents({}) == 0
    response = client.post("/events", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_get_events(client, sample_event):
    """Test getting all events"""
    response = client.post("/events", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get("/events")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == sample_event["title"]


@pytest.mark.asyncio
async def test_get_event(client, sample_event):
    """Test getting a single event"""
    response = client.post("/events", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED
    event_id = response.json()["id"]

    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == sample_event["title"]
    assert data["id"] == event_id


@pytest.mark.asyncio
async def test_update_event(client, sample_event):
    """Test updating (patching) an event"""
    response = client.post("/events", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED
    event_id = response.json()["id"]

    updated_data = {"title": "Updated Test Event"}
    response = client.patch(f"/events/{event_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Test Event"
    assert data["description"] == sample_event["description"]


@pytest.mark.asyncio
async def test_delete_event(client, sample_event):
    """Test deleting an event"""
    response = client.post("/events/", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED
    event_id = response.json()["id"]

    response = client.delete(f"/events/{event_id}")
    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_nonexistent_event(client):
    """Test correct response for getting an event that
    doesn't exist
    """
    nonexistent_id = str(ObjectId())
    response = client.get(f"/events/{nonexistent_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_event_invalid_data(client):
    """Test creating an event"""
    invalid_event = {
        "title": "",  # Empty title should be invalid
        "date": "invalid-date"  # Invalid date format
    }
    response = client.post("/events/", json=invalid_event)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
