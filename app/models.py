from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_serializer
from datetime import datetime, UTC
from typing import List, Optional


# Model for storing media-related URLs
class Media(BaseModel):
    images: List[HttpUrl] = []  # List of image URLs
    videos: List[HttpUrl] = []  # List of video URLs

    @field_serializer("images", "videos")
    def serialize_urls(self, value):
        return [str(url) for url in value]


# Base model for an event, containing common fields
class EventBase(BaseModel):
    title: str = Field(..., title="Event Title", max_length=255)  # Event title (required)
    description: Optional[str] = Field(None, title="Event Description")  # Optional description
    date: datetime = Field(..., title="Event Date")  # Date of the event (required)
    type: Optional[str] = Field(None, title="Event Type", max_length=100)  # Optional event type
    location: Optional[str] = Field(None, title="Event Location", max_length=255)  # Optional location
    source: Optional[HttpUrl] = Field(None, title="Source URL")  # Optional source link
    related_links: List[HttpUrl] = []  # List of related URLs
    tags: List[str] = []  # List of associated tags
    media: Optional[Media] = None  # Optional media containing images and videos

    # Convert HttpUrl fields to plain strings before storing in MongoDB
    @field_serializer("source", "related_links")
    def serialize_url(self, value):
        if isinstance(value, list):
            return [str(url) for url in value]
        return str(value) if value else None


# Model for creating a new event, inheriting from EventBase
class EventCreate(EventBase):
    pass  # No additional fields needed beyond EventBase


# Model for updating an existing event
class EventUpdate(EventBase):
    title: Optional[str] = Field(None, title="Event Title", max_length=255)  # Event title (required)
    date: Optional[datetime] = Field(None, title="Event Date")  # Date of the event
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))  # Timestamp of the last update


# Model for an event stored in the database
class EventDB(EventBase):
    id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))  # Timestamp when the event was created
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))  # Timestamp of the last update

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at", "updated_at")
    def serialize_datetimes(self, dt: datetime, _info):
        return dt.isoformat()