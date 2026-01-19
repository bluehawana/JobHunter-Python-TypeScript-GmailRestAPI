#!/usr/bin/env python3
"""
Universal Job Information Extractor
Extracts company name and job title from various job sites including LinkedIn, Omegapoint, etc.
"""

import re
from typing import Dict, Optional
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class UniversalJobExtractor:
    """Extract job information from various job sites"""
    
    def __init__(self):
        pass
    
    def extract_job_info_from_content(self, content: str, url: str) -> Dict[str, str]:
        """
        Extract company name and job title from job page content
        
        Args:
            content: HTML content from job page
            url: Original job URL for reference
            
        Returns:
            Dictionary with 'company', 'title', and 'success' keys
        """
        try:
            logger.info(f"Extracting job info from URL: {url}")
            
            # Determine the job site and use appropriate extraction method
            domain = self._get_domain(url)
            
            if 'omegapoint' in domain:
                return self._extract_omegapoint_info(content, url)
            elif 'linkedin' in domain:
                return self._extract_linkedin_info(content, url)
            else:
                # Generic extraction for other sites
                return self._extract_generic_info(content, url)
                
        except Exception as e:
            logger.error(f"Error extracting job info: {e}")
            return self._create_error_response(f"Extraction error: {str(e)}")
    
    def _get_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except:
            return ""
    
    def _extract_omegapoint_info(self, content: str, url: str) -> Dict[str, str]:
        """Extract job info specifically from Omegapoint job pages"""
        try:
            # For Omegapoint, the company is always "Omegapoint"
            company = "Omegapoint"
            
            # Extract job title from the page title or content
            title = None
            
            # Method 1: Extract from page title pattern "Job Title - Omegapoint"
            title_match = re.search(r'([^-]+?)\s*-\s*Omegapoint', content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
            
            # Method 2: Look for job title in URL
            if not title:
                url_match = re.search(r'/jobs/\d+-([^/?]+)', url)
                if url_match:
                    # Convert URL slug to readable title
                    title_slug = url_match.group(1)
                    title = title_slug.replace('-', ' ').title()
            
            # Method 3: Look for specific patterns in content
            if not title:
                patterns = [
                    r'Vi söker.*?([A-Za-z\s]+developer[A-Za-z\s]*)',
                    r'([A-Za-z\s]*developer[A-Za-z\s]*)',
                    r'([A-Za-z\s]*engineer[A-Za-z\s]*)',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        title = match.group(1).strip()
                        break
            
            if title:
                # Clean up the title
                title = re.sub(r'\s+', ' ', title).strip()
                title = title.title()  # Capitalize properly
                
                logger.info(f"Successfully extracted Omegapoint job: {title} at {company}")
                return {
                    'company': company,
                    'title': title,
                    'success': True,
                    'source': 'omegapoint_extraction'
                }
            
            # Fallback for Omegapoint
            return {
                'company': company,
                'title': 'Software Developer',
                'success': False,
                'source': 'omegapoint_fallback'
            }
            
        except Exception as e:
            logger.error(f"Error extracting Omegapoint job info: {e}")
            return self._create_error_response(f"Omegapoint extraction error: {str(e)}")
    
    def _extract_linkedin_info(self, content: str, url: str) -> Dict[str, str]:
        """Extract job info from LinkedIn (existing logic)"""
        try:
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
            return self._create_error_response(f"LinkedIn extraction error: {str(e)}")
    
    def _extract_generic_info(self, content: str, url: str) -> Dict[str, str]:
        """Generic extraction for other job sites"""
        try:
            # First, check for "Title | Company" or "Title — Company" pattern at the start
            lines = content.strip().split('\n')
            first_line = lines[0].strip() if lines else ""
            
            company = None
            title = None
            
            # Check for pipe or em-dash separator in first line
            if first_line and ('|' in first_line or '—' in first_line or ' - ' in first_line):
                for separator in [' | ', ' — ', ' - ']:
                    if separator in first_line:
                        parts = first_line.split(separator, 1)
                        if len(parts) == 2:
                            left, right = parts[0].strip(), parts[1].strip()
                            # Check which part is likely the title vs company
                            job_keywords = ['engineer', 'developer', 'architect', 'manager', 'specialist', 'analyst', 'lead', 'senior', 'consultant']
                            left_is_title = any(kw in left.lower() for kw in job_keywords)
                            right_is_title = any(kw in right.lower() for kw in job_keywords)
                            
                            if left_is_title and not right_is_title:
                                # "Infrastructure Architect | Stena Metall" pattern
                                title = left
                                company = right
                                logger.info(f"Extracted from first line: {title} at {company}")
                                return {
                                    'company': company,
                                    'title': title,
                                    'success': True,
                                    'source': 'first_line_extraction'
                                }
                            elif right_is_title and not left_is_title:
                                # "Stena Metall | Infrastructure Architect" pattern
                                company = left
                                title = right
                                logger.info(f"Extracted from first line: {title} at {company}")
                                return {
                                    'company': company,
                                    'title': title,
                                    'success': True,
                                    'source': 'first_line_extraction'
                                }
                        break
            
            # Fallback to content-based extraction
            if not company:
                company = self._extract_company_name(content)
            if not title:
                title = self._extract_job_title(content)
            
            if company and title:
                logger.info(f"Successfully extracted: {title} at {company}")
                return {
                    'company': company,
                    'title': title,
                    'success': True,
                    'source': 'generic_extraction'
                }
            else:
                return self._create_fallback_response(company, title)
        except Exception as e:
            logger.error(f"Error extracting generic job info: {e}")
            return self._create_error_response(f"Generic extraction error: {str(e)}")
    
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
        # Known companies - prioritize recruiting/staffing companies first
        known_recruiting_companies = [
            'Incluso', 'Academic Work', 'Randstad', 'Manpower', 'Adecco',
            'Jefferson Wells', 'Experis', 'TNG', 'Poolia', 'Jurek'
        ]

        known_companies = [
            'Emerson', 'Meltwater', 'Volvo', 'Spotify', 'Ericsson', 'IKEA', 'H&M', 'Klarna',
            'King', 'Mojang', 'Skype', 'Telia', 'Electrolux', 'ABB', 'Sandvik',
            'Atlas Copco', 'Hexagon', 'Autoliv', 'SKF', 'Alfa Laval', 'Getinge',
            'Husqvarna', 'Epiroc', 'Boliden', 'SSAB', 'Essity', 'SCA', 'Kinnevik',
            'Investor AB', 'Wallenberg', 'Nordea', 'SEB', 'Swedbank', 'Handelsbanken',
            'Omegapoint', 'CPAC Systems', 'ECARX', 'DoiT International', 'Kollmorgen',
            'Benifex', 'Ahlsell', 'ALTEN', 'Luxoft', 'eWorks', 'Tata', 'Nasdaq',
            'Thomson Reuters', 'Ascom', 'VFS Global', 'Cetasol', 'Saab', 'OmniModular'
        ]

        # Check recruiting companies first (they post jobs for other companies)
        # Use word boundary matching to avoid false positives (e.g., "king" in "making")
        import re as regex
        for company in known_recruiting_companies:
            # Match whole word only
            pattern = r'\b' + regex.escape(company) + r'\b'
            if regex.search(pattern, content, regex.IGNORECASE):
                return company

        for company in known_companies:
            # Match whole word only
            pattern = r'\b' + regex.escape(company) + r'\b'
            if regex.search(pattern, content, regex.IGNORECASE):
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
    Convenience function to extract job info from various job sites
    
    Args:
        content: Job page content
        url: Original URL for reference
        
    Returns:
        Dictionary with company, title, and success information
    """
    extractor = UniversalJobExtractor()
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