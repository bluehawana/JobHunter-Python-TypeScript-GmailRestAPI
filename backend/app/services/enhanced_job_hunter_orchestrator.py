import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
import json

from .real_job_scanner import RealJobScanner
from .real_job_scrapers import (
    LinkedInJobScraper, 
    IndeedJobScraper, 
    ArbetsformedlingenScraper, 
    CompanyCareerScraper
)
from .smart_cv_customization_service import SmartCVCustomizationService
from .smart_cover_letter_service import SmartCoverLetterService
from .job_scanner_service import JobScannerService

logger = logging.getLogger(__name__)

class EnhancedJobHunterOrchestrator:
    """
    Enhanced job hunting orchestrator that aggregates jobs from multiple sources
    and filters for positions suitable for developers with 5+ years experience
    """
    
    def __init__(self):
        # Initialize all scrapers
        self.gmail_scanner = RealJobScanner()
        self.linkedin_scraper = LinkedInJobScraper()
        self.indeed_scraper = IndeedJobScraper()
        self.arbetsformedlingen_scraper = ArbetsformedlingenScraper()
        self.company_scraper = CompanyCareerScraper()
        self.legacy_scanner = JobScannerService()
        
        # CV and Cover Letter services
        self.cv_service = SmartCVCustomizationService()
        self.cl_service = SmartCoverLetterService()
        
        # Target job types for experienced developer (5+ years)
        self.target_job_types = [
            "fullstack developer", "full stack developer", "senior developer",
            "backend developer", "frontend developer", "software engineer",
            "devops engineer", "cloud engineer", "cloud architect", "cloud developer",
            "software architect", "tech lead", "lead developer", "principal engineer"
        ]
        
        # Minimum experience level filter
        self.min_experience_levels = ["Senior", "Mid-level"]  # Filter out Junior positions
        
        # Technology keywords for filtering relevant positions
        self.relevant_tech_keywords = [
            "java", "python", "javascript", "typescript", "react", "angular", "vue",
            "spring", "spring boot", "nodejs", "django", "flask", ".net", "c#",
            "aws", "azure", "gcp", "docker", "kubernetes", "microservices",
            "postgresql", "mysql", "mongodb", "redis", "elasticsearch"
        ]
    
    async def hunt_jobs_comprehensive(self, max_jobs_per_source: int = 15) -> Dict:
        """
        Comprehensive job hunting across all sources with filtering for experienced developers
        """
        try:
            logger.info("🚀 Starting comprehensive job hunt for experienced developers...")
            
            results = {
                'total_found': 0,
                'filtered_jobs': [],
                'sources': {},
                'summary': {},
                'timestamp': datetime.now().isoformat()
            }
            
            # Run all job sources concurrently for maximum efficiency
            tasks = [
                self._scan_gmail_jobs(max_jobs_per_source),
                self._scan_linkedin_jobs(max_jobs_per_source),
                self._scan_indeed_jobs(max_jobs_per_source),
                self._scan_arbetsformedlingen_jobs(max_jobs_per_source),
                self._scan_company_careers(max_jobs_per_source)
            ]
            
            # Execute all tasks concurrently
            source_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results from each source
            source_names = ['gmail', 'linkedin', 'indeed', 'arbetsformedlingen', 'company_careers']
            all_jobs = []
            
            for i, (source_name, source_jobs) in enumerate(zip(source_names, source_results)):
                if isinstance(source_jobs, Exception):
                    logger.error(f"Error from {source_name}: {source_jobs}")
                    results['sources'][source_name] = {'count': 0, 'error': str(source_jobs)}
                else:
                    results['sources'][source_name] = {'count': len(source_jobs)}
                    all_jobs.extend(source_jobs)
                    logger.info(f"✅ {source_name}: {len(source_jobs)} jobs")
            
            results['total_found'] = len(all_jobs)
            
            # Filter jobs for experienced developers
            filtered_jobs = self._filter_for_experienced_developers(all_jobs)
            
            # Remove duplicates and rank jobs
            unique_jobs = self._remove_duplicates_and_rank(filtered_jobs)
            
            # Limit to reasonable number for processing
            final_jobs = unique_jobs[:50]  # Top 50 best matches
            
            results['filtered_jobs'] = final_jobs
            results['summary'] = {
                'total_sources': len(source_names),
                'total_raw_jobs': len(all_jobs),
                'filtered_jobs': len(filtered_jobs),
                'final_unique_jobs': len(final_jobs),
                'avg_experience_level': self._calculate_avg_experience_level(final_jobs),
                'top_companies': self._get_top_companies(final_jobs, limit=10),
                'top_keywords': self._get_top_keywords(final_jobs, limit=15)
            }
            
            logger.info(f"🎯 Job hunt complete: {len(final_jobs)} quality opportunities found")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in comprehensive job hunt: {e}")
            return {'error': str(e), 'total_found': 0, 'filtered_jobs': []}
    
    async def _scan_gmail_jobs(self, max_jobs: int) -> List[Dict]:
        """Scan Gmail for job opportunities"""
        try:
            return await self.gmail_scanner.scan_real_gmail_jobs(days_back=7)
        except Exception as e:
            logger.error(f"Gmail scanning error: {e}")
            return []
    
    async def _scan_linkedin_jobs(self, max_jobs: int) -> List[Dict]:
        """Scan LinkedIn for job opportunities"""
        try:
            return await self.linkedin_scraper.scrape_linkedin_jobs(max_jobs=max_jobs)
        except Exception as e:
            logger.error(f"LinkedIn scraping error: {e}")
            return []
    
    async def _scan_indeed_jobs(self, max_jobs: int) -> List[Dict]:
        """Scan Indeed for job opportunities"""
        try:
            return await self.indeed_scraper.scrape_indeed_jobs(max_jobs=max_jobs)
        except Exception as e:
            logger.error(f"Indeed scraping error: {e}")
            return []
    
    async def _scan_arbetsformedlingen_jobs(self, max_jobs: int) -> List[Dict]:
        """Scan Arbetsförmedlingen for job opportunities"""
        try:
            return await self.arbetsformedlingen_scraper.scrape_arbetsformedlingen_jobs(max_jobs=max_jobs)
        except Exception as e:
            logger.error(f"Arbetsförmedlingen scraping error: {e}")
            return []
    
    async def _scan_company_careers(self, max_jobs: int) -> List[Dict]:
        """Scan company career sites"""
        try:
            return await self.company_scraper.scrape_company_careers(max_jobs=max_jobs)
        except Exception as e:
            logger.error(f"Company careers scraping error: {e}")
            return []
    
    def _filter_for_experienced_developers(self, jobs: List[Dict]) -> List[Dict]:
        """
        Filter jobs suitable for developers with 5+ years experience
        """
        filtered_jobs = []
        
        for job in jobs:
            if self._is_suitable_for_experienced_developer(job):
                # Add quality score for ranking
                job['quality_score'] = self._calculate_job_quality_score(job)
                filtered_jobs.append(job)
        
        logger.info(f"Filtered {len(filtered_jobs)} suitable jobs from {len(jobs)} total")
        return filtered_jobs
    
    def _is_suitable_for_experienced_developer(self, job: Dict) -> bool:
        """
        Check if job is suitable for an experienced developer
        """
        # Check experience level
        experience_level = job.get('experience_level', 'Mid-level')
        if experience_level not in self.min_experience_levels:
            return False
        
        # Check if job title contains relevant developer keywords
        title = job.get('title', '').lower()
        if not any(job_type in title for job_type in self.target_job_types):
            return False
        
        # Check for relevant technical keywords
        keywords = job.get('keywords', [])
        description = job.get('description', '').lower()
        
        tech_keyword_matches = 0
        for keyword in self.relevant_tech_keywords:
            if keyword in keywords or keyword in description:
                tech_keyword_matches += 1
        
        # Must have at least 2 relevant tech keywords
        if tech_keyword_matches < 2:
            return False
        
        # Check for application method
        if not job.get('application_link') and not job.get('application_email'):
            return False
        
        return True
    
    def _calculate_job_quality_score(self, job: Dict) -> int:
        """
        Calculate quality score for job ranking (0-100)
        """
        score = 0
        
        # Experience level bonus
        if job.get('experience_level') == 'Senior':
            score += 20
        elif job.get('experience_level') == 'Mid-level':
            score += 15
        
        # Company reputation bonus
        prestigious_companies = [
            'spotify', 'klarna', 'volvo', 'skf', 'ericsson', 'h&m', 'ikea',
            'scania', 'electrolux', 'sandvik', 'atlas copco', 'alfa laval'
        ]
        company = job.get('company', '').lower()
        if any(company_name in company for company_name in prestigious_companies):
            score += 15
        
        # Keyword relevance bonus
        keywords = job.get('keywords', [])
        high_value_keywords = ['java', 'python', 'react', 'aws', 'kubernetes', 'microservices']
        for keyword in high_value_keywords:
            if keyword in keywords:
                score += 3
        
        # Description quality bonus
        description = job.get('description', '')
        if len(description) > 200:
            score += 10
        
        # Salary information bonus
        if job.get('salary'):
            score += 8
        
        # Application link bonus
        if job.get('application_link'):
            score += 5
        
        # Requirements clarity bonus
        requirements = job.get('requirements', [])
        if len(requirements) >= 3:
            score += 7
        
        return min(score, 100)  # Cap at 100
    
    def _remove_duplicates_and_rank(self, jobs: List[Dict]) -> List[Dict]:
        """
        Remove duplicates and rank by quality score
        """
        # Remove duplicates based on company + title
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            company = job.get('company', '').lower().strip()
            title = job.get('title', '').lower().strip()
            key = f"{company}_{title}".replace(' ', '_')
            
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        # Sort by quality score (highest first)
        unique_jobs.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        
        logger.info(f"Removed duplicates: {len(unique_jobs)} unique jobs from {len(jobs)}")
        return unique_jobs
    
    def _calculate_avg_experience_level(self, jobs: List[Dict]) -> str:
        """Calculate average experience level of jobs"""
        if not jobs:
            return "N/A"
        
        levels = [job.get('experience_level', 'Mid-level') for job in jobs]
        senior_count = levels.count('Senior')
        
        if senior_count > len(jobs) * 0.6:
            return "Mostly Senior"
        elif senior_count > len(jobs) * 0.3:
            return "Mixed Senior/Mid-level"
        else:
            return "Mostly Mid-level"
    
    def _get_top_companies(self, jobs: List[Dict], limit: int = 10) -> List[Dict]:
        """Get top companies by job count"""
        company_counts = {}
        for job in jobs:
            company = job.get('company', 'Unknown')
            company_counts[company] = company_counts.get(company, 0) + 1
        
        sorted_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'company': comp, 'count': count} for comp, count in sorted_companies[:limit]]
    
    def _get_top_keywords(self, jobs: List[Dict], limit: int = 15) -> List[Dict]:
        """Get top technical keywords"""
        keyword_counts = {}
        for job in jobs:
            keywords = job.get('keywords', [])
            for keyword in keywords:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'keyword': kw, 'count': count} for kw, count in sorted_keywords[:limit]]
    
    async def generate_application_documents(self, job: Dict) -> Dict:
        """
        Generate customized CV and Cover Letter for a specific job
        """
        try:
            logger.info(f"Generating application documents for {job['company']} - {job['title']}")
            
            # First analyze the job to extract requirements
            job_requirements = await self.cv_service.job_analyzer.analyze_job_posting(job)
            
            # Generate customized CV
            cv_result = await self.cv_service.create_customized_cv(job, job_requirements)
            
            # Generate customized Cover Letter
            cl_result = await self.cl_service.create_personalized_cover_letter(job, job_requirements)
            
            return {
                'job_info': {
                    'title': job['title'],
                    'company': job['company'],
                    'application_link': job.get('application_link', ''),
                    'quality_score': job.get('quality_score', 0)
                },
                'cv': cv_result,
                'cover_letter': cl_result,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating documents: {e}")
            return {'error': str(e)}
    
    async def process_top_jobs_with_documents(self, hunt_results: Dict, top_n: int = 10) -> List[Dict]:
        """
        Process top N jobs and generate application documents for each
        """
        try:
            jobs = hunt_results.get('filtered_jobs', [])[:top_n]
            logger.info(f"Processing top {len(jobs)} jobs with document generation...")
            
            # Generate documents for all top jobs concurrently
            document_tasks = [
                self.generate_application_documents(job) 
                for job in jobs
            ]
            
            document_results = await asyncio.gather(*document_tasks, return_exceptions=True)
            
            processed_jobs = []
            for i, result in enumerate(document_results):
                if isinstance(result, Exception):
                    logger.error(f"Error processing job {i}: {result}")
                else:
                    processed_jobs.append(result)
            
            logger.info(f"✅ Successfully processed {len(processed_jobs)} jobs with documents")
            return processed_jobs
            
        except Exception as e:
            logger.error(f"Error processing jobs with documents: {e}")
            return []
    
    def save_hunt_results(self, results: Dict, filename: str = None) -> str:
        """
        Save hunt results to JSON file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"job_hunt_results_{timestamp}.json"
            
            filepath = f"/Users/bluehawana/Projects/Jobhunter/backend/{filename}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Saved hunt results to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return ""