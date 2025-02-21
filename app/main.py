from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import events

app = FastAPI(
    title="Space Events API",
    description="API for managing space-related events and historical data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include event routes
app.include_router(events.router, prefix="/events", tags=["events"])

@app.get("/", tags=["root"])
async def read_root():
    return {
        "message": "Welcome to the Space Events API",
        "docs": "/docs",
        "endpoints": {
            "events": "/events"
        }
    }