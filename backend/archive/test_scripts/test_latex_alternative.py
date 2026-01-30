#!/usr/bin/env python3
"""
Test version of LaTeX service that creates mock PDFs for testing
"""
import sys
import os
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent))

from app.services.latex_resume_service import LaTeXResumeService
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MockLaTeXResumeService(LaTeXResumeService):
    """Mock LaTeX service for testing without requiring LaTeX installation"""
    
    async def _compile_latex_to_pdf(self, latex_content: str, filename: str) -> bytes:
        """Mock PDF compilation - returns dummy PDF content"""
        try:
            # Create a simple mock PDF content
            pdf_header = b'%PDF-1.4\n'
            pdf_content = f"""
Mock PDF: {filename}
Generated: {datetime.now()}

LaTeX Content Preview:
{latex_content[:500]}...

This is a mock PDF for testing purposes.
In production, this would be a real PDF generated from LaTeX.
""".encode('utf-8')
            
            # Return mock PDF (simplified format)
            return pdf_header + pdf_content
            
        except Exception as e:
            logger.error(f"Error creating mock PDF: {e}")
            return b"Mock PDF Generation Failed"

async def test_mock_latex_service():
    """Test the mock LaTeX service"""
    try:
        logger.info("Testing Mock LaTeX Service...")
        
        # Initialize mock service
        service = MockLaTeXResumeService()
        
        # Create test job data
        test_job = {
            'title': 'Senior Fullstack Developer',
            'company': 'TechCorp',
            'location': 'Gothenburg, Sweden',
            'description': 'We are looking for a senior fullstack developer with experience in Java, Spring Boot, React, and AWS.',
            'keywords': ['java', 'spring boot', 'react', 'aws', 'microservices'],
            'job_type': 'fulltime',
            'remote_option': True
        }
        
        # Generate CV
        logger.info("Generating mock CV...")
        cv_pdf = await service.generate_customized_cv(test_job)
        logger.info(f"CV generated: {len(cv_pdf)} bytes")
        
        # Generate cover letter
        logger.info("Generating mock cover letter...")
        cl_pdf = await service.generate_customized_cover_letter(test_job)
        logger.info(f"Cover letter generated: {len(cl_pdf)} bytes")
        
        # Save mock PDFs for inspection
        with open('mock_cv.pdf', 'wb') as f:
            f.write(cv_pdf)
        with open('mock_cover_letter.pdf', 'wb') as f:
            f.write(cl_pdf)
        
        logger.info("Mock PDFs saved: mock_cv.pdf, mock_cover_letter.pdf")
        logger.info("Mock LaTeX service test completed successfully!")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing mock LaTeX service: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_mock_latex_service())