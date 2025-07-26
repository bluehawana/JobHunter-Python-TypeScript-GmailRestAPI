import asyncio
from typing import List, Dict, Optional, Set
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

from app.services.google_jobs_service import GoogleJobsService
from app.services.indeed_service import IndeedService
from app.services.gmail_service import GmailService
from app.services.arbetsformedlingen_service import ArbetsformedlingenService
from app.services.linkedin_service import LinkedInService
from app.core.database import get_async_session
from app.models.job import JobPosting, JobCreate
import re

logger = logging.getLogger(__name__)

@dataclass
class JobSearchRequest:
    """Job search request parameters"""
    query: str
    location: str = ""
    max_results: int = 50
    include_remote: bool = True
    job_types: List[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    date_posted: str = "all"  # today, week, month, all
    experience_levels: List[str] = None  # junior, mid, senior
    companies_exclude: List[str] = None
    keywords_required: List[str] = None
    keywords_exclude: List[str] = None

class JobAggregationService:
    """Unified service for aggregating jobs from multiple sources"""
    
    def __init__(self):
        self.google_service = GoogleJobsService()
        self.indeed_service = IndeedService()
        self.arbetsformedlingen_service = ArbetsformedlingenService()
        self.linkedin_service = LinkedInService()
        self.gmail_service = None  # Will be initialized with user credentials
        
    async def search_jobs(self, search_request: JobSearchRequest, user_id: str) -> List[Dict]:
        """
        Search jobs from all available sources and return unified results
        
        Args:
            search_request: Search parameters
            user_id: User ID for personalization and storage
            
        Returns:
            List of unified job postings sorted by relevance
        """
        logger.info(f"Starting job search for user {user_id}: {search_request.query}")
        
        # Run searches in parallel
        search_tasks = []
        
        # Google Jobs search
        search_tasks.append(
            self._search_google_jobs(search_request)
        )
        
        # Indeed search
        search_tasks.append(
            self._search_indeed_jobs(search_request)
        )
        
        # Arbetsförmedlingen search (Swedish Employment Agency)
        search_tasks.append(
            self._search_arbetsformedlingen_jobs(search_request)
        )
        
        # LinkedIn search
        search_tasks.append(
            self._search_linkedin_jobs(search_request)
        )
        
        # Gmail search (if user has Gmail connected)
        if await self._has_gmail_access(user_id):
            search_tasks.append(
                self._search_gmail_jobs(search_request, user_id)
            )
        
        # Execute all searches in parallel
        try:
            search_results = await asyncio.gather(*search_tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Error during parallel job search: {e}")
            search_results = [[], [], []]
        
        # Combine and process results
        all_jobs = []
        for i, results in enumerate(search_results):
            if isinstance(results, Exception):
                logger.error(f"Search {i} failed: {results}")
                continue
            if isinstance(results, list):
                all_jobs.extend(results)
        
        logger.info(f"Found {len(all_jobs)} total jobs before processing")
        
        # Process and filter jobs
        processed_jobs = await self._process_jobs(all_jobs, search_request, user_id)
        
        # Remove duplicates
        unique_jobs = self._remove_duplicates(processed_jobs)
        
        # Apply filters
        filtered_jobs = self._apply_filters(unique_jobs, search_request)
        
        # Sort by relevance and match score
        sorted_jobs = self._sort_jobs(filtered_jobs, search_request)
        
        # Limit results
        final_jobs = sorted_jobs[:search_request.max_results]
        
        # Save search results to database
        await self._save_search_results(final_jobs, search_request, user_id)
        
        logger.info(f"Returning {len(final_jobs)} jobs after processing")
        return final_jobs
    
    async def _search_google_jobs(self, search_request: JobSearchRequest) -> List[Dict]:
        """Search jobs using Google Custom Search"""
        try:
            return await self.google_service.search_jobs(
                query=search_request.query,
                location=search_request.location,
                num_results=min(search_request.max_results // 2, 25)
            )
        except Exception as e:
            logger.error(f"Google jobs search failed: {e}")
            return []
    
    async def _search_indeed_jobs(self, search_request: JobSearchRequest) -> List[Dict]:
        """Search jobs using Indeed API"""
        try:
            # Map date filter
            indeed_date_map = {
                "today": "today",
                "week": "week", 
                "month": "month",
                "all": "all"
            }
            
            return await self.indeed_service.search_jobs(
                query=search_request.query,
                location=search_request.location,
                num_results=min(search_request.max_results // 3, 20),
                date_posted=indeed_date_map.get(search_request.date_posted, "all")
            )
        except Exception as e:
            logger.error(f"Indeed jobs search failed: {e}")
            return []
    
    async def _search_arbetsformedlingen_jobs(self, search_request: JobSearchRequest) -> List[Dict]:
        """Search jobs using Arbetsförmedlingen (Swedish Employment Agency) API"""
        try:
            # Map date filter
            arbetsformedlingen_date_map = {
                "today": "today",
                "week": "week", 
                "month": "month",
                "all": "all"
            }
            
            return await self.arbetsformedlingen_service.search_jobs(
                query=search_request.query,
                location=search_request.location,
                num_results=min(search_request.max_results // 3, 20),
                date_posted=arbetsformedlingen_date_map.get(search_request.date_posted, "all")
            )
        except Exception as e:
            logger.error(f"Arbetsförmedlingen jobs search failed: {e}")
            return []
    
    async def _search_linkedin_jobs(self, search_request: JobSearchRequest) -> List[Dict]:
        """Search jobs using LinkedIn API"""
        try:
            # Map date filter
            linkedin_date_map = {
                "today": "today",
                "week": "week", 
                "month": "month",
                "all": "all"
            }
            
            # Map experience levels
            experience_level = "all"
            if search_request.experience_levels:
                if "senior" in [level.lower() for level in search_request.experience_levels]:
                    experience_level = "senior"
                elif "junior" in [level.lower() for level in search_request.experience_levels]:
                    experience_level = "entry"
                elif "mid" in [level.lower() for level in search_request.experience_levels]:
                    experience_level = "mid"
            
            return await self.linkedin_service.search_jobs(
                query=search_request.query,
                location=search_request.location,
                num_results=min(search_request.max_results // 4, 15),
                date_posted=linkedin_date_map.get(search_request.date_posted, "all"),
                experience_level=experience_level
            )
        except Exception as e:
            logger.error(f"LinkedIn jobs search failed: {e}")
            return []
    
    async def _search_gmail_jobs(self, search_request: JobSearchRequest, user_id: str) -> List[Dict]:
        """Search job-related emails using Gmail API"""
        try:
            # Get user's Gmail credentials from database
            db = await get_database()
            user = await db.users.find_one({"_id": user_id})
            
            if not user or not user.get("gmail_credentials"):
                logger.info(f"No Gmail credentials found for user {user_id}")
                return []
            
            # Create Gmail credentials object
            from google.oauth2.credentials import Credentials
            gmail_creds = user["gmail_credentials"]
            credentials = Credentials(
                token=gmail_creds.get("token"),
                refresh_token=gmail_creds.get("refresh_token"),
                token_uri=gmail_creds.get("token_uri"),
                client_id=gmail_creds.get("client_id"),
                client_secret=gmail_creds.get("client_secret"),
                scopes=gmail_creds.get("scopes", ["https://www.googleapis.com/auth/gmail.readonly"])
            )
            
            # Initialize Gmail service
            gmail_service = GmailService(credentials)
            
            # Extract search keywords from query
            keywords = search_request.query.split() if search_request.query else []
            
            # Search for job-related emails
            job_emails = await gmail_service.search_job_emails(
                keywords=keywords,
                days_back=30  # Search last 30 days
            )
            
            # Convert email jobs to standard format
            standardized_jobs = []
            for email_job in job_emails:
                if email_job.get('source') in ['linkedin_email', 'indeed_email']:
                    # These are already properly formatted job objects
                    standardized_job = {
                        "title": email_job.get("title", ""),
                        "company": email_job.get("company", ""),
                        "location": email_job.get("location", ""),
                        "description": email_job.get("description", ""),
                        "url": email_job.get("url", ""),
                        "source": f"gmail_{email_job.get('email_source', 'email')}",
                        "posting_date": email_job.get("posting_date"),
                        "salary": email_job.get("salary"),
                        "job_type": email_job.get("job_type"),
                        "requirements": email_job.get("requirements", []),
                        "benefits": email_job.get("benefits", []),
                        "experience_level": email_job.get("experience_level"),
                        "remote_option": email_job.get("remote_option", False),
                        "keywords": email_job.get("keywords", []),
                        "confidence_score": email_job.get("confidence_score", 0.8),
                        "match_score": 0.0,  # Will be calculated later
                        "ats_score": email_job.get("ats_score", 0.7),
                        "category": email_job.get("category", "general"),
                        "email_id": email_job.get("email_id"),
                        "email_date": email_job.get("email_date")
                    }
                    standardized_jobs.append(standardized_job)
            
            logger.info(f"Found {len(standardized_jobs)} jobs from Gmail for user {user_id}")
            return standardized_jobs
            
        except Exception as e:
            logger.error(f"Gmail jobs search failed: {e}")
            return []
    
    async def _has_gmail_access(self, user_id: str) -> bool:
        """Check if user has connected Gmail account"""
        try:
            db = await get_database()
            user = await db.users.find_one({"_id": user_id})
            gmail_creds = user.get("gmail_credentials") if user else None
            return gmail_creds and gmail_creds.get("token") is not None
        except Exception:
            return False
    
    async def _process_jobs(self, jobs: List[Dict], search_request: JobSearchRequest, user_id: str) -> List[Dict]:
        """Process and enhance job data"""
        processed_jobs = []
        
        for job in jobs:
            try:
                enhanced_job = await self._enhance_job(job, search_request, user_id)
                if enhanced_job:
                    processed_jobs.append(enhanced_job)
            except Exception as e:
                logger.error(f"Error processing job: {e}")
                continue
        
        return processed_jobs
    
    async def _enhance_job(self, job: Dict, search_request: JobSearchRequest, user_id: str) -> Optional[Dict]:
        """Enhance job with additional data and scoring"""
        
        # Standardize job format
        standardized_job = self._standardize_job_format(job)
        
        # Calculate match score
        standardized_job["match_score"] = await self._calculate_match_score(
            standardized_job, search_request, user_id
        )
        
        # Calculate ATS compatibility score
        standardized_job["ats_score"] = self._calculate_ats_score(standardized_job)
        
        # Extract and enhance keywords
        standardized_job["keywords"] = self._extract_enhanced_keywords(standardized_job)
        
        # Classify job category
        standardized_job["category"] = self._classify_job_category(standardized_job)
        
        # Estimate application difficulty
        standardized_job["application_difficulty"] = self._estimate_application_difficulty(standardized_job)
        
        # Add processing metadata
        standardized_job["processed_at"] = datetime.utcnow()
        standardized_job["aggregation_source"] = "job_aggregation_service"
        
        return standardized_job
    
    def _standardize_job_format(self, job: Dict) -> Dict:
        """Standardize job format across different sources"""
        
        return {
            "title": job.get("title", "").strip(),
            "company": job.get("company", "").strip(),
            "location": job.get("location", "").strip(),
            "description": job.get("description", "").strip(),
            "url": job.get("url", ""),
            "source": job.get("source", "unknown"),
            "posting_date": job.get("posting_date"),
            "salary": job.get("salary"),
            "job_type": job.get("job_type"),
            "requirements": job.get("requirements", []),
            "benefits": job.get("benefits", []),
            "experience_level": job.get("experience_level"),
            "remote_option": job.get("remote_option", False),
            "keywords": job.get("keywords", []),
            "confidence_score": job.get("confidence_score", 0.5),
            "original_data": job  # Keep original for reference
        }
    
    async def _calculate_match_score(self, job: Dict, search_request: JobSearchRequest, user_id: str) -> float:
        """Calculate how well job matches search criteria and user profile"""
        
        score = 0.0
        
        # Query relevance (40% of score)
        query_score = self._calculate_query_relevance(job, search_request.query)
        score += query_score * 0.4
        
        # Location relevance (20% of score)
        location_score = self._calculate_location_relevance(job, search_request.location)
        score += location_score * 0.2
        
        # Salary match (15% of score)
        salary_score = self._calculate_salary_match(job, search_request.salary_min, search_request.salary_max)
        score += salary_score * 0.15
        
        # Recency (10% of score)
        recency_score = self._calculate_recency_score(job)
        score += recency_score * 0.1
        
        # User profile match (15% of score)
        profile_score = await self._calculate_profile_match(job, user_id)
        score += profile_score * 0.15
        
        return min(score, 1.0)
    
    def _calculate_query_relevance(self, job: Dict, query: str) -> float:
        """Calculate relevance to search query"""
        
        if not query:
            return 0.5
        
        query_terms = set(query.lower().split())
        job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('company', '')}".lower()
        
        # Count matching terms
        matching_terms = sum(1 for term in query_terms if term in job_text)
        
        # Calculate score
        if len(query_terms) == 0:
            return 0.5
        
        base_score = matching_terms / len(query_terms)
        
        # Bonus for title matches
        title_matches = sum(1 for term in query_terms if term in job.get('title', '').lower())
        title_bonus = (title_matches / len(query_terms)) * 0.3
        
        return min(base_score + title_bonus, 1.0)
    
    def _calculate_location_relevance(self, job: Dict, desired_location: str) -> float:
        """Calculate location match score"""
        
        job_location = job.get("location", "").lower()
        
        # Remote jobs always score high if location specified
        if job.get("remote_option") and desired_location:
            return 0.9
        
        if not desired_location or not job_location:
            return 0.5
        
        desired_lower = desired_location.lower()
        
        # Exact match
        if desired_lower in job_location or job_location in desired_lower:
            return 1.0
        
        # City/state extraction and matching
        desired_parts = re.findall(r'\b[A-Za-z]+\b', desired_lower)
        job_parts = re.findall(r'\b[A-Za-z]+\b', job_location)
        
        if desired_parts and job_parts:
            common_parts = set(desired_parts) & set(job_parts)
            return len(common_parts) / max(len(desired_parts), len(job_parts))
        
        return 0.3
    
    def _calculate_salary_match(self, job: Dict, min_salary: Optional[int], max_salary: Optional[int]) -> float:
        """Calculate salary match score"""
        
        job_salary = job.get("salary")
        if not job_salary or (not min_salary and not max_salary):
            return 0.5
        
        job_min = job_salary.get("min")
        job_max = job_salary.get("max")
        
        if not job_min and not job_max:
            return 0.5
        
        # Use job average if range available
        if job_min and job_max:
            job_avg = (job_min + job_max) / 2
        else:
            job_avg = job_min or job_max
        
        score = 0.5
        
        # Check minimum salary requirement
        if min_salary and job_avg:
            if job_avg >= min_salary:
                score += 0.3
            else:
                score -= 0.2
        
        # Check maximum salary preference
        if max_salary and job_avg:
            if job_avg <= max_salary:
                score += 0.2
            # No penalty for higher salary
        
        return max(0.0, min(score, 1.0))
    
    def _calculate_recency_score(self, job: Dict) -> float:
        """Calculate score based on posting recency"""
        
        posting_date = job.get("posting_date")
        if not posting_date:
            return 0.5
        
        days_ago = (datetime.utcnow() - posting_date).days
        
        if days_ago <= 1:
            return 1.0
        elif days_ago <= 7:
            return 0.8
        elif days_ago <= 14:
            return 0.6
        elif days_ago <= 30:
            return 0.4
        else:
            return 0.2
    
    async def _calculate_profile_match(self, job: Dict, user_id: str) -> float:
        """Calculate match with user profile and preferences"""
        
        try:
            db = await get_database()
            user = await db.users.find_one({"_id": user_id})
            
            if not user:
                return 0.5
            
            profile = user.get("profile", {})
            score = 0.5
            
            # Match skills
            user_skills = set(skill.lower() for skill in profile.get("skills", []))
            job_keywords = set(kw.lower() for kw in job.get("keywords", []))
            
            if user_skills and job_keywords:
                skill_overlap = len(user_skills & job_keywords)
                score += (skill_overlap / len(user_skills)) * 0.3
            
            # Match experience level
            user_level = profile.get("experience_level", "").lower()
            job_level = job.get("experience_level", "").lower()
            
            if user_level and job_level:
                if user_level == job_level:
                    score += 0.2
                elif (user_level == "senior" and job_level == "mid") or \
                     (user_level == "mid" and job_level == "junior"):
                    score += 0.1
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating profile match: {e}")
            return 0.5
    
    def _calculate_ats_score(self, job: Dict) -> float:
        """Calculate ATS compatibility score"""
        
        description = job.get("description", "")
        title = job.get("title", "")
        
        score = 0.0
        
        # Length check
        if len(description) > 200:
            score += 0.2
        
        # Keyword density
        tech_keywords = [
            "python", "java", "javascript", "react", "sql", "aws", "docker",
            "kubernetes", "api", "microservices", "agile", "scrum"
        ]
        
        content = f"{title} {description}".lower()
        keyword_matches = sum(1 for kw in tech_keywords if kw in content)
        score += min(keyword_matches / 10, 0.3)
        
        # Structure indicators
        if any(indicator in description.lower() for indicator in ["requirements", "responsibilities", "qualifications"]):
            score += 0.2
        
        # Contact information
        if any(contact in description.lower() for contact in ["email", "apply", "contact"]):
            score += 0.1
        
        # Company information
        if job.get("company") and len(job.get("company", "")) > 2:
            score += 0.2
        
        return min(score, 1.0)
    
    def _extract_enhanced_keywords(self, job: Dict) -> List[str]:
        """Extract and enhance job keywords"""
        
        existing_keywords = set(job.get("keywords", []))
        
        text = f"{job.get('title', '')} {job.get('description', '')}".lower()
        
        # Enhanced keyword extraction
        enhanced_keywords = [
            # Programming languages
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "php", "ruby",
            # Web frameworks
            "react", "angular", "vue", "django", "flask", "spring", "express", "laravel",
            # Databases
            "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra",
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible",
            # Data & AI
            "machine learning", "deep learning", "data science", "pandas", "numpy", "tensorflow",
            # Methodologies
            "agile", "scrum", "kanban", "devops", "ci/cd", "tdd", "microservices"
        ]
        
        found_keywords = existing_keywords.copy()
        for keyword in enhanced_keywords:
            if keyword in text and keyword not in found_keywords:
                found_keywords.add(keyword)
        
        return list(found_keywords)[:20]  # Limit to top 20
    
    def _classify_job_category(self, job: Dict) -> str:
        """Classify job into category"""
        
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        keywords = [kw.lower() for kw in job.get("keywords", [])]
        
        content = f"{title} {description} {' '.join(keywords)}"
        
        categories = {
            "software_engineering": ["developer", "engineer", "programmer", "software", "coding"],
            "data_science": ["data scientist", "analyst", "machine learning", "ai", "analytics"],
            "devops": ["devops", "sre", "infrastructure", "cloud", "deployment"],
            "frontend": ["frontend", "ui", "ux", "react", "angular", "vue"],
            "backend": ["backend", "api", "server", "database", "microservices"],
            "mobile": ["mobile", "ios", "android", "flutter", "react native"],
            "management": ["manager", "lead", "director", "head", "chief"],
            "qa": ["qa", "test", "quality", "automation"],
            "security": ["security", "cybersecurity", "penetration", "compliance"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in content for keyword in keywords):
                return category
        
        return "general"
    
    def _estimate_application_difficulty(self, job: Dict) -> str:
        """Estimate how difficult it might be to get this job"""
        
        factors = {
            "easy": 0,
            "medium": 0,
            "hard": 0
        }
        
        # Company size/prestige (rough estimation)
        company = job.get("company", "").lower()
        if any(big_tech in company for big_tech in ["google", "microsoft", "amazon", "apple", "meta", "netflix"]):
            factors["hard"] += 2
        elif any(unicorn in company for unicorn in ["uber", "airbnb", "stripe", "spotify"]):
            factors["hard"] += 1
        else:
            factors["easy"] += 1
        
        # Experience level
        exp_level = job.get("experience_level", "").lower()
        if exp_level == "senior":
            factors["hard"] += 1
        elif exp_level == "junior":
            factors["easy"] += 1
        
        # Salary level
        salary = job.get("salary")
        if salary and salary.get("min"):
            if salary["min"] > 150000:
                factors["hard"] += 2
            elif salary["min"] > 100000:
                factors["medium"] += 1
            else:
                factors["easy"] += 1
        
        # Requirements count
        requirements = job.get("requirements", [])
        if len(requirements) > 10:
            factors["hard"] += 1
        elif len(requirements) < 5:
            factors["easy"] += 1
        
        # Determine final difficulty
        max_score = max(factors.values())
        for difficulty, score in factors.items():
            if score == max_score:
                return difficulty
        
        return "medium"
    
    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on title, company, and location"""
        
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create unique key
            key = (
                job.get("title", "").lower().strip(),
                job.get("company", "").lower().strip(),
                job.get("location", "").lower().strip()
            )
            
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _apply_filters(self, jobs: List[Dict], search_request: JobSearchRequest) -> List[Dict]:
        """Apply search filters to job list"""
        
        filtered_jobs = []
        
        for job in jobs:
            # Job type filter
            if search_request.job_types:
                job_type = job.get("job_type", "").lower()
                if job_type not in [jt.lower() for jt in search_request.job_types]:
                    continue
            
            # Experience level filter
            if search_request.experience_levels:
                exp_level = job.get("experience_level", "").lower()
                if exp_level not in [el.lower() for el in search_request.experience_levels]:
                    continue
            
            # Company exclusion filter
            if search_request.companies_exclude:
                company = job.get("company", "").lower()
                if any(exc.lower() in company for exc in search_request.companies_exclude):
                    continue
            
            # Required keywords filter
            if search_request.keywords_required:
                job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()
                if not all(kw.lower() in job_text for kw in search_request.keywords_required):
                    continue
            
            # Excluded keywords filter
            if search_request.keywords_exclude:
                job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()
                if any(kw.lower() in job_text for kw in search_request.keywords_exclude):
                    continue
            
            # Remote option filter
            if not search_request.include_remote and job.get("remote_option"):
                continue
            
            filtered_jobs.append(job)
        
        return filtered_jobs
    
    def _sort_jobs(self, jobs: List[Dict], search_request: JobSearchRequest) -> List[Dict]:
        """Sort jobs by relevance and other factors"""
        
        def sort_key(job):
            # Primary sort: match score (descending)
            match_score = job.get("match_score", 0.0)
            
            # Secondary sort: confidence score (descending)
            confidence_score = job.get("confidence_score", 0.0)
            
            # Tertiary sort: recency (newer first)
            posting_date = job.get("posting_date")
            if posting_date:
                days_ago = (datetime.utcnow() - posting_date).days
                recency_score = max(0, 30 - days_ago) / 30  # Normalize to 0-1
            else:
                recency_score = 0.0
            
            # Combined score
            combined_score = (match_score * 0.6) + (confidence_score * 0.3) + (recency_score * 0.1)
            
            return -combined_score  # Negative for descending sort
        
        return sorted(jobs, key=sort_key)
    
    async def _save_search_results(self, jobs: List[Dict], search_request: JobSearchRequest, user_id: str):
        """Save search results to database for analytics and caching"""
        
        try:
            db = await get_database()
            
            # Save search query
            search_record = {
                "user_id": user_id,
                "query": search_request.query,
                "location": search_request.location,
                "filters": {
                    "job_types": search_request.job_types,
                    "salary_range": [search_request.salary_min, search_request.salary_max],
                    "experience_levels": search_request.experience_levels,
                    "date_posted": search_request.date_posted
                },
                "results_count": len(jobs),
                "search_timestamp": datetime.utcnow()
            }
            
            await db.job_searches.insert_one(search_record)
            
            # Save/update job postings
            for job in jobs:
                job_doc = {
                    "user_id": user_id,
                    "source": job.get("source"),
                    "title": job.get("title"),
                    "company": job.get("company"),
                    "location": job.get("location"),
                    "description": job.get("description"),
                    "url": job.get("url"),
                    "posting_date": job.get("posting_date"),
                    "salary": job.get("salary"),
                    "keywords": job.get("keywords", []),
                    "match_score": job.get("match_score", 0.0),
                    "confidence_score": job.get("confidence_score", 0.0),
                    "ats_score": job.get("ats_score", 0.0),
                    "category": job.get("category"),
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                # Upsert job (update if exists, insert if new)
                await db.jobs.update_one(
                    {
                        "title": job.get("title"),
                        "company": job.get("company"),
                        "url": job.get("url")
                    },
                    {"$set": job_doc},
                    upsert=True
                )
            
            logger.info(f"Saved search results for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error saving search results: {e}")
    
    async def get_saved_jobs(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's saved/bookmarked jobs"""
        
        try:
            db = await get_database()
            cursor = db.jobs.find(
                {"user_id": user_id, "is_saved": True}
            ).sort("updated_at", -1).limit(limit)
            
            return await cursor.to_list(length=limit)
            
        except Exception as e:
            logger.error(f"Error fetching saved jobs: {e}")
            return []
    
    async def get_search_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user's search history"""
        
        try:
            db = await get_database()
            cursor = db.job_searches.find(
                {"user_id": user_id}
            ).sort("search_timestamp", -1).limit(limit)
            
            return await cursor.to_list(length=limit)
            
        except Exception as e:
            logger.error(f"Error fetching search history: {e}")
            return []