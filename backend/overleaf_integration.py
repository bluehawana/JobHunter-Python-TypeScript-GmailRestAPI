#!/usr/bin/env python3
"""
Overleaf Integration for Job Automation System
Generates LaTeX resumes and provides Overleaf URLs for perfect compilation
"""
import os
import logging
from typing import Dict, Any
from overleaf_pdf_generator import OverleafPDFGenerator

logger = logging.getLogger(__name__)

class OverleafIntegration:
    def __init__(self):
        self.generator = OverleafPDFGenerator()
        self.base_url = os.getenv('LATEX_SERVER_URL', 'https://jobs.bluehawana.com')
    
    def create_resume_with_overleaf_url(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create resume and return both PDF content and Overleaf URL
        Perfect for job automation - gives you both options!
        """
        try:
            company = job.get('company', 'company').lower().replace(' ', '_')
            job_title = job.get('title', 'position').lower().replace(' ', '_')
            
            # Generate LaTeX content with LEGO intelligence
            latex_content = self.generator._generate_latex_content(job)
            
            # Generate local PDF for immediate use
            pdf_content = self.generator._compile_latex_locally(latex_content)
            
            # Create filename for potential upload
            import time
            timestamp = int(time.time())
            filename = f"resume_{company}_{job_title}_{timestamp}.tex"
            
            # Simulate Overleaf URL (you would upload to your server)
            latex_url = f"{self.base_url}/latex/{filename}"
            overleaf_url = f"https://www.overleaf.com/docs?snip_uri={latex_url}"
            
            result = {
                'pdf_content': pdf_content,
                'latex_content': latex_content,
                'latex_url': latex_url,
                'overleaf_url': overleaf_url,
                'filename': filename,
                'company': job.get('company', 'Unknown'),
                'job_title': job.get('title', 'Unknown'),
                'pdf_size': len(pdf_content) if pdf_content else 0,
                'latex_size': len(latex_content),
                'success': bool(pdf_content)
            }
            
            logger.info(f"✅ Created resume for {company} - PDF: {len(pdf_content)} bytes, LaTeX: {len(latex_content)} chars")
            logger.info(f"🔗 Overleaf URL: {overleaf_url}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error creating resume with Overleaf integration: {e}")
            return {
                'pdf_content': b'',
                'latex_content': '',
                'latex_url': '',
                'overleaf_url': '',
                'filename': '',
                'company': job.get('company', 'Unknown'),
                'job_title': job.get('title', 'Unknown'),
                'pdf_size': 0,
                'latex_size': 0,
                'success': False,
                'error': str(e)
            }
    
    def save_latex_for_overleaf(self, latex_content: str, filename: str) -> str:
        """Save LaTeX file locally and return path for serving"""
        try:
            # Create latex directory if it doesn't exist
            latex_dir = os.path.join(os.path.dirname(__file__), 'latex_files')
            os.makedirs(latex_dir, exist_ok=True)
            
            # Save LaTeX file
            file_path = os.path.join(latex_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            logger.info(f"💾 Saved LaTeX file: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"❌ Error saving LaTeX file: {e}")
            return ""

# Integration with your existing beautiful_pdf_generator.py
def create_beautiful_multi_page_pdf_with_overleaf(job: dict, latex_content: str = "") -> Dict[str, Any]:
    """
    Enhanced version that returns both PDF and Overleaf URL
    Drop-in replacement for your existing function
    """
    integration = OverleafIntegration()
    result = integration.create_resume_with_overleaf_url(job)
    
    # For backward compatibility, return PDF content as primary result
    # But also include Overleaf URL in logs/metadata
    if result['success']:
        logger.info(f"🎯 BONUS: Open in Overleaf: {result['overleaf_url']}")
        logger.info(f"📝 LaTeX file available at: {result['latex_url']}")
    
    return result['pdf_content']

if __name__ == "__main__":
    # Test the integration
    test_job = {
        'title': 'Senior Backend Developer',
        'company': 'Klarna',
        'description': 'Java, Spring Boot, microservices, Kubernetes, PostgreSQL, API development'
    }
    
    integration = OverleafIntegration()
    result = integration.create_resume_with_overleaf_url(test_job)
    
    print(f"✅ Success: {result['success']}")
    print(f"📄 PDF Size: {result['pdf_size']} bytes")
    print(f"📝 LaTeX Size: {result['latex_size']} characters")
    print(f"🔗 Overleaf URL: {result['overleaf_url']}")
    
    if result['pdf_content']:
        with open('test_klarna_resume.pdf', 'wb') as f:
            f.write(result['pdf_content'])
        print("💾 Saved test_klarna_resume.pdf")
    
    if result['latex_content']:
        with open('test_klarna_resume.tex', 'w') as f:
            f.write(result['latex_content'])
        print("💾 Saved test_klarna_resume.tex")
        print(f"🚀 Try: https://www.overleaf.com/docs?snip_uri=https://raw.githubusercontent.com/yourusername/yourrepo/main/test_klarna_resume.tex")