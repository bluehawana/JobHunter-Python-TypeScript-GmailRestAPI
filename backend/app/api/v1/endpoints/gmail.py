from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from typing import Dict
import logging
from app.api.v1.endpoints.auth import get_current_user
from app.core.database import get_async_session
from app.core.config import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import os

router = APIRouter()
logger = logging.getLogger(__name__)

# Gmail OAuth Configuration
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")

@router.get("/connect")
async def initiate_gmail_oauth(
    current_user: dict = Depends(get_current_user)
):
    """
    Initiate Gmail OAuth flow for connecting user's Gmail account
    """
    try:
        # Create the flow using the client secrets
        client_config = {
            "web": {
                "client_id": GMAIL_CLIENT_ID,
                "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),  # Set in environment
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [f"{settings.BASE_URL}/api/v1/gmail/callback"]
            }
        }
        
        flow = Flow.from_client_config(
            client_config,
            scopes=GMAIL_SCOPES
        )
        
        # Set the redirect URI
        flow.redirect_uri = f"{settings.BASE_URL}/api/v1/gmail/callback"
        
        # Generate authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'  # Force consent screen to get refresh token
        )
        
        # Store state in user session/database for verification
        db = await get_database()
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        await db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "gmail_oauth_state": state,
                    "gmail_oauth_initiated": True
                }
            }
        )
        
        return {
            "authorization_url": authorization_url,
            "state": state,
            "message": "Please visit the authorization URL to connect your Gmail account"
        }
        
    except Exception as e:
        logger.error(f"Error initiating Gmail OAuth: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate Gmail OAuth")

@router.get("/callback")
async def gmail_oauth_callback(
    code: str = Query(..., description="Authorization code from Google"),
    state: str = Query(..., description="State parameter for verification"),
    error: str = Query(None, description="Error from OAuth provider")
):
    """
    Handle Gmail OAuth callback and store credentials
    """
    try:
        if error:
            raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
        
        # Find user by OAuth state
        db = await get_database()
        user = await db.users.find_one({
            "gmail_oauth_state": state,
            "gmail_oauth_initiated": True
        })
        
        if not user:
            raise HTTPException(status_code=400, detail="Invalid OAuth state or expired session")
        
        # Create the flow for token exchange
        client_config = {
            "web": {
                "client_id": GMAIL_CLIENT_ID,
                "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [f"{settings.BASE_URL}/api/v1/gmail/callback"]
            }
        }
        
        flow = Flow.from_client_config(
            client_config,
            scopes=GMAIL_SCOPES,
            state=state
        )
        flow.redirect_uri = f"{settings.BASE_URL}/api/v1/gmail/callback"
        
        # Exchange authorization code for tokens
        flow.fetch_token(code=code)
        
        # Get credentials
        credentials = flow.credentials
        
        # Store credentials in database
        gmail_credentials = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }
        
        user_id = str(user["_id"])
        await db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "gmail_credentials": gmail_credentials,
                    "gmail_connected": True,
                    "gmail_connected_at": "2024-01-01T00:00:00Z"  # Current timestamp
                },
                "$unset": {
                    "gmail_oauth_state": "",
                    "gmail_oauth_initiated": ""
                }
            }
        )
        
        logger.info(f"Gmail connected successfully for user {user_id}")
        
        # Redirect to frontend success page
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/dashboard?gmail_connected=true",
            status_code=302
        )
        
    except Exception as e:
        logger.error(f"Error in Gmail OAuth callback: {e}")
        # Redirect to frontend error page
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/dashboard?gmail_error=true",
            status_code=302
        )

@router.get("/status")
async def get_gmail_connection_status(
    current_user: dict = Depends(get_current_user)
):
    """
    Get Gmail connection status for current user
    """
    try:
        db = await get_database()
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        user = await db.users.find_one({"_id": user_id})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        gmail_connected = bool(user.get("gmail_connected", False))
        gmail_credentials = user.get("gmail_credentials")
        
        # Check if credentials are valid
        credentials_valid = False
        if gmail_credentials and gmail_credentials.get("token"):
            try:
                # Test credentials by creating a minimal request
                credentials = Credentials(
                    token=gmail_credentials.get("token"),
                    refresh_token=gmail_credentials.get("refresh_token"),
                    token_uri=gmail_credentials.get("token_uri"),
                    client_id=gmail_credentials.get("client_id"),
                    client_secret=gmail_credentials.get("client_secret"),
                    scopes=gmail_credentials.get("scopes", GMAIL_SCOPES)
                )
                
                # Check if token is valid or can be refreshed
                if credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                    
                    # Update credentials in database
                    updated_creds = {
                        "token": credentials.token,
                        "refresh_token": credentials.refresh_token,
                        "token_uri": credentials.token_uri,
                        "client_id": credentials.client_id,
                        "client_secret": credentials.client_secret,
                        "scopes": credentials.scopes
                    }
                    
                    await db.users.update_one(
                        {"_id": user_id},
                        {"$set": {"gmail_credentials": updated_creds}}
                    )
                
                credentials_valid = True
                
            except Exception as e:
                logger.error(f"Error validating Gmail credentials: {e}")
                credentials_valid = False
        
        return {
            "gmail_connected": gmail_connected,
            "credentials_valid": credentials_valid,
            "connected_at": user.get("gmail_connected_at"),
            "email_count_estimate": "Unknown"  # Could add email count if needed
        }
        
    except Exception as e:
        logger.error(f"Error getting Gmail status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get Gmail status")

@router.post("/disconnect")
async def disconnect_gmail(
    current_user: dict = Depends(get_current_user)
):
    """
    Disconnect Gmail account and remove stored credentials
    """
    try:
        db = await get_database()
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        # Remove Gmail credentials from database
        await db.users.update_one(
            {"_id": user_id},
            {
                "$unset": {
                    "gmail_credentials": "",
                    "gmail_connected": "",
                    "gmail_connected_at": ""
                }
            }
        )
        
        logger.info(f"Gmail disconnected for user {user_id}")
        
        return {
            "message": "Gmail account disconnected successfully",
            "gmail_connected": False
        }
        
    except Exception as e:
        logger.error(f"Error disconnecting Gmail: {e}")
        raise HTTPException(status_code=500, detail="Failed to disconnect Gmail")

@router.get("/test-connection")
async def test_gmail_connection(
    current_user: dict = Depends(get_current_user)
):
    """
    Test Gmail connection by fetching a few recent emails
    """
    try:
        db = await get_database()
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        user = await db.users.find_one({"_id": user_id})
        
        if not user or not user.get("gmail_credentials"):
            raise HTTPException(status_code=400, detail="Gmail not connected")
        
        # Create Gmail credentials
        gmail_creds = user["gmail_credentials"]
        credentials = Credentials(
            token=gmail_creds.get("token"),
            refresh_token=gmail_creds.get("refresh_token"),
            token_uri=gmail_creds.get("token_uri"),
            client_id=gmail_creds.get("client_id"),
            client_secret=gmail_creds.get("client_secret"),
            scopes=gmail_creds.get("scopes", GMAIL_SCOPES)
        )
        
        # Test connection by searching for recent job-related emails
        from app.services.gmail_service import GmailService
        gmail_service = GmailService(credentials)
        
        # Search for job emails in last 7 days
        job_emails = await gmail_service.search_job_emails(
            keywords=["job", "opportunity"],
            days_back=7
        )
        
        return {
            "connection_status": "success",
            "recent_job_emails_count": len(job_emails),
            "sample_emails": [
                {
                    "subject": email.get("subject", ""),
                    "from": email.get("from", ""),
                    "date": email.get("date", "")
                }
                for email in job_emails[:3]  # Show first 3 emails
            ]
        }
        
    except Exception as e:
        logger.error(f"Error testing Gmail connection: {e}")
        raise HTTPException(status_code=500, detail=f"Gmail connection test failed: {str(e)}")