import asyncio
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

from app.services.email_scanner_service import EmailScannerService
from app.services.linkedin_service import LinkedInService
# from app.services.indeed_service import IndeedService  # Removed per user request
from app.services.arbetsformedlingen_service import ArbetsformedlingenService
from app.services.job_application_processor import JobApplicationProcessor
from app.models.job import AggregatedJob, JobCreate
from app.core.database import get_async_session

logger = logging.getLogger(__name__)

@dataclass
class JobSource:
    name: str
    enabled: bool
    last_sync: Optional[datetime] = None
    error_count: int = 0
    total_jobs_found: int = 0

class MultiSourceJobAggregator:
    """
    Unified job aggregation system that pulls jobs from multiple sources:
    1. LinkedIn Saved Jobs (manual saves)
    2. Gmail LinkedIn Job emails
    3. Gmail Indeed Job emails  
    4. Arbetsförmedlingen API
    5. LinkedIn Search API
    """
    
    def __init__(self):
        self.email_scanner = EmailScannerService()
        self.linkedin_service = LinkedInService()
        # self.indeed_service = IndeedService()  # Removed per user request
        self.arbetsformedlingen_service = ArbetsformedlingenService()
        self.job_processor = JobApplicationProcessor()
        
        self.sources = {
            'gmail_linkedin': JobSource('Gmail LinkedIn Jobs', True),
            'gmail_indeed': JobSource('Gmail Indeed Jobs', True),
            'linkedin_saved': JobSource('LinkedIn Saved Jobs', True),
            'linkedin_search': JobSource('LinkedIn Search API', True),
            # 'indeed_api': JobSource('Indeed API', True),  # Removed per user request
            'arbetsformedlingen': JobSource('Arbetsförmedlingen API', True),
        }
    
    async def aggregate_all_jobs(self, user_id: str, sync_preferences: Dict = None) -> Dict[str, Any]:
        """
        Run complete job aggregation from all enabled sources
        """
        logger.info(f"Starting job aggregation for user {user_id}")
        
        results = {
            'total_jobs_found': 0,
            'new_jobs': 0,
            'duplicates_removed': 0,
            'sources': {},
            'errors': []
        }
        
        # Run all sources in parallel for efficiency
        tasks = []
        
        if self.sources['gmail_linkedin'].enabled:
            tasks.append(self._sync_gmail_linkedin_jobs(user_id))
            
        if self.sources['gmail_indeed'].enabled:
            tasks.append(self._sync_gmail_indeed_jobs(user_id))
            
        if self.sources['linkedin_saved'].enabled:
            tasks.append(self._sync_linkedin_saved_jobs(user_id))
            
        if self.sources['arbetsformedlingen'].enabled:
            tasks.append(self._sync_arbetsformedlingen_jobs(user_id))
            
        if self.sources['linkedin_search'].enabled:
            tasks.append(self._sync_linkedin_search_jobs(user_id))
            
        # if self.sources['indeed_api'].enabled:
        #     tasks.append(self._sync_indeed_api_jobs(user_id))  # Removed per user request
        
        # Execute all sources concurrently
        source_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results from each source
        for i, result in enumerate(source_results):
            source_name = list(self.sources.keys())[i]
            
            if isinstance(result, Exception):
                error_msg = f"Error in {source_name}: {str(result)}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
                self.sources[source_name].error_count += 1
            else:
                results['sources'][source_name] = result
                results['total_jobs_found'] += result['jobs_found']
                results['new_jobs'] += result['new_jobs']
                self.sources[source_name].last_sync = datetime.utcnow()
                self.sources[source_name].total_jobs_found += result['jobs_found']
        
        # Remove duplicates across sources
        duplicates_removed = await self._remove_duplicates(user_id)
        results['duplicates_removed'] = duplicates_removed
        
        logger.info(f"Job aggregation completed. Total: {results['total_jobs_found']}, New: {results['new_jobs']}")
        
        return results
    
    async def _sync_gmail_linkedin_jobs(self, user_id: str) -> Dict[str, Any]:
        """Sync jobs from Gmail LinkedIn job emails"""
        logger.info("Syncing Gmail LinkedIn jobs...")
        
        try:
            # Scan for LinkedIn job emails from the last 7 days
            emails = await self.email_scanner.scan_linkedin_job_emails(
                email="bluehawana@gmail.com",
                days_back=7
            )
            
            new_jobs = 0
            for email_data in emails:
                job_data = await self._extract_job_from_linkedin_email(email_data)
                if job_data:
                    job_data['user_id'] = user_id
                    job_data['source'] = 'gmail_linkedin'
                    
                    if await self._save_job_if_new(job_data):
                        new_jobs += 1
            
            return {
                'jobs_found': len(emails),
                'new_jobs': new_jobs,
                'source': 'gmail_linkedin'
            }
            
        except Exception as e:
            logger.error(f"Error syncing Gmail LinkedIn jobs: {e}")
            raise
    
    async def _sync_gmail_indeed_jobs(self, user_id: str) -> Dict[str, Any]:
        """Sync jobs from Gmail Indeed job emails"""
        logger.info("Syncing Gmail Indeed jobs...")
        
        try:
            # Scan for Indeed job emails
            emails = await self.email_scanner.scan_indeed_job_emails(
                email="bluehawana@gmail.com", 
                days_back=7
            )
            
            new_jobs = 0
            for email_data in emails:
                job_data = await self._extract_job_from_indeed_email(email_data)
                if job_data:
                    job_data['user_id'] = user_id
                    job_data['source'] = 'gmail_indeed'
                    
                    if await self._save_job_if_new(job_data):
                        new_jobs += 1
            
            return {
                'jobs_found': len(emails),
                'new_jobs': new_jobs,
                'source': 'gmail_indeed'
            }
            
        except Exception as e:
            logger.error(f"Error syncing Gmail Indeed jobs: {e}")
            raise
    
    async def _sync_linkedin_saved_jobs(self, user_id: str) -> Dict[str, Any]:
        """Sync manually saved LinkedIn jobs"""
        logger.info("Syncing LinkedIn saved jobs...")
        
        try:
            # This would require LinkedIn authentication and API access
            # For now, we'll implement a manual import function
            saved_jobs = await self.linkedin_service.get_saved_jobs()
            
            new_jobs = 0
            for job_data in saved_jobs:
                job_data['user_id'] = user_id
                job_data['source'] = 'linkedin_saved'
                job_data['application_status'] = 'saved'  # User manually saved these
                
                if await self._save_job_if_new(job_data):
                    new_jobs += 1
            
            return {
                'jobs_found': len(saved_jobs),
                'new_jobs': new_jobs,
                'source': 'linkedin_saved'
            }
            
        except Exception as e:
            logger.error(f"Error syncing LinkedIn saved jobs: {e}")
            raise
    
    async def _sync_arbetsformedlingen_jobs(self, user_id: str) -> Dict[str, Any]:
        """Sync jobs from Arbetsförmedlingen API"""
        logger.info("Syncing Arbetsförmedlingen jobs...")
        
        try:
            # Search for relevant jobs based on user preferences
            search_params = {
                'occupation': ['developer', 'programmer', 'software engineer'],
                'location': ['Stockholm', 'Gothenburg', 'Malmö'],
                'published_after': (datetime.now() - timedelta(days=1)).isoformat()
            }
            
            jobs = await self.arbetsformedlingen_service.search_jobs(search_params)
            
            new_jobs = 0
            for job_data in jobs:
                job_data['user_id'] = user_id
                job_data['source'] = 'arbetsformedlingen'
                
                if await self._save_job_if_new(job_data):
                    new_jobs += 1
            
            return {
                'jobs_found': len(jobs),
                'new_jobs': new_jobs,
                'source': 'arbetsformedlingen'
            }
            
        except Exception as e:
            logger.error(f"Error syncing Arbetsförmedlingen jobs: {e}")
            raise
    
    async def _sync_linkedin_search_jobs(self, user_id: str) -> Dict[str, Any]:
        """Sync jobs from LinkedIn search API"""
        logger.info("Syncing LinkedIn search jobs...")
        
        try:
            search_params = {
                'keywords': ['python developer', 'backend developer', 'fullstack developer'],
                'location': 'Sweden',
                'posted_date': 'past_24_hours'
            }
            
            jobs = await self.linkedin_service.search_jobs(search_params)
            
            new_jobs = 0
            for job_data in jobs:
                job_data['user_id'] = user_id
                job_data['source'] = 'linkedin_search'
                
                if await self._save_job_if_new(job_data):
                    new_jobs += 1
            
            return {
                'jobs_found': len(jobs),
                'new_jobs': new_jobs,
                'source': 'linkedin_search'
            }
            
        except Exception as e:
            logger.error(f"Error syncing LinkedIn search jobs: {e}")
            raise
    
    # async def _sync_indeed_api_jobs(self, user_id: str) -> Dict[str, Any]:
    #     """Sync jobs from Indeed API - REMOVED per user request"""
    #     # Indeed API access was refused, so this functionality is disabled
    #     pass
    
    async def _extract_job_from_linkedin_email(self, email_data: Dict) -> Optional[Dict]:
        """Extract job information from LinkedIn email"""
        try:
            # Parse LinkedIn job email format
            content = email_data.get('content', '')
            subject = email_data.get('subject', '')
            
            # Extract job details using regex or BeautifulSoup
            # This is a simplified version - you'd need proper parsing
            job_data = {
                'title': self._extract_title_from_content(content),
                'company': self._extract_company_from_content(content),
                'location': self._extract_location_from_content(content),
                'description': content,
                'source_url': self._extract_linkedin_url_from_content(content),
                'email_id': email_data.get('id'),
                'email_subject': subject,
                'posting_date': email_data.get('date')
            }
            
            return job_data if job_data['title'] and job_data['company'] else None
            
        except Exception as e:
            logger.error(f"Error extracting job from LinkedIn email: {e}")
            return None
    
    async def _extract_job_from_indeed_email(self, email_data: Dict) -> Optional[Dict]:
        """Extract job information from Indeed email"""
        try:
            # Parse Indeed job email format
            content = email_data.get('content', '')
            subject = email_data.get('subject', '')
            
            job_data = {
                'title': self._extract_title_from_content(content),
                'company': self._extract_company_from_content(content),
                'location': self._extract_location_from_content(content),
                'description': content,
                'source_url': self._extract_indeed_url_from_content(content),
                'email_id': email_data.get('id'),
                'email_subject': subject,
                'posting_date': email_data.get('date')
            }
            
            return job_data if job_data['title'] and job_data['company'] else None
            
        except Exception as e:
            logger.error(f"Error extracting job from Indeed email: {e}")
            return None
    
    async def _save_job_if_new(self, job_data: Dict) -> bool:
        """Save job to database if it's not a duplicate"""
        try:
            # Check for duplicates based on title, company, and URL
            if await self._is_duplicate_job(job_data):
                return False
            
            # Create AggregatedJob instance and save to database
            async with get_async_session() as session:
                # Save job logic here
                logger.info(f"Saved new job: {job_data['title']} at {job_data['company']}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving job: {e}")
            return False
    
    async def _is_duplicate_job(self, job_data: Dict) -> bool:
        """Check if job already exists in database"""
        # Implement duplicate detection logic
        # Check by: title + company, URL, source_job_id
        return False
    
    async def _remove_duplicates(self, user_id: str) -> int:
        """Remove duplicate jobs across all sources"""
        # Implement cross-source duplicate removal
        return 0
    
    def _extract_title_from_content(self, content: str) -> Optional[str]:
        """Extract job title from email content"""
        # Implement title extraction logic
        return None
    
    def _extract_company_from_content(self, content: str) -> Optional[str]:
        """Extract company name from email content"""
        # Implement company extraction logic
        return None
    
    def _extract_location_from_content(self, content: str) -> Optional[str]:
        """Extract location from email content"""
        # Implement location extraction logic
        return None
    
    def _extract_linkedin_url_from_content(self, content: str) -> Optional[str]:
        """Extract LinkedIn job URL from email content"""
        # Implement URL extraction logic
        return None
    
    def _extract_indeed_url_from_content(self, content: str) -> Optional[str]:
        """Extract Indeed job URL from email content"""
        # Implement URL extraction logic  
        return None

    async def process_selected_jobs(self, user_id: str, job_ids: List[str]) -> Dict[str, Any]:
        """
        Generate applications for selected jobs
        """
        logger.info(f"Processing selected jobs for user {user_id}: {job_ids}")
        
        results = {
            'processed_jobs': 0,
            'successful_applications': 0,
            'errors': []
        }
        
        for job_id in job_ids:
            try:
                # Fetch job from database
                job = await self._get_job_by_id(job_id)
                if not job:
                    continue
                
                # Generate customized CV and cover letter
                documents = await self.job_processor.generate_application_documents(job)
                
                if documents['success']:
                    # Update job status
                    await self._update_job_status(job_id, 'generated')
                    results['successful_applications'] += 1
                    
                    # Optionally send email with documents
                    await self._send_application_email(job, documents)
                
                results['processed_jobs'] += 1
                
            except Exception as e:
                error_msg = f"Error processing job {job_id}: {str(e)}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
        
        return results
    
    async def _get_job_by_id(self, job_id: str):
        """Fetch job from database by ID"""
        # Implement database fetch
        return None
    
    async def _update_job_status(self, job_id: str, status: str):
        """Update job application status"""
        # Implement database update
        pass
    
    async def _send_application_email(self, job: Dict, documents: Dict):
        """Send application email with generated documents"""
        # Implement email sending
        pass