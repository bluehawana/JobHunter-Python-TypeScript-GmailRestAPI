import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings
import logging
import urllib.parse

logger = logging.getLogger(__name__)

class IndeedService:
    """Service for searching jobs using Indeed API and RapidAPI"""
    
    def __init__(self):
        self.rapidapi_key = settings.RAPIDAPI_KEY
        self.indeed_publisher_id = settings.INDEED_PUBLISHER_ID
        self.base_url = "https://indeed12.p.rapidapi.com"
        
    async def search_jobs(
        self, 
        query: str, 
        location: str = "", 
        num_results: int = 10,
        job_type: str = "all",
        date_posted: str = "all"
    ) -> List[Dict]:
        """
        Search for jobs using Indeed via RapidAPI
        
        Args:
            query: Job search query (e.g., "python developer")
            location: Location filter (e.g., "San Francisco, CA")
            num_results: Number of results to return
            job_type: Job type filter (fulltime, parttime, contract, internship, temporary)
            date_posted: Date filter (today, 3days, week, 2weeks, month)
            
        Returns:
            List of job postings with metadata
        """
        if not self.rapidapi_key:
            logger.error("RapidAPI key not configured for Indeed search")
            return []
        
        try:
            # Use RapidAPI Indeed endpoint
            jobs = await self._search_indeed_rapidapi(query, location, num_results, job_type, date_posted)
            
            # Enhance jobs with additional processing
            enhanced_jobs = []
            for job in jobs:
                enhanced_job = await self._enhance_job_data(job)
                enhanced_jobs.append(enhanced_job)
            
            return enhanced_jobs
            
        except Exception as e:
            logger.error(f"Error searching Indeed jobs: {e}")
            return []
    
    async def _search_indeed_rapidapi(
        self, 
        query: str, 
        location: str, 
        num_results: int,
        job_type: str,
        date_posted: str
    ) -> List[Dict]:
        """Search jobs using RapidAPI Indeed endpoint"""
        
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "indeed12.p.rapidapi.com"
        }
        
        params = {
            "query": query,
            "location": location,
            "page_id": "1",
            "locality": "us"
        }
        
        # Add optional filters
        if job_type != "all":
            params["job_type"] = job_type
        if date_posted != "all":
            params["date_posted"] = date_posted
        
        url = f"{self.base_url}/jobs/search"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_indeed_response(data)
                    else:
                        logger.error(f"Indeed API error: {response.status}")
                        error_text = await response.text()
                        logger.error(f"Error details: {error_text}")
                        return []
            except Exception as e:
                logger.error(f"Error calling Indeed API: {e}")
                return []
    
    def _parse_indeed_response(self, data: Dict) -> List[Dict]:
        """Parse Indeed API response into standardized format"""
        
        jobs = []
        hits = data.get("hits", [])
        
        for hit in hits:
            try:
                job = self._extract_indeed_job(hit)
                if job:
                    jobs.append(job)
            except Exception as e:
                logger.error(f"Error parsing Indeed job: {e}")
                continue
        
        return jobs
    
    def _extract_indeed_job(self, hit: Dict) -> Optional[Dict]:
        """Extract job information from Indeed API hit"""
        
        try:
            job = {
                "title": hit.get("title", "").strip(),
                "company": hit.get("company_name", "").strip(),
                "location": self._format_location(hit.get("location")),
                "description": hit.get("description", "").strip(),
                "url": hit.get("job_url", ""),
                "source": "indeed.com",
                "posting_date": self._parse_indeed_date(hit.get("pub_date_ts_milli")),
                "salary": self._extract_indeed_salary(hit),
                "job_type": self._extract_indeed_job_type(hit),
                "requirements": self._extract_requirements(hit.get("description", "")),
                "benefits": self._extract_benefits(hit.get("description", "")),
                "experience_level": self._extract_experience_level(hit.get("description", "")),
                "remote_option": self._check_remote_option(hit),
                "indeed_job_key": hit.get("job_key"),
                "scraped_at": datetime.utcnow(),
                "match_score": 0.0,  # Will be calculated later
                "confidence_score": 0.8,  # High confidence for direct API results
                "keywords": self._extract_job_keywords(hit.get("title", "") + " " + hit.get("description", ""))
            }
            
            return job
            
        except Exception as e:
            logger.error(f"Error extracting job data: {e}")
            return None
    
    def _format_location(self, location_data) -> Optional[str]:
        """Format location from Indeed API response"""
        if not location_data:
            return None
            
        if isinstance(location_data, dict):
            city = location_data.get("city", "")
            state = location_data.get("state", "")
            if city and state:
                return f"{city}, {state}"
            elif city:
                return city
        elif isinstance(location_data, str):
            return location_data
            
        return None
    
    def _parse_indeed_date(self, timestamp_ms) -> Optional[datetime]:
        """Parse Indeed timestamp to datetime"""
        if not timestamp_ms:
            return None
            
        try:
            # Convert milliseconds to seconds
            timestamp_s = int(timestamp_ms) / 1000
            return datetime.fromtimestamp(timestamp_s)
        except (ValueError, TypeError):
            return None
    
    def _extract_indeed_salary(self, hit: Dict) -> Optional[Dict]:
        """Extract salary information from Indeed job"""
        
        salary_info = hit.get("salary")
        estimated_salary = hit.get("estimated_salary")
        
        if salary_info:
            return {
                "min": salary_info.get("min"),
                "max": salary_info.get("max"),
                "currency": "USD",
                "type": salary_info.get("type", "yearly"),
                "source": "posted"
            }
        elif estimated_salary:
            return {
                "min": estimated_salary.get("min"),
                "max": estimated_salary.get("max"),
                "currency": "USD",
                "type": "yearly",
                "source": "estimated"
            }
            
        return None
    
    def _extract_indeed_job_type(self, hit: Dict) -> Optional[str]:
        """Extract job type from Indeed job"""
        
        job_types = hit.get("job_types", [])
        if job_types:
            return job_types[0].lower()
            
        # Fallback to description analysis
        description = hit.get("description", "").lower()
        
        if "full time" in description or "full-time" in description:
            return "fulltime"
        elif "part time" in description or "part-time" in description:
            return "parttime"
        elif "contract" in description:
            return "contract"
        elif "intern" in description:
            return "internship"
        elif "temporary" in description:
            return "temporary"
            
        return None
    
    def _extract_requirements(self, description: str) -> List[str]:
        """Extract job requirements from description"""
        
        if not description:
            return []
            
        requirements = []
        desc_lower = description.lower()
        
        # Common requirement patterns
        requirement_keywords = [
            "bachelor", "master", "degree", "certification", "experience",
            "python", "java", "javascript", "react", "angular", "vue",
            "sql", "database", "cloud", "aws", "azure", "docker", "kubernetes",
            "agile", "scrum", "git", "ci/cd", "testing", "rest api"
        ]
        
        for keyword in requirement_keywords:
            if keyword in desc_lower:
                requirements.append(keyword)
        
        return requirements[:10]  # Limit to top 10
    
    def _extract_benefits(self, description: str) -> List[str]:
        """Extract benefits from job description"""
        
        if not description:
            return []
            
        benefits = []
        desc_lower = description.lower()
        
        benefit_keywords = [
            "health insurance", "dental", "vision", "401k", "retirement",
            "vacation", "pto", "sick leave", "remote work", "flexible",
            "bonus", "stock options", "equity", "gym", "wellness"
        ]
        
        for benefit in benefit_keywords:
            if benefit in desc_lower:
                benefits.append(benefit)
        
        return benefits
    
    def _extract_experience_level(self, description: str) -> Optional[str]:
        """Extract experience level from description"""
        
        if not description:
            return None
            
        desc_lower = description.lower()
        
        if any(term in desc_lower for term in ["senior", "sr.", "lead", "principal", "architect"]):
            return "senior"
        elif any(term in desc_lower for term in ["junior", "jr.", "entry level", "entry-level", "associate"]):
            return "junior"
        elif any(term in desc_lower for term in ["mid level", "mid-level", "intermediate"]):
            return "mid"
        elif any(term in desc_lower for term in ["intern", "internship", "co-op"]):
            return "internship"
            
        return "mid"  # Default to mid-level
    
    def _check_remote_option(self, hit: Dict) -> bool:
        """Check if job offers remote work option"""
        
        # Check location
        location = str(hit.get("location", "")).lower()
        if "remote" in location:
            return True
            
        # Check description
        description = hit.get("description", "").lower()
        remote_indicators = [
            "remote", "work from home", "wfh", "telecommute", 
            "distributed", "anywhere"
        ]
        
        return any(indicator in description for indicator in remote_indicators)
    
    def _extract_job_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from job text"""
        
        if not text:
            return []
            
        text_lower = text.lower()
        
        # Technical keywords
        tech_keywords = [
            "python", "java", "javascript", "typescript", "react", "angular", "vue",
            "node.js", "express", "django", "flask", "spring", "laravel",
            "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
            "docker", "kubernetes", "aws", "azure", "gcp", "terraform",
            "git", "jenkins", "ci/cd", "devops", "agile", "scrum",
            "machine learning", "ai", "data science", "analytics", "big data",
            "microservices", "api", "rest", "graphql", "oauth", "jwt"
        ]
        
        found_keywords = []
        for keyword in tech_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords[:15]  # Limit to top 15
    
    async def _enhance_job_data(self, job: Dict) -> Dict:
        """Enhance job data with additional processing"""
        
        # Calculate match score based on various factors
        job["match_score"] = self._calculate_match_score(job)
        
        # Add job posting age
        if job.get("posting_date"):
            age_days = (datetime.utcnow() - job["posting_date"]).days
            job["posting_age_days"] = age_days
            job["is_recent"] = age_days <= 7
        
        # Categorize job level
        job["seniority_level"] = job.get("experience_level", "mid")
        
        # Add application deadline estimate (30 days from posting)
        if job.get("posting_date"):
            job["estimated_deadline"] = job["posting_date"] + timedelta(days=30)
        
        return job
    
    def _calculate_match_score(self, job: Dict) -> float:
        """Calculate job match score based on various factors"""
        
        score = 0.0
        
        # Recent postings get higher score
        if job.get("is_recent"):
            score += 0.2
        
        # Jobs with salary info get higher score
        if job.get("salary"):
            score += 0.2
        
        # Jobs with detailed descriptions get higher score
        description_length = len(job.get("description", ""))
        if description_length > 500:
            score += 0.2
        elif description_length > 200:
            score += 0.1
        
        # Jobs with many relevant keywords get higher score
        keywords_count = len(job.get("keywords", []))
        if keywords_count >= 10:
            score += 0.2
        elif keywords_count >= 5:
            score += 0.1
        
        # Remote jobs get a small bonus
        if job.get("remote_option"):
            score += 0.1
        
        # Jobs from known companies get a small bonus
        company = job.get("company", "").lower()
        if len(company) > 3 and company not in ["confidential", "private", "unnamed"]:
            score += 0.1
        
        return min(score, 1.0)
    
    async def get_job_details(self, job_key: str) -> Optional[Dict]:
        """Get detailed job information using Indeed job key"""
        
        if not self.rapidapi_key or not job_key:
            return None
        
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "indeed12.p.rapidapi.com"
        }
        
        url = f"{self.base_url}/job/{job_key}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_job_details(data)
                    else:
                        logger.error(f"Indeed job details API error: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Error fetching Indeed job details: {e}")
                return None
    
    def _parse_job_details(self, data: Dict) -> Dict:
        """Parse detailed job information"""
        
        return {
            "title": data.get("title"),
            "company": data.get("company_name"),
            "location": self._format_location(data.get("location")),
            "description": data.get("description"),
            "requirements": data.get("requirements", []),
            "benefits": data.get("benefits", []),
            "salary": self._extract_indeed_salary(data),
            "job_type": data.get("job_type"),
            "experience_level": data.get("experience_level"),
            "detailed": True,
            "fetched_at": datetime.utcnow()
        }
    
    async def search_by_company(self, company_name: str, location: str = "") -> List[Dict]:
        """Search for jobs by specific company"""
        
        query = f"company:{company_name}"
        return await self.search_jobs(query, location, num_results=20)
    
    async def search_similar_jobs(self, job_title: str, keywords: List[str], location: str = "") -> List[Dict]:
        """Search for similar jobs based on title and keywords"""
        
        query = f"{job_title} " + " ".join(keywords[:5])  # Limit keywords to avoid long queries
        return await self.search_jobs(query, location, num_results=15)