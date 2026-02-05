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
            elif 'computerswedenrecruitment.se' in domain or 'career.' in domain:
                # Swedish recruitment sites
                return self._extract_swedish_recruitment_job(url)
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
    
    def _extract_swedish_recruitment_job(self, url: str) -> Dict:
        """Extract job details from Swedish recruitment sites with AI parsing"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract raw title (often in format: "Title till Company" or "Title at Company")
            title_elem = soup.find('h1', class_=re.compile('font-company-header|job-title|position'))
            raw_title = title_elem.get_text(strip=True) if title_elem else ''
            
            # Extract description
            description_elem = soup.find('div', class_=re.compile('description|content|job-details'))
            description = description_elem.get_text(strip=True) if description_elem else ''
            
            # Use AI to parse Swedish job title and extract company
            parsed = self._parse_swedish_job_title_with_ai(raw_title, description, url)
            
            title = parsed.get('title', raw_title)
            company = parsed.get('company', 'Unknown Company')
            
            # Extract location
            location_elem = soup.find(class_=re.compile('location|place|city'))
            location = location_elem.get_text(strip=True) if location_elem else 'Sweden'
            
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
                    'source': 'Swedish Recruitment Site'
                }
            }
            
        except Exception as e:
            logger.error(f"Swedish recruitment extraction error: {str(e)}")
            return {'success': False, 'error': f'Swedish recruitment extraction failed: {str(e)}'}
    
    def _parse_swedish_job_title_with_ai(self, raw_title: str, description: str, url: str) -> Dict:
        """Use AI to parse Swedish job titles and extract company names"""
        try:
            import os
            import requests as req
            import json
            
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
            
            if not api_key:
                # Fallback to regex parsing
                return self._parse_swedish_title_regex(raw_title, url)
            
            # Common Swedish job title translations
            swedish_translations = {
                'fullstackutvecklare': 'Full-Stack Developer',
                'backend-utvecklare': 'Backend Developer',
                'frontend-utvecklare': 'Frontend Developer',
                'systemutvecklare': 'System Developer',
                'mjukvaruutvecklare': 'Software Developer',
                'devops-ingenjör': 'DevOps Engineer',
                'it-konsult': 'IT Consultant',
                'projektledare': 'Project Manager',
                'affärsanalytiker': 'Business Analyst',
                'it-arkitekt': 'IT Architect'
            }
            
            prompt = f"""Parse this Swedish job posting and extract the job title and company name.

RAW TITLE: {raw_title}
URL: {url}
DESCRIPTION (first 500 chars): {description[:500]}

Swedish job titles often use format: "[Title] till [Company]" or "[Title] at [Company]"
Common Swedish words: "till" = "to/at", "hos" = "at", "på" = "at"

TASK:
1. Identify the job title (translate from Swedish to English if needed)
2. Identify the company name (keep as-is, don't translate)
3. Handle formats like "Fullstackutvecklare till Aros Kapital" → Title: "Full-Stack Developer", Company: "Aros Kapital"

Common translations:
{json.dumps(swedish_translations, indent=2)}

Return ONLY a JSON object:
{{"title": "English Job Title", "company": "Company Name"}}"""

            url_api = f"{base_url}/v1/messages"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'anthropic-version': '2023-06-01'
            }
            
            payload = {
                "model": "glm-4.7",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = req.post(url_api, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if 'content' in result and len(result['content']) > 0:
                    text = result['content'][0].get('text', '{}')
                    # Extract JSON from response
                    json_match = re.search(r'\{[^}]+\}', text)
                    if json_match:
                        parsed = json.loads(json_match.group())
                        logger.info(f"AI parsed Swedish title: {parsed}")
                        return parsed
            
            # Fallback to regex
            return self._parse_swedish_title_regex(raw_title, url)
            
        except Exception as e:
            logger.warning(f"AI parsing failed, using regex fallback: {e}")
            return self._parse_swedish_title_regex(raw_title, url)
    
    def _parse_swedish_title_regex(self, raw_title: str, url: str) -> Dict:
        """Fallback regex parsing for Swedish job titles"""
        # Common Swedish patterns: "Title till Company" or "Title at Company"
        patterns = [
            r'(.+?)\s+till\s+(.+)',  # "Title till Company"
            r'(.+?)\s+hos\s+(.+)',   # "Title hos Company"
            r'(.+?)\s+på\s+(.+)',    # "Title på Company"
            r'(.+?)\s+at\s+(.+)',    # "Title at Company"
        ]
        
        for pattern in patterns:
            match = re.match(pattern, raw_title, re.IGNORECASE)
            if match:
                title_swedish = match.group(1).strip()
                company = match.group(2).strip()
                
                # Translate common Swedish titles
                title_english = self._translate_swedish_title(title_swedish)
                
                return {'title': title_english, 'company': company}
        
        # If no pattern matches, try to extract from URL
        url_parts = url.split('/')[-1].split('-')
        if len(url_parts) > 2:
            # URL like: "fullstackutvecklare-till-aros-kapital"
            if 'till' in url_parts:
                till_index = url_parts.index('till')
                title_parts = url_parts[:till_index]
                company_parts = url_parts[till_index+1:]
                
                title_swedish = ' '.join(title_parts)
                company = ' '.join(company_parts).title()
                title_english = self._translate_swedish_title(title_swedish)
                
                return {'title': title_english, 'company': company}
        
        # Last resort: return raw title
        return {'title': raw_title, 'company': 'Unknown Company'}
    
    def _translate_swedish_title(self, swedish_title: str) -> str:
        """Translate Swedish job title to English"""
        translations = {
            'fullstackutvecklare': 'Full-Stack Developer',
            'backend-utvecklare': 'Backend Developer',
            'backendutvecklare': 'Backend Developer',
            'frontend-utvecklare': 'Frontend Developer',
            'frontendutvecklare': 'Frontend Developer',
            'systemutvecklare': 'System Developer',
            'mjukvaruutvecklare': 'Software Developer',
            'devops-ingenjör': 'DevOps Engineer',
            'devopsingenjör': 'DevOps Engineer',
            'it-konsult': 'IT Consultant',
            'projektledare': 'Project Manager',
            'affärsanalytiker': 'Business Analyst',
            'it-arkitekt': 'IT Architect',
            'webbutvecklare': 'Web Developer',
            'apputvecklare': 'App Developer',
            'dataingenjör': 'Data Engineer',
            'it-tekniker': 'IT Technician',
            'systemadministratör': 'System Administrator'
        }
        
        swedish_lower = swedish_title.lower().strip()
        return translations.get(swedish_lower, swedish_title.title())
    
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
            
            raw_title = 'Unknown Position'
            for selector in title_selectors:
                elem = soup.select_one(selector)
                if elem and len(elem.get_text(strip=True)) > 5:
                    raw_title = elem.get_text(strip=True)
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
            
            # Check if this is a Swedish job posting (domain ends with .se or contains Swedish words)
            is_swedish = (
                '.se' in domain or 
                any(word in raw_title.lower() for word in ['till', 'hos', 'på', 'utvecklare', 'ingenjör', 'konsult'])
            )
            
            # Use AI parsing for Swedish titles
            if is_swedish:
                parsed = self._parse_swedish_job_title_with_ai(raw_title, description, url)
                title = parsed.get('title', raw_title)
                # Update company if AI found a better one
                if parsed.get('company') and parsed.get('company') != 'Unknown Company':
                    company = parsed.get('company')
            else:
                title = raw_title
            
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