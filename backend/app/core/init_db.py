import asyncio
import logging
from app.core.database import connect_to_mongo, close_mongo_connection, get_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_database():
    """Initialize database with collections and indexes"""
    try:
        await connect_to_mongo()
        db = await get_database()
        
        # Create collections if they don't exist
        collections = [
            "users",
            "jobs", 
            "applications",
            "documents",
            "email_monitoring",
            "oauth_tokens",
            "user_preferences"
        ]
        
        existing_collections = await db.list_collection_names()
        
        for collection_name in collections:
            if collection_name not in existing_collections:
                await db.create_collection(collection_name)
                logger.info(f"Created collection: {collection_name}")
            else:
                logger.info(f"Collection already exists: {collection_name}")
        
        # Create additional indexes
        await create_additional_indexes(db)
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        await close_mongo_connection()

async def create_additional_indexes(db):
    """Create additional indexes for better performance"""
    try:
        # OAuth tokens indexes
        await db.oauth_tokens.create_index([("user_id", 1), ("service", 1)], unique=True)
        await db.oauth_tokens.create_index("expires_at")
        
        # User preferences indexes
        await db.user_preferences.create_index("user_id", unique=True)
        
        # Compound indexes for common queries
        await db.applications.create_index([("user_id", 1), ("status", 1), ("application_date", -1)])
        await db.jobs.create_index([("user_id", 1), ("match_score", -1), ("posting_date", -1)])
        await db.documents.create_index([("user_id", 1), ("job_id", 1), ("document_type", 1)])
        
        logger.info("Additional indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error creating additional indexes: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_database())