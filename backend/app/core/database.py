import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError
from contextlib import asynccontextmanager
from app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

class Database:
    engine = None
    async_engine = None
    session_factory = None
    async_session_factory = None

db = Database()

def get_database_url():
    """Get database URL for Heroku or local development"""
    if settings.DATABASE_URL:
        # Heroku provides DATABASE_URL
        url = settings.DATABASE_URL
        # Fix mysql:// to mysql+pymysql:// for SQLAlchemy
        if url.startswith("mysql://"):
            url = url.replace("mysql://", "mysql+pymysql://", 1)
        # Fix postgres:// to postgresql:// for SQLAlchemy 1.4+
        elif url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url
    else:
        # Local development - use MySQL/PostgreSQL
        if settings.DB_TYPE == "mysql":
            return f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        else:  # PostgreSQL
            return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

def get_async_database_url():
    """Get async database URL"""
    url = get_database_url()
    if "mysql+pymysql" in url:
        return url.replace("mysql+pymysql://", "mysql+aiomysql://")
    elif "mysql" in url:
        return url.replace("mysql://", "mysql+aiomysql://")
    else:
        return url.replace("postgresql://", "postgresql+asyncpg://")

async def connect_to_database():
    """Create database connection"""
    try:
        logger.info("Connecting to SQL database...")
        
        # Create engines
        db.engine = create_engine(get_database_url(), pool_pre_ping=True)
        db.async_engine = create_async_engine(get_async_database_url(), pool_pre_ping=True)
        
        # Create session factories
        db.session_factory = sessionmaker(bind=db.engine)
        db.async_session_factory = async_sessionmaker(
            bind=db.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Test the connection
        async with db.async_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        logger.info("Connected to SQL database successfully")
        
    except OperationalError as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to database: {e}")
        raise

async def close_database_connection():
    """Close database connection"""
    try:
        if db.async_engine:
            logger.info("Closing database connection...")
            await db.async_engine.dispose()
            logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database connection: {e}")

@asynccontextmanager
async def get_async_session():
    """Get async database session"""
    async with db.async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def get_session():
    """Get sync database session"""
    return db.session_factory()

async def create_tables():
    """Create all database tables"""
    try:
        async with db.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

# Health check function
async def check_database_health():
    """Check if database is healthy"""
    try:
        async with db.async_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False