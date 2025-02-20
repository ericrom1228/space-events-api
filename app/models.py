from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List, Optional


# Model for storing media-related URLs
class Media(BaseModel):
    images: List[HttpUrl] = []  # List of image URLs
    videos: List[HttpUrl] = []  # List of video URLs


# Base model for an event, containing common fields
class EventBase(BaseModel):
    title: str = Field(..., title="Event Title", max_length=255)  # Event title (required)
    description: Optional[str] = Field(None, title="Event Description")  # Optional description
    date: datetime = Field(..., title="Event Date")  # Date of the event
    type: Optional[str] = Field(None, title="Event Type", max_length=100)  # Optional event type
    location: Optional[str] = Field(None, title="Event Location", max_length=255)  # Optional location
    source: Optional[HttpUrl] = Field(None, title="Source URL")  # Optional source link
    related_links: List[HttpUrl] = []  # List of related URLs
    tags: List[str] = []  # List of associated tags
    media: Optional[Media] = None  # Optional media containing images and videos


# Model for creating a new event, inheriting from EventBase
class EventCreate(EventBase):
    pass  # No additional fields needed beyond EventBase


# Model for updating an existing event
class EventUpdate(EventBase):
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Timestamp of the last update


# Model for an event stored in the database
class EventDB(EventBase):
    id: str = Field(..., alias="_id")  # MongoDB document ID
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Timestamp when the event was created
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Timestamp of the last update

    class Config:
        orm_mode = True  # Enables ORM-style access
        json_encoders = {datetime: lambda v: v.isoformat()}  # Ensures datetime fields are serialized properly
