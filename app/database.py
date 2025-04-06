from motor.motor_asyncio import AsyncIOMotorClient
import os
from app.settings import settings

# Load environment variables from .env file

# MongoDB's connection settings
print("MONGO_URI:", settings.MONGO_URI)
print("DB_NAME:", settings.DB_NAME)
# Create a MongoDB client
client = AsyncIOMotorClient(settings.MONGO_URI)

# Get the database instance
database = client[settings.DB_NAME]

# Get the events collection
events_collection = database["events"]