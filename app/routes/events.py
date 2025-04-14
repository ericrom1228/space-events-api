import bson
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime, UTC
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models import EventCreate, EventDB, EventUpdate
from app.dependencies import get_database
from fastapi.encoders import jsonable_encoder

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
async def create_event(event: EventCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    new_event = event.model_dump()
    new_event["created_at"] = datetime.now(UTC)
    new_event["updated_at"] = datetime.now(UTC)
    event_dict = jsonable_encoder(new_event)
    result = await db["events"].insert_one(event_dict)
    new_event["id"] = result.inserted_id
    return event_helper(new_event)


# Get all events
@router.get("/", response_model=List[EventDB])
async def get_events(db: AsyncIOMotorDatabase = Depends(get_database)):
    events_cursor = db["events"].find()
    events = await events_cursor.to_list(length=100)
    return [event_helper(event) for event in events]


# Get a single event by ID
@router.get("/{event_id}", response_model=EventDB)
async def get_event(event_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        event = await db["events"].find_one({"_id": ObjectId(event_id)})
    except bson.errors.InvalidId as e:
        raise HTTPException(
            status_code=400,
            detail=f"{e}"
        )

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_helper(event)


# Update an event by ID
@router.put("/{event_id}", response_model=EventDB)
async def update_event(event_id: str, event_update: EventUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    update_data = event_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    result = await db["events"].find_one_and_update(
        {"_id": ObjectId(event_id)},
        {"$set": update_data},
        return_document=True
    )

    if not result:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_helper(result)


# Delete an event by ID
@router.delete("/{event_id}", response_model=dict)
async def delete_event(event_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    result = await db["events"].find_one_and_delete({"_id": ObjectId(event_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Event deleted successfully"}
