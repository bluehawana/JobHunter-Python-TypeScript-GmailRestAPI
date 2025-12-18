"""
Custom exceptions for the MiniMax M2 search integration.
"""

from typing import Dict, Optional


class SearchError(Exception):
    """Base exception for search errors"""
    
    def __init__(self, message: str, error_code: str, details: Optional[Dict] = None):
        """
        Initialize search error.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Optional dictionary with additional error details
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"


class ValidationError(SearchError):
    """Query validation failed"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "VALIDATION_ERROR", details)


class AuthenticationError(SearchError):
    """API authentication failed"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "AUTHENTICATION_ERROR", details)


class RateLimitError(SearchError):
    """Rate limit exceeded"""
    
    def __init__(self, message: str, retry_after: int, details: Optional[Dict] = None):
        """
        Initialize rate limit error.
        
        Args:
            message: Human-readable error message
            retry_after: Seconds to wait before retrying
            details: Optional dictionary with additional error details
        """
        super().__init__(message, "RATE_LIMIT_EXCEEDED", details)
        self.retry_after = retry_after


class NetworkError(SearchError):
    """Network communication failed"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "NETWORK_ERROR", details)
