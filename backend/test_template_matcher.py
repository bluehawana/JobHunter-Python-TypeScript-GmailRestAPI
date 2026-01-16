"""
Unit Tests for TemplateMatcher
Tests the scoring and template matching logic
"""

import pytest
from template_matcher import TemplateMatcher


class TestTemplateMatcher:
    """Unit tests for TemplateMatcher"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Sample role categories for testing
        self.role_categories = {
            'android_developer': {
                'keywords': ['android', 'kotlin', 'mobile'],
                'priority': 1
            },
            'fullstack_developer': {
                'keywords': ['fullstack', 'react', 'typescript'],
                'priority': 2
            },
            'devops_cloud': {
                'keywords': ['devops', 'kubernetes', 'aws'],
                'priority': 4
            },
            'backend_developer': {
                'keywords': ['backend', 'java', 'spring'],
                'priority': 3
            }
        }
        self.matcher = TemplateMatcher(self.role_categories)
    
    def test_calculate_scores_with_priority_weighting(self):
        """Test that scores are calculated with priority weighting"""
        keyword_counts = {
            'android_developer': {'android': 5, 'kotlin': 3},  # raw=8, priority=1, weighted=8
            'fullstack_developer': {'react': 10},  # raw=10, priority=2, weighted=5
            'devops_cloud': {'kubernetes': 4},  # raw=4, priority=4, weighted=1
        }
        
        scores = self.matcher.calculate_scores(keyword_counts)
        
        # Verify priority weighting is applied correctly
        assert scores['android_developer'] == 8.0  # 8 / 1
        assert scores['fullstack_developer'] == 5.0  # 10 / 2
        assert scores['devops_cloud'] == 1.0  # 4 / 4
    
    def test_calculate_percentages_sums_to_100(self):
        """Test that percentages sum to 100%"""
        scores = {
            'android_developer': 8.0,
            'fullstack_developer': 5.0,
            'devops_cloud': 1.0,
            'backend_developer': 0.0
        }
        
        percentages = self.matcher.calculate_percentages(scores)
        
        # Verify percentages sum to 100%
        total = sum(percentages.values())
        assert abs(total - 100.0) < 0.01, f"Percentages should sum to 100%, got {total}"
        
        # Verify individual percentages
        assert abs(percentages['android_developer'] - 57.14) < 0.1  # 8/14 * 100
        assert abs(percentages['fullstack_developer'] - 35.71) < 0.1  # 5/14 * 100
        assert abs(percentages['devops_cloud'] - 7.14) < 0.1  # 1/14 * 100
        assert percentages['backend_developer'] == 0.0
    
    def test_calculate_percentages_handles_zero_scores(self):
        """Test that zero total score is handled gracefully"""
        scores = {
            'android_developer': 0.0,
            'fullstack_developer': 0.0,
            'devops_cloud': 0.0
        }
        
        percentages = self.matcher.calculate_percentages(scores)
        
        # All percentages should be 0
        for percentage in percentages.values():
            assert percentage == 0.0
    
    def test_get_role_breakdown_filters_by_threshold(self):
        """Test that role breakdown filters roles below threshold"""
        percentages = {
            'android_developer': 57.14,
            'fullstack_developer': 35.71,
            'devops_cloud': 7.14,
            'backend_developer': 0.0
        }
        
        breakdown = self.matcher.get_role_breakdown(percentages, threshold=5.0)
        
        # Should include roles >= 5%
        assert len(breakdown) == 3
        assert ('android_developer', 57.14) in breakdown
        assert ('fullstack_developer', 35.71) in breakdown
        assert ('devops_cloud', 7.14) in breakdown
        
        # Should not include backend_developer (0%)
        role_keys = [role for role, _ in breakdown]
        assert 'backend_developer' not in role_keys
    
    def test_get_role_breakdown_sorted_descending(self):
        """Test that role breakdown is sorted by percentage descending"""
        percentages = {
            'android_developer': 20.0,
            'fullstack_developer': 60.0,
            'devops_cloud': 15.0,
            'backend_developer': 5.0
        }
        
        breakdown = self.matcher.get_role_breakdown(percentages, threshold=5.0)
        
        # Should be sorted descending
        assert breakdown[0] == ('fullstack_developer', 60.0)
        assert breakdown[1] == ('android_developer', 20.0)
        assert breakdown[2] == ('devops_cloud', 15.0)
        assert breakdown[3] == ('backend_developer', 5.0)
    
    def test_select_best_match_returns_highest_score(self):
        """Test that best match selection returns the highest score"""
        scores = {
            'android_developer': 8.0,
            'fullstack_developer': 15.0,
            'devops_cloud': 3.0
        }
        
        best_role, best_score = self.matcher.select_best_match(scores)
        
        assert best_role == 'fullstack_developer'
        assert best_score == 15.0
    
    def test_select_best_match_handles_empty_scores(self):
        """Test that empty scores are handled gracefully"""
        scores = {}
        
        best_role, best_score = self.matcher.select_best_match(scores)
        
        assert best_role == ''
        assert best_score == 0.0
    
    def test_get_fallback_template_returns_default(self):
        """Test that fallback returns devops_cloud by default"""
        fallback = self.matcher.get_fallback_template()
        
        assert fallback == 'devops_cloud'
    
    def test_get_fallback_template_excludes_specified_roles(self):
        """Test that fallback excludes specified roles"""
        fallback = self.matcher.get_fallback_template(excluded=['devops_cloud'])
        
        # Should return the role with lowest priority number (highest priority)
        # that's not excluded
        assert fallback == 'android_developer'  # priority 1
    
    def test_get_fallback_template_with_multiple_exclusions(self):
        """Test fallback with multiple exclusions"""
        fallback = self.matcher.get_fallback_template(
            excluded=['devops_cloud', 'android_developer']
        )
        
        # Should return next highest priority role
        assert fallback == 'fullstack_developer'  # priority 2
    
    def test_calculate_confidence_score_perfect_separation(self):
        """Test confidence score with perfect separation (second best = 0)"""
        confidence = self.matcher.calculate_confidence_score(
            best_score=10.0,
            second_best_score=0.0,
            total_score=10.0
        )
        
        # Perfect separation (1.0) + high significance (1.0) = high confidence
        assert confidence > 0.9
    
    def test_calculate_confidence_score_close_match(self):
        """Test confidence score with close match"""
        confidence = self.matcher.calculate_confidence_score(
            best_score=10.0,
            second_best_score=9.0,
            total_score=19.0
        )
        
        # Low separation (0.1) should result in lower confidence
        assert confidence < 0.5
    
    def test_calculate_confidence_score_zero_total(self):
        """Test confidence score with zero total score"""
        confidence = self.matcher.calculate_confidence_score(
            best_score=0.0,
            second_best_score=0.0,
            total_score=0.0
        )
        
        assert confidence == 0.0
    
    def test_calculate_confidence_score_high_significance(self):
        """Test confidence score with high keyword count"""
        confidence = self.matcher.calculate_confidence_score(
            best_score=20.0,
            second_best_score=5.0,
            total_score=25.0
        )
        
        # High separation (0.75) + high significance (1.0) = very high confidence
        assert confidence > 0.8
    
    def test_real_world_scenario_clear_match(self):
        """Test real-world scenario: clear fullstack match"""
        keyword_counts = {
            'android_developer': {},
            'fullstack_developer': {'fullstack': 3, 'react': 5, 'typescript': 4},
            'devops_cloud': {'kubernetes': 1},
            'backend_developer': {}
        }
        
        scores = self.matcher.calculate_scores(keyword_counts)
        percentages = self.matcher.calculate_percentages(scores)
        best_role, best_score = self.matcher.select_best_match(scores)
        breakdown = self.matcher.get_role_breakdown(percentages)
        
        # Should select fullstack_developer
        assert best_role == 'fullstack_developer'
        
        # Fullstack should have highest percentage
        assert percentages['fullstack_developer'] > 80.0
        
        # Breakdown should be sorted correctly
        assert breakdown[0][0] == 'fullstack_developer'
    
    def test_real_world_scenario_mixed_role(self):
        """Test real-world scenario: mixed role (software engineering with some DevOps)"""
        keyword_counts = {
            'android_developer': {},
            'fullstack_developer': {'fullstack': 8, 'react': 10, 'typescript': 8},
            'devops_cloud': {'kubernetes': 3, 'aws': 2},
            'backend_developer': {'backend': 2, 'java': 3}
        }
        
        scores = self.matcher.calculate_scores(keyword_counts)
        percentages = self.matcher.calculate_percentages(scores)
        best_role, best_score = self.matcher.select_best_match(scores)
        
        # Should select fullstack_developer (highest score)
        assert best_role == 'fullstack_developer'
        
        # Fullstack should have majority percentage
        assert percentages['fullstack_developer'] > 50.0
        
        # Total should sum to 100%
        total = sum(percentages.values())
        assert abs(total - 100.0) < 0.01


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
