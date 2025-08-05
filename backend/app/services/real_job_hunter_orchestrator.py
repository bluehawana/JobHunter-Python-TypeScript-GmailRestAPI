import os
import logging
import asyncio
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import json
import subprocess
import tempfile

from .job_scanner_service import JobScannerService
from .real_job_scrapers import LinkedInJobScraper, IndeedJobScraper, ArbetsformedlingenScraper
from .job_analysis_service import JobAnalysisService
from .smart_cv_customization_service import SmartCVCustomizationService
from .smart_cover_letter_service import SmartCoverLetterService
from .professional_latex_service import ProfessionalLaTeXService

logger = logging.getLogger(__name__)

class RealJobHunterOrchestrator:
    """
    Advanced job hunting orchestrator that processes real job advertisements
    from Gmail, LinkedIn, Indeed, and Arbetsförmedlingen to generate
    highly customized CVs and cover letters
    """
    
    def __init__(self):
        # Initialize all services
        self.gmail_scanner = JobScannerService()
        self.linkedin_scraper = LinkedInJobScraper()
        self.indeed_scraper = IndeedJobScraper()
        self.arbetsformedlingen_scraper = ArbetsformedlingenScraper()
        self.job_analyzer = JobAnalysisService()
        self.cv_customizer = SmartCVCustomizationService()
        self.cover_letter_service = SmartCoverLetterService()
        self.latex_service = ProfessionalLaTeXService()
        
        # Configuration
        self.max_jobs_per_source = 10
        self.max_total_jobs = 25
        self.processed_jobs_file = "processed_real_jobs.json"
        self.reports_dir = "job_processing_reports"
        
        # Processing statistics
        self.processing_stats = {
            'session_start': datetime.now().isoformat(),
            'total_found': 0,
            'successfully_processed': 0,
            'failed_processing': 0,
            'pdfs_generated': 0,
            'emails_sent': 0,
            'sources_used': [],
            'processing_time': 0
        }
        
        # Create reports directory
        os.makedirs(self.reports_dir, exist_ok=True)

    async def run_comprehensive_job_hunt(self, sources: List[str] = None) -> Dict:
        """
        Run comprehensive job hunting across all sources with real job analysis
        """
        start_time = datetime.now()
        
        try:
            logger.info("🚀 Starting comprehensive real job hunting workflow...")
            
            # Default to all sources if none specified
            if sources is None:
                sources = ['gmail', 'linkedin', 'indeed', 'arbetsformedlingen']
            
            self.processing_stats['sources_used'] = sources
            
            # Load previously processed jobs
            processed_jobs = self._load_processed_jobs()
            
            # Phase 1: Collect jobs from all sources
            logger.info("📥 Phase 1: Collecting jobs from all sources...")
            all_jobs = await self._collect_jobs_from_sources(sources)
            
            self.processing_stats['total_found'] = len(all_jobs)
            logger.info(f"Found {len(all_jobs)} total job opportunities")
            
            # Phase 2: Filter new jobs and prioritize
            logger.info("🔍 Phase 2: Filtering and prioritizing jobs...")
            new_jobs = self._filter_new_jobs(all_jobs, processed_jobs)
            prioritized_jobs = await self._prioritize_jobs(new_jobs)
            
            # Limit number of jobs to process
            jobs_to_process = prioritized_jobs[:self.max_total_jobs]
            logger.info(f"Selected {len(jobs_to_process)} jobs for processing")
            
            # Phase 3: Analyze jobs in parallel
            logger.info("🧠 Phase 3: Analyzing job requirements...")
            analyzed_jobs = await self.job_analyzer.analyze_multiple_jobs(jobs_to_process)
            
            # Phase 4: Generate customized documents
            logger.info("📄 Phase 4: Generating customized CVs and cover letters...")
            document_results = await self._generate_all_documents(analyzed_jobs)
            
            # Phase 5: Compile PDFs and send emails
            logger.info("📧 Phase 5: Compiling PDFs and sending emails...")
            email_results = await self._compile_and_send_emails(document_results)
            
            # Phase 6: Update processed jobs and generate report
            self._update_processed_jobs(processed_jobs, email_results)
            processing_report = self._generate_processing_report(email_results)
            
            # Calculate processing time
            end_time = datetime.now()
            self.processing_stats['processing_time'] = (end_time - start_time).total_seconds()
            
            logger.info("✅ Comprehensive job hunting workflow completed!")
            return processing_report
            
        except Exception as e:
            logger.error(f"❌ Error in comprehensive job hunt: {e}")
            return {
                'error': str(e),
                'processing_stats': self.processing_stats,
                'timestamp': datetime.now().isoformat()
            }

    async def _collect_jobs_from_sources(self, sources: List[str]) -> List[Dict]:
        """
        Collect jobs from all requested sources in parallel
        """
        collection_tasks = []
        
        if 'gmail' in sources:
            collection_tasks.append(('gmail', self.gmail_scanner.scan_gmail_jobs(days_back=5)))
        
        if 'linkedin' in sources:
            collection_tasks.append(('linkedin', self.linkedin_scraper.scrape_linkedin_jobs(max_jobs=self.max_jobs_per_source)))
        
        if 'indeed' in sources:
            collection_tasks.append(('indeed', self.indeed_scraper.scrape_indeed_jobs(max_jobs=self.max_jobs_per_source)))
        
        if 'arbetsformedlingen' in sources:
            collection_tasks.append(('arbetsformedlingen', self.arbetsformedlingen_scraper.scrape_arbetsformedlingen_jobs(max_jobs=self.max_jobs_per_source)))
        
        # Execute collection tasks in parallel
        results = await asyncio.gather(*[task for _, task in collection_tasks], return_exceptions=True)
        
        all_jobs = []
        for i, (source_name, _) in enumerate(collection_tasks):
            result = results[i]
            if isinstance(result, Exception):
                logger.error(f"Error collecting from {source_name}: {result}")
                continue
            
            source_jobs = result or []
            logger.info(f"Collected {len(source_jobs)} jobs from {source_name}")
            
            # Add source metadata
            for job in source_jobs:
                job['collection_source'] = source_name
                job['collection_timestamp'] = datetime.now().isoformat()
            
            all_jobs.extend(source_jobs)
        
        return all_jobs

    def _filter_new_jobs(self, all_jobs: List[Dict], processed_jobs: Dict) -> List[Dict]:
        """
        Filter out jobs that have already been processed
        """
        new_jobs = []
        
        for job in all_jobs:
            job_id = self._generate_job_id(job)
            if job_id not in processed_jobs:
                new_jobs.append(job)
            else:
                logger.debug(f"Skipping already processed job: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}")
        
        logger.info(f"Filtered to {len(new_jobs)} new jobs from {len(all_jobs)} total")
        return new_jobs

    async def _prioritize_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """
        Prioritize jobs based on relevance, urgency, and company quality
        """
        try:
            scored_jobs = []
            
            for job in jobs:
                score = await self._calculate_job_priority_score(job)
                scored_jobs.append((job, score))
            
            # Sort by score (highest first)
            scored_jobs.sort(key=lambda x: x[1], reverse=True)
            
            # Log top jobs for transparency
            logger.info("🎯 Top prioritized jobs:")
            for i, (job, score) in enumerate(scored_jobs[:5]):
                logger.info(f"  {i+1}. {job.get('company', 'Unknown')} - {job.get('title', 'Unknown')} (Score: {score:.2f})")
            
            return [job for job, score in scored_jobs]
            
        except Exception as e:
            logger.error(f"Error prioritizing jobs: {e}")
            return jobs  # Return original order if prioritization fails

    async def _calculate_job_priority_score(self, job: Dict) -> float:
        """
        Calculate priority score for a job (0-10 scale)
        """
        score = 5.0  # Base score
        
        # Company quality bonus
        high_quality_companies = ['spotify', 'klarna', 'volvo', 'ericsson', 'google', 'microsoft', 'amazon']
        company_name = job.get('company', '').lower()
        if any(company in company_name for company in high_quality_companies):
            score += 2.0
        
        # Recent posting bonus
        if job.get('date_posted') == 'Today' or job.get('date_posted') == 'Idag':
            score += 1.5
        elif job.get('date_posted') in ['Yesterday', 'Igår', 'Recent']:
            score += 1.0
        
        # Technical relevance bonus
        job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()
        relevant_skills = ['java', 'javascript', 'python', 'react', 'spring', 'aws', 'docker', 'kubernetes']
        skill_matches = sum(1 for skill in relevant_skills if skill in job_text)
        score += min(skill_matches * 0.3, 2.0)  # Cap at 2.0 bonus
        
        # Location preference (Sweden-based jobs)
        location = job.get('location', '').lower()
        if any(city in location for city in ['stockholm', 'göteborg', 'gothenburg', 'malmö']):
            score += 1.0
        elif 'sweden' in location or 'sverige' in location:
            score += 0.5
        
        # Job type preference
        if job.get('employment_type') in ['Permanent', 'Tillsvidare', 'Full-time']:
            score += 0.5
        
        # Source quality bonus
        source = job.get('collection_source', '')
        if source == 'gmail':
            score += 1.0  # Direct emails are often high quality
        elif source == 'linkedin':
            score += 0.5
        
        # Urgency indicators
        urgent_keywords = ['urgent', 'immediate', 'asap', 'snabbt', 'omgående']
        if any(keyword in job_text for keyword in urgent_keywords):
            score += 1.0
        
        return min(score, 10.0)  # Cap at 10.0

    async def _generate_all_documents(self, analyzed_jobs: List[Dict]) -> List[Dict]:
        """
        Generate customized CVs and cover letters for all analyzed jobs
        """
        try:
            logger.info(f"📝 Generating documents for {len(analyzed_jobs)} jobs...")
            
            # Generate CVs and cover letters in parallel  
            cv_task = self.cv_customizer.batch_create_customized_cvs(analyzed_jobs)
            cl_task = self.cover_letter_service.batch_create_cover_letters(analyzed_jobs)
            
            cv_results, cl_results = await asyncio.gather(cv_task, cl_task)
            
            # Combine results
            document_results = []
            for i, job_analysis in enumerate(analyzed_jobs):
                job_data = job_analysis['job_data']
                
                # Find corresponding CV and cover letter
                cv_result = next((cv for cv in cv_results if cv['job_data']['company'] == job_data['company']), None)
                cl_result = next((cl for cl in cl_results if cl['job_data']['company'] == job_data['company']), None)
                
                if cv_result and cl_result:
                    document_results.append({
                        'job_data': job_data,
                        'job_requirements': job_analysis['requirements'],
                        'cv_latex': cv_result['cv_latex'],
                        'cover_letter_latex': cl_result['cover_letter_latex'],
                        'generation_successful': True
                    })
                    self.processing_stats['successfully_processed'] += 1
                else:
                    logger.warning(f"Failed to generate documents for {job_data.get('company', 'Unknown')}")
                    self.processing_stats['failed_processing'] += 1
            
            logger.info(f"✅ Successfully generated documents for {len(document_results)} jobs")
            return document_results
            
        except Exception as e:
            logger.error(f"❌ Error generating documents: {e}")
            return []

    async def _compile_and_send_emails(self, document_results: List[Dict]) -> List[Dict]:
        """
        Compile LaTeX to PDFs and send application emails
        """
        email_results = []
        
        for doc_result in document_results:
            try:
                job_data = doc_result['job_data']
                logger.info(f"📧 Processing email for {job_data.get('company', 'Unknown')}")
                
                # Compile LaTeX to PDFs
                cv_pdf = await self._compile_latex_to_pdf(doc_result['cv_latex'], 'cv')
                cl_pdf = await self._compile_latex_to_pdf(doc_result['cover_letter_latex'], 'cover_letter')
                
                if cv_pdf and cl_pdf:
                    self.processing_stats['pdfs_generated'] += 2
                    
                    # Send email with attachments
                    email_sent = await self.gmail_scanner.send_job_email(job_data, cv_pdf, cl_pdf)
                    
                    email_results.append({
                        'job_data': job_data,
                        'pdf_compilation_successful': True,
                        'email_sent': email_sent,
                        'cv_pdf_size': len(cv_pdf),
                        'cl_pdf_size': len(cl_pdf),
                        'processed_at': datetime.now().isoformat()
                    })
                    
                    if email_sent:
                        self.processing_stats['emails_sent'] += 1
                        logger.info(f"✅ Successfully sent application email for {job_data.get('company')}")
                    else:
                        logger.warning(f"⚠️ Failed to send email for {job_data.get('company')}")
                else:
                    logger.error(f"❌ Failed to compile PDFs for {job_data.get('company')}")
                    email_results.append({
                        'job_data': job_data,
                        'pdf_compilation_successful': False,
                        'email_sent': False,
                        'error': 'PDF compilation failed'
                    })
                
                # Small delay between emails to be respectful
                await asyncio.sleep(3)
                
            except Exception as e:
                logger.error(f"❌ Error processing email for {job_data.get('company', 'Unknown')}: {e}")
                email_results.append({
                    'job_data': job_data,
                    'error': str(e),
                    'email_sent': False
                })
        
        return email_results

    async def _compile_latex_to_pdf(self, latex_content: str, doc_type: str) -> Optional[bytes]:
        """
        Compile LaTeX content to PDF
        """
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Write LaTeX content to temporary file
                tex_file = os.path.join(temp_dir, f"{doc_type}.tex")
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                
                # Compile to PDF using pdflatex
                result = subprocess.run(
                    ['pdflatex', '-output-directory', temp_dir, '-interaction=nonstopmode', tex_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    pdf_file = os.path.join(temp_dir, f"{doc_type}.pdf")
                    if os.path.exists(pdf_file):
                        with open(pdf_file, 'rb') as f:
                            return f.read()
                
                logger.error(f"LaTeX compilation failed for {doc_type}: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error compiling {doc_type} to PDF: {e}")
            return None

    def _generate_job_id(self, job: Dict) -> str:
        """
        Generate unique ID for job to avoid duplicates
        """
        company = job.get('company', 'unknown').lower().replace(' ', '_')
        title = job.get('title', 'unknown').lower().replace(' ', '_')
        source = job.get('collection_source', 'unknown')
        
        # Include source to allow same job from different sources
        return f"{source}_{company}_{title}"

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

    def _update_processed_jobs(self, processed_jobs: Dict, email_results: List[Dict]):
        """
        Update processed jobs tracking
        """
        try:
            for result in email_results:
                job_data = result['job_data']
                job_id = self._generate_job_id(job_data)
                
                processed_jobs[job_id] = {
                    'job_data': {
                        'title': job_data.get('title'),
                        'company': job_data.get('company'),
                        'source': job_data.get('collection_source'),
                        'location': job_data.get('location')
                    },
                    'processed_date': datetime.now().isoformat(),
                    'email_sent': result.get('email_sent', False),
                    'pdf_compilation_successful': result.get('pdf_compilation_successful', False)
                }
            
            # Save updated processed jobs
            with open(self.processed_jobs_file, 'w') as f:
                json.dump(processed_jobs, f, indent=2)
            
            logger.info(f"Updated processed jobs tracking with {len(email_results)} new entries")
            
        except Exception as e:
            logger.error(f"Error updating processed jobs: {e}")

    def _generate_processing_report(self, email_results: List[Dict]) -> Dict:
        """
        Generate comprehensive processing report
        """
        successful_applications = [r for r in email_results if r.get('email_sent', False)]
        failed_applications = [r for r in email_results if not r.get('email_sent', False)]
        
        report = {
            'session_summary': {
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': self.processing_stats['processing_time'],
                'sources_used': self.processing_stats['sources_used']
            },
            'job_statistics': {
                'total_jobs_found': self.processing_stats['total_found'],
                'jobs_processed': self.processing_stats['successfully_processed'],
                'processing_failed': self.processing_stats['failed_processing'],
                'pdfs_generated': self.processing_stats['pdfs_generated'],
                'emails_sent': self.processing_stats['emails_sent']
            },
            'successful_applications': [
                {
                    'company': r['job_data'].get('company'),
                    'title': r['job_data'].get('title'),
                    'source': r['job_data'].get('collection_source'),
                    'location': r['job_data'].get('location'),
                    'application_link': r['job_data'].get('application_link')
                }
                for r in successful_applications
            ],
            'failed_applications': [
                {
                    'company': r['job_data'].get('company'),
                    'title': r['job_data'].get('title'),
                    'error': r.get('error', 'Unknown error')
                }
                for r in failed_applications
            ],
            'performance_metrics': {
                'success_rate': len(successful_applications) / max(len(email_results), 1) * 100,
                'average_processing_time_per_job': self.processing_stats['processing_time'] / max(len(email_results), 1),
                'jobs_per_minute': len(email_results) / max(self.processing_stats['processing_time'] / 60, 1)
            }
        }
        
        # Save report to file
        report_file = os.path.join(self.reports_dir, f"job_hunt_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"📊 Processing report saved to {report_file}")
        except Exception as e:
            logger.error(f"Error saving report: {e}")
        
        return report

    async def run_targeted_job_hunt(self, sources: List[str], keywords: List[str], max_jobs: int = 15) -> Dict:
        """
        Run targeted job hunting with specific keywords and sources
        """
        try:
            logger.info(f"🎯 Starting targeted job hunt for keywords: {keywords}")
            
            # Customize scrapers with specific keywords
            if 'linkedin' in sources:
                self.linkedin_scraper.keywords = keywords[:5]  # Limit to prevent blocking
            
            if 'indeed' in sources:
                self.indeed_scraper.keywords = [kw.replace(' ', ' ') for kw in keywords[:3]]
            
            # Run comprehensive hunt with limited scope
            self.max_total_jobs = max_jobs
            return await self.run_comprehensive_job_hunt(sources)
            
        except Exception as e:
            logger.error(f"Error in targeted job hunt: {e}")
            return {'error': str(e)}

    async def get_processing_status(self) -> Dict:
        """
        Get current processing status and statistics
        """
        return {
            'current_stats': self.processing_stats,
            'processed_jobs_count': len(self._load_processed_jobs()),
            'last_processing_time': self.processing_stats.get('session_start'),
            'active_sources': self.processing_stats.get('sources_used', []),
            'recent_reports': self._get_recent_reports()
        }

    def _get_recent_reports(self) -> List[str]:
        """Get list of recent processing reports"""
        try:
            reports = []
            for file in os.listdir(self.reports_dir):
                if file.startswith('job_hunt_report_') and file.endswith('.json'):
                    reports.append(file)
            
            # Sort by timestamp (newest first)
            reports.sort(reverse=True)
            return reports[:5]  # Return 5 most recent
            
        except Exception as e:
            logger.error(f"Error getting recent reports: {e}")
            return []