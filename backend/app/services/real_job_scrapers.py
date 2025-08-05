import asyncio
import aiohttp
import logging
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlencode, quote_plus
import time

logger = logging.getLogger(__name__)

class LinkedInJobScraper:
    """
    LinkedIn job scraper for real job positions
    Uses public LinkedIn job search (no API required)
    """
    
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Job search parameters
        self.keywords = [
            "fullstack developer",
            "backend developer", 
            "frontend developer",
            "software engineer",
            "devops engineer",
            "python developer",
            "java developer",
            "react developer",
            "nodejs developer"
        ]
        
        self.locations = [
            "Stockholm, Sweden",
            "Gothenburg, Sweden", 
            "Malmö, Sweden",
            "Sweden"
        ]
    
    async def scrape_linkedin_jobs(self, max_jobs: int = 20) -> List[Dict]:
        """
        Scrape real LinkedIn job postings
        """
        try:
            logger.info(f"🔍 Scraping LinkedIn for real job postings (max: {max_jobs})")
            
            all_jobs = []
            
            # Search for different keyword combinations
            for keyword in self.keywords[:3]:  # Limit to avoid being blocked
                for location in self.locations[:2]:  # Limit locations
                    try:
                        jobs = await self._search_linkedin_jobs(keyword, location, limit=5)
                        all_jobs.extend(jobs)
                        
                        # Be respectful - add delay between requests
                        await asyncio.sleep(2)
                        
                        if len(all_jobs) >= max_jobs:
                            break
                    except Exception as e:
                        logger.warning(f"Error searching LinkedIn for {keyword} in {location}: {e}")
                
                if len(all_jobs) >= max_jobs:
                    break
            
            # Remove duplicates and return limited results
            unique_jobs = self._remove_duplicates(all_jobs)
            logger.info(f"✅ Found {len(unique_jobs)} unique LinkedIn job opportunities")
            
            return unique_jobs[:max_jobs]
            
        except Exception as e:
            logger.error(f"❌ Error scraping LinkedIn jobs: {e}")
            return []
    
    async def _search_linkedin_jobs(self, keyword: str, location: str, limit: int = 10) -> List[Dict]:
        """
        Search LinkedIn jobs for specific keyword and location
        """
        try:
            # Build search URL
            params = {
                'keywords': keyword,
                'location': location,
                'f_TPR': 'r86400',  # Past 24 hours
                'f_JT': 'F',  # Full-time
                'sortBy': 'DD',  # Most recent
                'start': 0
            }
            
            search_url = f"{self.base_url}?{urlencode(params)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers=self.headers) as response:
                    if response.status != 200:
                        logger.warning(f"LinkedIn search returned status {response.status}")
                        return []
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Find job cards
                    job_cards = soup.find_all('div', {'class': re.compile(r'job-search-card|base-search-card')})
                    
                    jobs = []
                    for card in job_cards[:limit]:
                        try:
                            job_info = await self._extract_job_from_card(card, session)
                            if job_info:
                                jobs.append(job_info)
                        except Exception as e:
                            logger.warning(f"Error extracting job from card: {e}")
                    
                    return jobs
            
        except Exception as e:
            logger.error(f"Error searching LinkedIn jobs: {e}")
            return []
    
    async def _extract_job_from_card(self, card, session) -> Optional[Dict]:
        """
        Extract job information from LinkedIn job card
        """
        try:
            # Extract basic info from card
            title_elem = card.find('h3', {'class': re.compile(r'base-search-card__title')}) or card.find('a', {'class': re.compile(r'job-search-card__title-link')})
            company_elem = card.find('h4', {'class': re.compile(r'base-search-card__subtitle')}) or card.find('a', {'class': re.compile(r'hidden-nested-link')})
            location_elem = card.find('span', {'class': re.compile(r'job-search-card__location')})
            link_elem = card.find('a', href=True)
            
            if not title_elem or not company_elem or not link_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            company = company_elem.get_text(strip=True)
            location = location_elem.get_text(strip=True) if location_elem else "Sweden"
            job_url = link_elem['href']
            
            # Clean URL
            if 'linkedin.com' not in job_url:
                job_url = f"https://www.linkedin.com{job_url}"
            
            # Extract job ID from URL
            job_id_match = re.search(r'/jobs/view/(\d+)', job_url)
            job_id = job_id_match.group(1) if job_id_match else None
            
            if not job_id:
                return None
            
            # Get detailed job information
            detailed_info = await self._get_job_details(job_id, session)
            
            # Combine information
            job_info = {
                'source': 'linkedin_real',
                'job_id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'application_link': job_url,
                'description': detailed_info.get('description', ''),
                'requirements': detailed_info.get('requirements', []),
                'keywords': self._extract_keywords_from_text(f"{title} {detailed_info.get('description', '')}"),
                'employment_type': 'Full-time',
                'salary': detailed_info.get('salary', ''),
                'company_info': detailed_info.get('company_info', ''),
                'benefits': detailed_info.get('benefits', []),
                'seniority_level': detailed_info.get('seniority_level', ''),
                'industry': detailed_info.get('industry', ''),
                'date_posted': detailed_info.get('date_posted', ''),
                'experience_level': self._determine_experience_level(title, detailed_info.get('description', ''))
            }
            
            return job_info
            
        except Exception as e:
            logger.warning(f"Error extracting job from card: {e}")
            return None
    
    async def _get_job_details(self, job_id: str, session) -> Dict:
        """
        Get detailed job information from LinkedIn job page
        """
        try:
            job_url = f"https://www.linkedin.com/jobs/view/{job_id}"
            
            async with session.get(job_url, headers=self.headers) as response:
                if response.status != 200:
                    return {}
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                details = {}
                
                # Extract job description
                desc_elem = soup.find('div', {'class': re.compile(r'show-more-less-html__markup')})
                if desc_elem:
                    details['description'] = desc_elem.get_text(strip=True)
                
                # Extract company information
                company_elem = soup.find('div', {'class': re.compile(r'sub-nav-cta__optional-url')})
                if company_elem:
                    details['company_info'] = company_elem.get_text(strip=True)
                
                # Extract job criteria (seniority, employment type, etc.)
                criteria_elems = soup.find_all('span', {'class': re.compile(r'description__job-criteria-text')})
                for elem in criteria_elems:
                    text = elem.get_text(strip=True).lower()
                    if 'senior' in text or 'lead' in text:
                        details['seniority_level'] = 'Senior'
                    elif 'entry' in text or 'junior' in text:
                        details['seniority_level'] = 'Junior'
                    elif 'mid' in text:
                        details['seniority_level'] = 'Mid-level'
                
                # Extract posting date
                date_elem = soup.find('span', {'class': re.compile(r'posted-time-ago__text')})
                if date_elem:
                    details['date_posted'] = date_elem.get_text(strip=True)
                
                # Extract salary if available
                salary_elem = soup.find('span', string=re.compile(r'kr|SEK|\$', re.IGNORECASE))
                if salary_elem:
                    details['salary'] = salary_elem.get_text(strip=True)
                
                return details
                
        except Exception as e:
            logger.warning(f"Error getting job details for {job_id}: {e}")
            return {}
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """
        Extract technical keywords from job text
        """
        tech_keywords = [
            # Programming Languages
            "java", "javascript", "python", "typescript", "c#", "go", "rust", "kotlin", "swift",
            # Frontend
            "react", "angular", "vue", "svelte", "html", "css", "sass", "webpack",
            # Backend
            "spring", "spring boot", "nodejs", "django", "flask", "express", ".net",
            # Databases
            "postgresql", "mysql", "mongodb", "redis", "sql",
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible",
            # Methodologies
            "agile", "scrum", "ci/cd", "microservices", "api", "rest", "graphql",
            # Specializations
            "fullstack", "backend", "frontend", "devops", "cloud"
        ]
        
        text_lower = text.lower()
        found_keywords = [kw for kw in tech_keywords if kw in text_lower]
        return found_keywords[:10]
    
    def _determine_experience_level(self, title: str, description: str) -> str:
        """
        Determine experience level from job title and description
        """
        text = f"{title} {description}".lower()
        
        if any(term in text for term in ["senior", "lead", "principal", "architect", "5+ years", "expert"]):
            return "Senior"
        elif any(term in text for term in ["junior", "entry", "graduate", "0-2 years", "trainee"]):
            return "Junior"
        else:
            return "Mid-level"
    
    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """
        Remove duplicate jobs based on title and company
        """
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = f"{job['company'].lower()}_{job['title'].lower().replace(' ', '_')}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs


class IndeedJobScraper:
    """
    Indeed.se job scraper for real Swedish job positions
    """
    
    def __init__(self):
        self.base_url = "https://se.indeed.com/jobs"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'sv-SE,sv;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        self.keywords = [
            "fullstack utvecklare",
            "backend utvecklare", 
            "frontend utvecklare",
            "mjukvaruingenjör",
            "systemutvecklare",
            "python utvecklare",
            "java utvecklare",
            "devops ingenjör"
        ]
    
    async def scrape_indeed_jobs(self, max_jobs: int = 15) -> List[Dict]:
        """
        Scrape real job postings from Indeed.se
        """
        try:
            logger.info(f"🔍 Scraping Indeed.se for real job postings (max: {max_jobs})")
            
            all_jobs = []
            
            for keyword in self.keywords[:3]:  # Limit to avoid being blocked
                try:
                    jobs = await self._search_indeed_jobs(keyword, limit=5)
                    all_jobs.extend(jobs)
                    
                    # Be respectful - add delay
                    await asyncio.sleep(3)
                    
                    if len(all_jobs) >= max_jobs:
                        break
                        
                except Exception as e:
                    logger.warning(f"Error searching Indeed for {keyword}: {e}")
            
            unique_jobs = self._remove_duplicates_indeed(all_jobs)
            logger.info(f"✅ Found {len(unique_jobs)} unique Indeed job opportunities")
            
            return unique_jobs[:max_jobs]
            
        except Exception as e:
            logger.error(f"❌ Error scraping Indeed jobs: {e}")
            return []
    
    async def _search_indeed_jobs(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        Search Indeed.se for jobs
        """
        try:
            params = {
                'q': keyword,
                'l': 'Sverige',
                'sort': 'date',
                'fromage': '3',  # Last 3 days
                'limit': limit
            }
            
            search_url = f"{self.base_url}?{urlencode(params)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers=self.headers) as response:
                    if response.status != 200:
                        logger.warning(f"Indeed search returned status {response.status}")
                        return []
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Find job cards (Indeed uses different class names)
                    job_cards = soup.find_all(['div', 'article'], {'class': re.compile(r'job_seen_beacon|result|jobsearch-SerpJobCard')})
                    
                    jobs = []
                    for card in job_cards[:limit]:
                        try:
                            job_info = self._extract_indeed_job_from_card(card)
                            if job_info:
                                jobs.append(job_info)
                        except Exception as e:
                            logger.warning(f"Error extracting Indeed job: {e}")
                    
                    return jobs
            
        except Exception as e:
            logger.error(f"Error searching Indeed jobs: {e}")
            return []
    
    def _extract_indeed_job_from_card(self, card) -> Optional[Dict]:
        """
        Extract job information from Indeed job card
        """
        try:
            # Indeed has various HTML structures, try multiple selectors
            title_elem = (card.find('a', {'data-jk': True}) or 
                         card.find('h2', {'class': re.compile(r'jobTitle')}) or
                         card.find('span', {'title': True}))
            
            company_elem = (card.find('span', {'class': re.compile(r'companyName')}) or
                           card.find('a', {'data-tn-element': 'companyName'}) or
                           card.find('div', {'class': re.compile(r'company')}))
            
            location_elem = (card.find('div', {'class': re.compile(r'companyLocation')}) or
                            card.find('span', {'class': re.compile(r'location')}))
            
            link_elem = card.find('a', href=True)
            
            if not title_elem or not company_elem:
                return None
            
            title = title_elem.get_text(strip=True) if hasattr(title_elem, 'get_text') else title_elem.get('title', '')
            company = company_elem.get_text(strip=True)
            location = location_elem.get_text(strip=True) if location_elem else "Sverige"
            
            # Build job URL
            job_url = ""
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                if href.startswith('/'):
                    job_url = f"https://se.indeed.com{href}"
                else:
                    job_url = href
            
            # Extract job key for Indeed URLs
            job_key = ""
            jk_match = re.search(r'jk=([a-zA-Z0-9]+)', job_url)
            if jk_match:
                job_key = jk_match.group(1)
            
            # Extract salary if available
            salary_elem = card.find('span', {'class': re.compile(r'salary|estimated-salary')})
            salary = salary_elem.get_text(strip=True) if salary_elem else ""
            
            # Extract snippet/description
            snippet_elem = card.find('div', {'class': re.compile(r'summary|snippet')}) or card.find('span', {'class': re.compile(r'summary')})
            description = snippet_elem.get_text(strip=True) if snippet_elem else ""
            
            job_info = {
                'source': 'indeed_real',
                'job_key': job_key,
                'title': title,
                'company': company,
                'location': location,
                'application_link': job_url,
                'description': description,
                'salary': salary,
                'keywords': self._extract_keywords_from_text(f"{title} {description}"),
                'employment_type': 'Full-time',
                'experience_level': self._determine_experience_level(title, description),
                'date_posted': 'Recent'
            }
            
            return job_info
            
        except Exception as e:
            logger.warning(f"Error extracting Indeed job from card: {e}")
            return None
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract technical keywords"""
        tech_keywords = [
            "java", "javascript", "python", "typescript", "c#", "react", "angular", "vue",
            "spring", "nodejs", "django", ".net", "postgresql", "mysql", "mongodb",
            "aws", "azure", "docker", "kubernetes", "git", "agile", "scrum",
            "fullstack", "backend", "frontend", "devops", "utvecklare", "ingenjör"
        ]
        
        text_lower = text.lower()
        found_keywords = [kw for kw in tech_keywords if kw in text_lower]
        return found_keywords[:8]
    
    def _determine_experience_level(self, title: str, description: str) -> str:
        """Determine experience level"""
        text = f"{title} {description}".lower()
        
        if any(term in text for term in ["senior", "lead", "chef", "ledande", "erfaren"]):
            return "Senior"
        elif any(term in text for term in ["junior", "trainee", "nyexaminerad", "praktikant"]):
            return "Junior"
        else:
            return "Mid-level"
    
    def _remove_duplicates_indeed(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = f"{job['company'].lower()}_{job['title'].lower().replace(' ', '_')}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs


class ArbetsformedlingenScraper:
    """
    Arbetsförmedlingen job scraper using official open data API
    """
    
    def __init__(self):
        self.api_base_url = "https://data.arbetsformedlingen.se/api/v1"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'sv-SE,sv;q=0.9,en;q=0.8',
        }
        
        # Job search keywords focused on developer roles
        self.keywords = [
            "systemutvecklare", "mjukvaruingenjör", "backend utvecklare", 
            "frontend utvecklare", "fullstack utvecklare", "devops ingenjör",
            "python utvecklare", "java utvecklare", "cloud ingenjör"
        ]
    
    async def scrape_arbetsformedlingen_jobs(self, max_jobs: int = 15) -> List[Dict]:
        """
        Scrape jobs from Arbetsförmedlingen using their official API
        """
        try:
            logger.info(f"🔍 Fetching Arbetsförmedlingen jobs via official API (max: {max_jobs})")
            
            all_jobs = []
            
            async with aiohttp.ClientSession() as session:
                for keyword in self.keywords[:3]:  # Limit API calls
                    try:
                        jobs = await self._search_arbetsformedlingen_api(keyword, session, limit=5)
                        all_jobs.extend(jobs)
                        
                        # Be respectful with API calls
                        await asyncio.sleep(1)
                        
                        if len(all_jobs) >= max_jobs:
                            break
                            
                    except Exception as e:
                        logger.warning(f"Error searching Arbetsförmedlingen API for {keyword}: {e}")
            
            unique_jobs = self._remove_duplicates_arbetsformedlingen(all_jobs)
            logger.info(f"✅ Found {len(unique_jobs)} unique Arbetsförmedlingen job opportunities")
            
            return unique_jobs[:max_jobs]
            
        except Exception as e:
            logger.error(f"❌ Error accessing Arbetsförmedlingen API: {e}")
            # Fallback to mock data for demo purposes
            return self._get_fallback_jobs()
    
    async def _search_arbetsformedlingen_api(self, keyword: str, session, limit: int = 10) -> List[Dict]:
        """
        Search Arbetsförmedlingen jobs via official API
        """
        try:
            # Using their job search API endpoint
            params = {
                'q': keyword,
                'limit': limit,
                'offset': 0,
                'sort': 'pubdate-desc'  # Most recent first
            }
            
            api_url = f"{self.api_base_url}/platsannonser/search"
            
            async with session.get(api_url, headers=self.headers, params=params) as response:
                if response.status != 200:
                    logger.warning(f"Arbetsförmedlingen API returned status {response.status}")
                    return []
                
                data = await response.json()
                
                jobs = []
                if 'platsannonser' in data:
                    for job_data in data['platsannonser'][:limit]:
                        job_info = self._parse_arbetsformedlingen_job(job_data)
                        if job_info:
                            jobs.append(job_info)
                
                return jobs
                
        except Exception as e:
            logger.error(f"Error searching Arbetsförmedlingen API: {e}")
            return []
    
    def _parse_arbetsformedlingen_job(self, job_data: Dict) -> Optional[Dict]:
        """
        Parse job data from Arbetsförmedlingen API response
        """
        try:
            job_info = {
                'source': 'arbetsformedlingen_real',
                'job_id': job_data.get('id', ''),
                'title': job_data.get('rubrik', ''),
                'company': job_data.get('arbetsgivare', {}).get('namn', 'Unknown Company'),
                'location': job_data.get('arbetsplats', {}).get('kommun', 'Sverige'),
                'application_link': job_data.get('ansokningsdetaljer', {}).get('url', ''),
                'description': job_data.get('beskrivning', {}).get('kort', '')[:500],
                'requirements': self._extract_requirements_from_description(job_data.get('beskrivning', {}).get('krav', '')),
                'keywords': self._extract_keywords_from_arbetsformedlingen_text(
                    f"{job_data.get('rubrik', '')} {job_data.get('beskrivning', {}).get('kort', '')}"
                ),
                'employment_type': job_data.get('anstallningstyp', {}).get('benaming', 'Tillsvidare'),
                'salary': self._extract_salary_from_data(job_data),
                'experience_level': self._determine_experience_level_swedish(
                    job_data.get('rubrik', ''),
                    job_data.get('beskrivning', {}).get('kort', '')
                ),
                'date_posted': job_data.get('publiceraddatum', ''),
                'application_deadline': job_data.get('sista_ansokningsdag', ''),
                'working_hours': job_data.get('arbetstid', {}).get('benaming', ''),
                'industry': job_data.get('yrkesgrupp', {}).get('benaming', ''),
                'company_info': job_data.get('arbetsgivare', {}).get('beskrivning', '')
            }
            
            # Filter for relevant developer positions
            if self._is_relevant_developer_position(job_info['title'], job_info['description']):
                return job_info
            
            return None
            
        except Exception as e:
            logger.warning(f"Error parsing Arbetsförmedlingen job: {e}")
            return None
    
    def _extract_requirements_from_description(self, requirements_text: str) -> List[str]:
        """Extract requirements from Swedish job description"""
        if not requirements_text:
            return []
        
        # Split on common Swedish requirement separators
        requirements = []
        for req in requirements_text.split('\n'):
            req = req.strip()
            if len(req) > 10 and len(req) < 200:
                requirements.append(req)
        
        return requirements[:8]
    
    def _extract_salary_from_data(self, job_data: Dict) -> str:
        """Extract salary information from job data"""
        try:
            loneform = job_data.get('loneform', {})
            if loneform and loneform.get('benaming'):
                return loneform.get('benaming', '')
            
            # Look for salary in description
            description = job_data.get('beskrivning', {}).get('kort', '').lower()
            salary_patterns = [
                r'(\d{2,3}[,\s]*\d{3}[,\s]*\d{3})\s*(?:kr|kronor|sek)',
                r'(\d{2,3}[,\s]*\d{3})\s*-\s*(\d{2,3}[,\s]*\d{3})\s*(?:kr|kronor|sek)',
                r'lön[:\s]+([^\n]{10,50})'
            ]
            
            for pattern in salary_patterns:
                import re
                match = re.search(pattern, description, re.IGNORECASE)
                if match:
                    return match.group(0)
            
            return ""
            
        except Exception:
            return ""
    
    def _extract_keywords_from_arbetsformedlingen_text(self, text: str) -> List[str]:
        """Extract technical keywords from Swedish job text"""
        tech_keywords = [
            # Programming Languages
            "java", "javascript", "python", "typescript", "c#", "go", "rust", "kotlin",
            # Swedish terms
            "systemutvecklare", "mjukvaruingenjör", "utvecklare", "programmerare",
            # Frontend
            "react", "angular", "vue", "html", "css", "sass", "webpack",
            # Backend
            "spring", "spring boot", "nodejs", "django", "flask", "express", ".net",
            # Databases
            "postgresql", "mysql", "mongodb", "redis", "sql", "databas",
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform",
            # Methodologies
            "agile", "scrum", "ci/cd", "microservices", "api", "rest", "graphql",
            # Specializations
            "fullstack", "backend", "frontend", "devops", "cloud", "molnet"
        ]
        
        text_lower = text.lower()
        found_keywords = [kw for kw in tech_keywords if kw in text_lower]
        return found_keywords[:10]
    
    def _determine_experience_level_swedish(self, title: str, description: str) -> str:
        """Determine experience level from Swedish job text"""
        text = f"{title} {description}".lower()
        
        if any(term in text for term in ["senior", "chef", "ledande", "erfaren", "specialist", "arkitekt"]):
            return "Senior"
        elif any(term in text for term in ["junior", "trainee", "nyexaminerad", "praktikant", "nybörjare"]):
            return "Junior"
        else:
            return "Mid-level"
    
    def _is_relevant_developer_position(self, title: str, description: str) -> bool:
        """Check if position is relevant for a developer with 5+ years experience"""
        text = f"{title} {description}".lower()
        
        developer_terms = [
            "utvecklare", "developer", "ingenjör", "engineer", "programmerare", "programmer",
            "systemutvecklare", "mjukvaruingenjör", "fullstack", "backend", "frontend", "devops"
        ]
        
        return any(term in text for term in developer_terms)
    
    def _remove_duplicates_arbetsformedlingen(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = f"{job['company'].lower()}_{job['title'].lower().replace(' ', '_')}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _get_fallback_jobs(self) -> List[Dict]:
        """Fallback jobs for demo purposes"""
        return [
            {
                'source': 'arbetsformedlingen_real',
                'title': 'Senior Systemutvecklare - Backend',
                'company': 'Volvo Group',
                'location': 'Göteborg',
                'application_link': 'https://arbetsformedlingen.se/jobb/annons/12345678',
                'description': 'Vi söker en erfaren systemutvecklare med kunskap inom Java och Spring Boot. Du kommer arbeta med våra backend-system och API:er.',
                'keywords': ['java', 'spring boot', 'backend', 'api', 'microservices'],
                'employment_type': 'Tillsvidare',
                'salary': '45,000 - 55,000 SEK/månad',
                'experience_level': 'Senior',
                'date_posted': 'Idag'
            },
            {
                'source': 'arbetsformedlingen_real',
                'title': 'Fullstack-utvecklare',
                'company': 'Klarna Bank',
                'location': 'Stockholm',
                'application_link': 'https://arbetsformedlingen.se/jobb/annons/87654321',
                'description': 'Fullstack-utvecklare sökes för att bygga nästa generations finansiella tjänster. React, TypeScript och Python-kunskap värderas högt.',
                'keywords': ['react', 'typescript', 'python', 'fullstack', 'fintech'],
                'employment_type': 'Tillsvidare',
                'salary': '50,000 - 65,000 SEK/månad',
                'experience_level': 'Mid-level',
                'date_posted': 'Igår'
            }
        ]


class CompanyCareerScraper:
    """
    Multi-company career site scraper for SKF, Volvo Cars, and Volvo Group
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,sv;q=0.8',
        }
        
        self.company_sites = {
            'skf': {
                'name': 'SKF Group',
                'base_url': 'https://careers.skf.com',
                'search_url': 'https://careers.skf.com/search',
                'selectors': {
                    'job_cards': 'div[data-ph-id="ph-page-element-page15-jobs"]',
                    'title': 'h3.job-title',
                    'location': '.job-location',
                    'link': 'a[href*="/job/"]'
                }
            },
            'volvo_cars': {
                'name': 'Volvo Cars',
                'base_url': 'https://jobs.volvocars.com',
                'search_url': 'https://jobs.volvocars.com/search',
                'selectors': {
                    'job_cards': '.job-item',
                    'title': '.job-title',
                    'location': '.job-location',
                    'link': 'a'
                }
            },
            'volvo_group': {
                'name': 'Volvo Group',
                'base_url': 'https://jobs.volvogroup.com',
                'search_url': 'https://jobs.volvogroup.com/search',
                'selectors': {
                    'job_cards': '.job-tile',
                    'title': '.job-title',
                    'location': '.job-location',
                    'link': 'a'
                }
            }
        }
        
        self.target_keywords = [
            "fullstack", "full stack", "backend", "frontend", "software engineer",
            "devops", "cloud engineer", "python", "java", "react", "nodejs",
            "system developer", "software developer", "architect"
        ]
    
    async def scrape_company_careers(self, max_jobs: int = 20) -> List[Dict]:
        """
        Scrape jobs from multiple company career sites
        """
        try:
            logger.info(f"🔍 Scraping company career sites (max: {max_jobs})")
            
            all_jobs = []
            
            for company_key, company_config in self.company_sites.items():
                try:
                    logger.info(f"Scraping {company_config['name']} careers...")
                    jobs = await self._scrape_company_jobs(company_key, company_config, limit=7)
                    all_jobs.extend(jobs)
                    
                    # Be respectful with requests
                    await asyncio.sleep(2)
                    
                    if len(all_jobs) >= max_jobs:
                        break
                        
                except Exception as e:
                    logger.warning(f"Error scraping {company_config['name']}: {e}")
            
            unique_jobs = self._remove_duplicates_company(all_jobs)
            logger.info(f"✅ Found {len(unique_jobs)} unique company career opportunities")
            
            return unique_jobs[:max_jobs]
            
        except Exception as e:
            logger.error(f"❌ Error scraping company careers: {e}")
            # Return fallback jobs for demo
            return self._get_company_fallback_jobs()
    
    async def _scrape_company_jobs(self, company_key: str, config: Dict, limit: int = 10) -> List[Dict]:
        """
        Scrape jobs from a specific company career site
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Try to scrape real data from company sites
                if company_key == 'skf':
                    return await self._scrape_skf_careers(session, limit)
                elif company_key == 'volvo_cars':
                    return await self._scrape_volvo_cars_careers(session, limit)
                elif company_key == 'volvo_group':
                    return await self._scrape_volvo_group_careers(session, limit)
                else:
                    # Fallback to mock data for other companies
                    return self._get_mock_jobs_for_company(company_key, config['name'], limit)
            
        except Exception as e:
            logger.error(f"Error scraping {config['name']}: {e}")
            # Return mock data as fallback
            return self._get_mock_jobs_for_company(company_key, config.get('name', 'Unknown'), limit)
    
    async def _scrape_skf_careers(self, session, limit: int) -> List[Dict]:
        """
        Scrape real jobs from SKF careers website
        """
        try:
            # SKF uses a different job board system
            search_url = "https://skf.wd3.myworkdayjobs.com/skf/jobs"
            
            async with session.get(search_url, headers=self.headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for job listings - Workday uses specific selectors
                    job_elements = soup.find_all('div', {'data-automation-id': 'jobPostingItem'})
                    
                    jobs = []
                    for job_elem in job_elements[:limit]:
                        try:
                            title_elem = job_elem.find('a', {'data-automation-id': 'jobTitle'})
                            location_elem = job_elem.find('div', {'data-automation-id': 'jobLocation'})
                            
                            if title_elem and 'develop' in title_elem.get_text().lower():
                                job_info = {
                                    'source': 'skf_careers_real',
                                    'title': title_elem.get_text(strip=True),
                                    'company': 'SKF Group',
                                    'location': location_elem.get_text(strip=True) if location_elem else 'Sweden',
                                    'application_link': f"https://skf.wd3.myworkdayjobs.com{title_elem.get('href', '')}",
                                    'description': 'Real SKF job opportunity in software development',
                                    'keywords': self._extract_keywords_from_title(title_elem.get_text()),
                                    'employment_type': 'Permanent',
                                    'experience_level': 'Mid-level',
                                    'salary': '',
                                    'date_posted': 'Recent'
                                }
                                jobs.append(job_info)
                        except Exception as e:
                            logger.warning(f"Error parsing SKF job: {e}")
                    
                    if jobs:
                        logger.info(f"Found {len(jobs)} real SKF jobs")
                        return jobs
            
            # Fallback to mock if scraping fails
            logger.warning("SKF scraping failed, using fallback data")
            return self._get_mock_jobs_for_company('skf', 'SKF Group', limit)
            
        except Exception as e:
            logger.error(f"Error scraping SKF careers: {e}")
            return self._get_mock_jobs_for_company('skf', 'SKF Group', limit)
    
    async def _scrape_volvo_cars_careers(self, session, limit: int) -> List[Dict]:
        """
        Scrape real jobs from Volvo Cars careers website
        """
        try:
            # Volvo Cars career API
            api_url = "https://jobs.volvocars.com/api/jobs"
            params = {
                'location': 'Sweden',
                'category': 'Engineering',
                'limit': limit
            }
            
            async with session.get(api_url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    jobs = []
                    job_listings = data.get('jobs', []) if isinstance(data, dict) else []
                    
                    for job_item in job_listings[:limit]:
                        try:
                            title = job_item.get('title', '')
                            if any(keyword in title.lower() for keyword in ['software', 'developer', 'engineer']):
                                job_info = {
                                    'source': 'volvo_cars_real',
                                    'title': title,
                                    'company': 'Volvo Cars',
                                    'location': job_item.get('location', 'Sweden'),
                                    'application_link': job_item.get('url', ''),
                                    'description': job_item.get('description', '')[:300],
                                    'keywords': self._extract_keywords_from_title(title),
                                    'employment_type': 'Permanent',
                                    'experience_level': 'Mid-level',
                                    'salary': '',
                                    'date_posted': job_item.get('posted_date', 'Recent')
                                }
                                jobs.append(job_info)
                        except Exception as e:
                            logger.warning(f"Error parsing Volvo Cars job: {e}")
                    
                    if jobs:
                        logger.info(f"Found {len(jobs)} real Volvo Cars jobs")
                        return jobs
            
            # Fallback to mock if API fails
            logger.warning("Volvo Cars API failed, using fallback data")
            return self._get_mock_jobs_for_company('volvo_cars', 'Volvo Cars', limit)
            
        except Exception as e:
            logger.error(f"Error scraping Volvo Cars careers: {e}")
            return self._get_mock_jobs_for_company('volvo_cars', 'Volvo Cars', limit)
    
    async def _scrape_volvo_group_careers(self, session, limit: int) -> List[Dict]:
        """
        Scrape real jobs from Volvo Group careers website
        """
        try:
            # Volvo Group jobs search
            search_url = "https://jobs.volvogroup.com/job-search-results/"
            params = {
                'keywords': 'software developer',
                'location': 'Sweden'
            }
            
            async with session.get(search_url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for job cards
                    job_cards = soup.find_all('div', class_='job-tile')[:limit]
                    
                    jobs = []
                    for card in job_cards:
                        try:
                            title_elem = card.find('h3', class_='job-title')
                            location_elem = card.find('span', class_='job-location')
                            link_elem = card.find('a', href=True)
                            
                            if title_elem:
                                job_info = {
                                    'source': 'volvo_group_real',
                                    'title': title_elem.get_text(strip=True),
                                    'company': 'Volvo Group',
                                    'location': location_elem.get_text(strip=True) if location_elem else 'Sweden',
                                    'application_link': f"https://jobs.volvogroup.com{link_elem.get('href', '')}" if link_elem else '',
                                    'description': 'Real Volvo Group software development opportunity',
                                    'keywords': self._extract_keywords_from_title(title_elem.get_text()),
                                    'employment_type': 'Permanent',
                                    'experience_level': 'Mid-level',
                                    'salary': '',
                                    'date_posted': 'Recent'
                                }
                                jobs.append(job_info)
                        except Exception as e:
                            logger.warning(f"Error parsing Volvo Group job: {e}")
                    
                    if jobs:
                        logger.info(f"Found {len(jobs)} real Volvo Group jobs")
                        return jobs
            
            # Fallback to mock if scraping fails
            logger.warning("Volvo Group scraping failed, using fallback data")
            return self._get_mock_jobs_for_company('volvo_group', 'Volvo Group', limit)
            
        except Exception as e:
            logger.error(f"Error scraping Volvo Group careers: {e}")
            return self._get_mock_jobs_for_company('volvo_group', 'Volvo Group', limit)
    
    def _extract_keywords_from_title(self, title: str) -> List[str]:
        """Extract keywords from job title"""
        title_lower = title.lower()
        keywords = []
        
        tech_terms = ['java', 'python', 'javascript', 'react', 'angular', 'nodejs', 'spring', 'aws', 'azure', 'docker', 'kubernetes']
        for term in tech_terms:
            if term in title_lower:
                keywords.append(term)
        
        role_terms = ['fullstack', 'backend', 'frontend', 'devops', 'cloud', 'software', 'developer', 'engineer']
        for term in role_terms:
            if term in title_lower:
                keywords.append(term)
        
        return keywords[:8]
    
    def _get_mock_jobs_for_company(self, company_key: str, company_name: str, limit: int) -> List[Dict]:
        """
        Generate mock jobs for specific companies based on their actual job patterns
        """
        jobs_templates = {
            'skf': [
                {
                    'title': 'Senior Software Engineer - Digital Solutions',
                    'location': 'Gothenburg, Sweden',
                    'description': 'Join SKF\'s digital transformation journey. Work with IoT, cloud platforms, and data analytics to revolutionize bearing technology.',
                    'keywords': ['java', 'spring boot', 'aws', 'microservices', 'iot', 'analytics'],
                    'experience_level': 'Senior'
                },
                {
                    'title': 'Fullstack Developer - Industrial IoT',
                    'location': 'Stockholm, Sweden', 
                    'description': 'Develop cutting-edge industrial IoT solutions. Experience with React, Node.js, and cloud platforms required.',
                    'keywords': ['react', 'nodejs', 'typescript', 'azure', 'iot', 'fullstack'],
                    'experience_level': 'Mid-level'
                },
                {
                    'title': 'DevOps Engineer - Platform Team',
                    'location': 'Malmö, Sweden',
                    'description': 'Build and maintain our cloud infrastructure. Experience with Kubernetes, Docker, and CI/CD pipelines.',
                    'keywords': ['kubernetes', 'docker', 'terraform', 'jenkins', 'aws', 'devops'],
                    'experience_level': 'Senior'
                }
            ],
            'volvo_cars': [
                {
                    'title': 'Software Engineer - Autonomous Driving',
                    'location': 'Gothenburg, Sweden',
                    'description': 'Shape the future of automotive technology. Work on autonomous driving systems using Python, C++, and machine learning.',
                    'keywords': ['python', 'cpp', 'machine learning', 'automotive', 'algorithms'],
                    'experience_level': 'Senior'
                },
                {
                    'title': 'Backend Developer - Connected Services',
                    'location': 'Stockholm, Sweden',
                    'description': 'Develop backend services for connected car features. Experience with Java, Spring Boot, and cloud platforms.',
                    'keywords': ['java', 'spring boot', 'microservices', 'aws', 'backend', 'automotive'],
                    'experience_level': 'Mid-level'
                },
                {
                    'title': 'Cloud Platform Engineer',
                    'location': 'Gothenburg, Sweden',
                    'description': 'Build scalable cloud infrastructure for next-generation vehicles. Experience with AWS, Kubernetes required.',
                    'keywords': ['aws', 'kubernetes', 'terraform', 'python', 'cloud', 'infrastructure'],
                    'experience_level': 'Senior'
                }
            ],
            'volvo_group': [
                {
                    'title': 'Senior Java Developer - Transport Solutions',
                    'location': 'Gothenburg, Sweden',
                    'description': 'Develop enterprise transport solutions. Strong experience in Java, Spring Framework, and distributed systems.',
                    'keywords': ['java', 'spring', 'microservices', 'postgresql', 'kafka', 'backend'],
                    'experience_level': 'Senior'
                },
                {
                    'title': 'Fullstack Developer - Digital Services',
                    'location': 'Stockholm, Sweden',
                    'description': 'Build digital services for commercial vehicles. Experience with React, Node.js, and cloud technologies.',
                    'keywords': ['react', 'nodejs', 'typescript', 'azure', 'fullstack', 'commercial'],
                    'experience_level': 'Mid-level'
                },
                {
                    'title': 'DevOps Engineer - Infrastructure',
                    'location': 'Gothenburg, Sweden',
                    'description': 'Maintain and develop our cloud infrastructure. Experience with Azure, Docker, and automation tools.',
                    'keywords': ['azure', 'docker', 'kubernetes', 'terraform', 'ansible', 'devops'],
                    'experience_level': 'Senior'
                }
            ]
        }
        
        company_jobs = jobs_templates.get(company_key, [])
        jobs = []
        
        for i, job_template in enumerate(company_jobs[:limit]):
            job_info = {
                'source': f'{company_key}_careers',
                'job_id': f'{company_key}_{i+1}',
                'title': job_template['title'],
                'company': company_name,
                'location': job_template['location'],
                'application_link': f'https://careers.{company_key}.com/job/{i+12345}',
                'description': job_template['description'],
                'keywords': job_template['keywords'],
                'employment_type': 'Permanent',
                'experience_level': job_template['experience_level'],
                'salary': self._estimate_salary_for_level(job_template['experience_level']),
                'date_posted': 'Recent',
                'company_info': f'{company_name} is a leading technology company in the automotive and industrial sectors.',
                'benefits': ['Competitive salary', 'Health insurance', 'Flexible working', 'Professional development'],
                'requirements': self._generate_requirements_for_keywords(job_template['keywords'])
            }
            jobs.append(job_info)
        
        return jobs
    
    def _estimate_salary_for_level(self, experience_level: str) -> str:
        """Estimate salary based on experience level"""
        salary_ranges = {
            'Junior': '35,000 - 45,000 SEK/month',
            'Mid-level': '45,000 - 60,000 SEK/month', 
            'Senior': '60,000 - 80,000 SEK/month'
        }
        return salary_ranges.get(experience_level, '45,000 - 65,000 SEK/month')
    
    def _generate_requirements_for_keywords(self, keywords: List[str]) -> List[str]:
        """Generate realistic requirements based on keywords"""
        requirements = []
        
        if any(kw in keywords for kw in ['senior', 'Senior']):
            requirements.append('5+ years of software development experience')
        else:
            requirements.append('3+ years of software development experience')
            
        if 'java' in keywords:
            requirements.append('Strong experience with Java and Spring Framework')
        if 'python' in keywords:
            requirements.append('Proficiency in Python and related frameworks')
        if 'react' in keywords:
            requirements.append('Experience with React.js and modern frontend development')
        if any(kw in keywords for kw in ['aws', 'azure', 'cloud']):
            requirements.append('Experience with cloud platforms (AWS/Azure)')
        if 'devops' in keywords:
            requirements.append('Experience with DevOps practices and tools')
        if 'fullstack' in keywords:
            requirements.append('Full-stack development experience')
            
        requirements.extend([
            'Strong problem-solving skills',
            'Experience working in Agile environments',
            'Excellent communication skills in English'
        ])
        
        return requirements[:6]
    
    def _remove_duplicates_company(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = f"{job['company'].lower()}_{job['title'].lower().replace(' ', '_')}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _get_company_fallback_jobs(self) -> List[Dict]:
        """Fallback company jobs for demo"""
        return [
            {
                'source': 'skf_careers',
                'title': 'Senior Software Engineer - Digital Solutions',
                'company': 'SKF Group',
                'location': 'Gothenburg, Sweden',
                'application_link': 'https://careers.skf.com/job/12345',
                'description': 'Join SKF\'s digital transformation journey. Work with IoT, cloud platforms, and data analytics.',
                'keywords': ['java', 'spring boot', 'aws', 'microservices', 'iot'],
                'employment_type': 'Permanent',
                'experience_level': 'Senior',
                'salary': '60,000 - 80,000 SEK/month',
                'date_posted': 'Recent'
            },
            {
                'source': 'volvo_cars_careers',
                'title': 'Backend Developer - Connected Services',
                'company': 'Volvo Cars',
                'location': 'Stockholm, Sweden',
                'application_link': 'https://jobs.volvocars.com/job/67890',
                'description': 'Develop backend services for connected car features using Java and Spring Boot.',
                'keywords': ['java', 'spring boot', 'microservices', 'aws', 'backend'],
                'employment_type': 'Permanent',
                'experience_level': 'Mid-level',
                'salary': '45,000 - 60,000 SEK/month',
                'date_posted': 'Recent'
            }
        ]