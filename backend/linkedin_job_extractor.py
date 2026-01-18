#!/usr/bin/env python3
"""
LinkedIn Job Information Extractor
Extracts company name and job title from LinkedIn job URLs using webFetch
"""

import re
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class LinkedInJobExtractor:
    """Extract job information from LinkedIn job URLs"""
    
    def __init__(self):
        pass
    
    def extract_job_info_from_content(self, content: str, url: str) -> Dict[str, str]:
        """
        Extract company name and job title from LinkedIn job page content
        
        Args:
            content: HTML content from LinkedIn job page
            url: Original LinkedIn URL for reference
            
        Returns:
            Dictionary with 'company', 'title', and 'success' keys
        """
        try:
            logger.info(f"Extracting job info from LinkedIn content")
            
            # Extract company name and job title from content
            company = self._extract_company_name(content)
            title = self._extract_job_title(content)
            
            if company and title:
                logger.info(f"Successfully extracted: {title} at {company}")
                return {
                    'company': company,
                    'title': title,
                    'success': True,
                    'source': 'linkedin_extraction'
                }
            else:
                logger.warning(f"Could not extract complete job info. Company: {company}, Title: {title}")
                return self._create_fallback_response(company, title)
                
        except Exception as e:
            logger.error(f"Error extracting LinkedIn job info: {e}")
            return self._create_error_response(f"Extraction error: {str(e)}")
    
    def _extract_company_name(self, content: str) -> Optional[str]:
        """Extract company name from LinkedIn job page content"""
        
        # Method 1: Look for "at Company" patterns
        patterns = [
            r'at\s+([A-Z][a-zA-Z\s&.-]+?)(?:\s+you will|\s+we|\s+our|\s+is|\s+in\s+|\.|\n)',
            r'team at\s+([A-Z][a-zA-Z\s&.-]+?)(?:\s+you will|\s+we|\s+our|\s+is|\s+in\s+|\.|\n)',
            r'join\s+([A-Z][a-zA-Z\s&.-]+?)(?:\s+as|\s+team|\s+and|\s+to|\s+in\s+|\.|\n)',
            r'([A-Z][a-zA-Z\s&.-]+?)\s+(?:development teams|team|is looking|seeks|hiring)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                company = match.strip()
                # Filter out common false positives
                if (len(company) > 2 and len(company) < 50 and 
                    not any(word in company.lower() for word in ['software', 'engineer', 'developer', 'position', 'role', 'job', 'the', 'our', 'your'])):
                    return company
        
        # Method 2: Look for specific company names in content
        known_companies = [
            'Meltwater', 'Volvo', 'Spotify', 'Ericsson', 'IKEA', 'H&M', 'Klarna', 
            'King', 'Mojang', 'Skype', 'Telia', 'Electrolux', 'ABB', 'Sandvik',
            'Atlas Copco', 'Hexagon', 'Autoliv', 'SKF', 'Alfa Laval', 'Getinge',
            'Husqvarna', 'Epiroc', 'Boliden', 'SSAB', 'Essity', 'SCA', 'Kinnevik',
            'Investor AB', 'Wallenberg', 'Nordea', 'SEB', 'Swedbank', 'Handelsbanken'
        ]
        
        content_lower = content.lower()
        for company in known_companies:
            if company.lower() in content_lower:
                return company
        
        return None
    
    def _extract_job_title(self, content: str) -> Optional[str]:
        """Extract job title from LinkedIn job page content"""
        
        # Method 1: Look for "As a [Title]" patterns
        title_patterns = [
            r'As a\s+([A-Z][a-zA-Z\s&.-]+?)\s+(?:with|at|you will|in)',
            r'(?:seeking|looking for|hiring)\s+(?:a\s+)?([A-Z][a-zA-Z\s&.-]+?)(?:\s+to|\s+with|\s+at|\s+in)',
            r'([A-Z][a-zA-Z\s&.-]+?)\s+(?:position|role|opportunity)(?:\s+at|\s+with|\s+in)',
            r'join.*as\s+(?:a\s+)?([A-Z][a-zA-Z\s&.-]+?)(?:\s+to|\s+with|\s+at|\s+in)'
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                title = match.strip()
                # Filter for reasonable job titles
                if (len(title) > 5 and len(title) < 50 and 
                    any(word in title.lower() for word in ['engineer', 'developer', 'analyst', 'manager', 'specialist', 'architect', 'lead', 'senior', 'junior'])):
                    return title
        
        # Method 2: Look for common job titles directly
        job_titles = [
            'Software Engineer', 'Backend Developer', 'Frontend Developer', 
            'Fullstack Developer', 'DevOps Engineer', 'Cloud Engineer',
            'Senior Software Engineer', 'Senior Developer', 'Lead Developer',
            'Principal Engineer', 'Staff Engineer', 'Engineering Manager',
            'Product Manager', 'Data Engineer', 'Data Scientist',
            'Machine Learning Engineer', 'AI Engineer', 'Platform Engineer'
        ]
        
        content_lower = content.lower()
        for title in job_titles:
            if title.lower() in content_lower:
                return title
        
        return None
    
    def _create_error_response(self, error_message: str) -> Dict[str, str]:
        """Create error response with fallback values"""
        return {
            'company': 'Technology Company',
            'title': 'Software Engineer',
            'success': False,
            'error': error_message,
            'source': 'fallback'
        }
    
    def _create_fallback_response(self, company: Optional[str], title: Optional[str]) -> Dict[str, str]:
        """Create response with partial extraction"""
        return {
            'company': company or 'Technology Company',
            'title': title or 'Software Engineer',
            'success': bool(company and title),
            'source': 'partial_extraction'
        }


def extract_linkedin_job_info_from_content(content: str, url: str = "") -> Dict[str, str]:
    """
    Convenience function to extract job info from LinkedIn content
    
    Args:
        content: LinkedIn job page content
        url: Original URL for reference
        
    Returns:
        Dictionary with company, title, and success information
    """
    extractor = LinkedInJobExtractor()
    return extractor.extract_job_info_from_content(content, url)


# Test the extractor with sample content
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # Test with sample Meltwater content
    sample_content = """
    As a Software Engineer with the information retrieval team at Meltwater you will be building 
    petabyte-scale search and analytics systems using Elasticsearch running on AWS. Every day, 
    we add 1.3B new documents into our search platform and process over 6B engagement activities 
    to provide the most complete dataset possible.
    """
    
    print("🔍 Testing LinkedIn Job Extractor")
    print("=" * 50)
    print(f"Sample content: {sample_content[:100]}...")
    
    result = extract_linkedin_job_info_from_content(sample_content)
    
    print(f"\nResults:")
    print(f"  Company: {result['company']}")
    print(f"  Title: {result['title']}")
    print(f"  Success: {result['success']}")
    print(f"  Source: {result['source']}")
    
    if not result['success']:
        print(f"  Error: {result.get('error', 'Unknown error')}")