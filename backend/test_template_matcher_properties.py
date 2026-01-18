"""
Property-Based Tests for TemplateMatcher
Tests universal properties of role score calculation and template matching
"""

import pytest
from hypothesis import given, settings, strategies as st
from template_matcher import TemplateMatcher


# Test generators
@st.composite
def role_categories_generator(draw):
    """Generate valid role category configurations"""
    # Define some realistic role categories
    base_categories = {
        'android_developer': {
            'keywords': ['android', 'kotlin', 'mobile', 'java'],
            'priority': 1
        },
        'fullstack_developer': {
            'keywords': ['fullstack', 'react', 'typescript', 'javascript'],
            'priority': 2
        },
        'devops_cloud': {
            'keywords': ['devops', 'kubernetes', 'aws', 'docker'],
            'priority': 4
        },
        'backend_developer': {
            'keywords': ['backend', 'python', 'java', 'spring'],
            'priority': 3
        },
        'ai_product_engineer': {
            'keywords': ['machine learning', 'ai', 'tensorflow', 'pytorch'],
            'priority': 5
        }
    }
    
    # Randomly select a subset of categories (at least 2)
    num_categories = draw(st.integers(min_value=2, max_value=len(base_categories)))
    selected_keys = draw(st.lists(
        st.sampled_from(list(base_categories.keys())),
        min_size=num_categories,
        max_size=num_categories,
        unique=True
    ))
    
    return {key: base_categories[key] for key in selected_keys}


@st.composite
def keyword_counts_generator(draw, role_categories):
    """Generate keyword counts for given role categories"""
    keyword_counts = {}
    
    for role_key, role_data in role_categories.items():
        keywords = role_data['keywords']
        
        # Generate counts for some keywords (0 to all keywords)
        num_keywords = draw(st.integers(min_value=0, max_value=len(keywords)))
        
        if num_keywords > 0:
            selected_keywords = draw(st.lists(
                st.sampled_from(keywords),
                min_size=num_keywords,
                max_size=num_keywords,
                unique=True
            ))
            
            # Generate counts for selected keywords
            counts = {}
            for keyword in selected_keywords:
                count = draw(st.integers(min_value=1, max_value=20))
                counts[keyword] = count
            
            keyword_counts[role_key] = counts
        else:
            keyword_counts[role_key] = {}
    
    return keyword_counts


class TestTemplateMatcherRoleScoreProperties:
    """Property-based tests for role score calculation"""
    
    @settings(max_examples=100)
    @given(st.data())
    def test_role_score_calculation_non_negative(self, data):
        """
        Property: For any job description with multiple role keywords,
                 all calculated scores should be non-negative
        Feature: intelligent-cv-template-selection, Property 2: Role Score Calculation
        Validates: Requirements 1.3, 4.3
        """
        role_categories = data.draw(role_categories_generator())
        keyword_counts = data.draw(keyword_counts_generator(role_categories))
        
        matcher = TemplateMatcher(role_categories)
        scores = matcher.calculate_scores(keyword_counts)
        
        # All scores should be non-negative
        for role_key, score in scores.items():
            assert score >= 0.0, \
                f"Score for role '{role_key}' should be non-negative, got {score}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_role_score_calculation_applies_priority_weighting(self, data):
        """
        Property: For any job description with multiple role keywords,
                 scores should be calculated by dividing raw counts by priority values
        Feature: intelligent-cv-template-selection, Property 2: Role Score Calculation
        Validates: Requirements 1.3, 4.3
        """
        role_categories = data.draw(role_categories_generator())
        keyword_counts = data.draw(keyword_counts_generator(role_categories))
        
        matcher = TemplateMatcher(role_categories)
        scores = matcher.calculate_scores(keyword_counts)
        
        # Verify priority weighting is applied correctly
        for role_key, role_data in role_categories.items():
            matches = keyword_counts.get(role_key, {})
            raw_score = sum(matches.values())
            priority = role_data.get('priority', 1)
            expected_score = raw_score / priority
            
            assert abs(scores[role_key] - expected_score) < 0.001, \
                f"Score for '{role_key}' should be {expected_score}, got {scores[role_key]}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_role_score_higher_priority_gets_higher_weight(self, data):
        """
        Property: For equal raw keyword counts, roles with lower priority numbers
                 (higher priority) should have higher weighted scores
        Feature: intelligent-cv-template-selection, Property 2: Role Score Calculation
        Validates: Requirements 1.3, 4.3
        """
        # Create two roles with different priorities but same keyword count
        role_categories = {
            'high_priority_role': {
                'keywords': ['keyword1', 'keyword2'],
                'priority': 1  # Higher priority (lower number)
            },
            'low_priority_role': {
                'keywords': ['keyword3', 'keyword4'],
                'priority': 5  # Lower priority (higher number)
            }
        }
        
        # Generate same raw count for both roles
        raw_count = data.draw(st.integers(min_value=1, max_value=20))
        
        keyword_counts = {
            'high_priority_role': {'keyword1': raw_count},
            'low_priority_role': {'keyword3': raw_count}
        }
        
        matcher = TemplateMatcher(role_categories)
        scores = matcher.calculate_scores(keyword_counts)
        
        # High priority role should have higher weighted score
        assert scores['high_priority_role'] > scores['low_priority_role'], \
            f"High priority role (priority=1) should have higher score than low priority role (priority=5)"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_role_score_zero_keywords_gives_zero_score(self, data):
        """
        Property: For any role with zero keyword matches, the score should be zero
        Feature: intelligent-cv-template-selection, Property 2: Role Score Calculation
        Validates: Requirements 1.3, 4.3
        """
        role_categories = data.draw(role_categories_generator())
        
        # Create keyword counts with at least one role having zero matches
        keyword_counts = {}
        for role_key in role_categories.keys():
            keyword_counts[role_key] = {}  # Empty counts
        
        matcher = TemplateMatcher(role_categories)
        scores = matcher.calculate_scores(keyword_counts)
        
        # All scores should be zero
        for role_key, score in scores.items():
            assert score == 0.0, \
                f"Score for role '{role_key}' with zero keywords should be 0.0, got {score}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_role_score_increases_with_keyword_count(self, data):
        """
        Property: For any role, increasing keyword count should increase or maintain the score
        Feature: intelligent-cv-template-selection, Property 2: Role Score Calculation
        Validates: Requirements 1.3, 4.3
        """
        role_categories = {
            'test_role': {
                'keywords': ['keyword1', 'keyword2', 'keyword3'],
                'priority': 2
            }
        }
        
        # Generate two keyword counts where second has more matches
        count1 = data.draw(st.integers(min_value=1, max_value=10))
        count2 = data.draw(st.integers(min_value=count1, max_value=20))
        
        keyword_counts_1 = {
            'test_role': {'keyword1': count1}
        }
        
        keyword_counts_2 = {
            'test_role': {'keyword1': count2}
        }
        
        matcher = TemplateMatcher(role_categories)
        scores_1 = matcher.calculate_scores(keyword_counts_1)
        scores_2 = matcher.calculate_scores(keyword_counts_2)
        
        # Score should increase or stay the same
        assert scores_2['test_role'] >= scores_1['test_role'], \
            f"Score should increase with keyword count: {scores_1['test_role']} -> {scores_2['test_role']}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_role_score_calculation_includes_all_roles(self, data):
        """
        Property: For any set of role categories, calculate_scores should return
                 scores for all roles (even if zero)
        Feature: intelligent-cv-template-selection, Property 2: Role Score Calculation
        Validates: Requirements 1.3, 4.3
        """
        role_categories = data.draw(role_categories_generator())
        keyword_counts = data.draw(keyword_counts_generator(role_categories))
        
        matcher = TemplateMatcher(role_categories)
        scores = matcher.calculate_scores(keyword_counts)
        
        # All role categories should have scores
        for role_key in role_categories.keys():
            assert role_key in scores, \
                f"Role '{role_key}' should have a score in the results"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_role_score_calculation_deterministic(self, data):
        """
        Property: For any keyword counts, calculating scores twice should give identical results
        Feature: intelligent-cv-template-selection, Property 2: Role Score Calculation
        Validates: Requirements 1.3, 4.3
        """
        role_categories = data.draw(role_categories_generator())
        keyword_counts = data.draw(keyword_counts_generator(role_categories))
        
        matcher = TemplateMatcher(role_categories)
        scores_1 = matcher.calculate_scores(keyword_counts)
        scores_2 = matcher.calculate_scores(keyword_counts)
        
        # Scores should be identical
        assert scores_1 == scores_2, \
            "Score calculation should be deterministic"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_role_score_priority_weighting_formula(self, data):
        """
        Property: For any role, weighted_score = raw_score / priority
        Feature: intelligent-cv-template-selection, Property 2: Role Score Calculation
        Validates: Requirements 1.3, 4.3
        """
        # Create a role with known priority
        priority = data.draw(st.integers(min_value=1, max_value=10))
        role_categories = {
            'test_role': {
                'keywords': ['keyword1', 'keyword2'],
                'priority': priority
            }
        }
        
        # Generate keyword counts
        count1 = data.draw(st.integers(min_value=0, max_value=10))
        count2 = data.draw(st.integers(min_value=0, max_value=10))
        
        keyword_counts = {
            'test_role': {'keyword1': count1, 'keyword2': count2}
        }
        
        matcher = TemplateMatcher(role_categories)
        scores = matcher.calculate_scores(keyword_counts)
        
        # Verify formula: weighted_score = raw_score / priority
        raw_score = count1 + count2
        expected_weighted_score = raw_score / priority
        
        assert abs(scores['test_role'] - expected_weighted_score) < 0.001, \
            f"Weighted score should be {expected_weighted_score}, got {scores['test_role']}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_role_score_multiple_keywords_sum_correctly(self, data):
        """
        Property: For any role with multiple keyword matches, the raw score
                 should be the sum of all keyword counts before priority weighting
        Feature: intelligent-cv-template-selection, Property 2: Role Score Calculation
        Validates: Requirements 1.3, 4.3
        """
        role_categories = {
            'test_role': {
                'keywords': ['kw1', 'kw2', 'kw3', 'kw4'],
                'priority': 2
            }
        }
        
        # Generate counts for multiple keywords
        num_keywords = data.draw(st.integers(min_value=1, max_value=4))
        keyword_counts_dict = {}
        expected_raw_sum = 0
        
        for i in range(num_keywords):
            count = data.draw(st.integers(min_value=1, max_value=10))
            keyword_counts_dict[f'kw{i+1}'] = count
            expected_raw_sum += count
        
        keyword_counts = {
            'test_role': keyword_counts_dict
        }
        
        matcher = TemplateMatcher(role_categories)
        scores = matcher.calculate_scores(keyword_counts)
        
        # Verify: score = sum(counts) / priority
        expected_score = expected_raw_sum / 2
        assert abs(scores['test_role'] - expected_score) < 0.001, \
            f"Score should be {expected_score} (sum={expected_raw_sum}, priority=2), got {scores['test_role']}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
