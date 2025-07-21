from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class GmailAuthRequest(BaseModel):
    authorization_code: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"id": user_id, "email": payload.get("email")}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=Token)
async def register(user_data: UserRegister):
    """Register a new user"""
    # In a real app, you would check if user exists and save to database
    # For now, we'll just create a token
    
    hashed_password = get_password_hash(user_data.password)
    
    # Mock user creation - in real app, save to database
    user = {
        "id": "mock_user_id",
        "name": user_data.name,
        "email": user_data.email,
        "hashed_password": hashed_password
    }
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Login user"""
    # In a real app, you would verify credentials against database
    # For now, we'll accept any credentials
    
    # Mock user verification
    user = {
        "id": "mock_user_id",
        "name": "Test User",
        "email": user_data.email
    }
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/gmail/authorize")
async def authorize_gmail(
    auth_request: GmailAuthRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Handle Gmail OAuth authorization code and exchange for tokens
    This endpoint will be called after user authorizes Gmail access
    """
    try:
        # In a real implementation, you would:
        # 1. Exchange the authorization code for access and refresh tokens
        # 2. Store the tokens securely in your database
        # 3. Return success status
        
        # Mock implementation
        return {
            "message": "Gmail authorization successful",
            "status": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gmail authorization failed: {str(e)}"
        )

@router.get("/gmail/auth-url")
async def get_gmail_auth_url(current_user: dict = Depends(get_current_user)):
    """
    Generate Gmail OAuth authorization URL
    """
    # In a real implementation, you would generate the actual OAuth URL
    # For now, return a mock URL structure
    
    auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={settings.GMAIL_CLIENT_ID}&"
        f"redirect_uri=http://localhost:3000/auth/gmail/callback&"
        f"scope=https://www.googleapis.com/auth/gmail.readonly "
        f"https://www.googleapis.com/auth/gmail.send&"
        f"response_type=code&"
        f"access_type=offline"
    )
    
    return {
        "auth_url": auth_url,
        "message": "Visit this URL to authorize Gmail access"
    }