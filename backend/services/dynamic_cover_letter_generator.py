#!/usr/bin/env python3
"""
Dynamic Cover Letter Generator
Combines URL scraping with LEGO template system for personalized cover letters
"""

from typing import Dict
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.company_info_extractor import extract_company_info_from_url
from templates.cover_letter_template import generate_tailored_cover_letter

logger = logging.getLogger(__name__)

class DynamicCoverLetterGenerator:
    """Generates cover letters with dynamic company information from job URLs"""
    
    def generate_from_url(self, job_url: str, job_data: dict = None) -> str:
        """Generate cover letter by extracting company info from job URL"""
        try:
            # Extract company information from URL
            company_info = extract_company_info_from_url(job_url)
            logger.info(f"Extracted company info: {company_info['company_name']}")
            
            # Prepare job data
            if job_data is None:
                job_data = {
                    'title': 'Software Developer',
                    'company': company_info['company_name'],
                    'description': ''
                }
            
            # Update job data with extracted company name
            job_data['company'] = company_info['company_name']
            
            # Generate tailored cover letter
            cover_letter = generate_tailored_cover_letter(job_data, company_info)
            
            return cover_letter
            
        except Exception as e:
            logger.error(f"Failed to generate dynamic cover letter: {e}")
            # Fallback to standard template
            return generate_tailored_cover_letter(job_data or {})
    
    def preview_company_info(self, job_url: str) -> Dict[str, str]:
        """Preview what company information would be extracted from URL"""
        return extract_company_info_from_url(job_url)

# Global instance for easy access
dynamic_generator = DynamicCoverLetterGenerator()

def generate_dynamic_cover_letter(job_url: str, job_data: dict = None) -> str:
    """Main function to generate dynamic cover letter from job URL"""
    return dynamic_generator.generate_from_url(job_url, job_data)

def preview_extracted_info(job_url: str) -> Dict[str, str]:
    """Preview company information that would be extracted from URL"""
    return dynamic_generator.preview_company_info(job_url)