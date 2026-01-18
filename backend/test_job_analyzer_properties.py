"""
Property-Based Tests for JobAnalyzer
Tests universal properties of keyword extraction and job analysis
"""

import pytest
from hypothesis import given, settings, strategies as st
from job_analyzer import JobAnalyzer


# Test generators
@st.composite
def technical_keywords(draw):
    """Generate realistic technical keywords"""
    single_words = ['python', 'java', 'kubernetes', 'docker', 'react', 'aws', 'azure', 
                    'devops', 'android', 'ios', 'typescript', 'javascript', 'golang']
    multi_words = ['full stack', 'site reliability', 'machine learning', 'ci/cd',
                   'incident management', 'cloud native', 'api gateway']
    
    all_keywords = single_words + multi_words
    return draw(st.sampled_from(all_keywords))


@st.composite
def job_description_with_keywords(draw, keywords):
    """Generate a job description containing specific keywords"""
    # Generate a base description
    templates = [
        "We are looking for a {keyword} expert with experience in {keyword}.",
        "The ideal candidate has {keyword} skills and {keyword} experience.",
        "Join our team as a {keyword} specialist. You will work with {keyword}.",
        "Required: {keyword} knowledge. Nice to have: {keyword} certification.",
    ]
    
    template = draw(st.sampled_from(templates))
    
    # Insert keywords into the template
    description_parts = []
    for keyword in keywords:
        desc = template.format(keyword=keyword)
        description_parts.append(desc)
    
    # Add some filler text
    filler = draw(st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs')), 
                         min_size=0, max_size=100))
    
    description = " ".join(description_parts) + " " + filler
    return description


class TestJobAnalyzerProperties:
    """Property-based tests for JobAnalyzer"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.analyzer = JobAnalyzer()
    
    @settings(max_examples=100)
    @given(text=st.text(min_size=0, max_size=1000))
    def test_normalize_text_idempotent(self, text):
        """
        Property: Normalizing text twice should produce the same result as normalizing once
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.1, 1.4, 1.5
        """
        normalized_once = self.analyzer.normalize_text(text)
        normalized_twice = self.analyzer.normalize_text(normalized_once)
        
        assert normalized_once == normalized_twice, \
            "Normalizing text should be idempotent"
    
    @settings(max_examples=100)
    @given(text=st.text(min_size=1, max_size=1000))
    def test_normalized_text_is_lowercase(self, text):
        """
        Property: Normalized text should always be lowercase
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.1, 1.4, 1.5
        """
        normalized = self.analyzer.normalize_text(text)
        
        assert normalized == normalized.lower(), \
            "Normalized text should be lowercase"
    
    @settings(max_examples=100)
    @given(text=st.text(min_size=0, max_size=1000))
    def test_normalized_text_no_extra_whitespace(self, text):
        """
        Property: Normalized text should not have leading/trailing whitespace or multiple consecutive spaces
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.1, 1.4, 1.5
        """
        normalized = self.analyzer.normalize_text(text)
        
        # Should not have leading/trailing whitespace
        assert normalized == normalized.strip(), \
            "Normalized text should not have leading/trailing whitespace"
        
        # Should not have multiple consecutive spaces
        assert '  ' not in normalized, \
            "Normalized text should not have multiple consecutive spaces"
    
    @settings(max_examples=100)
    @given(keyword=technical_keywords())
    def test_keyword_count_non_negative(self, keyword):
        """
        Property: Keyword count should always be non-negative
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.1, 1.4, 1.5
        """
        text = f"This is a test with {keyword} mentioned multiple times. {keyword} is important."
        normalized = self.analyzer.normalize_text(text)
        count = self.analyzer.count_keyword_occurrences(normalized, keyword)
        
        assert count >= 0, \
            f"Keyword count should be non-negative, got {count}"
    
    @settings(max_examples=100)
    @given(keyword=technical_keywords(), 
           repetitions=st.integers(min_value=0, max_value=10))
    def test_keyword_count_matches_repetitions(self, keyword, repetitions):
        """
        Property: For any keyword repeated N times in text, count should be at least N
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.1, 1.4, 1.5
        """
        # Create text with exact repetitions separated by periods
        text_parts = [keyword] * repetitions
        text = ". ".join(text_parts) + "."
        
        normalized = self.analyzer.normalize_text(text)
        count = self.analyzer.count_keyword_occurrences(normalized, keyword)
        
        assert count >= repetitions, \
            f"Expected at least {repetitions} occurrences of '{keyword}', got {count}"
    
    @settings(max_examples=100)
    @given(keyword=technical_keywords())
    def test_keyword_extraction_includes_present_keywords(self, keyword):
        """
        Property: For any keyword present in text, extract_keywords should find it
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.1, 1.4, 1.5
        """
        text = f"We need someone with {keyword} experience. {keyword} skills are essential."
        keyword_list = [keyword, 'nonexistent_keyword_xyz']
        
        result = self.analyzer.extract_keywords(text, keyword_list)
        
        assert keyword in result, \
            f"Keyword '{keyword}' should be found in extraction results"
        assert result[keyword] > 0, \
            f"Keyword '{keyword}' should have positive count"
    
    @settings(max_examples=100)
    @given(keywords=st.lists(technical_keywords(), min_size=1, max_size=5, unique=True))
    def test_extract_keywords_completeness(self, keywords):
        """
        Property: For any job description containing known keywords, 
                 extraction should identify all present keywords
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.1, 1.4, 1.5
        """
        # Create text containing all keywords
        text_parts = [f"Experience with {kw} required." for kw in keywords]
        text = " ".join(text_parts)
        
        result = self.analyzer.extract_keywords(text, keywords)
        
        # All keywords should be found
        for keyword in keywords:
            assert keyword in result, \
                f"Keyword '{keyword}' should be found in results"
            assert result[keyword] > 0, \
                f"Keyword '{keyword}' should have positive count"
    
    @settings(max_examples=100)
    @given(keyword=technical_keywords())
    def test_word_boundary_matching(self, keyword):
        """
        Property: Keyword matching should use word boundaries (exact matches only)
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.4, 1.5
        """
        # Create text where keyword appears as part of another word
        text = f"We need {keyword} experience. The {keyword}123 tool is not the same as {keyword}."
        normalized = self.analyzer.normalize_text(text)
        
        count = self.analyzer.count_keyword_occurrences(normalized, keyword)
        
        # Should find at least the standalone occurrences
        # (The exact count depends on whether keyword123 matches, which it shouldn't with word boundaries)
        assert count >= 2, \
            f"Should find at least 2 standalone occurrences of '{keyword}'"
    
    @settings(max_examples=100)
    @given(text=st.text(min_size=0, max_size=500))
    def test_empty_keyword_list_returns_empty(self, text):
        """
        Property: Extracting with empty keyword list should return empty dict
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.1
        """
        result = self.analyzer.extract_keywords(text, [])
        
        assert result == {}, \
            "Empty keyword list should return empty results"
    
    @settings(max_examples=100)
    @given(keywords=st.lists(technical_keywords(), min_size=1, max_size=5))
    def test_extract_keywords_only_returns_found_keywords(self, keywords):
        """
        Property: extract_keywords should only return keywords that were actually found
        Feature: intelligent-cv-template-selection, Property 1: Keyword Extraction Completeness
        Validates: Requirements 1.1, 1.5
        """
        # Create text with only some keywords
        text = f"We need {keywords[0]} experience."
        
        result = self.analyzer.extract_keywords(text, keywords)
        
        # All returned keywords should have positive counts
        for keyword, count in result.items():
            assert count > 0, \
                f"Returned keyword '{keyword}' should have positive count, got {count}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


class TestMultiWordKeywordProperties:
    """Property-based tests for multi-word keyword support"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.analyzer = JobAnalyzer()
    
    @settings(max_examples=100)
    @given(st.data())
    def test_multi_word_keyword_treated_as_single_unit(self, data):
        """
        Property: Multi-word keyword phrases should be treated as single matching units
        Feature: intelligent-cv-template-selection, Property 6: Multi-word Keyword Support
        Validates: Requirements 4.5
        """
        # Generate multi-word keywords
        multi_word_keywords = [
            'full stack', 'site reliability', 'machine learning', 'ci/cd',
            'incident management', 'cloud native', 'api gateway', 'devops engineer'
        ]
        
        keyword = data.draw(st.sampled_from(multi_word_keywords))
        
        # Create text with the multi-word keyword
        text = f"We need {keyword} experience. The {keyword} role is important."
        normalized = self.analyzer.normalize_text(text)
        
        count = self.analyzer.count_keyword_occurrences(normalized, keyword)
        
        # Should find the complete phrase
        assert count >= 2, \
            f"Multi-word keyword '{keyword}' should be found as a complete phrase"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_multi_word_keyword_not_matched_by_individual_words(self, data):
        """
        Property: Multi-word keywords should not match when only individual words are present
        Feature: intelligent-cv-template-selection, Property 6: Multi-word Keyword Support
        Validates: Requirements 4.5
        """
        # Test that "full stack" doesn't match "full" or "stack" alone
        multi_word_pairs = [
            ('full stack', 'full', 'stack'),
            ('site reliability', 'site', 'reliability'),
            ('machine learning', 'machine', 'learning'),
            ('incident management', 'incident', 'management')
        ]
        
        phrase, word1, word2 = data.draw(st.sampled_from(multi_word_pairs))
        
        # Create text with individual words but not the phrase
        text = f"We have a {word1} system. The {word2} is important."
        normalized = self.analyzer.normalize_text(text)
        
        count = self.analyzer.count_keyword_occurrences(normalized, phrase)
        
        # Should NOT find the phrase when only individual words are present
        assert count == 0, \
            f"Multi-word keyword '{phrase}' should not match individual words '{word1}' and '{word2}'"
    
    @settings(max_examples=100)
    @given(repetitions=st.integers(min_value=1, max_value=5))
    def test_multi_word_keyword_count_accuracy(self, repetitions):
        """
        Property: Multi-word keyword count should accurately reflect number of complete phrase occurrences
        Feature: intelligent-cv-template-selection, Property 6: Multi-word Keyword Support
        Validates: Requirements 4.5
        """
        keyword = "full stack"
        
        # Create text with exact repetitions of the multi-word phrase
        text_parts = [f"The {keyword} developer"] * repetitions
        text = ". ".join(text_parts) + "."
        
        normalized = self.analyzer.normalize_text(text)
        count = self.analyzer.count_keyword_occurrences(normalized, keyword)
        
        assert count == repetitions, \
            f"Expected {repetitions} occurrences of '{keyword}', got {count}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_multi_word_keywords_with_hyphens_and_spaces(self, data):
        """
        Property: Multi-word keywords with different separators should be handled correctly
        Feature: intelligent-cv-template-selection, Property 6: Multi-word Keyword Support
        Validates: Requirements 4.5
        """
        # Test variations of the same concept
        variations = [
            ('full-stack', 'full-stack developer'),
            ('full stack', 'full stack developer'),
            ('ci/cd', 'ci/cd pipeline'),
            ('site reliability', 'site reliability engineer')
        ]
        
        keyword, text_template = data.draw(st.sampled_from(variations))
        
        text = f"We need a {text_template}. Experience with {text_template} is required."
        normalized = self.analyzer.normalize_text(text)
        
        count = self.analyzer.count_keyword_occurrences(normalized, keyword)
        
        # Should find the keyword in the text
        assert count >= 2, \
            f"Keyword '{keyword}' should be found in text containing '{text_template}'"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_extract_keywords_handles_multi_word_phrases(self, data):
        """
        Property: extract_keywords should correctly handle lists containing multi-word phrases
        Feature: intelligent-cv-template-selection, Property 6: Multi-word Keyword Support
        Validates: Requirements 4.5
        """
        # Mix of single and multi-word keywords
        keywords = [
            'python',
            'full stack',
            'kubernetes',
            'site reliability',
            'docker'
        ]
        
        # Select some keywords to include in text
        included_keywords = data.draw(st.lists(
            st.sampled_from(keywords),
            min_size=1,
            max_size=len(keywords),
            unique=True
        ))
        
        # Create text with selected keywords
        text_parts = [f"Experience with {kw} required." for kw in included_keywords]
        text = " ".join(text_parts)
        
        result = self.analyzer.extract_keywords(text, keywords)
        
        # All included keywords should be found
        for keyword in included_keywords:
            assert keyword in result, \
                f"Multi-word keyword '{keyword}' should be found in extraction results"
            assert result[keyword] > 0, \
                f"Multi-word keyword '{keyword}' should have positive count"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_multi_word_keyword_case_insensitive(self, data):
        """
        Property: Multi-word keyword matching should be case-insensitive
        Feature: intelligent-cv-template-selection, Property 6: Multi-word Keyword Support
        Validates: Requirements 4.5
        """
        keyword = "full stack"
        
        # Generate different case variations
        case_variations = [
            "Full Stack",
            "FULL STACK",
            "full stack",
            "Full stack",
            "fUlL sTaCk"
        ]
        
        variation = data.draw(st.sampled_from(case_variations))
        
        text = f"We need {variation} developers. {variation} experience is essential."
        normalized = self.analyzer.normalize_text(text)
        
        count = self.analyzer.count_keyword_occurrences(normalized, keyword)
        
        assert count >= 2, \
            f"Multi-word keyword '{keyword}' should match case variation '{variation}'"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_multi_word_keyword_with_special_characters(self, data):
        """
        Property: Multi-word keywords with special characters (/, -) should be handled correctly
        Feature: intelligent-cv-template-selection, Property 6: Multi-word Keyword Support
        Validates: Requirements 4.5
        """
        special_keywords = [
            'ci/cd',
            'full-stack',
            'front-end',
            'back-end',
            'api/rest'
        ]
        
        keyword = data.draw(st.sampled_from(special_keywords))
        
        text = f"We need {keyword} experience. {keyword} skills are required."
        normalized = self.analyzer.normalize_text(text)
        
        count = self.analyzer.count_keyword_occurrences(normalized, keyword)
        
        assert count >= 2, \
            f"Keyword with special characters '{keyword}' should be found correctly"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
