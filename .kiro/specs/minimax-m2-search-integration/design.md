# Design Document: MiniMax M2 Search Integration

## Overview

This design document describes the integration of MiniMax M2 free model API to provide intelligent search capabilities across job applications, CVs, cover letters, and job descriptions. The system will leverage the existing `AIAnalyzer` class pattern and extend it with a dedicated search service that uses natural language processing to understand user queries and return relevant results.

The search system will be built as a standalone service that can be integrated into both the backend API (`lego_api.py`) and used as a command-line tool for testing and development.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   User/Client   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Search API Endpoint           │
│   (FastAPI/Flask)               │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Search Service                │
│   - Query Processing            │
│   - Result Ranking              │
│   - Cache Management            │
└────────┬────────────────────────┘
         │
         ├──────────────┬──────────────┐
         ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  MiniMax M2  │ │  Document    │ │  Rate        │
│  API Client  │ │  Indexer     │ │  Limiter     │
└──────────────┘ └──────────────┘ └──────────────┘
         │              │              │
         ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  MiniMax     │ │  File System │ │  Usage       │
│  Cloud API   │ │  (LaTeX/PDF) │ │  Tracker     │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Component Interaction Flow

1. **User submits search query** → Search API Endpoint
2. **Query validation** → Search Service validates and preprocesses query
3. **Cache check** → Search Service checks if query is cached
4. **Rate limit check** → Rate Limiter verifies quota availability
5. **Document retrieval** → Document Indexer loads relevant documents
6. **API call** → MiniMax M2 API Client sends query with context
7. **Result processing** → Search Service ranks and formats results
8. **Response** → Results returned to user with metadata

## Components and Interfaces

### 1. MiniMaxSearchClient

Extends the existing `AIAnalyzer` pattern for search-specific functionality.

```python
class MiniMaxSearchClient:
    """Client for MiniMax M2 search API"""
    
    def __init__(self, api_key: str, model: str = "MiniMax-Text-01"):
        self.api_key: str
        self.model: str
        self.api_url: str
        self.timeout: int
        self.rate_limiter: RateLimiter
    
    def search(self, query: str, document_types: List[str] = None, 
               max_results: int = 10) -> SearchResponse:
        """Execute search query using MiniMax M2"""
        pass
    
    def is_available(self) -> bool:
        """Check if API is available"""
        pass
    
    def _build_search_prompt(self, query: str, documents: List[Document]) -> str:
        """Build prompt for MiniMax M2 search"""
        pass
    
    def _call_api(self, prompt: str) -> Dict:
        """Make API call to MiniMax M2"""
        pass
```

### 2. DocumentIndexer

Manages indexing and retrieval of searchable documents.

```python
class DocumentIndexer:
    """Indexes and retrieves documents for search"""
    
    def __init__(self, base_paths: List[Path]):
        self.base_paths: List[Path]
        self.index: Dict[str, DocumentMetadata]
    
    def build_index(self) -> None:
        """Build or rebuild document index"""
        pass
    
    def get_documents(self, document_types: List[str] = None) -> List[Document]:
        """Retrieve documents by type"""
        pass
    
    def update_document(self, file_path: Path) -> None:
        """Update index for a single document"""
        pass
    
    def extract_text(self, file_path: Path) -> str:
        """Extract text from LaTeX/PDF files"""
        pass
```

### 3. SearchService

Main service orchestrating search operations.

```python
class SearchService:
    """Main search service coordinating all components"""
    
    def __init__(self, client: MiniMaxSearchClient, 
                 indexer: DocumentIndexer,
                 cache: SearchCache):
        self.client: MiniMaxSearchClient
        self.indexer: DocumentIndexer
        self.cache: SearchCache
        self.result_ranker: ResultRanker
    
    def search(self, query: str, filters: SearchFilters) -> SearchResponse:
        """Execute search with caching and ranking"""
        pass
    
    def validate_query(self, query: str) -> bool:
        """Validate search query"""
        pass
    
    def suggest_alternatives(self, query: str) -> List[str]:
        """Suggest alternative queries when no results found"""
        pass
```

### 4. RateLimiter

Manages API rate limits and quota tracking.

```python
class RateLimiter:
    """Manages API rate limits for MiniMax M2 free tier"""
    
    def __init__(self, requests_per_minute: int = 60, 
                 requests_per_day: int = 1000):
        self.rpm_limit: int
        self.daily_limit: int
        self.request_count: int
        self.daily_count: int
        self.last_reset: datetime
    
    def check_limit(self) -> bool:
        """Check if request can be made"""
        pass
    
    def record_request(self) -> None:
        """Record a request"""
        pass
    
    def get_remaining_quota(self) -> Dict[str, int]:
        """Get remaining quota"""
        pass
    
    def wait_if_needed(self) -> None:
        """Wait if rate limit reached"""
        pass
```

### 5. SearchCache

Caches search results to reduce API calls.

```python
class SearchCache:
    """LRU cache for search results"""
    
    def __init__(self, max_size: int = 100, ttl_seconds: int = 300):
        self.max_size: int
        self.ttl: int
        self.cache: OrderedDict[str, CacheEntry]
    
    def get(self, query_hash: str) -> Optional[SearchResponse]:
        """Get cached result"""
        pass
    
    def set(self, query_hash: str, result: SearchResponse) -> None:
        """Cache result"""
        pass
    
    def invalidate(self, pattern: str = None) -> None:
        """Invalidate cache entries"""
        pass
```

### 6. ResultRanker

Ranks and scores search results.

```python
class ResultRanker:
    """Ranks search results by relevance"""
    
    def rank(self, results: List[SearchResult], query: str) -> List[SearchResult]:
        """Rank results by relevance"""
        pass
    
    def calculate_score(self, result: SearchResult, query: str) -> float:
        """Calculate relevance score"""
        pass
    
    def highlight_matches(self, text: str, query: str) -> str:
        """Highlight query terms in text"""
        pass
```

## Data Models

### Document

```python
@dataclass
class Document:
    """Represents a searchable document"""
    file_path: Path
    document_type: str  # 'cv', 'cover_letter', 'job_description'
    content: str
    metadata: Dict[str, Any]
    company_name: Optional[str]
    role_title: Optional[str]
    created_at: datetime
    modified_at: datetime
```

### SearchResult

```python
@dataclass
class SearchResult:
    """Represents a single search result"""
    document: Document
    relevance_score: float
    matched_excerpts: List[str]
    highlighted_text: str
    match_type: str  # 'exact', 'partial', 'semantic'
```

### SearchResponse

```python
@dataclass
class SearchResponse:
    """Response from search operation"""
    query: str
    results: List[SearchResult]
    total_count: int
    search_time_ms: int
    from_cache: bool
    suggested_queries: List[str]
```

### SearchFilters

```python
@dataclass
class SearchFilters:
    """Filters for search queries"""
    document_types: Optional[List[str]]
    company_names: Optional[List[str]]
    date_range: Optional[Tuple[datetime, datetime]]
    max_results: int = 10
```

### CacheEntry

```python
@dataclass
class CacheEntry:
    """Cache entry with TTL"""
    result: SearchResponse
    cached_at: datetime
    access_count: int
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Query validation consistency
*For any* string input, if the input contains only whitespace characters, the search system should reject it and return an error, and the document index should remain unchanged.
**Validates: Requirements 1.3**

### Property 2: API authentication requirement
*For any* API request, if the API key is missing or empty, the client should raise an authentication error before making any network calls.
**Validates: Requirements 2.2**

### Property 3: Rate limit enforcement
*For any* sequence of API requests, the total number of requests made within a one-minute window should never exceed the configured rate limit.
**Validates: Requirements 3.1**

### Property 4: Rate limit backoff behavior
*For any* rate limit error response from the API, the system should wait before retrying, and the wait time should increase exponentially with each subsequent failure.
**Validates: Requirements 3.2**

### Property 5: Result ranking monotonicity
*For any* search results list, if result A has a higher relevance score than result B, then A should appear before B in the returned results.
**Validates: Requirements 4.2**

### Property 6: Exact match prioritization
*For any* search query and result set, results containing exact matches of the query terms should have higher relevance scores than results with only partial matches.
**Validates: Requirements 4.3**

### Property 7: Network error handling
*For any* network failure during API calls, the system should catch the exception and return a user-friendly error message without exposing internal details.
**Validates: Requirements 5.1**

### Property 8: Retry with exponential backoff
*For any* timeout error, the system should retry up to three times, and each retry should wait longer than the previous one.
**Validates: Requirements 5.3**

### Property 9: Document type filtering
*For any* search query with document type filters specified, all returned results should match at least one of the specified document types.
**Validates: Requirements 6.2**

### Property 10: Index update consistency
*For any* document modification, after calling update_document, a subsequent search should reflect the updated content.
**Validates: Requirements 6.4**

### Property 11: Test mode isolation
*For any* API client in test mode, no actual HTTP requests should be made to the MiniMax API endpoints.
**Validates: Requirements 7.1**

### Property 12: Cache hit performance
*For any* cached query, the response time should be at least 10x faster than making an actual API call.
**Validates: Requirements 8.4**

### Property 13: Cache TTL expiration
*For any* cached entry, if the current time exceeds the cached_at time plus TTL, the entry should not be returned and should be treated as a cache miss.
**Validates: Requirements 8.4**

### Property 14: Credential security
*For any* log output or error message, API keys should never appear in plain text.
**Validates: Requirements 2.3**

### Property 15: Search result completeness
*For any* search result, the response should include document type, file path, and at least one excerpt from the matched content.
**Validates: Requirements 1.5**

## Error Handling

### Error Categories

1. **Validation Errors**
   - Empty or whitespace-only queries
   - Invalid document type filters
   - Invalid date ranges

2. **Authentication Errors**
   - Missing API key
   - Invalid API key format
   - Expired JWT token

3. **Rate Limit Errors**
   - Per-minute limit exceeded
   - Daily quota exceeded
   - Concurrent request limit exceeded

4. **Network Errors**
   - Connection timeout
   - DNS resolution failure
   - SSL/TLS errors

5. **API Errors**
   - 4xx client errors (bad request, unauthorized)
   - 5xx server errors (internal server error, service unavailable)
   - Malformed response

6. **System Errors**
   - File not found
   - Permission denied
   - Disk space exhausted

### Error Handling Strategy

```python
class SearchError(Exception):
    """Base exception for search errors"""
    def __init__(self, message: str, error_code: str, details: Dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}

class ValidationError(SearchError):
    """Query validation failed"""
    pass

class AuthenticationError(SearchError):
    """API authentication failed"""
    pass

class RateLimitError(SearchError):
    """Rate limit exceeded"""
    def __init__(self, message: str, retry_after: int):
        super().__init__(message, "RATE_LIMIT_EXCEEDED")
        self.retry_after = retry_after

class NetworkError(SearchError):
    """Network communication failed"""
    pass
```

### Circuit Breaker Pattern

When repeated failures occur (5+ failures in 60 seconds), the system enters a circuit breaker state:

1. **Open State**: All requests fail immediately without calling API
2. **Half-Open State**: After cooldown period, allow one test request
3. **Closed State**: Normal operation resumes if test succeeds

## Testing Strategy

### Unit Testing

Unit tests will cover:

1. **Query Validation**
   - Test empty string rejection
   - Test whitespace-only string rejection
   - Test valid query acceptance

2. **API Client**
   - Test authentication header construction
   - Test request payload formatting
   - Test response parsing

3. **Rate Limiter**
   - Test request counting
   - Test quota tracking
   - Test reset timing

4. **Cache**
   - Test cache hit/miss
   - Test TTL expiration
   - Test LRU eviction

5. **Result Ranker**
   - Test score calculation
   - Test result ordering
   - Test highlight generation

### Property-Based Testing

Property-based tests will use **Hypothesis** (Python PBT library) to verify universal properties:

1. **Query Validation Properties**
   - Property 1: Whitespace rejection
   - Property 2: Authentication requirement

2. **Rate Limiting Properties**
   - Property 3: Rate limit enforcement
   - Property 4: Backoff behavior

3. **Ranking Properties**
   - Property 5: Ranking monotonicity
   - Property 6: Exact match prioritization

4. **Error Handling Properties**
   - Property 7: Network error handling
   - Property 8: Retry behavior

5. **Filtering Properties**
   - Property 9: Document type filtering
   - Property 10: Index consistency

6. **Test Mode Properties**
   - Property 11: Test mode isolation

7. **Cache Properties**
   - Property 12: Cache performance
   - Property 13: TTL expiration

8. **Security Properties**
   - Property 14: Credential security

9. **Completeness Properties**
   - Property 15: Result completeness

**Configuration**: Each property-based test will run a minimum of 100 iterations to ensure thorough coverage of the input space.

### Integration Testing

Integration tests will verify:

1. End-to-end search flow with real documents
2. API integration with MiniMax M2 (using test API key)
3. File system integration for document indexing
4. Cache integration with search service

### Test Utilities

```python
class MockMiniMaxAPI:
    """Mock MiniMax API for testing"""
    def __init__(self, responses: List[Dict]):
        self.responses = responses
        self.call_count = 0
    
    def post(self, url: str, **kwargs) -> MockResponse:
        """Mock API call"""
        pass

class TestDocumentGenerator:
    """Generate test documents for property testing"""
    @staticmethod
    def generate_document(document_type: str) -> Document:
        """Generate random document"""
        pass
```

## Performance Considerations

### Caching Strategy

- **Cache Key**: SHA-256 hash of (query + filters)
- **Cache Size**: 100 entries (LRU eviction)
- **TTL**: 5 minutes
- **Invalidation**: On document updates

### Rate Limiting

- **Free Tier Limits** (assumed):
  - 60 requests per minute
  - 1000 requests per day
- **Strategy**: Token bucket algorithm
- **Backoff**: Exponential (1s, 2s, 4s, 8s)

### Document Indexing

- **Lazy Loading**: Index built on first search
- **Incremental Updates**: Watch file system for changes
- **Text Extraction**: Cache extracted text to avoid re-parsing

### API Optimization

- **Batch Queries**: Combine multiple documents in single API call
- **Prompt Optimization**: Limit document context to 2000 chars per doc
- **Parallel Processing**: Use asyncio for concurrent document processing

## Security Considerations

1. **API Key Storage**
   - Store in environment variables or `.idea/.env`
   - Never commit to version control
   - Use JWT token format (as currently implemented)

2. **Input Sanitization**
   - Validate all user inputs
   - Escape special characters in queries
   - Limit query length (max 500 chars)

3. **Output Sanitization**
   - Redact API keys from logs
   - Sanitize file paths in responses
   - Escape HTML in excerpts

4. **Access Control**
   - Restrict file system access to designated directories
   - Validate file paths to prevent directory traversal
   - Check file permissions before reading

## Deployment Considerations

### Environment Variables

```bash
MINIMAX_API_KEY=<jwt_token>
AI_ENABLED=true
SEARCH_CACHE_SIZE=100
SEARCH_CACHE_TTL=300
RATE_LIMIT_RPM=60
RATE_LIMIT_DAILY=1000
SEARCH_INDEX_PATHS=/path/to/job_applications,/path/to/templates
```

### API Endpoint

```python
# Add to backend/app/lego_api.py
@app.post("/api/search")
async def search_documents(request: SearchRequest) -> SearchResponse:
    """Search documents using MiniMax M2"""
    pass
```

### CLI Tool

```bash
# Command-line interface for testing
python -m backend.minimax_search "find DevOps jobs with Kubernetes"
python -m backend.minimax_search --type cv --company Volvo "cloud engineer"
```

## Future Enhancements

1. **Semantic Search**: Use embeddings for better semantic matching
2. **Multi-language Support**: Support queries in multiple languages
3. **Advanced Filters**: Date ranges, salary ranges, location filters
4. **Search Analytics**: Track popular queries and result click-through rates
5. **Auto-complete**: Suggest queries as user types
6. **Saved Searches**: Allow users to save and rerun searches
7. **Export Results**: Export search results to CSV/JSON
8. **Search History**: Track and display recent searches
