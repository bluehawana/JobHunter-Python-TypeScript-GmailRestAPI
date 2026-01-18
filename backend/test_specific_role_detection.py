#!/usr/bin/env python3
"""
Unit tests for specific role detection
Tests that specific job descriptions map to the correct templates

Requirements tested:
- 2.2: Android-related job → Android developer template
- 2.3: CI/CD or DevOps job → DevOps cloud template  
- 2.4: Incident management or SRE job → Incident management template
- 2.5: Full-stack development job → Full-stack developer template
"""

import pytest
from cv_templates import CVTemplateManager


class TestSpecificRoleDetection:
    """Unit tests for specific role detection mappings"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.manager = CVTemplateManager()
    
    def test_android_job_selects_android_template(self):
        """
        Test Android job → Android template
        Validates: Requirements 2.2
        """
        android_job = """
        Android Platform Developer
        
        We are looking for an Android Platform Developer to work on automotive infotainment systems.
        You will work with Kotlin, Java, and AOSP to build cutting-edge mobile experiences.
        
        Requirements:
        - Strong experience with Android SDK and Android Studio
        - Proficiency in Kotlin and Java
        - Experience with AOSP (Android Open Source Project)
        - Knowledge of automotive infotainment systems
        - Experience with Android Auto and mobile app development
        """
        
        detected_role = self.manager.analyze_job_role(android_job)
        
        assert detected_role == 'android_developer', \
            f"Android job should select 'android_developer' template, got '{detected_role}'"
    
    def test_cicd_job_selects_devops_template(self):
        """
        Test CI/CD job → DevOps template
        Validates: Requirements 2.3
        """
        cicd_job = """
        DevOps Engineer - CI/CD Pipeline Specialist
        
        We're looking for a DevOps Engineer to manage our CI/CD infrastructure.
        
        Requirements:
        - Strong experience with CI/CD pipelines
        - Jenkins, GitLab CI, or GitHub Actions
        - Docker and Kubernetes
        - AWS or Azure cloud platforms
        - Infrastructure as Code with Terraform
        - Experience with monitoring and observability tools
        """
        
        detected_role = self.manager.analyze_job_role(cicd_job)
        
        # Should select a DevOps-related template
        devops_templates = ['devops_cloud', 'devops_fintech', 'cloud_engineer', 'platform_engineer']
        assert detected_role in devops_templates, \
            f"CI/CD job should select a DevOps template, got '{detected_role}'"
    
    def test_devops_job_selects_devops_template(self):
        """
        Test DevOps job → DevOps template
        Validates: Requirements 2.3
        """
        devops_job = """
        DevOps Engineer - Cloud Infrastructure
        
        We're looking for a DevOps Engineer to manage our AWS infrastructure.
        
        Requirements:
        - AWS, Azure, or GCP experience
        - Kubernetes and Docker containerization
        - Terraform and Infrastructure as Code
        - CI/CD pipelines (Jenkins, GitHub Actions)
        - Python and Bash scripting
        - Experience with monitoring tools like Prometheus and Grafana
        """
        
        detected_role = self.manager.analyze_job_role(devops_job)
        
        # Should select a DevOps-related template
        devops_templates = ['devops_cloud', 'devops_fintech', 'cloud_engineer', 'platform_engineer']
        assert detected_role in devops_templates, \
            f"DevOps job should select a DevOps template, got '{detected_role}'"
    
    def test_sre_job_selects_incident_management_template(self):
        """
        Test SRE job → Incident Management template
        Validates: Requirements 2.4
        """
        sre_job = """
        Site Reliability Engineer (SRE)
        
        We're seeking an experienced SRE to join our platform team.
        
        Requirements:
        - Strong experience in site reliability engineering
        - Incident management and on-call responsibilities
        - Experience with monitoring and observability (Prometheus, Grafana)
        - Production support and troubleshooting
        - MTTR optimization and post-mortem analysis
        - Experience with PagerDuty or similar alerting systems
        """
        
        detected_role = self.manager.analyze_job_role(sre_job)
        
        assert detected_role == 'incident_management_sre', \
            f"SRE job should select 'incident_management_sre' template, got '{detected_role}'"
    
    def test_incident_management_job_selects_incident_management_template(self):
        """
        Test Incident Management job → Incident Management template
        Validates: Requirements 2.4
        """
        incident_job = """
        Incident Management Specialist
        
        We need an Incident Management Specialist to handle production incidents.
        
        Requirements:
        - Strong experience in incident management processes
        - On-call support and escalation procedures
        - Experience with incident response and resolution
        - Knowledge of ITIL incident management practices
        - Experience with monitoring tools and alerting systems
        - Production support experience with high-availability systems
        """
        
        detected_role = self.manager.analyze_job_role(incident_job)
        
        assert detected_role == 'incident_management_sre', \
            f"Incident Management job should select 'incident_management_sre' template, got '{detected_role}'"
    
    def test_fullstack_job_selects_fullstack_template(self):
        """
        Test Full-stack job → Full-stack template
        Validates: Requirements 2.5
        """
        fullstack_job = """
        Full-Stack Developer
        
        We're looking for a Full-Stack Developer to work on our web applications.
        
        Requirements:
        - Strong experience with React and TypeScript
        - Backend development with Node.js or Python
        - Experience with RESTful APIs and microservices
        - Database experience (PostgreSQL, MongoDB)
        - Full-stack web development experience
        - Experience with modern web frameworks and tools
        """
        
        detected_role = self.manager.analyze_job_role(fullstack_job)
        
        assert detected_role == 'fullstack_developer', \
            f"Full-stack job should select 'fullstack_developer' template, got '{detected_role}'"
    
    def test_fullstack_with_explicit_keywords_selects_fullstack_template(self):
        """
        Test Full-stack job with explicit keywords → Full-stack template
        Validates: Requirements 2.5
        """
        fullstack_explicit_job = """
        Fullstack Software Engineer
        
        We need a fullstack engineer for frontend and backend development.
        
        Requirements:
        - Frontend: React, Vue.js, or Angular
        - Backend: Python, Java, or Node.js
        - Full-stack development experience
        - Experience building web applications end-to-end
        - RESTful API development
        - Database design and optimization
        """
        
        detected_role = self.manager.analyze_job_role(fullstack_explicit_job)
        
        assert detected_role == 'fullstack_developer', \
            f"Explicit fullstack job should select 'fullstack_developer' template, got '{detected_role}'"


if __name__ == '__main__':
    # Run the tests
    pytest.main([__file__, '-v'])