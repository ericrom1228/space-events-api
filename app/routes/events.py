from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from bson import ObjectId
from app.database import events_collection
from app.models import EventCreate, EventDB, EventUpdate

router = APIRouter()


# Helper function to convert MongoDB document to Pydantic model
def event_helper(event) -> EventDB:
    return EventDB(
        id=str(event["_id"]),
        title=event["title"],
        description=event.get("description"),
        date=event["date"],
        type=event.get("type"),
        location=event.get("location"),
        source=event.get("source"),
        related_links=event.get("related_links", []),
        tags=event.get("tags", []),
        media=event.get("media"),
        created_at=event["created_at"],
        updated_at=event["updated_at"]
    )


# Create an event
@router.post("/", response_model=EventDB)
async def create_event(event: EventCreate):
    new_event = event.dict()
    new_event["created_at"] = datetime.utcnow()
    new_event["updated_at"] = datetime.utcnow()

    result = await events_collection.insert_one(new_event)
    new_event["_id"] = result.inserted_id

    return event_helper(new_event)


# Get all events
@router.get("/", response_model=List[EventDB])
async def get_events():
    events_cursor = events_collection.find()
    events = await events_cursor.to_list(length=100)

    return [event_helper(event) for event in events]


# Get a single event by ID
@router.get("/{event_id}", response_model=EventDB)
async def get_event(event_id: str):
    event = await events_collection.find_one({"_id": ObjectId(event_id)})

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_helper(event)


# Update an event by ID
@router.put("/{event_id}", response_model=EventDB)
async def update_event(event_id: str, event_update: EventUpdate):
    update_data = event_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    result = await events_collection.find_one_and_update(
        {"_id": ObjectId(event_id)},
        {"$set": update_data},
        return_document=True
    )

    if not result:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_helper(result)


# Delete an event by ID
@router.delete("/{event_id}", response_model=dict)
async def delete_event(event_id: str):
    result = await events_collection.delete_one({"_id": ObjectId(event_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Event deleted successfully"}
