"""Main entry point for the application."""
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.logging_config import configure_logging
from app.routes import events
from app.settings import settings
from app.dependencies import connect_to_mongo, close_mongo_connection

configure_logging()
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Lifespan context: defines code that will be executed before startup and after shutdown
    :param application:
    """
    logger.info("Starting Space Events API")
    logger.info("Connecting to mongo")
    await connect_to_mongo(application)
    yield
    logger.info("Shutting down Space Events API")
    await close_mongo_connection(application)


app = FastAPI(
    title="Space Events API",
    description="API for managing space-related events and historical data",
    version=settings.API_VERSION,
    lifespan=lifespan
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
    """Get the root route."""
    logger.info("GET /")
    return {
        "message": "Welcome to the Space Events API",
        "docs": "/docs",
        "endpoints": {
            "events": "/events"
        }
    }

@app.get("/about", tags=["admin"])
async def read_about():
    """Get the information about the API."""
    logger.info("GET /about")
    return {
        "name": "Space Events API",
        "description": "API for managing space-related events and historical data",
        "version": settings.VERSION,
        "build datetime": settings.BUILD_DATETIME,
        "api version": settings.API_VERSION,
        "mongo URI": settings.MONGO_URI,
        "database": settings.DB_NAME
    }


@app.get("/health", tags=["admin"])
async def read_health():
    """Get the health status of the API."""
    logger.info("GET /health")
    return {}
