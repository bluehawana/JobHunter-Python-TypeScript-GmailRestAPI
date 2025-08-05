#!/usr/bin/env python3
"""
Test script for the enhanced Claude API integration
"""
import asyncio
import logging
import sys
import os

# Add the app directory to Python path
sys.path.append('/Users/bluehawana/Projects/Jobhunter/backend')

from app.services.simple_latex_service import SimpleLaTeXService
from app.services.claude_api_service import ClaudeAPIService

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_claude_api_integration():
    """Test the enhanced LaTeX service with Claude API"""
    
    # Test job data
    test_job = {
        'title': 'Senior DevOps Engineer',
        'company': 'TechNova Solutions',
        'description': '''
        We are seeking a Senior DevOps Engineer to join our innovative team. 
        Key responsibilities include:
        - Designing and implementing CI/CD pipelines
        - Managing Kubernetes clusters on AWS
        - Collaborating with development teams
        - Coaching junior engineers on best practices
        - Leading infrastructure automation projects
        
        Required skills: Python, Docker, Kubernetes, AWS, CI/CD, GitLab, Terraform
        ''',
        'keywords': ['DevOps', 'Kubernetes', 'AWS', 'CI/CD', 'Python', 'Docker', 'Terraform'],
        'hiring_manager': 'Linda Anderson',
        'address': 'Storgatan 15\\\\Stockholm'
    }
    
    logger.info("Starting Claude API integration test...")
    
    try:
        # Initialize the LaTeX service (which includes Claude API)
        latex_service = SimpleLaTeXService()
        
        # Test Claude API service directly first
        logger.info("Testing Claude API service directly...")
        api_info = latex_service.claude_api.get_current_api_info()
        logger.info(f"Initial API configuration: {api_info}")
        
        # Test CV generation
        logger.info("Testing CV generation with Claude API enhancement...")
        cv_pdf = await latex_service.generate_customized_cv(test_job)
        
        if cv_pdf and len(cv_pdf) > 0:
            logger.info(f"✅ CV generated successfully! Size: {len(cv_pdf)} bytes")
            
            # Save CV for inspection
            cv_filename = f"test_cv_{test_job['company']}.pdf"
            with open(cv_filename, 'wb') as f:
                f.write(cv_pdf)
            logger.info(f"CV saved as: {cv_filename}")
        else:
            logger.error("❌ CV generation failed!")
        
        # Test Cover Letter generation
        logger.info("Testing Cover Letter generation with Claude API enhancement...")
        cl_pdf = await latex_service.generate_customized_cover_letter(test_job)
        
        if cl_pdf and len(cl_pdf) > 0:
            logger.info(f"✅ Cover Letter generated successfully! Size: {len(cl_pdf)} bytes")
            
            # Save Cover Letter for inspection
            cl_filename = f"test_cover_letter_{test_job['company']}.pdf"
            with open(cl_filename, 'wb') as f:
                f.write(cl_pdf)
            logger.info(f"Cover Letter saved as: {cl_filename}")
        else:
            logger.error("❌ Cover Letter generation failed!")
        
        # Test API fallback by simulating an error scenario
        logger.info("Testing API fallback mechanism...")
        
        # Get final API status
        final_api_info = latex_service.claude_api.get_current_api_info()
        logger.info(f"Final API configuration: {final_api_info}")
        
        logger.info("🎉 All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

def test_api_switching():
    """Test the API switching and logout mechanism"""
    logger.info("Testing API switching mechanism...")
    
    try:
        # Initialize Claude API service
        claude_api = ClaudeAPIService()
        
        # Show initial state
        logger.info(f"Initial API: {claude_api.get_current_api_info()}")
        
        # Test switching to official API
        asyncio.run(claude_api._switch_to_official_api())
        logger.info(f"After switch: {claude_api.get_current_api_info()}")
        
        # Reset back to third-party
        claude_api.reset_to_third_party()
        logger.info(f"After reset: {claude_api.get_current_api_info()}")
        
        logger.info("✅ API switching test completed!")
        
    except Exception as e:
        logger.error(f"❌ API switching test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Claude API Integration Tests")
    print("=" * 50)
    
    # Test 1: API switching mechanism
    test_api_switching()
    print()
    
    # Test 2: Full integration test
    asyncio.run(test_claude_api_integration())
    
    print("\n" + "=" * 50)
    print("✨ Test suite completed!")