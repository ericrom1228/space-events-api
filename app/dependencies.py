"""Dependencies for FastAPI startup"""
import logging
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError
from app.settings import settings

logger = logging.getLogger("app")

# MongoDB's connection settings
logger.info("MONGO_URI: %s", settings.MONGO_URI)
logger.info("DB_NAME: %s", settings.DB_NAME)


async def connect_to_mongo(app: FastAPI) -> None:
    """Establishes connection to Mongo"""
    try:
        logger.info("MONGO_URI: %s",  settings.MONGO_URI)
        logger.info("DB_NAME: %s", settings.DB_NAME)
        logger.info("MONGO_CONNECTION_TIMEOUT: %s milliseconds", settings.MONGO_CONNECTION_TIMEOUT)
        app.state.mongo_client = AsyncIOMotorClient(
            settings.MONGO_URI,
            serverSelectionTimeoutMS=settings.MONGO_CONNECTION_TIMEOUT
        )
        await app.state.mongo_client.admin.command('ping')

    except ServerSelectionTimeoutError as e:
        raise RuntimeError(f"Could not connect to mongo: {e}") from e


async def close_mongo_connection(app: FastAPI) -> None:
    """Closes connection to Mongo"""
    logger.info("Closing mongo connection")
    app.state.mongo_client.close()


def get_database(request: Request) -> AsyncIOMotorDatabase:
    """Establishes DB connection"""
    return request.app.state.mongo_client[settings.DB_NAME]
