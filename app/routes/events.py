"""Routes and CRUD operations for events endpoints."""
from typing import List
from datetime import datetime, UTC
import logging
import bson
from fastapi import APIRouter, HTTPException, Depends, encoders
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models import EventCreate, EventDB, EventUpdate
from app.dependencies import get_database
from app.settings import settings

logger = logging.getLogger("app")

router = APIRouter()


def event_helper(event: dict) -> EventDB:
    """Helper function to convert MongoDB document to Pydantic model

    :param event: MongoDB document
    :return: Pydantic EventDB model
    """
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


@router.post("/", response_model=EventDB, status_code=201)
async def create_event(event: EventCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Create a new event in the database.
    """
    logger.info("Creating new event")
    new_event = event.model_dump()
    now = datetime.now(UTC)
    new_event["created_at"] = now
    new_event["updated_at"] = now
    event_dict = encoders.jsonable_encoder(new_event)
    result = await db["events"].insert_one(event_dict)
    new_event["_id"] = result.inserted_id
    logger.info(
        "New Event: %s inserted in database: %s, collection: events",
        new_event,
        settings.DB_NAME
    )
    return event_helper(new_event)


@router.get("/", response_model=List[EventDB], status_code=200)
async def get_events(db: AsyncIOMotorDatabase = Depends(get_database)) -> List[EventDB]:
    """
    Get all events in the database.
    """
    events_cursor = db["events"].find()
    events = await events_cursor.to_list(length=100)
    return [event_helper(event) for event in events]


@router.get("/{event_id}", response_model=EventDB, status_code=200)
async def get_event(event_id: str, db: AsyncIOMotorDatabase = Depends(get_database)) -> EventDB:
    """
    Get an event by id.
    """
    try:
        event = await db["events"].find_one({"_id": ObjectId(event_id)})

    except bson.errors.InvalidId as e:
        raise HTTPException(
            status_code=400,
            detail=f"{e}"
        ) from e

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_helper(event)


@router.patch("/{event_id}", response_model=EventDB, status_code=200)
async def update_event(
        event_id: str,
        event_update: EventUpdate,
        db: AsyncIOMotorDatabase = Depends(get_database)
) -> EventDB:
    """
    Update an event by id.
    """
    update_data = event_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(UTC)

    result = await db["events"].find_one_and_update(
        {"_id": ObjectId(event_id)},
        {"$set": update_data},
        return_document=True
    )

    if not result:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_helper(result)


@router.delete("/{event_id}", response_model=dict, status_code=200)
async def delete_event(event_id: str, db: AsyncIOMotorDatabase = Depends(get_database)) -> dict:
    """
    Delete an event by id.
    """
    result = await db["events"].find_one_and_delete({"_id": ObjectId(event_id)})

    if not result:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Event deleted successfully"}
