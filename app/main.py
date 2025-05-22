"""Main entry point for the application."""
from contextlib import asynccontextmanager
import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Log 422 pydantic validation exceptions"""
    logger.error(
        "Validation error at %s: %s",
        request.url,
        exc.errors()
    )
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(exc: Exception):
    """Log all generic exceptions"""
    logger.error("Unhandled exception: %s\n%s", exc, traceback.format_exc())
    return PlainTextResponse("Internal server error", status_code=500)


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
    return {}
