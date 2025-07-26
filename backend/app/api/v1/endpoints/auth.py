from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.security import create_access_token, verify_token
from app.models.user import (
    UserCreate, UserLogin, Token, UserPublic, GmailAuthRequest,
    PasswordReset, PasswordResetConfirm, EmailVerification
)
from app.services.user_service import UserService
from app.services.oauth_service import OAuthService

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user_service = UserService()
        user = await user_service.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        user_service = UserService()
        
        # Create user
        user = await user_service.create_user(user_data)
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}, 
            expires_delta=access_token_expires
        )
        
        # Create public user object
        user_public = UserPublic(
            id=str(user.id),
            email=user.email,
            first_name=user.profile.first_name,
            last_name=user.profile.last_name,
            is_active=user.is_active,
            created_at=user.created_at
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_public
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Login user"""
    try:
        user_service = UserService()
        
        # Authenticate user
        user = await user_service.authenticate_user(user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}, 
            expires_delta=access_token_expires
        )
        
        # Create public user object
        user_public = UserPublic(
            id=str(user.id),
            email=user.email,
            first_name=user.profile.first_name,
            last_name=user.profile.last_name,
            is_active=user.is_active,
            created_at=user.created_at
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_public
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/me", response_model=UserPublic)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return UserPublic(
        id=str(current_user.id),
        email=current_user.email,
        first_name=current_user.profile.first_name,
        last_name=current_user.profile.last_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

@router.post("/gmail/authorize")
async def authorize_gmail(
    auth_request: GmailAuthRequest,
    current_user = Depends(get_current_user)
):
    """Handle Gmail OAuth authorization code and exchange for tokens"""
    try:
        oauth_service = OAuthService()
        
        # Exchange authorization code for tokens
        token_data = await oauth_service.exchange_code_for_tokens(
            auth_request.authorization_code
        )
        
        # Update user's Gmail integration status
        user_service = UserService()
        integration_data = {
            "connected": True,
            "email": token_data.get("user_info", {}).get("email"),
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "expires_at": datetime.utcnow() + timedelta(seconds=token_data["expires_in"]),
            "scopes": token_data["scope"].split(" "),
            "last_sync": datetime.utcnow()
        }
        
        await user_service.update_integration_status(
            str(current_user.id), 
            "gmail", 
            integration_data
        )
        
        return {
            "message": "Gmail authorization successful",
            "status": "connected",
            "email": token_data.get("user_info", {}).get("email"),
            "expires_in": token_data["expires_in"],
            "scope": token_data["scope"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gmail authorization failed: {str(e)}"
        )

@router.get("/gmail/auth-url")
async def get_gmail_auth_url(current_user = Depends(get_current_user)):
    """Generate Gmail OAuth authorization URL"""
    try:
        oauth_service = OAuthService()
        auth_url = oauth_service.get_authorization_url(str(current_user.id))
        
        return {
            "auth_url": auth_url,
            "message": "Visit this URL to authorize Gmail access",
            "client_id": settings.GMAIL_CLIENT_ID,
            "scopes": oauth_service.scopes
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate authorization URL: {str(e)}"
        )

@router.get("/gmail/status")
async def get_gmail_connection_status(current_user = Depends(get_current_user)):
    """Check Gmail connection status"""
    try:
        gmail_integration = current_user.integrations.gmail
        
        return {
            "connected": gmail_integration.connected,
            "email": gmail_integration.email,
            "last_sync": gmail_integration.last_sync,
            "expires_at": gmail_integration.expires_at
        }
        
    except Exception as e:
        return {
            "connected": False,
            "error": f"Failed to check Gmail status: {str(e)}"
        }

@router.delete("/gmail/revoke")
async def revoke_gmail_access(current_user = Depends(get_current_user)):
    """Revoke Gmail access"""
    try:
        oauth_service = OAuthService()
        user_service = UserService()
        
        # Revoke tokens with Google
        if current_user.integrations.gmail.access_token:
            await oauth_service.revoke_token(current_user.integrations.gmail.access_token)
        
        # Update user's integration status
        integration_data = {
            "connected": False,
            "email": None,
            "access_token": None,
            "refresh_token": None,
            "expires_at": None,
            "scopes": [],
            "last_sync": None
        }
        
        success = await user_service.update_integration_status(
            str(current_user.id), 
            "gmail", 
            integration_data
        )
        
        if success:
            return {"message": "Gmail access revoked successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to revoke Gmail access"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error revoking Gmail access: {str(e)}"
        )

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user = Depends(get_current_user)
):
    """Change user password"""
    try:
        user_service = UserService()
        
        # Verify current password
        user = await user_service.authenticate_user(current_user.email, current_password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Change password
        success = await user_service.change_password(str(current_user.id), new_password)
        if success:
            return {"message": "Password changed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to change password"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error changing password"
        )

@router.get("/stats")
async def get_user_stats(current_user = Depends(get_current_user)):
    """Get user statistics"""
    try:
        user_service = UserService()
        stats = await user_service.get_user_stats(str(current_user.id))
        
        if stats:
            return stats
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User statistics not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user statistics"
        )