"""
MiniMax M2 Search Integration Module

This module provides intelligent search capabilities across job applications,
CVs, cover letters, and related documents using the MiniMax M2 API.
"""

from .client import MiniMaxSearchClient
from .service import SearchService
from .indexer import DocumentIndexer
from .cache import SearchCache
from .rate_limiter import RateLimiter
from .ranker import ResultRanker
from .models import (
    Document,
    SearchResult,
    SearchResponse,
    SearchFilters,
    CacheEntry,
)
from .exceptions import (
    SearchError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    NetworkError,
)

__all__ = [
    "MiniMaxSearchClient",
    "SearchService",
    "DocumentIndexer",
    "SearchCache",
    "RateLimiter",
    "ResultRanker",
    "Document",
    "SearchResult",
    "SearchResponse",
    "SearchFilters",
    "CacheEntry",
    "SearchError",
    "ValidationError",
    "AuthenticationError",
    "RateLimitError",
    "NetworkError",
]

__version__ = "0.1.0"
