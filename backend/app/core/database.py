import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def get_database():
    return db.database


async def connect_to_mongo():
    """Create database connection"""
    logger.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.database = db.client[settings.DATABASE_NAME]
    logger.info("Connected to MongoDB successfully")


async def close_mongo_connection():
    """Close database connection"""
    logger.info("Closing connection to MongoDB...")
    if db.client:
        db.client.close()
    logger.info("Disconnected from MongoDB")