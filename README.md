# Space Events API

## Overview
Space Events API is a FastAPI-based project designed to provide a historical archive of space-related events. It integrates with MongoDB to store and retrieve event data efficiently, offering a RESTful interface for CRUD operations.

## Project Structure
```
space-events-api/
│── app/
│   ├── main.py               # Entry point for FastAPI
│   ├── settings              # pydantic-settings (reads in from .env file)
│   ├── database.py           # MongoDB connection
│   ├── models.py             # Event schema/model
│   ├── routes/
│   │   ├── events.py         # API routes for events
│── requirements.txt          # Dependencies
│── .env                      # Environment variables
│── README.md                 # Project documentation
```

## Installation
### Prerequisites
- Python 3.12+
- MongoDB installed and running

### Install Dependencies
Run the following command to install required Python packages:
```sh
pip install -r requirements.txt
```

## Configuration
Configuration is done with the following heirarchy from lowest to highest priority:
1. **Default variables:** can be found in [settings.py](./app/settings.py).
2. **Environment file:** `.env` file should be placed in the project root (not `/app`). The variables in this file override
the default variables.
3. **Environment variables:** can be set directly in the shell. The variables set directly in the environment override the 
variables in the environment file.

## Running the API
1. Make sure MongoDB is running and accessible at localhost:27017

2. Run FastAPI with Uvicorn:
```sh
uvicorn app.main:app --host 0.0.0.0 --port 3001 --reload
```

The API will be available at:
- API: http://localhost:3001
- Interactive API docs: http://localhost:3001/docs
- [Redoc](https://github.com/Redocly/redoc) docs: http://localhost:3001/redoc

## API Endpoints

### Root Endpoint
- `GET /`
  - Returns a welcome message and API information.

### Events Endpoints
- `GET /events/`
  - Retrieves a list of all events.
- `GET /events/{event_id}`
  - Retrieves a specific event by ID.
- `POST /events/`
  - Creates a new event.
- `PUT /events/{event_id}`
  - Updates an existing event.
- `DELETE /events/{event_id}`
  - Deletes an event.

## Event Schema
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "date": "datetime (required, ISO format)",
  "type": "string (optional)",
  "location": "string (optional)",
  "source": "URL (optional)",
  "related_links": ["URL"],
  "tags": ["string"],
  "media": {
    "images": ["URL"],
    "videos": ["URL"]
  },
  "created_at": "datetime (auto-generated)",
  "updated_at": "datetime (auto-generated)"
}
```

## Example Usage

### Create a New Event
```bash
curl -X POST "http://localhost:3001/events/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "SpaceX Starship Launch",
    "description": "First orbital test flight of Starship",
    "date": "2024-03-14T10:00:00Z",
    "type": "Launch",
    "location": "Starbase, Texas",
    "tags": ["SpaceX", "Starship", "Test Flight"]
  }'
```

### Get All Events
```bash
curl "http://localhost:3001/events/"
```

### Get a Specific Event
```bash
curl "http://localhost:3001/events/{event_id}"
```

### Update an Event
```bash
curl -X PUT "http://localhost:3001/events/{event_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description"
  }'
```

### Delete an Event
```bash
curl -X DELETE "http://localhost:3001/events/{event_id}"
```

## Postman
You can find a comprehensive postman collection under the [postman directory](./tests/postman).

To use this collection:
1. Open postman
2. Select `Import`
3. Drop the collection file here

## Future Enhancements
- Implement user authentication
- Add data fetching from external space news sources
- Advanced search and filtering
- Pagination for event listings
- Event categories and filtering

---
Developed using FastAPI and MongoDB 🚀
