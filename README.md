# Space API

## Overview
Space API is a FastAPI-based project designed to provide space-related news and a historical archive of space events. It integrates with MongoDB to store and retrieve event data efficiently.

## Project Structure
```
space_api/
│── app/
│   ├── main.py               # Entry point for FastAPI
│   ├── database.py           # MongoDB connection
│   ├── models.py             # Event schema/model
│   ├── routes/
│   │   ├── events.py         # API routes for events
│   ├── services/
│   │   ├── event_service.py  # Business logic for event handling
│   ├── config.py             # Configuration settings
│── requirements.txt          # Dependencies
│── .env                      # Environment variables
│── README.md                 # Project documentation
```

## Installation
### Prerequisites
- Python 3.8+
- MongoDB installed and running

### Install Dependencies
Run the following command to install required Python packages:
```sh
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the project root with the following content:
```
MONGO_URI=mongodb://localhost:27017
DB_NAME=space_db
```

## Running the API
Start MongoDB (if not already running):
```sh
mongod --dbpath /your/db/path
```

Run FastAPI with Uvicorn:
```sh
uvicorn app.main:app --reload
```

## API Endpoints

### Root Endpoint
- `GET /`
  - Returns a welcome message.

### Events Endpoints
- `GET /events/`
  - Retrieves a list of all events.
- `GET /events/{event_id}`
  - Retrieves a specific event by ID.
- `POST /events/`
  - Creates a new event.

## Database Schema
```json
{
  "title": "string",
  "description": "string",
  "date": "ISODate",
  "type": "string",
  "location": "string",
  "source": "string",
  "related_links": ["string"],
  "tags": ["string"],
  "media": { "images": ["string"], "videos": ["string"] },
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

## Swagger UI
Once the API is running, visit:
```
http://127.0.0.1:8000/docs
```
for interactive API documentation.

## Future Enhancements
- Implement user authentication
- Add data fetching from external space news sources
- Advanced search and filtering

---
Developed using FastAPI and MongoDB 🚀

