import asyncio
import aiohttp
import re
from typing import List, Dict, Optional
from datetime import datetime
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class GoogleJobsService:
    """Service for searching jobs using Google Custom Search API and job sites"""
    
    def __init__(self):
        self.api_key = settings.GOOGLE_CUSTOM_SEARCH_API_KEY
        self.search_engine_id = settings.GOOGLE_CUSTOM_SEARCH_ENGINE_ID
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
    async def search_jobs(
        self, 
        query: str, 
        location: str = "", 
        num_results: int = 10,
        job_sites: List[str] = None
    ) -> List[Dict]:
        """
        Search for jobs using Google Custom Search API
        
        Args:
            query: Job search query (e.g., "python developer")
            location: Location filter (e.g., "San Francisco")
            num_results: Number of results to return
            job_sites: List of job sites to search (e.g., ["indeed.com", "linkedin.com"])
            
        Returns:
            List of job postings with metadata
        """
        if not self.api_key or not self.search_engine_id:
            logger.error("Google Custom Search API key or Engine ID not configured")
            return []
            
        if job_sites is None:
            job_sites = [
                "indeed.com", 
                "linkedin.com/jobs", 
                "glassdoor.com", 
                "monster.com",
                "dice.com",
                "ziprecruiter.com"
            ]
        
        all_jobs = []
        
        # Search each job site
        for site in job_sites:
            try:
                site_jobs = await self._search_site(query, location, site, num_results // len(job_sites))
                all_jobs.extend(site_jobs)
            except Exception as e:
                logger.error(f"Error searching {site}: {e}")
                continue
                
        # Remove duplicates and sort by relevance
        unique_jobs = self._remove_duplicates(all_jobs)
        return sorted(unique_jobs, key=lambda x: x.get('relevance_score', 0), reverse=True)[:num_results]
    
    async def _search_site(self, query: str, location: str, site: str, num_results: int) -> List[Dict]:
        """Search jobs on a specific site using Google Custom Search"""
        
        # Build search query
        search_query = f"{query}"
        if location:
            search_query += f" {location}"
        search_query += f" site:{site}"
        
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': search_query,
            'num': min(num_results, 10),  # Google limits to 10 per request
            'fields': 'items(title,link,snippet,displayLink,pagemap)'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_search_results(data, site)
                    else:
                        logger.error(f"Google Search API error: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"Error calling Google Search API: {e}")
                return []
    
    def _parse_search_results(self, data: Dict, source_site: str) -> List[Dict]:
        """Parse Google Search results into job posting format"""
        jobs = []
        
        items = data.get('items', [])
        for item in items:
            try:
                job = self._extract_job_info(item, source_site)
                if job:
                    jobs.append(job)
            except Exception as e:
                logger.error(f"Error parsing job item: {e}")
                continue
                
        return jobs
    
    def _extract_job_info(self, item: Dict, source_site: str) -> Optional[Dict]:
        """Extract job information from search result"""
        
        title = item.get('title', '')
        link = item.get('link', '')
        snippet = item.get('snippet', '')
        
        # Skip non-job results
        if not self._is_job_posting(title, snippet):
            return None
        
        # Extract job details
        job = {
            'title': self._clean_title(title),
            'company': self._extract_company(title, snippet, source_site),
            'location': self._extract_location(snippet),
            'description': snippet,
            'url': link,
            'source': source_site,
            'posting_date': self._extract_date(snippet),
            'salary': self._extract_salary(snippet),
            'job_type': self._extract_job_type(snippet),
            'relevance_score': self._calculate_relevance_score(title, snippet),
            'scraped_at': datetime.utcnow(),
            'keywords': self._extract_keywords(title, snippet)
        }
        
        return job
    
    def _is_job_posting(self, title: str, snippet: str) -> bool:
        """Check if search result is actually a job posting"""
        
        # Job indicators in title
        job_indicators = [
            'job', 'position', 'hiring', 'career', 'opening', 
            'vacancy', 'employment', 'work', 'role'
        ]
        
        # Non-job indicators
        non_job_indicators = [
            'about us', 'company profile', 'reviews', 'salary guide',
            'interview tips', 'career advice', 'blog', 'news'
        ]
        
        title_lower = title.lower()
        snippet_lower = snippet.lower()
        content = f"{title_lower} {snippet_lower}"
        
        # Check for non-job indicators first
        if any(indicator in content for indicator in non_job_indicators):
            return False
            
        # Check for job indicators
        if any(indicator in content for indicator in job_indicators):
            return True
            
        # Check for job site specific patterns
        if 'indeed.com' in content and ('apply' in content or 'salary' in content):
            return True
        if 'linkedin.com/jobs' in content:
            return True
        if 'glassdoor.com' in content and 'jobs' in content:
            return True
            
        return False
    
    def _clean_title(self, title: str) -> str:
        """Clean job title by removing site name and extra text"""
        
        # Remove common site suffixes
        site_patterns = [
            r' - Indeed\.com$',
            r' \| LinkedIn$',
            r' - Glassdoor$',
            r' - Monster\.com$',
            r' \| Dice\.com$',
            r' - ZipRecruiter$'
        ]
        
        cleaned = title
        for pattern in site_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
            
        return cleaned.strip()
    
    def _extract_company(self, title: str, snippet: str, source_site: str) -> Optional[str]:
        """Extract company name from title or snippet"""
        
        # Common patterns for company extraction
        company_patterns = [
            r'at ([^-\|]+?)(?:\s*-|\s*\||\s*$)',  # "Position at Company"
            r'([^-\|]+?)\s*-\s*',  # "Company - Position"
            r'hiring.*?at\s+([^\.]+)',  # "Hiring at Company"
        ]
        
        content = f"{title} {snippet}"
        
        for pattern in company_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                # Clean company name
                company = re.sub(r'\s*jobs?\s*$', '', company, flags=re.IGNORECASE)
                if len(company) > 3 and len(company) < 100:
                    return company
                    
        return None
    
    def _extract_location(self, snippet: str) -> Optional[str]:
        """Extract location from snippet"""
        
        location_patterns = [
            r'(?:in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,?\s*[A-Z]{2})',  # "in San Francisco, CA"
            r'([A-Z][a-z]+,\s*[A-Z]{2})',  # "Boston, MA"
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)',  # "New York"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, snippet)
            if match:
                return match.group(1).strip()
                
        return None
    
    def _extract_salary(self, snippet: str) -> Optional[Dict]:
        """Extract salary information from snippet"""
        
        salary_patterns = [
            r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*-\s*\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # "$50,000 - $70,000"
            r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:per\s+year|annually|/year)?',  # "$60,000 per year"
            r'(\d{1,3}(?:,\d{3})*)\s*-\s*(\d{1,3}(?:,\d{3})*)\s*(?:USD|dollars?)',  # "50,000 - 70,000 USD"
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, snippet, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return {
                        'min': self._parse_salary(match.group(1)),
                        'max': self._parse_salary(match.group(2)),
                        'currency': 'USD'
                    }
                else:
                    return {
                        'min': self._parse_salary(match.group(1)),
                        'max': None,
                        'currency': 'USD'
                    }
                    
        return None
    
    def _parse_salary(self, salary_str: str) -> int:
        """Parse salary string to integer"""
        return int(re.sub(r'[,$.]', '', salary_str.replace('.00', '')))
    
    def _extract_date(self, snippet: str) -> Optional[datetime]:
        """Extract posting date from snippet"""
        
        date_patterns = [
            r'(\d+)\s+days?\s+ago',
            r'(\d+)\s+hours?\s+ago',
            r'posted\s+(\d+)\s+days?\s+ago',
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # MM/DD/YYYY
        ]
        
        from datetime import timedelta
        
        for pattern in date_patterns:
            match = re.search(pattern, snippet, re.IGNORECASE)
            if match:
                if 'days ago' in match.group(0).lower():
                    days_ago = int(match.group(1))
                    return datetime.utcnow() - timedelta(days=days_ago)
                elif 'hours ago' in match.group(0).lower():
                    hours_ago = int(match.group(1))
                    return datetime.utcnow() - timedelta(hours=hours_ago)
                elif len(match.groups()) == 3:  # Date format
                    try:
                        month, day, year = match.groups()
                        return datetime(int(year), int(month), int(day))
                    except ValueError:
                        continue
                        
        return None
    
    def _extract_job_type(self, snippet: str) -> Optional[str]:
        """Extract job type (full-time, part-time, contract, etc.)"""
        
        job_types = {
            'full-time': ['full time', 'full-time', 'fulltime', 'permanent'],
            'part-time': ['part time', 'part-time', 'parttime'],
            'contract': ['contract', 'contractor', 'freelance', 'temporary', 'temp'],
            'internship': ['intern', 'internship', 'co-op', 'coop'],
            'remote': ['remote', 'work from home', 'wfh', 'telecommute']
        }
        
        snippet_lower = snippet.lower()
        
        for job_type, keywords in job_types.items():
            if any(keyword in snippet_lower for keyword in keywords):
                return job_type
                
        return None
    
    def _calculate_relevance_score(self, title: str, snippet: str) -> float:
        """Calculate relevance score based on various factors"""
        
        score = 0.0
        content = f"{title} {snippet}".lower()
        
        # Higher score for recent postings
        if 'days ago' in content or 'hours ago' in content:
            score += 0.3
            
        # Higher score for direct job postings
        if any(word in content for word in ['hiring', 'apply', 'position', 'job']):
            score += 0.2
            
        # Higher score for salary information
        if '$' in content or 'salary' in content:
            score += 0.2
            
        # Higher score for company information
        if any(word in content for word in ['company', 'team', 'join']):
            score += 0.1
            
        # Higher score for location information
        if any(word in content for word in [',', 'ca', 'ny', 'tx', 'fl']):
            score += 0.1
            
        # Bonus for full job descriptions
        if len(snippet) > 100:
            score += 0.1
            
        return min(score, 1.0)
    
    def _extract_keywords(self, title: str, snippet: str) -> List[str]:
        """Extract relevant keywords from job posting"""
        
        content = f"{title} {snippet}".lower()
        
        # Common tech keywords
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'angular', 'vue',
            'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'machine learning', 'ai', 'data science',
            'fullstack', 'frontend', 'backend', 'devops', 'cloud', 'api',
            'rest', 'graphql', 'microservices', 'agile', 'scrum'
        ]
        
        found_keywords = []
        for keyword in tech_keywords:
            if keyword in content:
                found_keywords.append(keyword)
                
        return found_keywords
    
    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate job postings based on title and company"""
        
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a unique key based on title, company, and location
            key = (
                job.get('title', '').lower().strip(),
                job.get('company', '').lower().strip(),
                job.get('location', '').lower().strip()
            )
            
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
                
        return unique_jobs
    
    async def get_job_details(self, job_url: str) -> Optional[Dict]:
        """Get detailed job information by scraping the job page"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(job_url, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_job_page(html, job_url)
                    else:
                        logger.error(f"Failed to fetch job page: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching job details: {e}")
            return None
    
    def _parse_job_page(self, html: str, url: str) -> Dict:
        """Parse job page HTML to extract detailed information"""
        
        # This is a simplified parser - in production, you'd want more sophisticated parsing
        # for each job site's specific HTML structure
        
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract title
        title_selectors = ['h1', '.jobsearch-JobInfoHeader-title', '[data-testid="jobTitle"]']
        title = None
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                break
        
        # Extract company
        company_selectors = ['.icl-u-lg-mr--sm', '[data-testid="companyName"]', '.company']
        company = None
        for selector in company_selectors:
            element = soup.select_one(selector)
            if element:
                company = element.get_text(strip=True)
                break
        
        # Extract description
        desc_selectors = ['.jobsearch-jobDescriptionText', '[data-testid="jobDescription"]', '.job-description']
        description = None
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                description = element.get_text(strip=True)
                break
        
        return {
            'title': title,
            'company': company,
            'description': description,
            'url': url,
            'detailed': True,
            'scraped_at': datetime.utcnow()
        }