"""Dependencies for FastAPI startup"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI, Request
from app.settings import settings

# MongoDB's connection settings
print("MONGO_URI:", settings.MONGO_URI)
print("DB_NAME:", settings.DB_NAME)


async def connect_to_mongo(app: FastAPI) -> None:
    """Establishes connection to Mongo"""
    app.state.mongo_client = AsyncIOMotorClient(settings.MONGO_URI)


async def close_mongo_connection(app: FastAPI) -> None:
    """Closes connection to Mongo"""
    app.state.mongo_client.close()


def get_database(request: Request) -> AsyncIOMotorDatabase:
    """Establishes DB connection"""
    return request.app.state.mongo_client[settings.DB_NAME]
