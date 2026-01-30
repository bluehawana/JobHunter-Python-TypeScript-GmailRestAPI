"""
Integration Tests for JobAnalyzer + TemplateMatcher
Tests the complete workflow from job description to template selection
"""

import pytest
from job_analyzer import JobAnalyzer
from template_matcher import TemplateMatcher


class TestJobAnalyzerTemplateMatcherIntegration:
    """Integration tests for JobAnalyzer and TemplateMatcher"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.analyzer = JobAnalyzer()
        
        # Sample role categories
        self.role_categories = {
            'android_developer': {
                'keywords': ['android', 'kotlin', 'mobile', 'apk'],
                'priority': 1
            },
            'fullstack_developer': {
                'keywords': ['fullstack', 'full-stack', 'full stack', 'react', 'typescript'],
                'priority': 2
            },
            'devops_cloud': {
                'keywords': ['devops', 'kubernetes', 'aws', 'ci/cd', 'terraform'],
                'priority': 4
            },
            'backend_developer': {
                'keywords': ['backend', 'java', 'spring boot', 'microservices'],
                'priority': 3
            }
        }
        
        self.matcher = TemplateMatcher(self.role_categories)
    
    def test_complete_workflow_android_job(self):
        """Test complete workflow: Android job description → Android template"""
        job_description = """
        We are looking for an Android Developer to work on our mobile app.
        You will use Kotlin and Android SDK to build features for our APK.
        Experience with mobile development is essential.
        """
        
        # Step 1: Analyze job description
        role_indicators = self.analyzer.identify_role_indicators(
            job_description, 
            self.role_categories
        )
        
        # Step 2: Calculate scores
        scores = self.matcher.calculate_scores(role_indicators)
        
        # Step 3: Calculate percentages
        percentages = self.matcher.calculate_percentages(scores)
        
        # Step 4: Select best match
        best_role, best_score = self.matcher.select_best_match(scores)
        
        # Verify Android is selected
        assert best_role == 'android_developer'
        assert percentages['android_developer'] > 50.0
    
    def test_complete_workflow_fullstack_job(self):
        """Test complete workflow: Fullstack job description → Fullstack template"""
        job_description = """
        Full-Stack Developer needed. You will work with React and TypeScript
        on the frontend, and build backend services. Full stack experience required.
        We need someone who can handle fullstack development.
        """
        
        # Complete workflow
        role_indicators = self.analyzer.identify_role_indicators(
            job_description, 
            self.role_categories
        )
        scores = self.matcher.calculate_scores(role_indicators)
        percentages = self.matcher.calculate_percentages(scores)
        best_role, best_score = self.matcher.select_best_match(scores)
        
        # Verify Fullstack is selected
        assert best_role == 'fullstack_developer'
        assert percentages['fullstack_developer'] > 50.0
    
    def test_complete_workflow_mixed_role(self):
        """Test complete workflow: Mixed role with clear winner"""
        job_description = """
        Backend Developer position. Strong Java and Spring Boot experience required.
        You will build microservices and work with our DevOps team on Kubernetes deployments.
        Some AWS experience is helpful.
        """
        
        # Complete workflow
        role_indicators = self.analyzer.identify_role_indicators(
            job_description, 
            self.role_categories
        )
        scores = self.matcher.calculate_scores(role_indicators)
        percentages = self.matcher.calculate_percentages(scores)
        breakdown = self.matcher.get_role_breakdown(percentages)
        best_role, best_score = self.matcher.select_best_match(scores)
        
        # Verify Backend is selected (higher priority than DevOps)
        assert best_role == 'backend_developer'
        
        # Verify breakdown includes both roles
        role_keys = [role for role, _ in breakdown]
        assert 'backend_developer' in role_keys
        assert 'devops_cloud' in role_keys
        
        # Verify percentages sum to 100%
        total = sum(percentages.values())
        assert abs(total - 100.0) < 0.01
    
    def test_complete_workflow_with_multi_word_keywords(self):
        """Test complete workflow with multi-word keywords"""
        job_description = """
        We need a Full Stack Developer with CI/CD experience.
        You will work on full-stack projects and set up CI/CD pipelines.
        Spring Boot and microservices knowledge is required.
        """
        
        # Complete workflow
        role_indicators = self.analyzer.identify_role_indicators(
            job_description, 
            self.role_categories
        )
        scores = self.matcher.calculate_scores(role_indicators)
        percentages = self.matcher.calculate_percentages(scores)
        best_role, best_score = self.matcher.select_best_match(scores)
        
        # Should detect both fullstack and devops keywords
        assert 'full-stack' in role_indicators['fullstack_developer'] or \
               'full stack' in role_indicators['fullstack_developer']
        assert 'ci/cd' in role_indicators['devops_cloud']
        assert 'spring boot' in role_indicators['backend_developer']
        
        # Best match should be determined by weighted scores
        assert best_role in ['fullstack_developer', 'backend_developer', 'devops_cloud']
    
    def test_percentage_based_scoring_prevents_misclassification(self):
        """
        Test that percentage-based scoring prevents misclassification
        
        Scenario: Job is 85% backend, 15% devops
        Should select backend template, not devops
        """
        job_description = """
        Senior Backend Developer position. You will build Java microservices
        using Spring Boot. Strong Java experience required. You will design
        and implement backend APIs and work with our backend team.
        Some Kubernetes knowledge is helpful for deployments.
        """
        
        # Complete workflow
        role_indicators = self.analyzer.identify_role_indicators(
            job_description, 
            self.role_categories
        )
        scores = self.matcher.calculate_scores(role_indicators)
        percentages = self.matcher.calculate_percentages(scores)
        best_role, best_score = self.matcher.select_best_match(scores)
        
        # Verify backend is selected (not devops)
        assert best_role == 'backend_developer'
        
        # Verify backend has higher percentage than devops
        assert percentages['backend_developer'] > percentages['devops_cloud']
        
        # Verify backend is the majority
        assert percentages['backend_developer'] > 50.0
    
    def test_role_breakdown_filtering(self):
        """Test that role breakdown filters out insignificant roles"""
        job_description = """
        Fullstack Developer with React and TypeScript.
        Full-stack development experience required.
        """
        
        # Complete workflow
        role_indicators = self.analyzer.identify_role_indicators(
            job_description, 
            self.role_categories
        )
        scores = self.matcher.calculate_scores(role_indicators)
        percentages = self.matcher.calculate_percentages(scores)
        breakdown = self.matcher.get_role_breakdown(percentages, threshold=5.0)
        
        # Breakdown should only include significant roles (>5%)
        for role, percentage in breakdown:
            assert percentage >= 5.0
        
        # Should be sorted descending
        for i in range(len(breakdown) - 1):
            assert breakdown[i][1] >= breakdown[i + 1][1]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
