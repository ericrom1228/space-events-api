from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.settings import settings
from fastapi import FastAPI, Request

# Load environment variables from .env file

# MongoDB's connection settings
print("MONGO_URI:", settings.MONGO_URI)
print("DB_NAME:", settings.DB_NAME)


async def connect_to_mongo(app: FastAPI) -> None:
    app.state.mongo_client = AsyncIOMotorClient(settings.MONGO_URI)


async def close_mongo_connection(app: FastAPI) -> None:
    app.state.mongo_client.close()


def get_database(request: Request) -> AsyncIOMotorDatabase:
    return request.app.state.mongo_client[settings.DB_NAME]