import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import re

from app.services.job_aggregation_service import JobAggregationService, JobSearchRequest
from app.services.latex_resume_service import LaTeXResumeService
from app.services.email_automation_service import EmailAutomationService
from app.core.database import get_async_session

logger = logging.getLogger(__name__)

@dataclass
class UserProfile:
    """User profile configuration for job automation"""
    name: str = "Hongzhi Li"
    email: str = "leeharvad@gmail.com"
    swedish_level: str = "B2"  # B2 level Swedish
    max_experience_years: int = 5
    
    # Your technical skills from resume
    skills: List[str] = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = [
                # Programming Languages
                "java", "javascript", "c#", "python", "typescript",
                
                # Frontend Technologies  
                "react", "reactjs", "angular", "vue", "vuejs", "html", "css",
                
                # Backend Technologies
                "spring", "spring boot", "nodejs", "net core", "asp.net",
                
                # Cloud Platforms
                "aws", "azure", "gcp", "cloud", "serverless",
                
                # Databases
                "sql", "postgresql", "mysql", "mongodb", "nosql",
                
                # DevOps & Infrastructure
                "docker", "kubernetes", "jenkins", "ci/cd", "devops",
                "terraform", "ansible", "grafana",
                
                # Architecture & Patterns
                "microservices", "api", "rest", "restful", "graphql",
                "fullstack", "full stack", "backend", "frontend",
                
                # Roles & Positions
                "developer", "engineer", "architect", "specialist",
                "cloud developer", "cloud architect", "integration specialist",
                "platform architect", "project coordinator"
            ]

class JobAutomationService:
    """Service for automated job processing, filtering, and application generation"""
    
    def __init__(self):
        self.job_service = JobAggregationService()
        self.latex_service = LaTeXResumeService()
        self.email_service = EmailAutomationService()
        self.user_profile = UserProfile()
        
        # Job search queries for different roles
        self.search_queries = [
            "fullstack developer",
            "backend developer", 
            "java developer",
            "c# developer",
            "cloud developer",
            "cloud architect",
            "devops engineer",
            "platform architect",
            "integration specialist",
            "software engineer"
        ]
        
        # Swedish locations to search
        self.locations = [
            "Stockholm",
            "Göteborg", 
            "Gothenburg",
            "Malmö",
            "Uppsala",
            "Linköping",
            "Örebro",
            "Sweden"
        ]
    
    async def run_daily_job_automation(self, user_id: str) -> Dict:
        """
        Main automation function - runs daily at 6:00 AM on weekdays
        """
        try:
            logger.info("Starting daily job automation for user: %s", user_id)
            
            # Step 1: Fetch jobs from all sources
            all_jobs = await self._fetch_all_jobs(user_id)
            logger.info("Fetched %d total jobs", len(all_jobs))
            
            # Step 2: Apply comprehensive filtering
            filtered_jobs = await self._apply_comprehensive_filters(all_jobs)
            logger.info("After filtering: %d qualifying jobs", len(filtered_jobs))
            
            # Step 3: Remove already processed jobs
            new_jobs = await self._filter_new_jobs(filtered_jobs, user_id)
            logger.info("New jobs to process: %d", len(new_jobs))
            
            # Step 4: Generate applications for each job
            processed_applications = []
            for job in new_jobs:
                try:
                    application = await self._process_single_job(job, user_id)
                    if application:
                        processed_applications.append(application)
                        
                        # Mark job as processed
                        await self._mark_job_as_processed(job, user_id)
                        
                except Exception as e:
                    logger.error("Error processing job %s: %s", job.get('title', 'Unknown'), e)
                    continue
            
            # Step 5: Save automation results
            await self._save_automation_results(processed_applications, user_id)
            
            return {
                "status": "success",
                "total_jobs_fetched": len(all_jobs),
                "jobs_after_filtering": len(filtered_jobs),
                "new_jobs_processed": len(new_jobs),
                "applications_sent": len(processed_applications),
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error("Error in daily job automation: %s", e)
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
    
    async def _fetch_all_jobs(self, user_id: str) -> List[Dict]:
        """Fetch jobs from all sources with multiple queries"""
        all_jobs = []
        
        for query in self.search_queries:
            for location in self.locations:
                try:
                    search_request = JobSearchRequest(
                        query=query,
                        location=location,
                        max_results=20,  # Limit per query to avoid overwhelming
                        include_remote=True,
                        date_posted="all"  # We'll filter by date separately
                    )
                    
                    jobs = await self.job_service.search_jobs(search_request, user_id)
                    all_jobs.extend(jobs)
                    
                    # Small delay to respect API limits
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error("Error fetching jobs for query '%s' in '%s': %s", query, location, e)
                    continue
        
        return all_jobs
    
    async def _apply_comprehensive_filters(self, jobs: List[Dict]) -> List[Dict]:
        """Apply all filtering criteria"""
        filtered_jobs = []
        
        for job in jobs:
            try:
                # Filter 1: Job age (within 2 weeks)
                if not self._is_recent_job(job):
                    continue
                
                # Filter 2: Experience level (≤5 years)
                if not self._matches_experience_requirement(job):
                    continue
                
                # Filter 3: Swedish language requirement (≤B2)
                if not self._matches_swedish_requirement(job):
                    continue
                
                # Filter 4: Skill matching
                if not self._matches_skill_requirements(job):
                    continue
                
                # Filter 5: Job quality check
                if not self._is_quality_job(job):
                    continue
                
                filtered_jobs.append(job)
                
            except Exception as e:
                logger.error("Error filtering job %s: %s", job.get('title', 'Unknown'), e)
                continue
        
        return filtered_jobs
    
    def _is_recent_job(self, job: Dict) -> bool:
        """Check if job was posted within 2 weeks"""
        posting_date = job.get('posting_date')
        if not posting_date:
            return True  # If no date, assume recent
        
        if isinstance(posting_date, str):
            try:
                posting_date = datetime.fromisoformat(posting_date.replace('Z', '+00:00'))
            except:
                return True
        
        cutoff_date = datetime.utcnow() - timedelta(days=14)
        return posting_date >= cutoff_date
    
    def _matches_experience_requirement(self, job: Dict) -> bool:
        """Check if job requires ≤5 years experience"""
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        requirements = ' '.join(job.get('requirements', [])).lower()
        
        content = f"{title} {description} {requirements}"
        
        # Look for experience requirements
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*års?\s*erfarenhet',  # Swedish
            r'minimum\s*(\d+)\s*years?',
            r'minst\s*(\d+)\s*år',  # Swedish
            r'senior',  # Often indicates >5 years
            r'lead',    # Often indicates >5 years
            r'principal' # Often indicates >5 years
        ]
        
        # Check for senior-level keywords that typically require >5 years
        senior_keywords = ['senior', 'lead', 'principal', 'staff', 'architect']
        if any(keyword in content for keyword in senior_keywords):
            # Allow architect roles as they match your background
            if 'architect' in content:
                return True
            return False
        
        # Extract years from patterns
        for pattern in experience_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                try:
                    years = int(match)
                    if years > 5:
                        return False
                except ValueError:
                    continue
        
        return True
    
    def _matches_swedish_requirement(self, job: Dict) -> bool:
        """Check if Swedish language requirement is ≤B2"""
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        requirements = ' '.join(job.get('requirements', [])).lower()
        
        content = f"{title} {description} {requirements}"
        
        # Swedish language requirement patterns
        swedish_patterns = [
            r'svenska\s*(?:språket?)?\s*(?:som\s*)?(?:modersmål|förstaspråk)',  # Native Swedish
            r'flyt(?:ande|ende)\s*svenska',  # Fluent Swedish
            r'svenska\s*(?:på\s*)?(?:modersmålsnivå|c1|c2)',  # C1/C2 level
            r'perfekt\s*svenska',  # Perfect Swedish
            r'svensk\s*som\s*modersmål',  # Swedish as native language
        ]
        
        # Check for high Swedish requirements
        for pattern in swedish_patterns:
            if re.search(pattern, content):
                logger.info("Job filtered out due to high Swedish requirement: %s", job.get('title'))
                return False
        
        return True
    
    def _matches_skill_requirements(self, job: Dict) -> bool:
        """Check if job matches your technical skills"""
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        keywords = [kw.lower() for kw in job.get('keywords', [])]
        requirements = ' '.join(job.get('requirements', [])).lower()
        
        content = f"{title} {description} {requirements} {' '.join(keywords)}"
        
        # Count matching skills
        matching_skills = 0
        for skill in self.user_profile.skills:
            if skill in content:
                matching_skills += 1
        
        # Require at least 2 matching skills
        return matching_skills >= 2
    
    def _is_quality_job(self, job: Dict) -> bool:
        """Basic quality checks for job postings"""
        # Must have title and company
        if not job.get('title') or not job.get('company'):
            return False
        
        # Must have description with reasonable length
        description = job.get('description', '')
        if len(description) < 50:
            return False
        
        # Must have application URL
        if not job.get('url'):
            return False
        
        # Filter out obvious spam/low-quality jobs
        spam_keywords = ['work from home', 'easy money', 'no experience needed', '$$$']
        content = f"{job.get('title', '')} {description}".lower()
        
        if any(spam in content for spam in spam_keywords):
            return False
        
        return True
    
    async def _filter_new_jobs(self, jobs: List[Dict], user_id: str) -> List[Dict]:
        """Filter out jobs that have already been processed"""
        try:
            db = await get_database()
            
            # Get processed job URLs from database
            processed_jobs = await db.processed_jobs.find(
                {"user_id": user_id},
                {"url": 1}
            ).to_list(length=None)
            
            processed_urls = {job["url"] for job in processed_jobs}
            
            # Filter out already processed jobs
            new_jobs = [job for job in jobs if job.get('url') not in processed_urls]
            
            return new_jobs
            
        except Exception as e:
            logger.error("Error filtering new jobs: %s", e)
            return jobs  # Return all jobs if filtering fails
    
    async def _process_single_job(self, job: Dict, user_id: str) -> Optional[Dict]:
        """Process a single job: generate CV, cover letter, and send email"""
        try:
            logger.info("Processing job: %s at %s", job.get('title'), job.get('company'))
            
            # Generate customized CV
            cv_content = await self.latex_service.generate_customized_cv(job)
            
            # Generate customized cover letter
            cover_letter = await self.latex_service.generate_customized_cover_letter(job)
            
            # Prepare email
            email_subject = f"Application: {job.get('title')} at {job.get('company')}"
            email_body = self._create_application_email_body(job)
            
            # Send email with attachments
            email_sent = await self.email_service.send_application_email(
                to_email=self.user_profile.email,
                subject=email_subject,
                body=email_body,
                cv_content=cv_content,
                cover_letter_content=cover_letter,
                job_data=job
            )
            
            if email_sent:
                logger.info("Successfully sent application for: %s", job.get('title'))
                return {
                    "job_title": job.get('title'),
                    "company": job.get('company'),
                    "url": job.get('url'),
                    "email_sent": True,
                    "processed_at": datetime.utcnow()
                }
            else:
                logger.error("Failed to send email for job: %s", job.get('title'))
                return None
                
        except Exception as e:
            logger.error("Error processing job %s: %s", job.get('title', 'Unknown'), e)
            return None
    
    def _create_application_email_body(self, job: Dict) -> str:
        """Create email body for job application"""
        return f"""
Dear Hiring Manager at {job.get('company', 'Your Company')},

I am writing to express my interest in the {job.get('title', 'position')} role at {job.get('company', 'your company')}.

As an experienced Fullstack Developer with expertise in Java, C#, cloud technologies (AWS/Azure), and modern web frameworks, I believe I would be a valuable addition to your team.

Please find attached my customized resume and cover letter for this position.

Application Link: {job.get('url', 'N/A')}

I look forward to hearing from you.

Best regards,
Hongzhi Li

---
This application was automatically generated and sent on {datetime.utcnow().strftime('%Y-%m-%d at %H:%M UTC')}.
        """.strip()
    
    async def _mark_job_as_processed(self, job: Dict, user_id: str):
        """Mark job as processed in database"""
        try:
            db = await get_database()
            
            processed_job = {
                "user_id": user_id,
                "job_title": job.get('title'),
                "company": job.get('company'),
                "url": job.get('url'),
                "source": job.get('source'),
                "processed_at": datetime.utcnow(),
                "job_data": job
            }
            
            await db.processed_jobs.insert_one(processed_job)
            
        except Exception as e:
            logger.error("Error marking job as processed: %s", e)
    
    async def _save_automation_results(self, applications: List[Dict], user_id: str):
        """Save automation run results"""
        try:
            db = await get_database()
            
            automation_result = {
                "user_id": user_id,
                "run_date": datetime.utcnow(),
                "applications_sent": len(applications),
                "applications": applications,
                "status": "completed"
            }
            
            await db.automation_runs.insert_one(automation_result)
            
        except Exception as e:
            logger.error("Error saving automation results: %s", e)
    
    async def get_automation_stats(self, user_id: str, days: int = 30) -> Dict:
        """Get automation statistics for the last N days"""
        try:
            db = await get_database()
            
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Get automation runs
            runs = await db.automation_runs.find({
                "user_id": user_id,
                "run_date": {"$gte": cutoff_date}
            }).to_list(length=None)
            
            # Get processed jobs
            processed = await db.processed_jobs.find({
                "user_id": user_id,
                "processed_at": {"$gte": cutoff_date}
            }).to_list(length=None)
            
            return {
                "total_runs": len(runs),
                "total_applications": len(processed),
                "average_applications_per_run": len(processed) / max(len(runs), 1),
                "last_run": runs[-1]["run_date"] if runs else None,
                "companies_applied": list(set(job["company"] for job in processed if job.get("company")))
            }
            
        except Exception as e:
            logger.error("Error getting automation stats: %s", e)
            return {"error": str(e)}