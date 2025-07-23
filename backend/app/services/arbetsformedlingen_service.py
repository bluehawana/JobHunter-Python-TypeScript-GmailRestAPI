import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings
import logging
import urllib.parse

logger = logging.getLogger(__name__)

class ArbetsformedlingenService:
    """Service for searching jobs using Arbetsförmedlingen (Swedish Employment Agency) API"""
    
    def __init__(self):
        self.base_url = "https://jobsearch.api.jobtechdev.se"
        # Arbetsförmedlingen API appears to be open and doesn't require API keys
        
    async def search_jobs(
        self, 
        query: str, 
        location: str = "", 
        num_results: int = 10,
        job_type: str = "all",
        date_posted: str = "all",
        experience_required: bool = False
    ) -> List[Dict]:
        """
        Search for jobs using Arbetsförmedlingen API
        
        Args:
            query: Job search query (e.g., "python developer")
            location: Location filter (e.g., "Stockholm" or county/region)
            num_results: Number of results to return (max 100)
            job_type: Job type filter 
            date_posted: Date filter (today, week, month, all)
            experience_required: Filter for jobs requiring experience
            
        Returns:
            List of job postings with metadata
        """
        try:
            jobs = await self._search_arbetsformedlingen_api(
                query, location, num_results, job_type, date_posted, experience_required
            )
            
            # Enhance jobs with additional processing
            enhanced_jobs = []
            for job in jobs:
                enhanced_job = await self._enhance_job_data(job)
                enhanced_jobs.append(enhanced_job)
            
            return enhanced_jobs
            
        except Exception as e:
            logger.error(f"Error searching Arbetsförmedlingen jobs: {e}")
            return []
    
    async def _search_arbetsformedlingen_api(
        self, 
        query: str, 
        location: str, 
        num_results: int,
        job_type: str,
        date_posted: str,
        experience_required: bool
    ) -> List[Dict]:
        """Search jobs using Arbetsförmedlingen API endpoint"""
        
        # Build search parameters
        params = {
            "q": query,  # Free text search
            "limit": min(num_results, 100),  # API limit
            "offset": 0
        }
        
        # Add location filter if specified
        if location:
            params["region"] = location
            
        # Add date filter
        if date_posted != "all":
            published_after = self._get_date_filter(date_posted)
            if published_after:
                params["published-after"] = published_after.isoformat()
        
        # Add experience filter
        if experience_required:
            params["experience-required"] = "true"
        
        url = f"{self.base_url}/search"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_arbetsformedlingen_response(data)
                    else:
                        logger.error(f"Arbetsförmedlingen API error: {response.status}")
                        error_text = await response.text()
                        logger.error(f"Error details: {error_text}")
                        return []
            except asyncio.TimeoutError:
                logger.error("Arbetsförmedlingen API request timed out")
                return []
            except Exception as e:
                logger.error(f"Error calling Arbetsförmedlingen API: {e}")
                return []
    
    def _get_date_filter(self, date_posted: str) -> Optional[datetime]:
        """Convert date filter to datetime for API"""
        now = datetime.utcnow()
        
        if date_posted == "today":
            return now - timedelta(days=1)
        elif date_posted == "week":
            return now - timedelta(days=7)
        elif date_posted == "month":
            return now - timedelta(days=30)
        
        return None
    
    def _parse_arbetsformedlingen_response(self, data: Dict) -> List[Dict]:
        """Parse Arbetsförmedlingen API response into standardized format"""
        
        jobs = []
        hits = data.get("hits", [])
        
        for hit in hits:
            try:
                job = self._extract_arbetsformedlingen_job(hit)
                if job:
                    jobs.append(job)
            except Exception as e:
                logger.error(f"Error parsing Arbetsförmedlingen job: {e}")
                continue
        
        return jobs
    
    def _extract_arbetsformedlingen_job(self, hit: Dict) -> Optional[Dict]:
        """Extract job information from Arbetsförmedlingen API hit"""
        
        try:
            # Arbetsförmedlingen job structure (based on common patterns)
            job_source = hit.get("_source", hit)  # Handle different response structures
            
            job = {
                "title": job_source.get("headline", "").strip(),
                "company": self._extract_employer(job_source),
                "location": self._extract_location(job_source),
                "description": self._extract_description(job_source),
                "url": self._extract_job_url(job_source),
                "source": "arbetsformedlingen.se",
                "posting_date": self._parse_date(job_source.get("publication_date")),
                "application_deadline": self._parse_date(job_source.get("last_publication_date")),
                "salary": self._extract_salary(job_source),
                "job_type": self._extract_job_type(job_source),
                "requirements": self._extract_requirements(job_source),
                "qualifications": self._extract_qualifications(job_source),
                "benefits": self._extract_benefits(job_source),
                "experience_level": self._extract_experience_level(job_source),
                "remote_option": self._check_remote_option(job_source),
                "job_id": job_source.get("id"),
                "external_id": job_source.get("external_id"),
                "occupation": job_source.get("occupation", {}).get("label"),
                "employment_type": job_source.get("employment_type", {}).get("label"),
                "working_hours_type": job_source.get("working_hours_type", {}).get("label"),
                "duration": job_source.get("duration", {}).get("label"),
                "scope_of_work": job_source.get("scope_of_work", {}).get("min"),
                "scraped_at": datetime.utcnow(),
                "match_score": 0.0,  # Will be calculated later
                "confidence_score": 0.9,  # High confidence for official API
                "keywords": self._extract_job_keywords(job_source),
                "original_data": job_source  # Keep for reference
            }
            
            return job
            
        except Exception as e:
            logger.error(f"Error extracting Arbetsförmedlingen job data: {e}")
            return None
    
    def _extract_employer(self, job_data: Dict) -> str:
        """Extract employer/company name"""
        employer = job_data.get("employer", {})
        if isinstance(employer, dict):
            return employer.get("name", "").strip()
        elif isinstance(employer, str):
            return employer.strip()
        return "Company not specified"
    
    def _extract_location(self, job_data: Dict) -> str:
        """Extract job location"""
        workplace_address = job_data.get("workplace_address", {})
        if isinstance(workplace_address, dict):
            municipality = workplace_address.get("municipality", "")
            region = workplace_address.get("region", "")
            
            if municipality and region:
                return f"{municipality}, {region}"
            elif municipality:
                return municipality
            elif region:
                return region
        
        # Fallback to other location fields
        location = job_data.get("location", {})
        if isinstance(location, dict):
            return location.get("label", "Location not specified")
        
        return "Location not specified"
    
    def _extract_description(self, job_data: Dict) -> str:
        """Extract job description"""
        description_parts = []
        
        # Main description
        description = job_data.get("description", {})
        if isinstance(description, dict):
            text = description.get("text", "")
            if text:
                description_parts.append(text)
        elif isinstance(description, str):
            description_parts.append(description)
        
        # Additional description fields
        for field in ["requirements", "conditions", "other_information"]:
            field_data = job_data.get(field, {})
            if isinstance(field_data, dict):
                text = field_data.get("text", "")
                if text:
                    description_parts.append(f"{field.title()}: {text}")
        
        return "\n\n".join(description_parts) if description_parts else "Description not available"
    
    def _extract_job_url(self, job_data: Dict) -> str:
        """Extract job URL"""
        # Try different URL fields
        url_fields = ["application_details", "webpage_url", "url"]
        
        for field in url_fields:
            url_data = job_data.get(field)
            if isinstance(url_data, dict):
                url = url_data.get("url", "")
                if url:
                    return url
            elif isinstance(url_data, str) and url_data.startswith("http"):
                return url_data
        
        # Fallback: construct URL from job ID
        job_id = job_data.get("id")
        if job_id:
            return f"https://arbetsformedlingen.se/platsbanken/annonser/{job_id}"
        
        return ""
    
    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse date string to datetime"""
        if not date_string:
            return None
            
        try:
            # Try different date formats
            date_formats = [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ"
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_string, fmt)
                except ValueError:
                    continue
                    
            return None
        except Exception:
            return None
    
    def _extract_salary(self, job_data: Dict) -> Optional[Dict]:
        """Extract salary information"""
        salary_data = job_data.get("salary_description")
        if not salary_data:
            return None
            
        # Try to extract numerical salary values
        import re
        
        salary_text = str(salary_data)
        
        # Look for Swedish Krona amounts
        kr_pattern = r'(\d{1,3}(?:\s?\d{3})*)\s*kr'
        amounts = re.findall(kr_pattern, salary_text, re.IGNORECASE)
        
        if amounts:
            # Convert amounts to integers
            numeric_amounts = []
            for amount in amounts:
                try:
                    # Remove spaces and convert to int
                    numeric_amount = int(amount.replace(' ', ''))
                    numeric_amounts.append(numeric_amount)
                except ValueError:
                    continue
            
            if len(numeric_amounts) >= 2:
                return {
                    "min": min(numeric_amounts),
                    "max": max(numeric_amounts),
                    "currency": "SEK",
                    "type": "monthly",
                    "description": salary_text
                }
            elif len(numeric_amounts) == 1:
                return {
                    "min": numeric_amounts[0],
                    "max": None,
                    "currency": "SEK",
                    "type": "monthly",
                    "description": salary_text
                }
        
        return {
            "description": salary_text,
            "currency": "SEK"
        }
    
    def _extract_job_type(self, job_data: Dict) -> Optional[str]:
        """Extract job type"""
        employment_type = job_data.get("employment_type", {})
        if isinstance(employment_type, dict):
            label = employment_type.get("label", "").lower()
            
            # Map Swedish terms to English
            type_mapping = {
                "tillsvidare": "permanent",
                "visstid": "temporary",
                "vikariat": "temporary",
                "provanställning": "probation",
                "säsong": "seasonal",
                "heltid": "fulltime",
                "deltid": "parttime"
            }
            
            for swedish, english in type_mapping.items():
                if swedish in label:
                    return english
            
            return label if label else None
        
        return None
    
    def _extract_requirements(self, job_data: Dict) -> List[str]:
        """Extract job requirements"""
        requirements = []
        
        # Extract from requirements field
        req_data = job_data.get("requirements", {})
        if isinstance(req_data, dict):
            text = req_data.get("text", "")
            if text:
                # Simple requirement extraction
                req_lines = text.split('\n')
                for line in req_lines:
                    line = line.strip('- •*').strip()
                    if line and len(line) > 10:  # Filter out short/empty lines
                        requirements.append(line)
        
        return requirements[:10]  # Limit to top 10
    
    def _extract_qualifications(self, job_data: Dict) -> List[str]:
        """Extract required qualifications"""
        qualifications = []
        
        # Check for qualification fields
        qual_fields = ["qualifications", "education", "experience"]
        
        for field in qual_fields:
            qual_data = job_data.get(field, {})
            if isinstance(qual_data, dict):
                text = qual_data.get("text", "")
                if text:
                    qualifications.append(text)
        
        return qualifications
    
    def _extract_benefits(self, job_data: Dict) -> List[str]:
        """Extract job benefits"""
        benefits = []
        
        conditions = job_data.get("conditions", {})
        if isinstance(conditions, dict):
            text = conditions.get("text", "")
            if text:
                # Look for benefit keywords in Swedish/English
                benefit_keywords = [
                    "förmåner", "benefits", "pension", "försäkring", "insurance",
                    "semester", "vacation", "flexibel", "flexible", "hälsa", "health",
                    "friskvård", "wellness", "bil", "car", "telefon", "phone"
                ]
                
                text_lower = text.lower()
                for keyword in benefit_keywords:
                    if keyword in text_lower:
                        benefits.append(keyword)
        
        return list(set(benefits))  # Remove duplicates
    
    def _extract_experience_level(self, job_data: Dict) -> Optional[str]:
        """Extract experience level"""
        # Check various fields for experience indicators
        text_fields = [
            job_data.get("description", {}).get("text", ""),
            job_data.get("requirements", {}).get("text", ""),
            job_data.get("qualifications", {}).get("text", "")
        ]
        
        combined_text = " ".join(text_fields).lower()
        
        # Swedish and English experience keywords
        if any(term in combined_text for term in ["senior", "erfaren", "många år", "years experience", "specialist"]):
            return "senior"
        elif any(term in combined_text for term in ["junior", "nyexaminerad", "entry level", "trainee", "praktikant"]):
            return "junior"
        elif any(term in combined_text for term in ["medior", "mellannivå", "intermediate", "några år"]):
            return "mid"
        
        return "mid"  # Default
    
    def _check_remote_option(self, job_data: Dict) -> bool:
        """Check if job offers remote work"""
        # Check various fields for remote work indicators
        text_fields = [
            job_data.get("description", {}).get("text", ""),
            job_data.get("conditions", {}).get("text", ""),
            str(job_data.get("workplace_address", {}))
        ]
        
        combined_text = " ".join(text_fields).lower()
        
        # Swedish and English remote work keywords
        remote_keywords = [
            "distans", "hemarbete", "remote", "work from home", 
            "hemifrån", "flexibelt", "anywhere", "virtuell"
        ]
        
        return any(keyword in combined_text for keyword in remote_keywords)
    
    def _extract_job_keywords(self, job_data: Dict) -> List[str]:
        """Extract relevant keywords from job posting"""
        
        text_content = f"{job_data.get('headline', '')} {self._extract_description(job_data)}".lower()
        
        # Swedish and international tech keywords
        tech_keywords = [
            # Programming languages
            "python", "java", "javascript", "typescript", "c#", "c++", "php", "ruby", "go", "rust",
            # Frameworks
            "react", "angular", "vue", "django", "flask", "spring", "express", "laravel", ".net",
            # Databases
            "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform",
            # Swedish specific terms
            "systemutvecklare", "mjukvaruutvecklare", "programmerare", "utvecklare",
            "dataanalytiker", "systemarkitekt", "projektledare", "agil", "scrum"
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
        
        # Official employers get bonus
        company = job.get("company", "").lower()
        if company and "not specified" not in company:
            score += 0.1
        
        return min(score, 1.0)
    
    def _categorize_job(self, job: Dict) -> str:
        """Categorize job based on title and description"""
        
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        keywords = [kw.lower() for kw in job.get("keywords", [])]
        
        content = f"{title} {description} {' '.join(keywords)}"
        
        categories = {
            "software_engineering": ["utvecklare", "programmerare", "developer", "engineer", "software"],
            "data_science": ["dataanalytiker", "data scientist", "analyst", "machine learning", "ai"],
            "project_management": ["projektledare", "project manager", "scrum master", "agil"],
            "system_administration": ["systemadministratör", "sysadmin", "infrastructure", "drift"],
            "web_development": ["webbutvecklare", "frontend", "backend", "fullstack"],
            "mobile_development": ["mobilutvecklare", "ios", "android", "app developer"],
            "devops": ["devops", "infrastructure", "kubernetes", "docker", "cloud"],
            "security": ["säkerhet", "security", "cybersecurity", "infosec"],
            "consulting": ["konsult", "consultant", "rådgivare", "advisor"]
        }
        
        for category, keywords_list in categories.items():
            if any(keyword in content for keyword in keywords_list):
                return category
        
        return "general"
    
    async def get_job_details(self, job_id: str) -> Optional[Dict]:
        """Get detailed job information using Arbetsförmedlingen job ID"""
        
        if not job_id:
            return None
        
        url = f"{self.base_url}/ad/{job_id}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._extract_arbetsformedlingen_job(data)
                    else:
                        logger.error(f"Arbetsförmedlingen job details API error: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Error fetching Arbetsförmedlingen job details: {e}")
                return None
    
    async def search_by_occupation(self, occupation_code: str, location: str = "") -> List[Dict]:
        """Search for jobs by occupation code (SSYK - Swedish Standard Classification of Occupations)"""
        
        params = {
            "occupation-group": occupation_code,
            "limit": 50
        }
        
        if location:
            params["region"] = location
        
        url = f"{self.base_url}/search"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        jobs = self._parse_arbetsformedlingen_response(data)
                        
                        enhanced_jobs = []
                        for job in jobs:
                            enhanced_job = await self._enhance_job_data(job)
                            enhanced_jobs.append(enhanced_job)
                        
                        return enhanced_jobs
                    else:
                        logger.error(f"Arbetsförmedlingen occupation search error: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"Error searching by occupation: {e}")
                return []
    
    async def get_statistics(self, region: str = None) -> Dict:
        """Get job market statistics from Arbetsförmedlingen"""
        
        params = {}
        if region:
            params["region"] = region
        
        url = f"{self.base_url}/statistics"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Arbetsförmedlingen statistics API error: {response.status}")
                        return {}
            except Exception as e:
                logger.error(f"Error fetching statistics: {e}")
                return {}