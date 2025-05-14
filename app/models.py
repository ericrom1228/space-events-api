"""Models/Schemas for events"""
from datetime import datetime, UTC
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_serializer
from app.utils.serializers import serialize_httpurls


class Media(BaseModel):
    """
    Model for storing media-related URLs
    """
    images: List[HttpUrl] = []  # List of image URLs
    videos: List[HttpUrl] = []  # List of video URLs

    @field_serializer("images", "videos")
    def _serialize_urls(self, urls):
        return serialize_httpurls(urls)


class EventBase(BaseModel):
    """
    Base model for an event, containing common fields
    """
    title: str = Field(
        ...,
        title="Event Title",
        max_length=255
    )
    description: Optional[str] = Field(
        None,
        title="Event Description"
    )
    date: datetime = Field(
        ...,
        title="Event Date"
    )
    type: Optional[str] = Field(
        None, title="Event Type",
        max_length=100
    )
    location: Optional[str] = Field(
        None, title="Event Location",
        max_length=255
    )
    source: Optional[HttpUrl] = Field(
        None,
        title="Source URL"
    )
    related_links: List[HttpUrl] = []
    tags: List[str] = []
    media: Optional[Media] = None

    # Convert HttpUrl fields to plain strings before storing in MongoDB
    @field_serializer("source", "related_links")
    def _serialize_urls(self, urls):
        return serialize_httpurls(urls)


class EventCreate(EventBase):
    """
    Model for creating a new event, inheriting from EventBase
    """


class EventUpdate(EventBase):
    """
    Model for updating an existing event
    """
    title: Optional[str] = Field(
        None,
        title="Event Title",
        max_length=255
    )
    date: Optional[datetime] = Field(
        None,
        title="Event Date"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )


class EventDB(EventBase):
    """
    Model for an event stored in the database
    """
    id: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at", "updated_at")
    def _serialize_datetimes(self, dt: datetime, _info):
        return dt.isoformat()
