#!/usr/bin/env python3
"""
Job URL Extractor Service
Extracts job details from various job board URLs
"""

import requests
from bs4 import BeautifulSoup
import re
import logging
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin
import json

logger = logging.getLogger(__name__)

class JobUrlExtractor:
    """Extract job details from job URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_job_details(self, url: str) -> Dict:
        """Extract job details from URL"""
        try:
            logger.info(f"Extracting job details from: {url}")
            
            # Determine the job board type
            domain = urlparse(url).netloc.lower()
            
            if 'linkedin.com' in domain:
                return self._extract_linkedin_job(url)
            elif 'indeed.com' in domain:
                return self._extract_indeed_job(url)
            elif 'glassdoor.com' in domain:
                return self._extract_glassdoor_job(url)
            else:
                # Generic extraction for company career pages
                return self._extract_generic_job(url)
                
        except Exception as e:
            logger.error(f"Error extracting job details: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to extract job details: {str(e)}'
            }
    
    def _extract_linkedin_job(self, url: str) -> Dict:
        """Extract job details from LinkedIn"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job title
            title_elem = soup.find('h1', class_='top-card-layout__title')
            title = title_elem.get_text(strip=True) if title_elem else 'Unknown Position'
            
            # Extract company
            company_elem = soup.find('a', class_='topcard__org-name-link') or soup.find('span', class_='topcard__flavor')
            company = company_elem.get_text(strip=True) if company_elem else 'Unknown Company'
            
            # Extract location
            location_elem = soup.find('span', class_='topcard__flavor topcard__flavor--bullet')
            location = location_elem.get_text(strip=True) if location_elem else 'Unknown Location'
            
            # Extract description
            description_elem = soup.find('div', class_='show-more-less-html__markup')
            description = description_elem.get_text(strip=True) if description_elem else ''
            
            # Extract requirements
            requirements = self._extract_requirements_from_text(description)
            
            return {
                'success': True,
                'job_details': {
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description,
                    'requirements': requirements,
                    'url': url,
                    'source': 'LinkedIn'
                }
            }
            
        except Exception as e:
            logger.error(f"LinkedIn extraction error: {str(e)}")
            return {'success': False, 'error': f'LinkedIn extraction failed: {str(e)}'}
    
    def _extract_indeed_job(self, url: str) -> Dict:
        """Extract job details from Indeed"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job title
            title_elem = soup.find('h1', class_='jobsearch-JobInfoHeader-title')
            title = title_elem.get_text(strip=True) if title_elem else 'Unknown Position'
            
            # Extract company
            company_elem = soup.find('div', class_='jobsearch-InlineCompanyRating') or soup.find('span', class_='jobsearch-JobInfoHeader-companyNameSimple')
            company = company_elem.get_text(strip=True) if company_elem else 'Unknown Company'
            
            # Extract location
            location_elem = soup.find('div', class_='jobsearch-JobInfoHeader-subtitle')
            location = location_elem.get_text(strip=True) if location_elem else 'Unknown Location'
            
            # Extract description
            description_elem = soup.find('div', class_='jobsearch-jobDescriptionText')
            description = description_elem.get_text(strip=True) if description_elem else ''
            
            requirements = self._extract_requirements_from_text(description)
            
            return {
                'success': True,
                'job_details': {
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description,
                    'requirements': requirements,
                    'url': url,
                    'source': 'Indeed'
                }
            }
            
        except Exception as e:
            logger.error(f"Indeed extraction error: {str(e)}")
            return {'success': False, 'error': f'Indeed extraction failed: {str(e)}'}
    
    def _extract_generic_job(self, url: str) -> Dict:
        """Extract job details from generic company career pages"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find job title in various common selectors
            title_selectors = [
                'h1', 'h2', '.job-title', '.position-title', 
                '[class*="title"]', '[class*="job"]', '.role-title'
            ]
            
            title = 'Unknown Position'
            for selector in title_selectors:
                elem = soup.select_one(selector)
                if elem and len(elem.get_text(strip=True)) > 5:
                    title = elem.get_text(strip=True)
                    break
            
            # Extract company from domain or page
            domain = urlparse(url).netloc
            company = domain.replace('www.', '').replace('.com', '').replace('.se', '').title()
            
            # Try to find company name in page
            company_selectors = ['.company-name', '.employer', '[class*="company"]']
            for selector in company_selectors:
                elem = soup.select_one(selector)
                if elem:
                    company = elem.get_text(strip=True)
                    break
            
            # Extract location
            location_selectors = ['.location', '.job-location', '[class*="location"]']
            location = 'Sweden'  # Default for Swedish companies
            for selector in location_selectors:
                elem = soup.select_one(selector)
                if elem:
                    location = elem.get_text(strip=True)
                    break
            
            # Extract description from main content
            description_selectors = [
                '.job-description', '.description', '.content', 
                '.job-details', 'main', '.main-content'
            ]
            
            description = ''
            for selector in description_selectors:
                elem = soup.select_one(selector)
                if elem:
                    description = elem.get_text(strip=True)
                    if len(description) > 100:  # Only use if substantial content
                        break
            
            requirements = self._extract_requirements_from_text(description)
            
            return {
                'success': True,
                'job_details': {
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description,
                    'requirements': requirements,
                    'url': url,
                    'source': 'Company Career Page'
                }
            }
            
        except Exception as e:
            logger.error(f"Generic extraction error: {str(e)}")
            return {'success': False, 'error': f'Generic extraction failed: {str(e)}'}
    
    def _extract_requirements_from_text(self, text: str) -> List[str]:
        """Extract requirements from job description text"""
        requirements = []
        
        # Common requirement patterns
        patterns = [
            r'(?:•|\*|-|\d+\.)\s*([^•\*\-\n]+(?:experience|skills?|knowledge|proficiency|expertise)[^•\*\-\n]*)',
            r'(?:Requirements?|Qualifications?|Skills?)[:\s]*\n([^•\*\-\n]+)',
            r'(?:Must have|Required|Essential)[:\s]*([^•\*\-\n]+)',
            r'(\d+\+?\s*years?[^•\*\-\n]*)',
            r'((?:Bachelor|Master|PhD)[^•\*\-\n]*)',
            r'((?:Java|Python|JavaScript|React|Angular|Spring|Docker|Kubernetes|AWS|Azure)[^•\*\-\n]*)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                req = match.strip()
                if len(req) > 10 and len(req) < 200:  # Filter reasonable length requirements
                    requirements.append(req)
        
        # Remove duplicates and limit to top 10
        requirements = list(dict.fromkeys(requirements))[:10]
        
        return requirements
    
    def _extract_glassdoor_job(self, url: str) -> Dict:
        """Extract job details from Glassdoor"""
        # Glassdoor has anti-scraping measures, so this is a basic implementation
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Basic extraction (Glassdoor structure changes frequently)
            title = 'Unknown Position'
            company = 'Unknown Company'
            location = 'Unknown Location'
            description = ''
            
            # Try to extract from JSON-LD structured data
            json_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_scripts:
                try:
                    data = json.loads(script.string)
                    if data.get('@type') == 'JobPosting':
                        title = data.get('title', title)
                        company = data.get('hiringOrganization', {}).get('name', company)
                        location = data.get('jobLocation', {}).get('address', {}).get('addressLocality', location)
                        description = data.get('description', description)
                        break
                except:
                    continue
            
            requirements = self._extract_requirements_from_text(description)
            
            return {
                'success': True,
                'job_details': {
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description,
                    'requirements': requirements,
                    'url': url,
                    'source': 'Glassdoor'
                }
            }
            
        except Exception as e:
            logger.error(f"Glassdoor extraction error: {str(e)}")
            return {'success': False, 'error': f'Glassdoor extraction failed: {str(e)}'}