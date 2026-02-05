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
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract ALL text content for AI analysis
            page_text = soup.get_text(separator='\n', strip=True)
            
            # Extract raw title from h1 or title tag
            raw_title = ''
            title_elem = soup.find('h1')
            if title_elem:
                raw_title = title_elem.get_text(strip=True)
            elif soup.title:
                raw_title = soup.title.get_text(strip=True)
            
            # Extract description from main content areas
            description = ''
            description_selectors = [
                'div[class*="description"]', 'div[class*="content"]', 
                'div[class*="job-details"]', 'main', 'article',
                'div[id*="description"]', 'div[id*="content"]'
            ]
            for selector in description_selectors:
                elem = soup.select_one(selector)
                if elem:
                    description = elem.get_text(separator='\n', strip=True)
                    if len(description) > 200:
                        break
            
            # If no description found, use page text
            if not description or len(description) < 100:
                description = page_text[:3000]  # First 3000 chars
            
            # Use AI to intelligently parse the ENTIRE page content
            parsed = self._ai_extract_job_from_page(raw_title, description, page_text[:5000], url)
            
            title = parsed.get('title', raw_title)
            company = parsed.get('company', 'Unknown Company')
            location = parsed.get('location', 'Sweden')
            
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
    
    def _ai_extract_job_from_page(self, raw_title: str, description: str, page_text: str, url: str) -> Dict:
        """
        Use AI to intelligently extract job details from ENTIRE page content.
        This is more robust than regex parsing for complex job sites.
        """
        try:
            import os
            import requests as req
            import json
            
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
            
            if not api_key:
                logger.warning("No API key, falling back to regex")
                return self._parse_swedish_title_regex(raw_title, url)
            
            # Determine if Swedish or English
            is_swedish = any(word in page_text.lower()[:1000] for word in ['till', 'hos', 'på', 'utvecklare', 'ingenjör', 'söker vi'])
            
            prompt = f"""You are an expert at extracting job information from web pages. Analyze this job posting and extract the key details.

URL: {url}
RAW TITLE: {raw_title}

PAGE CONTENT (first 5000 chars):
{page_text}

DESCRIPTION:
{description[:1000]}

CRITICAL RULES:
1. **Company Name**: Extract the ACTUAL hiring company, NOT the recruitment agency
   - Recruitment agencies (Computer Sweden, Academic Work, TNG, etc.) should be IGNORED
   - Look for phrases like "till [Company]", "hos [Company]", "at [Company]"
   - Example: "Fullstackutvecklare till Aros Kapital - Computer Sweden Recruitment"
     → Company: "Aros Kapital" (NOT "Computer Sweden Recruitment")

2. **Job Title**: Translate Swedish titles to English
   - fullstackutvecklare → Full-Stack Developer
   - backend-utvecklare → Backend Developer
   - systemutvecklare → System Developer
   - devops-ingenjör → DevOps Engineer
   - Keep it clean and professional

3. **Location**: Extract city/region (default to "Sweden" if unclear)

TASK: Extract and return ONLY a JSON object with these fields:
{{"title": "Clean English Job Title", "company": "Actual Company Name", "location": "City, Country"}}

Example outputs:
- {{"title": "Full-Stack Developer", "company": "Aros Kapital", "location": "Gothenburg, Sweden"}}
- {{"title": "DevOps Engineer", "company": "Kamstrup", "location": "Malmö, Sweden"}}
- {{"title": "Backend Developer", "company": "Spotify", "location": "Stockholm, Sweden"}}

Return ONLY the JSON, no explanation."""

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
            
            response = req.post(url_api, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if 'content' in result and len(result['content']) > 0:
                    text = result['content'][0].get('text', '{}')
                    # Extract JSON from response
                    json_match = re.search(r'\{[^}]+\}', text)
                    if json_match:
                        parsed = json.loads(json_match.group())
                        logger.info(f"✅ AI extracted from page: {parsed}")
                        return parsed
            
            logger.warning(f"AI extraction failed, status: {response.status_code}")
            # Fallback to regex
            return self._parse_swedish_title_regex(raw_title, url)
            
        except Exception as e:
            logger.warning(f"AI page extraction failed: {e}, using regex fallback")
            return self._parse_swedish_title_regex(raw_title, url)
    
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

IMPORTANT: Recruitment agency names should be IGNORED!
- If title contains " - [Recruitment Agency]", ignore the agency part
- Example: "Fullstackutvecklare till Aros Kapital - Computer Sweden Recruitment"
  → Title: "Full-Stack Developer", Company: "Aros Kapital" (NOT "Computer Sweden Recruitment")

Common recruitment agencies to ignore: "Computer Sweden", "Academic Work", "TNG", "Randstad", "Manpower", "Wise Professionals"

TASK:
1. Identify the job title (translate from Swedish to English if needed)
2. Identify the ACTUAL company name (not the recruitment agency)
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
        # Remove recruitment agency names first (they appear after dash at the end)
        recruitment_agencies = [
            'Computer Sweden Recruitment', 'Computer Sweden', 'Academic Work', 
            'TNG', 'Randstad', 'Manpower', 'Wise Professionals', 'Poolia',
            'Adecco', 'Lernia', 'Proffice', 'Studentconsulting'
        ]
        
        cleaned_title = raw_title
        for agency in recruitment_agencies:
            # Remove " - Agency" or " | Agency" from end
            if cleaned_title.endswith(f' - {agency}'):
                cleaned_title = cleaned_title[:-len(f' - {agency}')].strip()
            elif cleaned_title.endswith(f' | {agency}'):
                cleaned_title = cleaned_title[:-len(f' | {agency}')].strip()
        
        # Now parse the cleaned title
        # Common Swedish patterns: "Title till Company" or "Title at Company"
        patterns = [
            r'(.+?)\s+till\s+(.+)',  # "Title till Company"
            r'(.+?)\s+hos\s+(.+)',   # "Title hos Company"
            r'(.+?)\s+på\s+(.+)',    # "Title på Company"
            r'(.+?)\s+at\s+(.+)',    # "Title at Company"
        ]
        
        for pattern in patterns:
            match = re.match(pattern, cleaned_title, re.IGNORECASE)
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
        
        # Last resort: return cleaned title
        return {'title': cleaned_title, 'company': 'Unknown Company'}
    
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
    
    def _parse_job_title_with_ai(self, raw_title: str, description: str, url: str, fallback_company: str) -> Dict:
        """Use AI to parse English job titles and extract company names"""
        try:
            import os
            import requests as req
            import json
            
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
            
            if not api_key:
                # Fallback to regex parsing
                return self._parse_english_title_regex(raw_title, fallback_company)
            
            prompt = f"""Parse this job posting and extract the job title and company name.

RAW TITLE: {raw_title}
URL: {url}
DESCRIPTION (first 500 chars): {description[:500]}
FALLBACK COMPANY: {fallback_company}

Job titles often use formats like:
- "Senior Developer at Google"
- "Software Engineer - Microsoft"
- "Full Stack Developer | Amazon"
- "DevOps Engineer (Netflix)"

TASK:
1. Identify the clean job title (remove company name if present)
2. Identify the company name (extract from title if present, otherwise use fallback)
3. Handle separators: "at", "-", "|", "()", "/"

Return ONLY a JSON object:
{{"title": "Clean Job Title", "company": "Company Name"}}"""

            url_api = f"{base_url}/v1/messages"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'anthropic-version': '2023-06-01'
            }
            
            payload = {
                "model": "glm-4.7",
                "max_tokens": 300,
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
                        logger.info(f"AI parsed English title: {parsed}")
                        return parsed
            
            # Fallback to regex
            return self._parse_english_title_regex(raw_title, fallback_company)
            
        except Exception as e:
            logger.warning(f"AI parsing failed, using regex fallback: {e}")
            return self._parse_english_title_regex(raw_title, fallback_company)
    
    def _parse_english_title_regex(self, raw_title: str, fallback_company: str) -> Dict:
        """Fallback regex parsing for English job titles"""
        # Common English patterns
        patterns = [
            r'(.+?)\s+at\s+(.+)',      # "Title at Company"
            r'(.+?)\s+-\s+(.+)',       # "Title - Company"
            r'(.+?)\s+\|\s+(.+)',      # "Title | Company"
            r'(.+?)\s+\((.+?)\)',      # "Title (Company)"
            r'(.+?)\s+/\s+(.+)',       # "Title / Company"
        ]
        
        for pattern in patterns:
            match = re.match(pattern, raw_title, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                company = match.group(2).strip()
                return {'title': title, 'company': company}
        
        # No pattern matched, return as-is
        return {'title': raw_title, 'company': fallback_company}
    
    def _extract_generic_job(self, url: str) -> Dict:
        """Extract job details from generic company career pages with AI-powered scraping"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements for cleaner text
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            # Extract ALL text content for AI analysis
            page_text = soup.get_text(separator='\n', strip=True)
            
            # Try to find job title in various common selectors
            raw_title = ''
            title_selectors = ['h1', 'h2', '.job-title', '.position-title', '[class*="title"]']
            for selector in title_selectors:
                elem = soup.select_one(selector)
                if elem and len(elem.get_text(strip=True)) > 5:
                    raw_title = elem.get_text(strip=True)
                    break
            
            if not raw_title and soup.title:
                raw_title = soup.title.get_text(strip=True)
            
            # Extract description from main content
            description = ''
            description_selectors = [
                '.job-description', '.description', '.content', 
                '.job-details', 'main', 'article'
            ]
            for selector in description_selectors:
                elem = soup.select_one(selector)
                if elem:
                    description = elem.get_text(separator='\n', strip=True)
                    if len(description) > 200:
                        break
            
            # If no description found, use page text
            if not description or len(description) < 100:
                description = page_text[:3000]
            
            # Use AI to intelligently extract from ENTIRE page (works for all languages)
            parsed = self._ai_extract_job_from_page(raw_title, description, page_text[:5000], url)
            
            title = parsed.get('title', raw_title or 'Unknown Position')
            company = parsed.get('company', 'Unknown Company')
            location = parsed.get('location', 'Sweden')
            
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