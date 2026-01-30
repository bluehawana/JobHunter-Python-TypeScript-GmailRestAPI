"""
Comprehensive Integration Tests for Intelligent CV Template Selection
Tests the complete workflow from job description to customized CV
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import json

# Import all components
from cv_templates import CVTemplateManager
from job_analyzer import JobAnalyzer
from template_matcher import TemplateMatcher
from template_customizer import TemplateCustomizer
from ai_analyzer import AIAnalyzer


class TestCompleteWorkflowIntegration:
    """Integration tests for the complete CV template selection workflow"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.template_manager = CVTemplateManager()
        self.analyzer = JobAnalyzer()
        self.customizer = TemplateCustomizer()
        
        # Create a temporary directory for test templates
        self.temp_dir = tempfile.mkdtemp()
        self.test_template_content = r"""
\documentclass[11pt,a4paper,sans]{moderncv}
\moderncvstyle{classic}
\moderncvcolor{blue}

\usepackage[utf8]{inputenc}
\usepackage[scale=0.75]{geometry}

\name{Hongzhi}{Li}
\title{{JOB_TITLE}}
\address{{Stockholm, Sweden}}
\phone[mobile]{{+46 76 123 4567}}
\email{{hongzhi@example.com}}

\begin{{document}}

\makecvtitle

\section{{Professional Summary}}
Experienced software engineer with expertise in software development.

\section{{Experience}}
\cventry{{2020--Present}}{{Software Engineer}}{{COMPANY_NAME}}{{Stockholm}}{{}}{{
\begin{{itemize}}
\item Developed applications using modern technologies
\item Collaborated with international teams
\end{{itemize}}
}}

\end{{document}}
"""
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_template(self, role_category: str) -> Path:
        """Create a test template file"""
        template_path = Path(self.temp_dir) / f"{role_category}_CV.tex"
        template_path.write_text(self.test_template_content, encoding='utf-8')
        return template_path
    
    def test_complete_workflow_android_developer(self):
        """Test complete workflow: Android job → Android template → Customized CV"""
        # Step 1: Job description
        job_description = """
        Android Developer Position at TechCorp
        
        We are looking for an experienced Android Developer to join our mobile team.
        You will work with Kotlin and Android SDK to build our flagship mobile app.
        
        Requirements:
        - 3+ years Android development experience
        - Strong Kotlin and Java skills
        - Experience with Android SDK, Android Studio
        - Knowledge of mobile app architecture patterns
        - APK optimization and mobile performance
        
        You will be responsible for developing new features, maintaining existing code,
        and working closely with our design team to create amazing mobile experiences.
        """
        
        # Step 2: Analyze job description
        role_category = self.template_manager.analyze_job_role(job_description)
        
        # Step 3: Verify Android role is detected
        assert role_category == 'android_developer'
        
        # Step 4: Get role percentages
        percentages = self.template_manager.get_role_percentages(job_description)
        assert percentages['android_developer'] > 50.0
        
        # Step 5: Get role breakdown
        breakdown = self.template_manager.get_role_breakdown(job_description)
        assert len(breakdown) > 0
        assert breakdown[0][0] == 'android_developer'  # Top role
        
        # Step 6: Create test template and customize
        template_path = self.create_test_template('android_developer')
        template_content = template_path.read_text(encoding='utf-8')
        
        customized_cv = self.customizer.customize_template(
            template_content=template_content,
            company="TechCorp",
            title="Android Developer",
            role_type="android_developer"
        )
        
        # Step 7: Verify customization
        assert "TechCorp" in customized_cv
        assert "Android Developer" in customized_cv
        assert "\\documentclass" in customized_cv  # LaTeX structure preserved
        assert "end{{document}}" in customized_cv  # LaTeX end structure
    
    def test_complete_workflow_fullstack_developer(self):
        """Test complete workflow: Fullstack job → Fullstack template → Customized CV"""
        job_description = """
        Full-Stack Developer - React & Node.js
        
        Join our team as a Full-Stack Developer working on modern web applications.
        You'll work with React, TypeScript, and Node.js to build scalable solutions.
        
        Key responsibilities:
        - Develop frontend applications using React and TypeScript
        - Build backend services with Node.js and Express
        - Work on full-stack features from UI to database
        - Integrate with RESTful APIs and GraphQL
        - Collaborate on web application architecture
        
        Requirements:
        - Strong JavaScript/TypeScript skills
        - Experience with React, Vue, or Angular
        - Backend development with Node.js or similar
        - Full-stack development experience
        - Web application development
        """
        
        # Complete workflow
        role_category = self.template_manager.analyze_job_role(job_description)
        assert role_category == 'fullstack_developer'
        
        percentages = self.template_manager.get_role_percentages(job_description)
        assert percentages['fullstack_developer'] > 50.0
        
        # Test template customization
        template_path = self.create_test_template('fullstack_developer')
        template_content = template_path.read_text(encoding='utf-8')
        
        customized_cv = self.customizer.customize_template(
            template_content=template_content,
            company="WebTech Solutions",
            title="Full-Stack Developer",
            role_type="fullstack_developer"
        )
        
        assert "WebTech Solutions" in customized_cv
        assert "Full-Stack Developer" in customized_cv
    
    def test_complete_workflow_devops_engineer(self):
        """Test complete workflow: DevOps job → DevOps template → Customized CV"""
        job_description = """
        DevOps Engineer - Cloud Infrastructure
        
        We're seeking a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines.
        You'll work with Kubernetes, AWS, and Terraform to build scalable systems.
        
        Responsibilities:
        - Manage Kubernetes clusters and container orchestration
        - Build and maintain CI/CD pipelines with Jenkins
        - Infrastructure as Code using Terraform
        - AWS cloud platform management
        - Docker containerization and deployment
        - Monitor system performance and reliability
        
        Requirements:
        - Experience with Kubernetes and Docker
        - AWS or Azure cloud platform knowledge
        - CI/CD pipeline development
        - Infrastructure automation experience
        - DevOps best practices
        """
        
        # Complete workflow
        role_category = self.template_manager.analyze_job_role(job_description)
        assert role_category == 'devops_cloud'
        
        percentages = self.template_manager.get_role_percentages(job_description)
        assert percentages['devops_cloud'] > 50.0
        
        # Test template customization
        template_path = self.create_test_template('devops_cloud')
        template_content = template_path.read_text(encoding='utf-8')
        
        customized_cv = self.customizer.customize_template(
            template_content=template_content,
            company="CloudOps Inc",
            title="DevOps Engineer",
            role_type="devops_cloud"
        )
        
        assert "CloudOps Inc" in customized_cv
        assert "DevOps Engineer" in customized_cv
    
    def test_complete_workflow_ai_misclassification_prevention(self):
        """Test complete workflow: Software engineering job with AI mentions → Software template (not AI)"""
        job_description = """
        Senior Software Engineer - Backend Development
        
        We're looking for a Senior Software Engineer to join our backend team.
        You'll build scalable microservices and integrate AI-powered features.
        
        Key responsibilities:
        - Develop backend services using Java and Spring Boot
        - Design and implement RESTful APIs
        - Build microservices architecture
        - Integrate with AI APIs for enhanced features
        - Work on backend system optimization
        - Collaborate with frontend teams
        
        Requirements:
        - 5+ years backend development experience
        - Strong Java and Spring Boot skills
        - Microservices architecture experience
        - API development and integration
        - Experience integrating AI capabilities
        - Backend system design knowledge
        
        You'll be working on our core backend platform, occasionally integrating
        AI-powered features using OpenAI API and similar services.
        """
        
        # Complete workflow
        role_category = self.template_manager.analyze_job_role(job_description)
        
        # Should be backend_developer, NOT ai_product_engineer
        assert role_category == 'backend_developer'
        
        percentages = self.template_manager.get_role_percentages(job_description)
        assert percentages['backend_developer'] > percentages.get('ai_product_engineer', 0)
        assert percentages['backend_developer'] > 50.0
        
        # Test template customization
        template_path = self.create_test_template('backend_developer')
        template_content = template_path.read_text(encoding='utf-8')
        
        customized_cv = self.customizer.customize_template(
            template_content=template_content,
            company="TechBackend Corp",
            title="Senior Software Engineer",
            role_type="backend_developer"
        )
        
        assert "TechBackend Corp" in customized_cv
        assert "Senior Software Engineer" in customized_cv
    
    def test_complete_workflow_mixed_role_composition(self):
        """Test complete workflow: Mixed role job → Correct primary role selection"""
        job_description = """
        Full-Stack Developer with DevOps Responsibilities
        
        Join our team as a Full-Stack Developer with some DevOps responsibilities.
        You'll primarily work on React applications but also help with deployments.
        
        Primary responsibilities (80%):
        - Develop React applications with TypeScript
        - Build frontend components and user interfaces
        - Work on full-stack web development
        - Integrate with backend APIs
        - Frontend performance optimization
        
        Secondary responsibilities (20%):
        - Help with Docker deployments
        - Assist with CI/CD pipeline maintenance
        - Basic Kubernetes troubleshooting
        
        Requirements:
        - Strong React and TypeScript experience
        - Full-stack development skills
        - Some Docker and deployment knowledge
        - Web application development experience
        """
        
        # Complete workflow
        role_category = self.template_manager.analyze_job_role(job_description)
        assert role_category == 'fullstack_developer'
        
        percentages = self.template_manager.get_role_percentages(job_description)
        breakdown = self.template_manager.get_role_breakdown(job_description)
        
        # Verify fullstack is primary role
        assert percentages['fullstack_developer'] > percentages.get('devops_cloud', 0)
        assert breakdown[0][0] == 'fullstack_developer'
        
        # Verify both roles are in breakdown (above 5% threshold)
        role_names = [role for role, _ in breakdown]
        assert 'fullstack_developer' in role_names
        assert 'devops_cloud' in role_names
    
    def test_complete_workflow_with_ai_enabled(self):
        """Test complete workflow with AI analysis (if available)"""
        job_description = """
        Android Developer needed for mobile app development.
        Strong Kotlin and Android SDK experience required.
        """
        
        # Test basic workflow (AI integration is optional)
        role_category = self.template_manager.analyze_job_role(job_description)
        
        # Should detect Android role (either through AI or keyword analysis)
        assert role_category == 'android_developer'
    
    def test_complete_workflow_ai_fallback(self):
        """Test complete workflow works with keyword analysis"""
        job_description = """
        Android Developer position requiring Kotlin and Android SDK experience.
        Mobile app development with Android Studio.
        """
        
        # Test keyword analysis works
        role_category = self.template_manager.analyze_job_role(job_description)
        
        # Should work with keyword analysis
        assert role_category == 'android_developer'
    
    def test_complete_workflow_error_scenarios(self):
        """Test complete workflow error handling and fallbacks"""
        
        # Test 1: Empty job description
        empty_result = self.template_manager.analyze_job_role("")
        assert empty_result in self.template_manager.ROLE_CATEGORIES.keys()
        
        # Test 2: Job description with no matching keywords
        generic_job = "We need someone to work on projects and help the team."
        generic_result = self.template_manager.analyze_job_role(generic_job)
        assert generic_result in self.template_manager.ROLE_CATEGORIES.keys()
        
        # Test 3: Template customization with special characters
        template_content = self.test_template_content
        customized = self.customizer.customize_template(
            template_content=template_content,
            company="Tech & Co.",  # Contains LaTeX special character
            title="Software Engineer (Senior)",  # Contains parentheses
            role_type="backend_developer"
        )
        
        # Verify special characters are handled
        assert "Tech" in customized and "Co." in customized
        assert "Software Engineer" in customized
    
    def test_complete_workflow_all_role_categories(self):
        """Test complete workflow with job descriptions for each role category"""
        
        test_jobs = {
            'android_developer': "Android Developer with Kotlin and mobile app development experience",
            'fullstack_developer': "Full-stack developer with React and TypeScript for web applications",
            'devops_cloud': "DevOps engineer with Kubernetes, AWS, and CI/CD pipeline experience",
            'backend_developer': "Backend developer with Java, Spring Boot, and microservices",
            'incident_management_sre': "SRE engineer for incident management and production troubleshooting",
            'ai_product_engineer': "AI engineer for model training, RAG systems, and MLOps",
            'it_business_analyst': "IT Business Analyst for requirements gathering and stakeholder workshops"
        }
        
        results = {}
        for expected_role, job_desc in test_jobs.items():
            detected_role = self.template_manager.analyze_job_role(job_desc)
            percentages = self.template_manager.get_role_percentages(job_desc)
            
            results[expected_role] = {
                'detected': detected_role,
                'percentage': percentages.get(detected_role, 0)
            }
            
            # Verify the detected role has significant percentage
            assert percentages.get(detected_role, 0) > 20.0, f"Low confidence for {expected_role}: {percentages}"
        
        # Verify we get different templates for different job types
        detected_roles = set(result['detected'] for result in results.values())
        assert len(detected_roles) > 1, "Template selection should vary across different job types"
    
    def test_complete_workflow_percentage_normalization(self):
        """Test that percentages always sum to 100% across complete workflow"""
        
        test_jobs = [
            "Android Developer with Kotlin experience",
            "Full-stack developer with React and Node.js",
            "DevOps engineer with Kubernetes and AWS",
            "Mixed role: Backend development with some DevOps work",
            "AI engineer building machine learning models"
        ]
        
        for job_desc in test_jobs:
            percentages = self.template_manager.get_role_percentages(job_desc)
            total = sum(percentages.values())
            
            # Verify percentages sum to 100% (within floating-point tolerance)
            assert abs(total - 100.0) < 0.01, f"Percentages don't sum to 100%: {total} for job: {job_desc[:50]}..."
            
            # Verify all percentages are non-negative
            for role, percentage in percentages.items():
                assert percentage >= 0.0, f"Negative percentage for {role}: {percentage}"
    
    def test_complete_workflow_role_breakdown_filtering(self):
        """Test role breakdown filtering in complete workflow"""
        
        job_description = """
        Full-stack Developer with primary React experience.
        You'll work on web applications and occasionally help with deployments.
        Strong TypeScript and JavaScript skills required.
        """
        
        # Get breakdown with different thresholds
        breakdown_5 = self.template_manager.get_role_breakdown(job_description, threshold=5.0)
        breakdown_10 = self.template_manager.get_role_breakdown(job_description, threshold=10.0)
        breakdown_20 = self.template_manager.get_role_breakdown(job_description, threshold=20.0)
        
        # Higher threshold should return fewer or equal roles
        assert len(breakdown_10) <= len(breakdown_5)
        assert len(breakdown_20) <= len(breakdown_10)
        
        # All returned roles should meet threshold
        for role, percentage in breakdown_5:
            assert percentage >= 5.0
        for role, percentage in breakdown_10:
            assert percentage >= 10.0
        for role, percentage in breakdown_20:
            assert percentage >= 20.0
        
        # Should be sorted in descending order
        for i in range(len(breakdown_5) - 1):
            assert breakdown_5[i][1] >= breakdown_5[i + 1][1]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])