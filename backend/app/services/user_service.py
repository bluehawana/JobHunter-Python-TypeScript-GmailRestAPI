from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId
from app.models.user import UserCreate, UserInDB, User, UserUpdate, UserProfile, UserPreferences
from app.core.security import get_password_hash, verify_password
from app.core.database import get_database
from app.utils.crud import CRUDBase
import logging

logger = logging.getLogger(__name__)

class UserService(CRUDBase[UserInDB, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__("users")
    
    async def create_user(self, user_data: UserCreate) -> UserInDB:
        """Create a new user with hashed password"""
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Create user profile from registration data
            profile = UserProfile(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                skills=[],
                summary=None,
                current_title=None,
                experience_years=None,
                education=None,
                phone=None,
                location=None,
                linkedin_url=None,
                portfolio_url=None
            )
            
            # Hash password
            hashed_password = get_password_hash(user_data.password)
            
            # Create user document
            user_doc = {
                "email": user_data.email,
                "profile": profile.dict(),
                "preferences": UserPreferences().dict(),
                "integrations": {
                    "gmail": {"connected": False},
                    "linkedin": {"connected": False},
                    "indeed": {"connected": False}
                },
                "hashed_password": hashed_password,
                "is_active": True,
                "is_verified": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "last_login": None,
                "total_jobs_found": 0,
                "total_applications": 0,
                "total_documents_generated": 0
            }
            
            collection = await self.get_collection()
            result = await collection.insert_one(user_doc)
            
            # Retrieve and return the created user
            created_user = await collection.find_one({"_id": result.inserted_id})
            return UserInDB(**created_user)
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email address"""
        try:
            collection = await self.get_collection()
            user_doc = await collection.find_one({"email": email})
            
            if user_doc:
                return UserInDB(**user_doc)
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """Get user by ID"""
        try:
            if not ObjectId.is_valid(user_id):
                return None
                
            collection = await self.get_collection()
            user_doc = await collection.find_one({"_id": ObjectId(user_id)})
            
            if user_doc:
                return UserInDB(**user_doc)
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with email and password"""
        try:
            user = await self.get_user_by_email(email)
            
            if not user:
                return None
            
            if not user.is_active:
                return None
            
            if not verify_password(password, user.hashed_password):
                return None
            
            # Update last login
            await self.update_last_login(str(user.id))
            
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    async def update_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp"""
        try:
            collection = await self.get_collection()
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
            return False
    
    async def update_user_profile(self, user_id: str, profile_data: UserProfile) -> Optional[UserInDB]:
        """Update user profile"""
        try:
            collection = await self.get_collection()
            
            update_data = {
                "profile": profile_data.dict(),
                "updated_at": datetime.utcnow()
            }
            
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return await self.get_user_by_id(user_id)
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            return None
    
    async def update_user_preferences(self, user_id: str, preferences: UserPreferences) -> Optional[UserInDB]:
        """Update user preferences"""
        try:
            collection = await self.get_collection()
            
            update_data = {
                "preferences": preferences.dict(),
                "updated_at": datetime.utcnow()
            }
            
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return await self.get_user_by_id(user_id)
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating user preferences: {e}")
            return None
    
    async def update_integration_status(self, user_id: str, service: str, integration_data: Dict[str, Any]) -> bool:
        """Update integration status for a service"""
        try:
            collection = await self.get_collection()
            
            update_data = {
                f"integrations.{service}": integration_data,
                "updated_at": datetime.utcnow()
            }
            
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating integration status: {e}")
            return False
    
    async def increment_user_stats(self, user_id: str, stat_field: str, increment: int = 1) -> bool:
        """Increment user statistics"""
        try:
            collection = await self.get_collection()
            
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$inc": {stat_field: increment},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error incrementing user stats: {e}")
            return False
    
    async def deactivate_user(self, user_id: str) -> bool:
        """Deactivate user account"""
        try:
            collection = await self.get_collection()
            
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "is_active": False,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error deactivating user: {e}")
            return False
    
    async def verify_user_email(self, user_id: str) -> bool:
        """Mark user email as verified"""
        try:
            collection = await self.get_collection()
            
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "is_verified": True,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error verifying user email: {e}")
            return False
    
    async def change_password(self, user_id: str, new_password: str) -> bool:
        """Change user password"""
        try:
            hashed_password = get_password_hash(new_password)
            
            collection = await self.get_collection()
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "hashed_password": hashed_password,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return False
    
    async def get_user_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user statistics"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None
            
            return {
                "total_jobs_found": user.total_jobs_found,
                "total_applications": user.total_applications,
                "total_documents_generated": user.total_documents_generated,
                "account_created": user.created_at,
                "last_login": user.last_login,
                "integrations_connected": sum([
                    1 for integration in user.integrations.dict().values()
                    if integration.get("connected", False)
                ])
            }
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return None