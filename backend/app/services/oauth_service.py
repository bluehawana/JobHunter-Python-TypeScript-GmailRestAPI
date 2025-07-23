import httpx
from typing import Dict, Optional
from urllib.parse import urlencode
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class OAuthService:
    """Service for handling OAuth authentication with Google"""
    
    def __init__(self):
        self.client_id = "126140999463-llvuijb64539veav9i80la40kt3oom62.apps.googleusercontent.com"
        self.client_secret = settings.GMAIL_CLIENT_SECRET
        self.redirect_uri = "http://localhost:3000/auth/gmail/callback"
        
        # Gmail API scopes
        self.scopes = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.modify",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ]
    
    def get_authorization_url(self, user_id: str) -> str:
        """
        Generate Google OAuth authorization URL
        
        Args:
            user_id: User ID to include in state parameter
            
        Returns:
            Authorization URL
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",  # Force consent to get refresh token
            "state": user_id,
            "include_granted_scopes": "true"
        }
        
        auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
        return auth_url
    
    async def exchange_code_for_tokens(self, authorization_code: str) -> Dict:
        """
        Exchange authorization code for access and refresh tokens
        
        Args:
            authorization_code: Authorization code from OAuth callback
            
        Returns:
            Dictionary containing tokens and user info
        """
        try:
            token_url = "https://oauth2.googleapis.com/token"
            
            token_data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": authorization_code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=token_data)
                
                if response.status_code != 200:
                    logger.error(f"Token exchange failed: {response.text}")
                    raise Exception(f"Token exchange failed: {response.text}")
                
                tokens = response.json()
                
                # Get user info using the access token
                user_info = await self._get_user_info(tokens["access_token"])
                
                return {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens.get("refresh_token"),
                    "expires_in": tokens["expires_in"],
                    "scope": tokens["scope"],
                    "token_type": tokens["token_type"],
                    "user_info": user_info
                }
                
        except Exception as e:
            logger.error(f"Error exchanging code for tokens: {e}")
            raise
    
    async def _get_user_info(self, access_token: str) -> Dict:
        """
        Get user information using access token
        
        Args:
            access_token: Google access token
            
        Returns:
            User information dictionary
        """
        try:
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(user_info_url, headers=headers)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"Failed to get user info: {response.text}")
                    return {}
                    
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {}
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict]:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Google refresh token
            
        Returns:
            New token information or None if failed
        """
        try:
            token_url = "https://oauth2.googleapis.com/token"
            
            token_data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=token_data)
                
                if response.status_code == 200:
                    tokens = response.json()
                    return {
                        "access_token": tokens["access_token"],
                        "expires_in": tokens["expires_in"],
                        "token_type": tokens["token_type"],
                        "scope": tokens.get("scope")
                    }
                else:
                    logger.error(f"Token refresh failed: {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return None
    
    def create_credentials(self, access_token: str, refresh_token: str = None) -> Credentials:
        """
        Create Google Credentials object for API calls
        
        Args:
            access_token: Google access token
            refresh_token: Google refresh token (optional)
            
        Returns:
            Google Credentials object
        """
        return Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.scopes
        )
    
    async def revoke_token(self, token: str) -> bool:
        """
        Revoke a Google OAuth token
        
        Args:
            token: Token to revoke (access or refresh token)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            revoke_url = f"https://oauth2.googleapis.com/revoke?token={token}"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(revoke_url)
                
                return response.status_code == 200
                
        except Exception as e:
            logger.error(f"Error revoking token: {e}")
            return False
    
    async def test_gmail_connection(self, user_id: str) -> Dict:
        """
        Test Gmail connection for a user
        
        Args:
            user_id: User ID to check connection for
            
        Returns:
            Connection status information
        """
        try:
            # In a real implementation, you would:
            # 1. Get stored tokens from database for this user
            # 2. Test if tokens are valid by making a simple API call
            # 3. Refresh tokens if needed
            
            # Mock implementation for now
            return {
                "connected": False,
                "message": "Gmail connection not configured yet",
                "client_id": self.client_id,
                "scopes_required": self.scopes
            }
            
        except Exception as e:
            logger.error(f"Error testing Gmail connection: {e}")
            return {
                "connected": False,
                "error": str(e)
            }
    
    async def revoke_access(self, user_id: str) -> bool:
        """
        Revoke Gmail access for a user
        
        Args:
            user_id: User ID to revoke access for
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # In a real implementation, you would:
            # 1. Get stored tokens from database for this user
            # 2. Revoke the tokens using Google's revoke endpoint
            # 3. Remove tokens from database
            
            # Mock implementation for now
            logger.info(f"Revoking Gmail access for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error revoking access for user {user_id}: {e}")
            return False