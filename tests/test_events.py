import pytest
from fastapi import status
from bson import ObjectId

@pytest.mark.asyncio
async def test_create_event(client, mock_db, sample_event):
    response = client.post("/events/", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == sample_event["title"]
    assert "_id" in data

@pytest.mark.asyncio
async def test_get_events(client, mock_db, sample_event):
    # Create a test event first
    response = client.post("/events/", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Get all events
    response = client.get("/events/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == sample_event["title"]

@pytest.mark.asyncio
async def test_get_event(client, mock_db, sample_event):
    # Create a test event first
    response = client.post("/events/", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED
    event_id = response.json()["_id"]
    
    # Get the specific event
    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == sample_event["title"]
    assert data["_id"] == event_id

@pytest.mark.asyncio
async def test_update_event(client, mock_db, sample_event):
    # Create a test event first
    response = client.post("/events/", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED
    event_id = response.json()["_id"]
    
    # Update the event
    updated_data = {"title": "Updated Test Event"}
    response = client.put(f"/events/{event_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Test Event"
    assert data["description"] == sample_event["description"]

@pytest.mark.asyncio
async def test_delete_event(client, mock_db, sample_event):
    # Create a test event first
    response = client.post("/events/", json=sample_event)
    assert response.status_code == status.HTTP_201_CREATED
    event_id = response.json()["_id"]
    
    # Delete the event
    response = client.delete(f"/events/{event_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify event is deleted
    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_nonexistent_event(client, mock_db):
    nonexistent_id = str(ObjectId())
    response = client.get(f"/events/{nonexistent_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_create_event_invalid_data(client, mock_db):
    invalid_event = {
        "title": "",  # Empty title should be invalid
        "date": "invalid-date"  # Invalid date format
    }
    response = client.post("/events/", json=invalid_event)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY