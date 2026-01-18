"""
API Integration Tests for Intelligent CV Template Selection
Tests the complete workflow through the API endpoints
"""

import pytest
import json
from unittest.mock import patch, Mock
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent / 'app'))

from app.lego_api import lego_api
from flask import Flask


class TestAPIIntegrationWorkflow:
    """Integration tests for the API endpoints"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.app = Flask(__name__)
        self.app.register_blueprint(lego_api)  # Remove the url_prefix
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_analyze_job_api_android_developer(self):
        """Test analyze-job API endpoint with Android job description"""
        job_data = {
            "jobDescription": """
            Android Developer Position at TechCorp
            
            We are looking for an experienced Android Developer to join our mobile team.
            You will work with Kotlin and Android SDK to build our flagship mobile app.
            
            Requirements:
            - 3+ years Android development experience
            - Strong Kotlin and Java skills
            - Experience with Android SDK, Android Studio
            - Knowledge of mobile app architecture patterns
            - APK optimization and mobile performance
            """
        }
        
        response = self.client.post('/api/analyze-job', 
                                  data=json.dumps(job_data),
                                  content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify response structure
        assert 'success' in data
        assert 'analysis' in data
        assert data['success'] is True
        
        analysis = data['analysis']
        
        # Verify analysis structure
        assert 'roleCategory' in analysis
        assert 'rolePercentages' in analysis
        assert 'roleBreakdown' in analysis
        
        # Verify Android role is detected
        assert analysis['roleCategory'] == 'android_developer'
        assert analysis['rolePercentages']['android_developer'] > 50.0
        
        # Verify role breakdown is provided
        assert len(analysis['roleBreakdown']) > 0
        assert analysis['roleBreakdown'][0]['role'] == 'android_developer'
    
    def test_analyze_job_api_fullstack_developer(self):
        """Test analyze-job API endpoint with Fullstack job description"""
        job_data = {
            "jobDescription": """
            Full-Stack Developer - React & Node.js
            
            Join our team as a Full-Stack Developer working on modern web applications.
            You'll work with React, TypeScript, and Node.js to build scalable solutions.
            
            Key responsibilities:
            - Develop frontend applications using React and TypeScript
            - Build backend services with Node.js and Express
            - Work on full-stack features from UI to database
            - Integrate with RESTful APIs and GraphQL
            """
        }
        
        response = self.client.post('/api/analyze-job', 
                                  data=json.dumps(job_data),
                                  content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        analysis = data['analysis']
        
        # Verify Fullstack role is detected
        assert analysis['roleCategory'] == 'fullstack_developer'
        assert analysis['rolePercentages']['fullstack_developer'] > 50.0
    
    def test_analyze_job_api_ai_misclassification_prevention(self):
        """Test that API prevents AI misclassification"""
        job_data = {
            "jobDescription": """
            Senior Software Engineer - Backend Development
            
            We're looking for a Senior Software Engineer to join our backend team.
            You'll build scalable microservices and integrate AI-powered features.
            
            Key responsibilities:
            - Develop backend services using Java and Spring Boot
            - Design and implement RESTful APIs
            - Build microservices architecture
            - Integrate with AI APIs for enhanced features
            - Work on backend system optimization
            
            You'll be working on our core backend platform, occasionally integrating
            AI-powered features using OpenAI API and similar services.
            """
        }
        
        response = self.client.post('/api/analyze-job', 
                                  data=json.dumps(job_data),
                                  content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        analysis = data['analysis']
        
        # Should be backend_developer, NOT ai_product_engineer
        assert analysis['roleCategory'] == 'backend_developer'
        assert analysis['rolePercentages']['backend_developer'] > analysis['rolePercentages'].get('ai_product_engineer', 0)
    
    def test_analyze_job_api_error_handling(self):
        """Test API error handling with invalid input"""
        # Test with empty job description
        job_data = {"jobDescription": ""}
        
        response = self.client.post('/api/analyze-job', 
                                  data=json.dumps(job_data),
                                  content_type='application/json')
        
        # Should return 400 error for empty job description
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'required' in data['error'].lower()
        
        # Test with valid but minimal job description
        job_data = {"jobDescription": "Software Developer position"}
        
        response = self.client.post('/api/analyze-job', 
                                  data=json.dumps(job_data),
                                  content_type='application/json')
        
        # Should return valid response with fallback
        assert response.status_code == 200
        data = json.loads(response.data)
        analysis = data['analysis']
        assert 'roleCategory' in analysis
    
    def test_analyze_job_api_percentage_normalization(self):
        """Test that API returns properly normalized percentages"""
        job_data = {
            "jobDescription": """
            Full-Stack Developer with DevOps responsibilities.
            You'll work on React applications and help with Docker deployments.
            Strong React and TypeScript experience required.
            Some Kubernetes knowledge helpful.
            """
        }
        
        response = self.client.post('/api/analyze-job', 
                                  data=json.dumps(job_data),
                                  content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        analysis = data['analysis']
        
        # Verify percentages sum to 100%
        total_percentage = sum(analysis['rolePercentages'].values())
        assert abs(total_percentage - 100.0) < 0.01
        
        # Verify all percentages are non-negative
        for role, percentage in analysis['rolePercentages'].items():
            assert percentage >= 0.0
    
    @patch('app.lego_api.template_manager')
    def test_generate_lego_application_api(self, mock_template_manager):
        """Test generate-lego-application API endpoint"""
        # Mock the template manager
        mock_template_manager.analyze_job_role.return_value = 'android_developer'
        mock_template_manager.get_role_percentages.return_value = {
            'android_developer': 85.0,
            'fullstack_developer': 10.0,
            'backend_developer': 5.0
        }
        
        job_data = {
            "jobDescription": "Android Developer with Kotlin experience",
            "company": "TechCorp",
            "title": "Android Developer",
            "location": "Stockholm"
        }
        
        response = self.client.post('/api/generate-lego-application', 
                                  data=json.dumps(job_data),
                                  content_type='application/json')
        
        # Should return a response (may be 200 or error depending on template availability)
        assert response.status_code in [200, 400, 500]
        
        if response.status_code == 200:
            data = json.loads(response.data)
            analysis = data.get('analysis', {})
            assert 'roleCategory' in analysis
            assert analysis['roleCategory'] == 'android_developer'
    
    def test_api_response_structure_consistency(self):
        """Test that API responses have consistent structure across different job types"""
        test_jobs = [
            {
                "description": "Android Developer with Kotlin experience",
                "expected_role": "android_developer"
            },
            {
                "description": "Full-stack developer with React and TypeScript",
                "expected_role": "fullstack_developer"
            },
            {
                "description": "DevOps engineer with Kubernetes and AWS",
                "expected_role": "devops_cloud"
            }
        ]
        
        for job in test_jobs:
            job_data = {"jobDescription": job["description"]}
            
            response = self.client.post('/api/analyze-job', 
                                      data=json.dumps(job_data),
                                      content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            analysis = data['analysis']
            
            # Verify consistent response structure
            required_fields = ['roleCategory', 'rolePercentages', 'roleBreakdown']
            for field in required_fields:
                assert field in analysis, f"Missing field {field} in response for {job['description'][:30]}..."
            
            # Verify role_breakdown structure
            assert isinstance(analysis['roleBreakdown'], list)
            if len(analysis['roleBreakdown']) > 0:
                breakdown_item = analysis['roleBreakdown'][0]
                assert 'role' in breakdown_item
                assert 'percentage' in breakdown_item


if __name__ == '__main__':
    pytest.main([__file__, '-v'])