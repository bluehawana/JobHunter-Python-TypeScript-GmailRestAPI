import os
import logging
import asyncio
from typing import List, Dict
from datetime import datetime
import json

from .job_scanner_service import JobScannerService
from .professional_latex_service import ProfessionalLaTeXService

logger = logging.getLogger(__name__)

class JobHunterOrchestrator:
    """
    Main orchestrator for the complete job hunting automation workflow
    Scans jobs, generates personalized CV/CL, and sends application emails
    """
    
    def __init__(self):
        self.job_scanner = JobScannerService()
        self.latex_service = ProfessionalLaTeXService()
        
        # Processing settings
        self.max_jobs_per_run = 5  # Limit to avoid spam
        self.processed_jobs_file = "processed_jobs.json"
        
    async def run_daily_job_scan(self) -> Dict:
        """
        Main daily job scanning workflow
        """
        try:
            logger.info("🚀 Starting daily job scanning workflow...")
            
            # Load previously processed jobs to avoid duplicates
            processed_jobs = self._load_processed_jobs()
            
            # Scan for new jobs
            gmail_jobs = await self.job_scanner.scan_gmail_jobs(days_back=3)
            linkedin_jobs = await self.job_scanner.scan_linkedin_jobs()
            
            all_jobs = gmail_jobs + linkedin_jobs
            logger.info(f"Found {len(all_jobs)} total job opportunities")
            
            # Filter out already processed jobs
            new_jobs = []
            for job in all_jobs:
                job_id = self._generate_job_id(job)
                if job_id not in processed_jobs:
                    new_jobs.append(job)
            
            logger.info(f"Found {len(new_jobs)} new job opportunities to process")
            
            # Limit number of jobs to process
            jobs_to_process = new_jobs[:self.max_jobs_per_run]
            
            results = {
                'total_found': len(all_jobs),
                'new_jobs': len(new_jobs),
                'processed': 0,
                'successful_emails': 0,
                'failed_emails': 0,
                'jobs_processed': []
            }
            
            # Process each job
            for job in jobs_to_process:
                try:
                    logger.info(f"Processing job: {job['title']} at {job['company']}")
                    
                    # Generate personalized CV and Cover Letter
                    cv_pdf = await self.latex_service.generate_customized_cv(job)
                    cl_pdf = await self.latex_service.generate_customized_cover_letter(job)
                    
                    if cv_pdf and cl_pdf:
                        # Send job notification email with attachments
                        email_sent = await self.job_scanner.send_job_email(job, cv_pdf, cl_pdf)
                        
                        if email_sent:
                            results['successful_emails'] += 1
                            
                            # Mark job as processed
                            job_id = self._generate_job_id(job)
                            processed_jobs[job_id] = {
                                'title': job['title'],
                                'company': job['company'],
                                'processed_date': datetime.now().isoformat(),
                                'email_sent': True
                            }
                            
                            results['jobs_processed'].append({
                                'title': job['title'],
                                'company': job['company'],
                                'status': 'success'
                            })
                            
                        else:
                            results['failed_emails'] += 1
                            results['jobs_processed'].append({
                                'title': job['title'],
                                'company': job['company'],
                                'status': 'email_failed'
                            })
                    else:
                        logger.error(f"Failed to generate documents for {job['company']}")
                        results['failed_emails'] += 1
                        results['jobs_processed'].append({
                            'title': job['title'],
                            'company': job['company'],
                            'status': 'document_generation_failed'
                        })
                    
                    results['processed'] += 1
                    
                    # Small delay between jobs to be respectful
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error processing job {job.get('title', 'Unknown')}: {e}")
                    results['failed_emails'] += 1
                    results['jobs_processed'].append({
                        'title': job.get('title', 'Unknown'),
                        'company': job.get('company', 'Unknown'),
                        'status': 'processing_error',
                        'error': str(e)
                    })
            
            # Save processed jobs
            self._save_processed_jobs(processed_jobs)
            
            # Log summary
            logger.info(f"✅ Job scanning completed:")
            logger.info(f"   📧 Successful emails: {results['successful_emails']}")
            logger.info(f"   ❌ Failed emails: {results['failed_emails']}")
            logger.info(f"   📊 Total processed: {results['processed']}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in daily job scan workflow: {e}")
            return {
                'error': str(e),
                'total_found': 0,
                'processed': 0,
                'successful_emails': 0,
                'failed_emails': 0
            }
    
    async def process_single_job(self, job_data: Dict) -> bool:
        """
        Process a single job manually (for testing or manual triggers)
        """
        try:
            logger.info(f"Processing single job: {job_data['title']} at {job_data['company']}")
            
            # Generate documents
            cv_pdf = await self.latex_service.generate_customized_cv(job_data)
            cl_pdf = await self.latex_service.generate_customized_cover_letter(job_data)
            
            if cv_pdf and cl_pdf:
                # Send email
                email_sent = await self.job_scanner.send_job_email(job_data, cv_pdf, cl_pdf)
                
                if email_sent:
                    logger.info(f"✅ Successfully processed job: {job_data['company']}")
                    return True
                else:
                    logger.error(f"❌ Failed to send email for: {job_data['company']}")
                    return False
            else:
                logger.error(f"❌ Failed to generate documents for: {job_data['company']}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error processing single job: {e}")
            return False
    
    def _generate_job_id(self, job: Dict) -> str:
        """
        Generate unique ID for job to avoid duplicates
        """
        company = job.get('company', 'unknown').lower().replace(' ', '_')
        title = job.get('title', 'unknown').lower().replace(' ', '_')
        link = job.get('application_link', '')
        
        if link:
            # Use link hash for uniqueness
            import hashlib
            link_hash = hashlib.md5(link.encode()).hexdigest()[:8]
            return f"{company}_{title}_{link_hash}"
        else:
            # Fallback to company_title
            return f"{company}_{title}"
    
    def _load_processed_jobs(self) -> Dict:
        """
        Load previously processed jobs from file
        """
        try:
            if os.path.exists(self.processed_jobs_file):
                with open(self.processed_jobs_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading processed jobs: {e}")
        
        return {}
    
    def _save_processed_jobs(self, processed_jobs: Dict):
        """
        Save processed jobs to file
        """
        try:
            with open(self.processed_jobs_file, 'w') as f:
                json.dump(processed_jobs, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving processed jobs: {e}")
    
    async def test_gmail_connection(self) -> bool:
        """
        Test Gmail connection for job scanning
        """
        try:
            logger.info("Testing Gmail connection...")
            jobs = await self.job_scanner.scan_gmail_jobs(days_back=1)
            logger.info(f"✅ Gmail connection successful! Found {len(jobs)} recent jobs")
            return True
        except Exception as e:
            logger.error(f"❌ Gmail connection failed: {e}")
            return False
    
    async def get_job_summary(self) -> Dict:
        """
        Get summary of processed jobs
        """
        try:
            processed_jobs = self._load_processed_jobs()
            
            # Count jobs by date
            from collections import defaultdict
            jobs_by_date = defaultdict(int)
            
            for job_id, job_info in processed_jobs.items():
                date = job_info.get('processed_date', '')[:10]  # Get date part
                jobs_by_date[date] += 1
            
            return {
                'total_processed': len(processed_jobs),
                'jobs_by_date': dict(jobs_by_date),
                'recent_jobs': list(processed_jobs.values())[-10:]  # Last 10 jobs
            }
            
        except Exception as e:
            logger.error(f"Error getting job summary: {e}")
            return {'error': str(e)}
    
    async def cleanup_old_processed_jobs(self, days_to_keep: int = 30):
        """
        Clean up old processed jobs to prevent file from growing too large
        """
        try:
            processed_jobs = self._load_processed_jobs()
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            cleaned_jobs = {}
            removed_count = 0
            
            for job_id, job_info in processed_jobs.items():
                try:
                    processed_date = datetime.fromisoformat(job_info.get('processed_date', ''))
                    if processed_date >= cutoff_date:
                        cleaned_jobs[job_id] = job_info
                    else:
                        removed_count += 1
                except:
                    # Keep jobs with invalid dates
                    cleaned_jobs[job_id] = job_info
            
            if removed_count > 0:
                self._save_processed_jobs(cleaned_jobs)
                logger.info(f"Cleaned up {removed_count} old processed jobs")
            
        except Exception as e:
            logger.error(f"Error cleaning up processed jobs: {e}")