"""
Property-based tests for minimax_search data models

**Feature: minimax-m2-search-integration, Property 1: Query validation consistency**
Tests that whitespace-only queries are consistently rejected.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pytest

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hypothesis import given, strategies as st, settings
from minimax_search.models import (
    Document,
    SearchResult,
    SearchResponse,
    SearchFilters,
    CacheEntry,
)


# Strategies for generating test data
@st.composite
def document_strategy(draw):
    """Generate valid Document instances"""
    doc_types = ['cv', 'cover_letter', 'job_description', 'other']
    
    return Document(
        file_path=Path(draw(st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_characters='/\\')))),
        document_type=draw(st.sampled_from(doc_types)),
        content=draw(st.text(min_size=1, max_size=1000)),
        company_name=draw(st.one_of(st.none(), st.text(min_size=1, max_size=50))),
        role_title=draw(st.one_of(st.none(), st.text(min_size=1, max_size=50))),
    )


@st.composite
def search_result_strategy(draw):
    """Generate valid SearchResult instances"""
    doc = draw(document_strategy())
    match_types = ['exact', 'partial', 'semantic']
    
    return SearchResult(
        document=doc,
        relevance_score=draw(st.floats(min_value=0.0, max_value=1.0)),
        matched_excerpts=draw(st.lists(st.text(max_size=100), max_size=5)),
        highlighted_text=draw(st.text(max_size=200)),
        match_type=draw(st.sampled_from(match_types)),
    )



# Property 1: Query validation consistency
# **Validates: Requirements 1.3**
@given(st.text().filter(lambda s: s.strip() == ''))
@settings(max_examples=100)
def test_property_whitespace_query_rejection(whitespace_query):
    """
    **Feature: minimax-m2-search-integration, Property 1: Query validation consistency**
    
    Property: For any string input containing only whitespace characters,
    the SearchResponse validation should reject it with an error.
    
    This ensures that empty or whitespace-only queries are consistently
    rejected across all system components.
    
    **Validates: Requirements 1.3**
    """
    # Create a SearchResponse with whitespace-only query
    response = SearchResponse(
        query=whitespace_query,
        results=[],
        total_count=0,
        search_time_ms=100
    )
    
    # Validation should fail for whitespace-only queries
    with pytest.raises(ValueError, match="query cannot be empty"):
        response.validate()


# Property 2: Document validation consistency
@given(document_strategy())
@settings(max_examples=100)
def test_property_document_validation_consistency(document):
    """
    Property: For any valid Document, validation should succeed.
    
    This ensures that all properly constructed documents pass validation.
    """
    assert document.validate() is True


# Property 3: Relevance score bounds
@given(search_result_strategy())
@settings(max_examples=100)
def test_property_relevance_score_bounds(search_result):
    """
    Property: For any SearchResult, the relevance score must be between 0 and 1.
    
    This ensures that relevance scores are always normalized.
    """
    assert 0.0 <= search_result.relevance_score <= 1.0
    assert search_result.validate() is True


# Property 4: SearchFilters document type validation
@given(st.lists(st.sampled_from(['cv', 'cover_letter', 'job_description', 'other']), min_size=1, max_size=4))
@settings(max_examples=100)
def test_property_valid_document_types(doc_types):
    """
    Property: For any list of valid document types, SearchFilters should accept them.
    
    This ensures that all valid document type combinations are accepted.
    """
    filters = SearchFilters(document_types=doc_types)
    assert filters.validate() is True


# Property 5: Invalid document types rejection
@given(st.lists(st.text(min_size=1, max_size=20).filter(
    lambda s: s not in ['cv', 'cover_letter', 'job_description', 'other']
), min_size=1, max_size=3))
@settings(max_examples=100)
def test_property_invalid_document_types_rejection(invalid_types):
    """
    Property: For any list containing invalid document types,
    SearchFilters initialization should raise ValueError.
    
    This ensures that invalid document types are consistently rejected.
    """
    with pytest.raises(ValueError, match="Invalid document_types"):
        SearchFilters(document_types=invalid_types)


# Property 6: Cache entry expiration consistency
@given(st.integers(min_value=1, max_value=1000))
@settings(max_examples=100)
def test_property_cache_expiration_consistency(ttl_seconds):
    """
    Property: For any cache entry, if current time exceeds cached_at + TTL,
    the entry should be marked as expired.
    
    This ensures cache TTL is consistently enforced.
    """
    # Create a cache entry from the past
    past_time = datetime.now() - timedelta(seconds=ttl_seconds + 1)
    
    response = SearchResponse(
        query="test",
        results=[],
        total_count=0,
        search_time_ms=100
    )
    
    cache_entry = CacheEntry(
        result=response,
        cached_at=past_time,
        access_count=0
    )
    
    # Entry should be expired
    assert cache_entry.is_expired(ttl_seconds) is True


# Property 7: Cache entry not expired when fresh
@given(st.integers(min_value=10, max_value=1000))
@settings(max_examples=100)
def test_property_cache_not_expired_when_fresh(ttl_seconds):
    """
    Property: For any cache entry created now, it should not be expired
    if checked within the TTL period.
    
    This ensures fresh cache entries are not incorrectly marked as expired.
    """
    response = SearchResponse(
        query="test",
        results=[],
        total_count=0,
        search_time_ms=100
    )
    
    cache_entry = CacheEntry(
        result=response,
        cached_at=datetime.now(),
        access_count=0
    )
    
    # Entry should not be expired
    assert cache_entry.is_expired(ttl_seconds) is False


# Property 8: SearchResponse result count consistency
@given(st.lists(search_result_strategy(), min_size=0, max_size=10))
@settings(max_examples=100)
def test_property_search_response_count_consistency(results):
    """
    Property: For any SearchResponse, the number of results should not exceed total_count.
    
    This ensures result count consistency.
    """
    response = SearchResponse(
        query="test query",
        results=results,
        total_count=len(results),
        search_time_ms=100
    )
    
    assert len(response.results) <= response.total_count
    assert response.validate() is True


# Property 9: Document type filtering
@given(
    st.lists(document_strategy(), min_size=1, max_size=20),
    st.sampled_from(['cv', 'cover_letter', 'job_description', 'other'])
)
@settings(max_examples=100)
def test_property_document_type_filtering(documents, filter_type):
    """
    Property: For any list of documents and a document type filter,
    all documents matching the filter should be of that type.
    
    This validates the document type filtering logic.
    """
    # Filter documents by type
    filtered = [doc for doc in documents if doc.document_type == filter_type]
    
    # All filtered documents should match the filter type
    for doc in filtered:
        assert doc.document_type == filter_type
        assert doc.is_valid_type([filter_type])


# Property 10: Max results validation
@given(st.integers(min_value=1, max_value=1000))
@settings(max_examples=100)
def test_property_max_results_valid_range(max_results):
    """
    Property: For any positive integer up to 1000, SearchFilters should accept it as max_results.
    
    This ensures valid max_results values are accepted.
    """
    filters = SearchFilters(max_results=max_results)
    assert filters.validate() is True
    assert filters.max_results == max_results


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
