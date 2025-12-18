# Implementation Plan: MiniMax M2 Search Integration

- [ ] 1. Set up project structure and core data models
  - [x] 1.1 Create `backend/minimax_search/` directory structure
    - Create `__init__.py`, `client.py`, `indexer.py`, `service.py`, `cache.py`, `rate_limiter.py`, `ranker.py`
    - Create `models.py` for data classes
    - Create `exceptions.py` for custom exceptions
    - _Requirements: All requirements_

  - [x] 1.2 Implement core data models
    - Implement `Document`, `SearchResult`, `SearchResponse`, `SearchFilters`, `CacheEntry` dataclasses
    - Add validation methods to data models
    - _Requirements: 1.5, 6.5_

  - [x] 1.3 Write property test for data model validation
    - **Property 1: Query validation consistency**
    - **Validates: Requirements 1.3**

- [ ] 2. Implement Rate Limiter component
  - [ ] 2.1 Create RateLimiter class with token bucket algorithm
    - Implement request counting and quota tracking
    - Implement per-minute and daily limit enforcement
    - Add reset timing logic
    - _Requirements: 3.1, 3.4_

  - [ ] 2.2 Add exponential backoff for rate limit errors
    - Implement retry logic with exponential backoff
    - Add wait_if_needed method
    - _Requirements: 3.2_

  - [ ] 2.3 Write property test for rate limit enforcement
    - **Property 3: Rate limit enforcement**
    - **Validates: Requirements 3.1**

  - [ ] 2.4 Write property test for backoff behavior
    - **Property 4: Rate limit backoff behavior**
    - **Validates: Requirements 3.2**

  - [ ] 2.5 Write property test for concurrent request handling
    - **Property: Concurrent request serialization**
    - **Validates: Requirements 3.5**

  - [ ] 2.6 Write property test for quota tracking accuracy
    - **Property: Quota tracking accuracy**
    - **Validates: Requirements 3.4**

- [ ] 3. Implement MiniMax M2 API Client
  - [ ] 3.1 Create MiniMaxSearchClient class extending AIAnalyzer pattern
    - Implement initialization with API key and model configuration
    - Add is_available method
    - Load configuration from environment variables
    - _Requirements: 2.1, 2.4_

  - [ ] 3.2 Implement API authentication and request handling
    - Build authentication headers
    - Implement _call_api method with proper error handling
    - Add request timeout configuration
    - _Requirements: 2.2, 2.4_

  - [ ] 3.3 Write property test for authentication requirement
    - **Property 2: API authentication requirement**
    - **Validates: Requirements 2.2**

  - [ ] 3.4 Write property test for authentication headers
    - **Property: Authentication header inclusion**
    - **Validates: Requirements 2.4**

  - [ ] 3.5 Implement search prompt building
    - Create _build_search_prompt method
    - Format documents and query for MiniMax M2
    - Limit context to avoid token limits
    - _Requirements: 4.1_

  - [ ] 3.6 Implement API response parsing
    - Parse MiniMax M2 response format
    - Extract search results from API response
    - Handle malformed responses
    - _Requirements: 1.1_

  - [ ] 3.7 Add network error handling
    - Catch connection errors, timeouts, DNS failures
    - Implement retry logic with exponential backoff
    - Return user-friendly error messages
    - _Requirements: 5.1, 5.3_

  - [ ] 3.8 Write property test for network error handling
    - **Property 7: Network error handling**
    - **Validates: Requirements 5.1**

  - [ ] 3.9 Write property test for retry behavior
    - **Property 8: Retry with exponential backoff**
    - **Validates: Requirements 5.3**

  - [ ] 3.10 Implement circuit breaker pattern
    - Track consecutive failures
    - Enter open state after threshold
    - Implement half-open state with test requests
    - _Requirements: 5.5_

  - [ ] 3.11 Add test mode support
    - Implement mock response generation
    - Add mode switching logic
    - Log requests in test mode without making API calls
    - _Requirements: 7.1, 7.2, 7.4_

  - [ ] 3.12 Write property test for test mode isolation
    - **Property 11: Test mode isolation**
    - **Validates: Requirements 7.1**

  - [ ] 3.13 Write property test for credential security
    - **Property 14: Credential security**
    - **Validates: Requirements 2.3**

- [ ] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Document Indexer
  - [ ] 5.1 Create DocumentIndexer class
    - Initialize with base paths for job_applications and templates
    - Create index data structure
    - _Requirements: 6.1_

  - [ ] 5.2 Implement document discovery and indexing
    - Scan directories for .tex and .pdf files
    - Extract metadata (company name, role, document type)
    - Build searchable index
    - _Requirements: 6.1_

  - [ ] 5.3 Implement text extraction from LaTeX files
    - Parse .tex files and extract content
    - Remove LaTeX commands and formatting
    - Handle special characters and encoding
    - _Requirements: 6.1_

  - [ ] 5.4 Add document type classification
    - Identify CVs, cover letters, and job descriptions
    - Extract company and role information from filenames
    - _Requirements: 6.1, 6.5_

  - [ ] 5.5 Implement incremental index updates
    - Add update_document method for single file updates
    - Track file modification times
    - _Requirements: 6.4_

  - [ ] 5.6 Write property test for index update consistency
    - **Property 10: Index update consistency**
    - **Validates: Requirements 6.4**

  - [ ] 5.7 Write property test for document type inclusion
    - **Property: Document type inclusion**
    - **Validates: Requirements 6.1**

- [ ] 6. Implement Search Cache
  - [ ] 6.1 Create SearchCache class with LRU eviction
    - Implement OrderedDict-based cache
    - Add TTL tracking for entries
    - Configure max size and TTL from environment
    - _Requirements: 8.3, 8.5_

  - [ ] 6.2 Implement cache operations
    - Add get method with TTL checking
    - Add set method with LRU eviction
    - Implement cache key generation (query hash)
    - _Requirements: 8.4_

  - [ ] 6.3 Add cache invalidation
    - Implement pattern-based invalidation
    - Add clear method
    - _Requirements: 8.3_

  - [ ] 6.4 Write property test for cache TTL expiration
    - **Property 13: Cache TTL expiration**
    - **Validates: Requirements 8.4**

  - [ ] 6.5 Write property test for LRU eviction
    - **Property: LRU eviction behavior**
    - **Validates: Requirements 8.5**

  - [ ] 6.6 Write property test for cache hit performance
    - **Property 12: Cache hit performance**
    - **Validates: Requirements 8.4**

- [ ] 7. Implement Result Ranker
  - [ ] 7.1 Create ResultRanker class
    - Initialize with scoring configuration
    - _Requirements: 4.2_

  - [ ] 7.2 Implement relevance scoring
    - Calculate scores based on exact matches, partial matches, semantic similarity
    - Prioritize exact matches over partial matches
    - _Requirements: 4.2, 4.3_

  - [ ] 7.3 Implement result ranking
    - Sort results by relevance score
    - Maintain stable sort for equal scores
    - _Requirements: 4.2_

  - [ ] 7.4 Write property test for ranking monotonicity
    - **Property 5: Result ranking monotonicity**
    - **Validates: Requirements 4.2**

  - [ ] 7.5 Write property test for exact match prioritization
    - **Property 6: Exact match prioritization**
    - **Validates: Requirements 4.3**

  - [ ] 7.6 Implement query term highlighting
    - Highlight matched terms in excerpts
    - Handle case-insensitive matching
    - Escape HTML in output
    - _Requirements: 4.4_

  - [ ] 7.7 Write property test for highlighting
    - **Property: Query term highlighting**
    - **Validates: Requirements 4.4**

- [ ] 8. Implement Search Service
  - [ ] 8.1 Create SearchService class
    - Initialize with client, indexer, cache, and ranker
    - _Requirements: All requirements_

  - [ ] 8.2 Implement query validation
    - Check for empty or whitespace-only queries
    - Validate query length (max 500 chars)
    - Sanitize input
    - _Requirements: 1.3_

  - [ ] 8.3 Implement main search method
    - Check cache first
    - Validate query
    - Get documents from indexer
    - Apply filters
    - Call MiniMax M2 API
    - Rank results
    - Cache results
    - Return SearchResponse
    - _Requirements: 1.1, 1.2, 8.3, 8.4_

  - [ ] 8.4 Add document type filtering
    - Filter documents by type before search
    - Validate filter values
    - _Requirements: 6.2, 6.3_

  - [ ] 8.5 Write property test for document type filtering
    - **Property 9: Document type filtering**
    - **Validates: Requirements 6.2**

  - [ ] 8.6 Implement alternative query suggestions
    - Generate suggestions when no results found
    - Use common search patterns
    - _Requirements: 4.5_

  - [ ] 8.7 Add search metadata to response
    - Include total count, search time, cache status
    - Add suggested queries
    - _Requirements: 1.4_

  - [ ] 8.8 Write property test for result completeness
    - **Property 15: Search result completeness**
    - **Validates: Requirements 1.5**

  - [ ] 8.9 Write property test for search result ordering
    - **Property: Result ordering with highlighting**
    - **Validates: Requirements 1.2**

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Create API endpoint integration
  - [ ] 10.1 Add search endpoint to lego_api.py
    - Create POST /api/search endpoint
    - Define request/response models
    - Add error handling
    - _Requirements: 1.1_

  - [ ] 10.2 Initialize search service in API
    - Load configuration from environment
    - Create service instance
    - Add health check endpoint
    - _Requirements: 2.1_

  - [ ] 10.3 Add request validation middleware
    - Validate request format
    - Check authentication if needed
    - Rate limit API endpoint
    - _Requirements: 1.3_

  - [ ] 10.4 Write integration test for API endpoint
    - Test end-to-end search flow
    - Test error responses
    - Test rate limiting
    - _Requirements: All requirements_

- [ ] 11. Create CLI tool for testing
  - [ ] 11.1 Create minimax_search/__main__.py
    - Add argument parsing (query, filters, options)
    - Initialize search service
    - Format and display results
    - _Requirements: 7.1, 7.2_

  - [ ] 11.2 Add CLI commands
    - search: Execute search query
    - index: Rebuild document index
    - test: Run in test mode
    - stats: Show usage statistics
    - _Requirements: 7.1, 7.3_

  - [ ] 11.3 Add output formatting
    - Pretty-print results
    - Add color highlighting
    - Support JSON output
    - _Requirements: 1.2, 1.5_

- [ ] 12. Add configuration and documentation
  - [ ] 12.1 Update .env.example with search configuration
    - Add MINIMAX_API_KEY (already exists)
    - Add SEARCH_CACHE_SIZE, SEARCH_CACHE_TTL
    - Add RATE_LIMIT_RPM, RATE_LIMIT_DAILY
    - Add SEARCH_INDEX_PATHS
    - _Requirements: 2.1_

  - [ ] 12.2 Create README.md for minimax_search module
    - Document installation and setup
    - Provide usage examples
    - Document API endpoints
    - Include troubleshooting guide
    - _Requirements: All requirements_

  - [ ] 12.3 Add inline documentation
    - Add docstrings to all classes and methods
    - Include type hints
    - Add usage examples in docstrings
    - _Requirements: All requirements_

- [ ] 13. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
