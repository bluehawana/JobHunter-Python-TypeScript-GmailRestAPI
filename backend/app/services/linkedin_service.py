import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings
import logging
import urllib.parse
import os

logger = logging.getLogger(__name__)

class LinkedInService:
    """Service for searching jobs using LinkedIn API"""
    
    def __init__(self):
        self.base_url = "https://api.linkedin.com/v2"
        # LinkedIn API credentials - these should be stored in environment variables
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID", "77duha47hcbh8o")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET", "WPL_AP1.KCsCGIG1HHXfY8LV.1OEJWQ==")
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN", "AQUpeVun7rV5mxXjIEgIy1PC7H4tHEcNZz9A03H2OFCfg1Nd7mHu7BxWZvC3uY1v_fZZjWSVVbsnaB4HiqDi7zhmZdywj6VtExEt-GvCg4Vs8agrPWBwHMPDJyB1X5NbI35U98lEjI5eSAzh4njG05Vbk1SWl5Er4O_SY2We-D6NWloGZHmHJa_N3bm3OTzXNOoG6WSSXC1jsmHEMaeWUwaWbM7yrSAcZnbZMCHGd-9F1j0n-NiAnBW_UPWN689h4N2vfkQiIN2c-ccLzCOXacnQgFh0lb5NVFUN9kdZrDeS8_XCV12risfNaEALOV2-olZfdGOIO3HKt_bW6ShFLsGGpCbzFA")
        
    async def search_jobs(
        self, 
        query: str, 
        location: str = "", 
        num_results: int = 10,
        job_type: str = "all",
        date_posted: str = "all",
        experience_level: str = "all"
    ) -> List[Dict]:
        """
        Search for jobs using LinkedIn API
        
        Args:
            query: Job search query (e.g., "python developer")
            location: Location filter (e.g., "San Francisco, CA")
            num_results: Number of results to return (max 200)
            job_type: Job type filter 
            date_posted: Date filter (today, week, month, all)
            experience_level: Experience level filter (entry, mid, senior, all)
            
        Returns:
            List of job postings with metadata
        """
        try:
            jobs = await self._search_linkedin_api(
                query, location, num_results, job_type, date_posted, experience_level
            )
            
            # Enhance jobs with additional processing
            enhanced_jobs = []
            for job in jobs:
                enhanced_job = await self._enhance_job_data(job)
                enhanced_jobs.append(enhanced_job)
            
            return enhanced_jobs
            
        except Exception as e:
            logger.error(f"Error searching LinkedIn jobs: {e}")
            return []
    
    async def _search_linkedin_api(
        self, 
        query: str, 
        location: str, 
        num_results: int,
        job_type: str,
        date_posted: str,
        experience_level: str
    ) -> List[Dict]:
        """Search jobs using LinkedIn Job Search API"""
        
        # Build search parameters
        params = {
            "q": "keyword",
            "keywords": query,
            "count": min(num_results, 200),  # LinkedIn API limit
            "start": 0
        }
        
        # Add location filter if specified
        if location:
            params["location"] = location
            
        # Add date filter
        if date_posted != "all":
            date_range = self._get_date_filter(date_posted)
            if date_range:
                params["dateRange"] = date_range
        
        # Add experience level filter
        if experience_level != "all":
            params["experienceLevel"] = self._map_experience_level(experience_level)
        
        # Add job type filter
        if job_type != "all":
            params["jobType"] = self._map_job_type(job_type)
        
        url = f"{self.base_url}/jobSearch"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_linkedin_response(data)
                    elif response.status == 401:
                        logger.error("LinkedIn API authentication failed - token may be expired")
                        return []
                    else:
                        logger.error(f"LinkedIn API error: {response.status}")
                        error_text = await response.text()
                        logger.error(f"Error details: {error_text}")
                        return []
            except asyncio.TimeoutError:
                logger.error("LinkedIn API request timed out")
                return []
            except Exception as e:
                logger.error(f"Error calling LinkedIn API: {e}")
                return []
    
    def _get_date_filter(self, date_posted: str) -> Optional[str]:
        """Convert date filter to LinkedIn API format"""
        date_mapping = {
            "today": "r86400",      # Past 24 hours
            "week": "r604800",      # Past week
            "month": "r2592000"     # Past month
        }
        return date_mapping.get(date_posted)
    
    def _map_experience_level(self, experience_level: str) -> str:
        """Map experience level to LinkedIn API format"""
        level_mapping = {
            "entry": "1",
            "mid": "2,3",
            "senior": "4,5,6"
        }
        return level_mapping.get(experience_level, "")
    
    def _map_job_type(self, job_type: str) -> str:
        """Map job type to LinkedIn API format"""
        type_mapping = {
            "fulltime": "F",
            "parttime": "P", 
            "contract": "C",
            "temporary": "T",
            "internship": "I"
        }
        return type_mapping.get(job_type, "")
    
    def _parse_linkedin_response(self, data: Dict) -> List[Dict]:
        """Parse LinkedIn API response into standardized format"""
        
        jobs = []
        elements = data.get("elements", [])
        
        for element in elements:
            try:
                job = self._extract_linkedin_job(element)
                if job:
                    jobs.append(job)
            except Exception as e:
                logger.error(f"Error parsing LinkedIn job: {e}")
                continue
        
        return jobs
    
    def _extract_linkedin_job(self, element: Dict) -> Optional[Dict]:
        """Extract job information from LinkedIn API element"""
        
        try:
            # LinkedIn job posting structure
            job = {
                "title": element.get("title", "").strip(),
                "company": self._extract_company_name(element),
                "location": self._extract_location(element),
                "description": self._extract_description(element),
                "url": self._extract_job_url(element),
                "source": "linkedin.com",
                "posting_date": self._parse_date(element.get("listedAt")),
                "application_deadline": self._parse_date(element.get("expireAt")),
                "salary": self._extract_salary(element),
                "job_type": self._extract_job_type(element),
                "requirements": self._extract_requirements(element),
                "benefits": self._extract_benefits(element),
                "experience_level": self._extract_experience_level(element),
                "remote_option": self._check_remote_option(element),
                "job_id": str(element.get("id", "")),
                "external_id": element.get("jobPostingId"),
                "industry": self._extract_industry(element),
                "company_size": self._extract_company_size(element),
                "employment_type": element.get("employmentStatus"),
                "seniority_level": element.get("seniorityLevel"),
                "job_functions": self._extract_job_functions(element),
                "scraped_at": datetime.utcnow(),
                "match_score": 0.0,  # Will be calculated later
                "confidence_score": 0.95,  # High confidence for official API
                "keywords": self._extract_job_keywords(element),
                "original_data": element  # Keep for reference
            }
            
            return job
            
        except Exception as e:
            logger.error(f"Error extracting LinkedIn job data: {e}")
            return None
    
    def _extract_company_name(self, element: Dict) -> str:
        """Extract company name from LinkedIn job element"""
        company_info = element.get("companyDetails", {})
        if isinstance(company_info, dict):
            company = company_info.get("company", {})
            if isinstance(company, str):
                return company
            elif isinstance(company, dict):
                return company.get("name", "Company not specified")
        return "Company not specified"
    
    def _extract_location(self, element: Dict) -> str:
        """Extract job location from LinkedIn element"""
        location_info = element.get("formattedLocation", "")
        if location_info:
            return location_info
        
        # Fallback to structured location data
        location_data = element.get("locationDescription", "")
        if location_data:
            return location_data
        
        return "Location not specified"
    
    def _extract_description(self, element: Dict) -> str:
        """Extract job description from LinkedIn element"""
        description_parts = []
        
        # Main description
        description = element.get("description", {})
        if isinstance(description, dict):
            text = description.get("text", "")
            if text:
                description_parts.append(text)
        elif isinstance(description, str):
            description_parts.append(description)
        
        # Additional description fields
        for field in ["criteria", "benefits", "qualifications"]:
            field_data = element.get(field, {})
            if isinstance(field_data, dict):
                text = field_data.get("text", "")
                if text:
                    description_parts.append(f"{field.title()}: {text}")
        
        return "\n\n".join(description_parts) if description_parts else "Description not available"
    
    def _extract_job_url(self, element: Dict) -> str:
        """Extract job URL from LinkedIn element"""
        # LinkedIn job URLs typically follow this pattern
        job_id = element.get("id") or element.get("jobPostingId")
        if job_id:
            return f"https://www.linkedin.com/jobs/view/{job_id}"
        
        # Fallback to any URL in the element
        url_fields = ["applyUrl", "viewJobUrl", "url"]
        for field in url_fields:
            url = element.get(field)
            if url and url.startswith("http"):
                return url
        
        return ""
    
    def _parse_date(self, timestamp: int) -> Optional[datetime]:
        """Parse LinkedIn timestamp to datetime"""
        if not timestamp:
            return None
            
        try:
            # LinkedIn timestamps are typically in milliseconds
            return datetime.fromtimestamp(timestamp / 1000)
        except (ValueError, TypeError):
            return None
    
    def _extract_salary(self, element: Dict) -> Optional[Dict]:
        """Extract salary information from LinkedIn element"""
        salary_data = element.get("salaryInsights")
        if not salary_data:
            return None
        
        try:
            salary_info = {
                "currency": "USD",  # Default assumption
                "type": "yearly"    # Default assumption
            }
            
            # Extract salary range
            if "baseRange" in salary_data:
                base_range = salary_data["baseRange"]
                if "min" in base_range:
                    salary_info["min"] = int(base_range["min"])
                if "max" in base_range:
                    salary_info["max"] = int(base_range["max"])
            
            # Extract currency if available
            if "currency" in salary_data:
                salary_info["currency"] = salary_data["currency"]
            
            return salary_info if "min" in salary_info or "max" in salary_info else None
            
        except (ValueError, KeyError, TypeError):
            return None
    
    def _extract_job_type(self, element: Dict) -> Optional[str]:
        """Extract job type from LinkedIn element"""
        employment_type = element.get("employmentStatus", "")
        
        # Map LinkedIn employment types to standard types
        type_mapping = {
            "FULL_TIME": "fulltime",
            "PART_TIME": "parttime",
            "CONTRACT": "contract",
            "TEMPORARY": "temporary",
            "INTERNSHIP": "internship",
            "VOLUNTEER": "volunteer"
        }
        
        return type_mapping.get(employment_type.upper(), "fulltime")
    
    def _extract_requirements(self, element: Dict) -> List[str]:
        """Extract job requirements from LinkedIn element"""
        requirements = []
        
        # Look for requirements in description or specific fields
        description = self._extract_description(element).lower()
        
        # Common requirement patterns
        requirement_patterns = [
            r"requirements?[:\s]*([^.]+)",
            r"qualifications?[:\s]*([^.]+)",
            r"must have[:\s]*([^.]+)",
            r"required[:\s]*([^.]+)"
        ]
        
        import re
        for pattern in requirement_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                # Clean up and split requirements
                req_items = [item.strip() for item in match.split(",") if item.strip()]
                requirements.extend(req_items[:3])  # Limit to avoid too many
        
        return requirements[:10]  # Limit to top 10
    
    def _extract_benefits(self, element: Dict) -> List[str]:
        """Extract job benefits from LinkedIn element"""
        benefits = []
        
        description = self._extract_description(element).lower()
        
        # Common benefit keywords
        benefit_keywords = [
            "health insurance", "dental", "vision", "401k", "retirement",
            "vacation", "pto", "flexible", "remote", "work from home",
            "gym", "fitness", "free lunch", "stock options", "equity"
        ]
        
        for benefit in benefit_keywords:
            if benefit in description:
                benefits.append(benefit)
        
        return list(set(benefits))  # Remove duplicates
    
    def _extract_experience_level(self, element: Dict) -> Optional[str]:
        """Extract experience level from LinkedIn element"""
        seniority = element.get("seniorityLevel", "")
        
        # Map LinkedIn seniority levels
        seniority_mapping = {
            "INTERNSHIP": "internship",
            "ENTRY_LEVEL": "junior",
            "ASSOCIATE": "junior",
            "MID_SENIOR": "mid",
            "DIRECTOR": "senior",
            "EXECUTIVE": "senior"
        }
        
        mapped_level = seniority_mapping.get(seniority.upper(), "mid")
        
        # Also check job title for experience indicators
        title = element.get("title", "").lower()
        if any(term in title for term in ["senior", "sr.", "lead", "principal"]):
            return "senior"
        elif any(term in title for term in ["junior", "jr.", "entry", "associate"]):
            return "junior"
        elif any(term in title for term in ["intern", "internship"]):
            return "internship"
        
        return mapped_level
    
    def _check_remote_option(self, element: Dict) -> bool:
        """Check if job offers remote work"""
        # Check location and description for remote indicators
        location = self._extract_location(element).lower()
        description = self._extract_description(element).lower()
        
        remote_keywords = [
            "remote", "work from home", "telecommute", "distributed",
            "anywhere", "virtual", "home office"
        ]
        
        content = f"{location} {description}"
        return any(keyword in content for keyword in remote_keywords)
    
    def _extract_industry(self, element: Dict) -> Optional[str]:
        """Extract industry from LinkedIn element"""
        company_details = element.get("companyDetails", {})
        if isinstance(company_details, dict):
            industry_info = company_details.get("company", {})
            if isinstance(industry_info, dict):
                return industry_info.get("industry", {}).get("name")
        return None
    
    def _extract_company_size(self, element: Dict) -> Optional[str]:
        """Extract company size from LinkedIn element"""
        company_details = element.get("companyDetails", {})
        if isinstance(company_details, dict):
            company_info = company_details.get("company", {})
            if isinstance(company_info, dict):
                return company_info.get("staffCount")
        return None
    
    def _extract_job_functions(self, element: Dict) -> List[str]:
        """Extract job functions from LinkedIn element"""
        functions = element.get("jobFunctions", [])
        if isinstance(functions, list):
            return [func.get("name", "") for func in functions if isinstance(func, dict)]
        return []
    
    def _extract_job_keywords(self, element: Dict) -> List[str]:
        """Extract relevant keywords from LinkedIn job posting"""
        
        text_content = f"{element.get('title', '')} {self._extract_description(element)}".lower()
        
        # Technology and skill keywords
        tech_keywords = [
            # Programming languages
            "python", "java", "javascript", "typescript", "c#", "c++", "php", "ruby", "go", "rust",
            # Frameworks and libraries
            "react", "angular", "vue", "django", "flask", "spring", "express", ".net", "laravel",
            # Databases
            "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "oracle",
            # Cloud and DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible",
            # Data and AI
            "machine learning", "data science", "ai", "analytics", "big data", "spark", "pandas",
            # Methodologies
            "agile", "scrum", "kanban", "devops", "ci/cd", "microservices"
        ]
        
        found_keywords = []
        for keyword in tech_keywords:
            if keyword in text_content:
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
        
        # Categorize job
        job["category"] = self._categorize_job(job)
        
        # Add application deadline info
        if job.get("application_deadline"):
            days_until_deadline = (job["application_deadline"] - datetime.utcnow()).days
            job["days_until_deadline"] = max(0, days_until_deadline)
            job["application_urgent"] = days_until_deadline <= 7
        
        # Add ATS score estimation
        job["ats_score"] = self._calculate_ats_score(job)
        
        return job
    
    def _calculate_match_score(self, job: Dict) -> float:
        """Calculate job match score based on various factors"""
        
        score = 0.0
        
        # Recent postings get higher score
        if job.get("is_recent"):
            score += 0.2
        
        # Jobs with salary info get higher score
        if job.get("salary") and job["salary"].get("min"):
            score += 0.2
        
        # Jobs with detailed descriptions get higher score
        description_length = len(job.get("description", ""))
        if description_length > 500:
            score += 0.2
        elif description_length > 200:
            score += 0.1
        
        # Jobs with many relevant keywords get higher score
        keywords_count = len(job.get("keywords", []))
        if keywords_count >= 8:
            score += 0.2
        elif keywords_count >= 4:
            score += 0.1
        
        # Remote jobs get a small bonus
        if job.get("remote_option"):
            score += 0.1
        
        # LinkedIn premium score (official API)
        score += 0.1
        
        return min(score, 1.0)
    
    def _categorize_job(self, job: Dict) -> str:
        """Categorize job based on title, description, and functions"""
        
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        keywords = [kw.lower() for kw in job.get("keywords", [])]
        functions = [f.lower() for f in job.get("job_functions", [])]
        
        content = f"{title} {description} {' '.join(keywords)} {' '.join(functions)}"
        
        categories = {
            "software_engineering": ["developer", "engineer", "programmer", "software", "coding"],
            "data_science": ["data scientist", "analyst", "machine learning", "ai", "analytics"],
            "product_management": ["product manager", "product owner", "pm", "product"],
            "design": ["designer", "ux", "ui", "graphic", "visual", "creative"],
            "marketing": ["marketing", "growth", "digital marketing", "content", "social media"],
            "sales": ["sales", "business development", "account", "revenue"],
            "devops": ["devops", "sre", "infrastructure", "cloud", "deployment"],
            "frontend": ["frontend", "front-end", "ui", "react", "angular", "vue"],
            "backend": ["backend", "back-end", "api", "server", "database"],
            "mobile": ["mobile", "ios", "android", "flutter", "react native"],
            "management": ["manager", "director", "head", "chief", "vp", "cto", "ceo"],
            "qa": ["qa", "test", "quality", "automation", "sdet"],
            "security": ["security", "cybersecurity", "infosec", "penetration"]
        }
        
        for category, category_keywords in categories.items():
            if any(keyword in content for keyword in category_keywords):
                return category
        
        return "general"
    
    def _calculate_ats_score(self, job: Dict) -> float:
        """Calculate ATS compatibility score for LinkedIn jobs"""
        
        score = 0.8  # Start with high score for LinkedIn jobs
        
        # Jobs with detailed descriptions score higher
        description = job.get("description", "")
        if len(description) > 300:
            score += 0.1
        
        # Jobs with salary information score higher
        if job.get("salary"):
            score += 0.05
        
        # Jobs with requirements listed score higher
        if job.get("requirements"):
            score += 0.05
        
        return min(score, 1.0)
    
    async def get_job_details(self, job_id: str) -> Optional[Dict]:
        """Get detailed job information using LinkedIn job ID"""
        
        if not job_id:
            return None
        
        url = f"{self.base_url}/jobs/{job_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._extract_linkedin_job(data)
                    else:
                        logger.error(f"LinkedIn job details API error: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Error fetching LinkedIn job details: {e}")
                return None
    
    async def refresh_access_token(self) -> bool:
        """Refresh LinkedIn access token if needed"""
        # This would implement OAuth token refresh logic
        # For now, return True assuming token is valid
        return True