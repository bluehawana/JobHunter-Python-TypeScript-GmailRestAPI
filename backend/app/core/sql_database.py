from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Database URL - works with Heroku JawsDB or local MySQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:password@localhost:3306/jobhunter"
)

# Handle JawsDB URL format
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(50), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Gmail credentials (JSON)
    gmail_credentials = Column(JSON)
    gmail_connected = Column(Boolean, default=False)
    gmail_connected_at = Column(DateTime)
    
    # Automation configuration (JSON)
    automation_config = Column(JSON)
    automation_updated_at = Column(DateTime)
    automation_paused_at = Column(DateTime)
    automation_resumed_at = Column(DateTime)
    
    # User profile (JSON)
    profile = Column(JSON)

class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, index=True)
    
    # Job basic info
    title = Column(String(500), nullable=False)
    company = Column(String(300), nullable=False)
    location = Column(String(200))
    description = Column(LONGTEXT)
    url = Column(String(1000), nullable=False)
    source = Column(String(100), nullable=False)
    
    # Job metadata
    posting_date = Column(DateTime)
    application_deadline = Column(DateTime)
    job_type = Column(String(100))
    experience_level = Column(String(100))
    remote_option = Column(Boolean, default=False)
    
    # Salary info (JSON)
    salary = Column(JSON)
    
    # Job details (JSON arrays)
    requirements = Column(JSON)
    benefits = Column(JSON)
    keywords = Column(JSON)
    
    # Scoring
    match_score = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.0)
    ats_score = Column(Float, default=0.0)
    
    # Classification
    category = Column(String(100))
    application_difficulty = Column(String(50))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Original data (JSON)
    original_data = Column(JSON)
    
    # Indexes for performance
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

class ProcessedJob(Base):
    __tablename__ = "processed_jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, index=True)
    
    # Job identification
    job_title = Column(String(500), nullable=False)
    company = Column(String(300), nullable=False)
    url = Column(String(1000), nullable=False, unique=True)  # Prevent duplicates
    source = Column(String(100))
    location = Column(String(200))
    
    # Processing info
    processed_at = Column(DateTime, default=datetime.utcnow, index=True)
    email_sent = Column(Boolean, default=False)
    cv_generated = Column(Boolean, default=False)
    cover_letter_generated = Column(Boolean, default=False)
    
    # Application details
    application_status = Column(String(100), default="sent")  # sent, failed, pending
    email_subject = Column(String(500))
    
    # Job data snapshot (JSON)
    job_data = Column(JSON)
    
    # Indexes
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

class AutomationRun(Base):
    __tablename__ = "automation_runs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, index=True)
    
    # Run details
    run_date = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(100), default="running")  # running, completed, failed
    
    # Statistics
    total_jobs_fetched = Column(Integer, default=0)
    jobs_after_filtering = Column(Integer, default=0)
    applications_sent = Column(Integer, default=0)
    applications_failed = Column(Integer, default=0)
    
    # Runtime info
    execution_time_seconds = Column(Float)
    error_message = Column(Text)
    
    # Detailed results (JSON)
    applications = Column(JSON)
    sources_used = Column(JSON)
    filters_applied = Column(JSON)
    
    # Indexes
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

class JobSearch(Base):
    __tablename__ = "job_searches"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, index=True)
    
    # Search parameters
    query = Column(String(500), nullable=False)
    location = Column(String(200))
    filters = Column(JSON)  # All search filters as JSON
    
    # Results
    results_count = Column(Integer, default=0)
    search_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Performance
    execution_time_seconds = Column(Float)

# Database connection and session management
engine = None
SessionLocal = None

def init_database():
    """Initialize database connection and create tables"""
    global engine, SessionLocal
    
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False  # Set to True for SQL debugging
        )
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def get_db() -> Session:
    """Get database session"""
    if SessionLocal is None:
        init_database()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_database():
    """Async version for compatibility with existing code"""
    if SessionLocal is None:
        init_database()
    
    return DatabaseWrapper()

class DatabaseWrapper:
    """Wrapper to make SQLAlchemy work with existing MongoDB-style code"""
    
    def __init__(self):
        self.db = SessionLocal()
        
        # Create collections-like attributes
        self.users = UserCollection(self.db)
        self.jobs = JobCollection(self.db) 
        self.processed_jobs = ProcessedJobCollection(self.db)
        self.automation_runs = AutomationRunCollection(self.db)
        self.job_searches = JobSearchCollection(self.db)
    
    def close(self):
        self.db.close()

class UserCollection:
    def __init__(self, db: Session):
        self.db = db
    
    async def find_one(self, filter_dict: dict) -> Optional[dict]:
        user_id = filter_dict.get("_id")
        if user_id:
            user = self.db.query(User).filter(User.id == user_id).first()
            return self._user_to_dict(user) if user else None
        return None
    
    async def update_one(self, filter_dict: dict, update_dict: dict, upsert: bool = False):
        user_id = filter_dict.get("_id")
        if user_id:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                self._update_user_from_dict(user, update_dict)
                self.db.commit()
            elif upsert:
                # Create new user
                user_data = update_dict.get("$set", {})
                user = User(id=user_id, **user_data)
                self.db.add(user)
                self.db.commit()
    
    def _user_to_dict(self, user: User) -> dict:
        return {
            "_id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "gmail_credentials": user.gmail_credentials,
            "gmail_connected": user.gmail_connected,
            "automation_config": user.automation_config,
            "profile": user.profile
        }
    
    def _update_user_from_dict(self, user: User, update_dict: dict):
        set_data = update_dict.get("$set", {})
        unset_data = update_dict.get("$unset", {})
        
        for key, value in set_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        for key in unset_data.keys():
            if hasattr(user, key):
                setattr(user, key, None)

class JobCollection:
    def __init__(self, db: Session):
        self.db = db
    
    async def update_one(self, filter_dict: dict, update_dict: dict, upsert: bool = False):
        # Find existing job by title, company, url
        existing = self.db.query(JobPosting).filter(
            JobPosting.title == filter_dict.get("title"),
            JobPosting.company == filter_dict.get("company"),
            JobPosting.url == filter_dict.get("url")
        ).first()
        
        job_data = update_dict.get("$set", {})
        
        if existing:
            # Update existing
            for key, value in job_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
        elif upsert:
            # Create new
            job = JobPosting(**job_data)
            self.db.add(job)
        
        self.db.commit()

class ProcessedJobCollection:
    def __init__(self, db: Session):
        self.db = db
    
    async def find(self, filter_dict: dict):
        query = self.db.query(ProcessedJob)
        
        if "user_id" in filter_dict:
            query = query.filter(ProcessedJob.user_id == filter_dict["user_id"])
        
        if "processed_at" in filter_dict:
            date_filter = filter_dict["processed_at"]
            if "$gte" in date_filter:
                query = query.filter(ProcessedJob.processed_at >= date_filter["$gte"])
            if "$lt" in date_filter:
                query = query.filter(ProcessedJob.processed_at < date_filter["$lt"])
        
        return AsyncQueryResult(query)
    
    async def insert_one(self, data: dict):
        job = ProcessedJob(**data)
        self.db.add(job)
        self.db.commit()
    
    async def delete_many(self, filter_dict: dict):
        query = self.db.query(ProcessedJob)
        
        if "processed_at" in filter_dict and "$lt" in filter_dict["processed_at"]:
            query = query.filter(ProcessedJob.processed_at < filter_dict["processed_at"]["$lt"])
        
        deleted_count = query.count()
        query.delete()
        self.db.commit()
        
        return MockDeleteResult(deleted_count)
    
    async def count_documents(self, filter_dict: dict) -> int:
        query = self.db.query(ProcessedJob)
        
        if "user_id" in filter_dict:
            query = query.filter(ProcessedJob.user_id == filter_dict["user_id"])
        
        return query.count()
    
    async def aggregate(self, pipeline: list):
        # Simplified aggregation - would need more complex implementation for full MongoDB compatibility
        return AsyncQueryResult([])

class AutomationRunCollection:
    def __init__(self, db: Session):
        self.db = db
    
    async def find_one(self, filter_dict: dict) -> Optional[dict]:
        query = self.db.query(AutomationRun)
        
        if "user_id" in filter_dict:
            query = query.filter(AutomationRun.user_id == filter_dict["user_id"])
        
        if "run_date" in filter_dict:
            date_filter = filter_dict["run_date"]
            if "$gte" in date_filter:
                query = query.filter(AutomationRun.run_date >= date_filter["$gte"])
            if "$lt" in date_filter:
                query = query.filter(AutomationRun.run_date < date_filter["$lt"])
        
        result = query.first()
        return self._automation_run_to_dict(result) if result else None
    
    async def find(self, filter_dict: dict):
        query = self.db.query(AutomationRun)
        
        if "user_id" in filter_dict:
            query = query.filter(AutomationRun.user_id == filter_dict["user_id"])
        
        return AsyncQueryResult(query)
    
    async def insert_one(self, data: dict):
        run = AutomationRun(**data)
        self.db.add(run)
        self.db.commit()
    
    async def delete_many(self, filter_dict: dict):
        query = self.db.query(AutomationRun)
        
        if "run_date" in filter_dict and "$lt" in filter_dict["run_date"]:
            query = query.filter(AutomationRun.run_date < filter_dict["run_date"]["$lt"])
        
        deleted_count = query.count()
        query.delete()
        self.db.commit()
        
        return MockDeleteResult(deleted_count)
    
    def _automation_run_to_dict(self, run: AutomationRun) -> dict:
        return {
            "user_id": run.user_id,
            "run_date": run.run_date,
            "status": run.status,
            "applications_sent": run.applications_sent,
            "total_jobs_fetched": run.total_jobs_fetched,
            "jobs_after_filtering": run.jobs_after_filtering,
            "applications": run.applications
        }

class JobSearchCollection:
    def __init__(self, db: Session):
        self.db = db
    
    async def insert_one(self, data: dict):
        search = JobSearch(**data)
        self.db.add(search)
        self.db.commit()

class AsyncQueryResult:
    def __init__(self, query):
        self.query = query
    
    def sort(self, field: str, direction: int = -1):
        if hasattr(self.query.column_descriptions[0]['type'], field):
            order_field = getattr(self.query.column_descriptions[0]['type'], field)
            if direction == -1:
                self.query = self.query.order_by(order_field.desc())
            else:
                self.query = self.query.order_by(order_field.asc())
        return self
    
    def limit(self, count: int):
        self.query = self.query.limit(count)
        return self
    
    def skip(self, count: int):
        self.query = self.query.offset(count)
        return self
    
    async def to_list(self, length: int = None):
        results = self.query.all()
        return [self._model_to_dict(r) for r in results]
    
    def _model_to_dict(self, model) -> dict:
        # Convert SQLAlchemy model to dict
        result = {}
        for column in model.__table__.columns:
            result[column.name] = getattr(model, column.name)
        return result

class MockDeleteResult:
    def __init__(self, deleted_count: int):
        self.deleted_count = deleted_count