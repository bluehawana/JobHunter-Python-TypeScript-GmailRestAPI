"""
Data models for the MiniMax M2 search integration.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Document:
    """Represents a searchable document"""
    
    file_path: Path
    document_type: str  # 'cv', 'cover_letter', 'job_description'
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    company_name: Optional[str] = None
    role_title: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate document after initialization"""
        if self.document_type not in ['cv', 'cover_letter', 'job_description', 'other']:
            raise ValueError(f"Invalid document_type: {self.document_type}")
        
        if not isinstance(self.file_path, Path):
            self.file_path = Path(self.file_path)
    
    def validate(self) -> bool:
        """
        Validate document data.
        
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if not self.content or not self.content.strip():
            raise ValueError("Document content cannot be empty")
        
        if not self.file_path:
            raise ValueError("Document file_path cannot be empty")
        
        return True
    
    def is_valid_type(self, allowed_types: List[str]) -> bool:
        """
        Check if document type is in allowed list.
        
        Args:
            allowed_types: List of allowed document types
            
        Returns:
            True if document type is allowed
        """
        return self.document_type in allowed_types
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert document to dictionary.
        
        Returns:
            Dictionary representation of document
        """
        return {
            'file_path': str(self.file_path),
            'document_type': self.document_type,
            'content': self.content[:200] + '...' if len(self.content) > 200 else self.content,
            'metadata': self.metadata,
            'company_name': self.company_name,
            'role_title': self.role_title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None,
        }


@dataclass
class SearchResult:
    """Represents a single search result"""
    
    document: Document
    relevance_score: float
    matched_excerpts: List[str] = field(default_factory=list)
    highlighted_text: str = ""
    match_type: str = "semantic"  # 'exact', 'partial', 'semantic'
    
    def __post_init__(self):
        """Validate search result after initialization"""
        if self.match_type not in ['exact', 'partial', 'semantic']:
            raise ValueError(f"Invalid match_type: {self.match_type}")
        
        if not 0.0 <= self.relevance_score <= 1.0:
            raise ValueError(f"relevance_score must be between 0 and 1, got {self.relevance_score}")
    
    def validate(self) -> bool:
        """
        Validate search result data.
        
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if not self.document:
            raise ValueError("SearchResult must have a document")
        
        self.document.validate()
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert search result to dictionary.
        
        Returns:
            Dictionary representation of search result
        """
        return {
            'document': self.document.to_dict(),
            'relevance_score': self.relevance_score,
            'matched_excerpts': self.matched_excerpts,
            'highlighted_text': self.highlighted_text,
            'match_type': self.match_type,
        }


@dataclass
class SearchResponse:
    """Response from search operation"""
    
    query: str
    results: List[SearchResult]
    total_count: int
    search_time_ms: int
    from_cache: bool = False
    suggested_queries: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate search response after initialization"""
        if self.total_count < 0:
            raise ValueError(f"total_count must be non-negative, got {self.total_count}")
        
        if self.search_time_ms < 0:
            raise ValueError(f"search_time_ms must be non-negative, got {self.search_time_ms}")
    
    def validate(self) -> bool:
        """
        Validate search response data.
        
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if not self.query or not self.query.strip():
            raise ValueError("SearchResponse query cannot be empty")
        
        if len(self.results) > self.total_count:
            raise ValueError(f"Number of results ({len(self.results)}) cannot exceed total_count ({self.total_count})")
        
        # Validate each result
        for result in self.results:
            result.validate()
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert search response to dictionary.
        
        Returns:
            Dictionary representation of search response
        """
        return {
            'query': self.query,
            'results': [r.to_dict() for r in self.results],
            'total_count': self.total_count,
            'search_time_ms': self.search_time_ms,
            'from_cache': self.from_cache,
            'suggested_queries': self.suggested_queries,
        }


@dataclass
class SearchFilters:
    """Filters for search queries"""
    
    document_types: Optional[List[str]] = None
    company_names: Optional[List[str]] = None
    date_range: Optional[Tuple[datetime, datetime]] = None
    max_results: int = 10
    
    def __post_init__(self):
        """Validate search filters after initialization"""
        if self.max_results <= 0:
            raise ValueError(f"max_results must be positive, got {self.max_results}")
        
        if self.document_types:
            valid_types = {'cv', 'cover_letter', 'job_description', 'other'}
            invalid = set(self.document_types) - valid_types
            if invalid:
                raise ValueError(f"Invalid document_types: {invalid}")
        
        if self.date_range:
            start, end = self.date_range
            if start > end:
                raise ValueError(f"date_range start must be before end")
    
    def validate(self) -> bool:
        """
        Validate search filters.
        
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if self.max_results > 1000:
            raise ValueError(f"max_results cannot exceed 1000, got {self.max_results}")
        
        return True
    
    def has_filters(self) -> bool:
        """
        Check if any filters are applied.
        
        Returns:
            True if any filters are set
        """
        return bool(self.document_types or self.company_names or self.date_range)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert filters to dictionary.
        
        Returns:
            Dictionary representation of filters
        """
        return {
            'document_types': self.document_types,
            'company_names': self.company_names,
            'date_range': [d.isoformat() for d in self.date_range] if self.date_range else None,
            'max_results': self.max_results,
        }


@dataclass
class CacheEntry:
    """Cache entry with TTL"""
    
    result: SearchResponse
    cached_at: datetime
    access_count: int = 0
    
    def is_expired(self, ttl_seconds: int) -> bool:
        """
        Check if cache entry has expired.
        
        Args:
            ttl_seconds: Time-to-live in seconds
            
        Returns:
            True if expired, False otherwise
        """
        age = (datetime.now() - self.cached_at).total_seconds()
        return age > ttl_seconds
    
    def validate(self) -> bool:
        """
        Validate cache entry.
        
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if not self.result:
            raise ValueError("CacheEntry must have a result")
        
        if self.access_count < 0:
            raise ValueError(f"access_count must be non-negative, got {self.access_count}")
        
        self.result.validate()
        
        return True
    
    def increment_access(self) -> None:
        """Increment the access count for this cache entry"""
        self.access_count += 1
    
    def age_seconds(self) -> float:
        """
        Get the age of this cache entry in seconds.
        
        Returns:
            Age in seconds
        """
        return (datetime.now() - self.cached_at).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert cache entry to dictionary.
        
        Returns:
            Dictionary representation of cache entry
        """
        return {
            'result': self.result.to_dict(),
            'cached_at': self.cached_at.isoformat(),
            'access_count': self.access_count,
            'age_seconds': self.age_seconds(),
        }
