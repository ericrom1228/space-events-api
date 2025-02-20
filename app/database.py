from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "space_db")

# Create a MongoDB client
client = AsyncIOMotorClient(MONGO_URI)

# Get the database instance
database = client[DB_NAME]

# Get the events collection
events_collection = database["events"]