"""Tests for models.py"""
from datetime import datetime, UTC
import pytest
from pydantic import HttpUrl
from app.models import EventBase, Media


def test_event_model_valid():
    """Test EventBase model valid"""
    event_data = {
        "title": "Test Event",
        "description": "Test Description",
        "date": datetime.now(UTC),
        "type": "Test",
        "location": "Test Location",
        "source": "https://test.com",
        "related_links": ["https://test.com/related"],
        "tags": ["test", "event"],
        "media": {
            "images": ["https://test.com/image.jpg"],
            "videos": ["https://test.com/video.mp4"]
        }
    }
    event = EventBase(**event_data)
    assert event.title == event_data["title"]
    assert event.description == event_data["description"]
    assert isinstance(event.media, Media)


def test_event_model_minimal():
    """Test EventBase with minimal required fields"""
    event_data = {
        "title": "Test Event",
        "date": datetime.now(UTC)
    }
    event = EventBase(**event_data)
    assert event.title == event_data["title"]
    assert event.description is None
    assert not event.tags
    assert event.media is None


def test_event_model_invalid_date():
    """Test EventBase with invalid date"""
    with pytest.raises(ValueError):
        EventBase(title="Test Event", date="invalid-date")


def test_media_model():
    """Test Media model"""
    media_data = {
        "images": ["https://test.com/image1.jpg", "https://test.com/image2.jpg"],
        "videos": ["https://test.com/video1.mp4"]
    }
    media = Media(**media_data)
    assert len(media.images) == 2
    assert len(media.videos) == 1
    assert media.images[0] == HttpUrl(media_data["images"][0])
    assert media.videos[0] == HttpUrl(media_data["videos"][0])
