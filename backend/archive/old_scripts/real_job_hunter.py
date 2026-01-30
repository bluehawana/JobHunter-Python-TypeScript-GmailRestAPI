#!/usr/bin/env python3
"""
Real Job Hunter - Comprehensive real job scanning and application system
Scans actual job postings from Gmail, LinkedIn, Indeed, and Arbetsförmedlingen
"""
import asyncio
import logging
import sys
import os
from datetime import datetime
from typing import List, Dict

# Add the app directory to Python path
sys.path.append('/Users/bluehawana/Projects/Jobhunter/backend')

from app.services.real_job_scanner import RealJobScanner
from app.services.real_job_scrapers import LinkedInJobScraper, IndeedJobScraper, ArbetsformedlingenScraper
from app.services.professional_latex_service import ProfessionalLaTeXService
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RealJobHunter:
    """
    Comprehensive real job hunting system that scans actual job advertisements
    """
    
    def __init__(self):
        self.gmail_scanner = RealJobScanner()
        self.linkedin_scraper = LinkedInJobScraper()
        self.indeed_scraper = IndeedJobScraper()
        self.arbetsformedlingen_scraper = ArbetsformedlingenScraper()
        self.latex_service = ProfessionalLaTeXService()
        
        # Email configuration
        self.sender_email = os.getenv("SENDER_EMAIL", "leeharvad@gmail.com")
        self.sender_password = os.getenv("SMTP_PASSWORD", "")
        self.target_email = "hongzhili01@gmail.com"
        
        # Processing settings
        self.max_jobs_per_source = 5
        self.processed_jobs_file = "real_processed_jobs.json"
    
    async def hunt_real_jobs(self) -> Dict:
        """
        Main method to hunt for real job opportunities
        """
        try:
            logger.info("🚀 Starting REAL job hunting workflow...")
            logger.info("🎯 Scanning actual job advertisements from multiple sources")
            
            # Scan all sources concurrently for better performance
            tasks = [
                self._scan_gmail_jobs(),
                self._scan_linkedin_jobs(),
                self._scan_indeed_jobs(),
                self._scan_arbetsformedlingen_jobs()
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combine all jobs
            all_jobs = []
            source_counts = {}
            
            for i, result in enumerate(results):
                source_names = ['Gmail', 'LinkedIn', 'Indeed', 'Arbetsförmedlingen']
                source_name = source_names[i]
                
                if isinstance(result, Exception):
                    logger.error(f"❌ Error scanning {source_name}: {result}")
                    source_counts[source_name] = 0
                else:
                    jobs = result or []
                    all_jobs.extend(jobs)
                    source_counts[source_name] = len(jobs)
                    logger.info(f"✅ {source_name}: Found {len(jobs)} jobs")
            
            logger.info(f"📊 Total jobs found: {len(all_jobs)}")
            
            # Remove duplicates and prioritize quality jobs
            unique_jobs = self._prioritize_quality_jobs(all_jobs)
            logger.info(f"🎯 After quality filtering: {len(unique_jobs)} unique opportunities")
            
            # Process each job with custom CV/CL
            processed_results = {
                'total_found': len(all_jobs),
                'unique_jobs': len(unique_jobs),
                'source_breakdown': source_counts,
                'processed': 0,
                'successful_emails': 0,
                'failed_emails': 0,
                'job_details': []
            }
            
            # Limit processing to avoid overwhelming
            jobs_to_process = unique_jobs[:8]  # Process max 8 quality jobs
            
            for job in jobs_to_process:
                try:
                    logger.info(f"🔄 Processing: {job['title']} at {job['company']}")
                    
                    # Generate customized CV and Cover Letter
                    cv_pdf = await self.latex_service.generate_customized_cv(job)
                    cl_pdf = await self.latex_service.generate_customized_cover_letter(job)
                    
                    if cv_pdf and cl_pdf:
                        # Send personalized job email
                        email_sent = await self._send_real_job_email(job, cv_pdf, cl_pdf)
                        
                        job_result = {
                            'title': job['title'],
                            'company': job['company'],
                            'source': job.get('source', 'unknown'),
                            'application_link': job.get('application_link', ''),
                            'status': 'success' if email_sent else 'email_failed',
                            'keywords': job.get('keywords', [])[:5],
                            'salary': job.get('salary', ''),
                            'location': job.get('location', '')
                        }
                        
                        if email_sent:
                            processed_results['successful_emails'] += 1
                            logger.info(f"✅ Email sent for {job['company']} - {job['title']}")
                        else:
                            processed_results['failed_emails'] += 1
                            logger.error(f"❌ Email failed for {job['company']} - {job['title']}")
                        
                        processed_results['job_details'].append(job_result)
                    else:
                        logger.error(f"❌ Document generation failed for {job['company']}")
                        processed_results['failed_emails'] += 1
                    
                    processed_results['processed'] += 1
                    
                    # Small delay between jobs
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"❌ Error processing job {job.get('title', 'Unknown')}: {e}")
                    processed_results['failed_emails'] += 1
            
            # Summary
            logger.info("🎉 REAL Job hunting completed!")
            logger.info(f"📧 Successful applications: {processed_results['successful_emails']}")
            logger.info(f"❌ Failed applications: {processed_results['failed_emails']}")
            logger.info(f"📊 Total processed: {processed_results['processed']}")
            
            if processed_results['successful_emails'] > 0:
                logger.info(f"💌 Check {self.target_email} for {processed_results['successful_emails']} personalized job opportunities!")
            
            return processed_results
            
        except Exception as e:
            logger.error(f"❌ Error in real job hunting workflow: {e}")
            return {'error': str(e)}
    
    async def _scan_gmail_jobs(self) -> List[Dict]:
        """Scan real Gmail jobs"""
        try:
            return await self.gmail_scanner.scan_real_gmail_jobs(days_back=3)
        except Exception as e:
            logger.error(f"Gmail scanning error: {e}")
            return []
    
    async def _scan_linkedin_jobs(self) -> List[Dict]:
        """Scan real LinkedIn jobs"""
        try:
            return await self.linkedin_scraper.scrape_linkedin_jobs(max_jobs=self.max_jobs_per_source)
        except Exception as e:
            logger.error(f"LinkedIn scanning error: {e}")
            return []
    
    async def _scan_indeed_jobs(self) -> List[Dict]:
        """Scan real Indeed jobs"""
        try:
            return await self.indeed_scraper.scrape_indeed_jobs(max_jobs=self.max_jobs_per_source)
        except Exception as e:
            logger.error(f"Indeed scanning error: {e}")
            return []
    
    async def _scan_arbetsformedlingen_jobs(self) -> List[Dict]:
        """Scan real Arbetsförmedlingen jobs"""
        try:
            return await self.arbetsformedlingen_scraper.scrape_arbetsformedlingen_jobs(max_jobs=self.max_jobs_per_source)
        except Exception as e:
            logger.error(f"Arbetsförmedlingen scanning error: {e}")
            return []
    
    def _prioritize_quality_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """
        Prioritize and filter quality job opportunities
        """
        # Remove duplicates
        seen_combinations = set()
        unique_jobs = []
        
        for job in jobs:
            job_id = f"{job.get('company', '').lower()}_{job.get('title', '').lower().replace(' ', '_')}"
            if job_id not in seen_combinations and job_id != "_":
                seen_combinations.add(job_id)
                unique_jobs.append(job)
        
        # Quality scoring
        scored_jobs = []
        for job in unique_jobs:
            score = self._calculate_job_quality_score(job)
            if score >= 15:  # Minimum quality threshold
                scored_jobs.append((job, score))
        
        # Sort by score and return top jobs
        scored_jobs.sort(key=lambda x: x[1], reverse=True)
        return [job for job, score in scored_jobs[:15]]  # Top 15 quality jobs
    
    def _calculate_job_quality_score(self, job: Dict) -> int:
        """
        Calculate quality score for job prioritization
        """
        score = 0
        
        # Application method available
        if job.get('application_link'):
            score += 5
        if job.get('application_email'):
            score += 3
        
        # Content quality
        description = job.get('description', '')
        if len(description) > 200:
            score += 4
        if len(description) > 500:
            score += 2
        
        # Technical relevance
        keywords = job.get('keywords', [])
        relevant_keywords = ['fullstack', 'backend', 'frontend', 'devops', 'python', 'java', 'react', 'nodejs', 'aws', 'azure', 'kubernetes']
        relevant_count = sum(1 for kw in keywords if kw in relevant_keywords)
        score += min(relevant_count * 2, 10)  # Max 10 points for keywords
        
        # Company and role quality
        title_lower = job.get('title', '').lower()
        if any(level in title_lower for level in ['senior', 'lead', 'principal']):
            score += 3
        if any(tech in title_lower for tech in ['developer', 'engineer', 'architect']):
            score += 2
        
        # Salary information
        if job.get('salary'):
            score += 2
        
        # Requirements
        if job.get('requirements'):
            score += 2
        
        # Recent posting
        date_posted = job.get('date_posted', '').lower()
        if any(recent in date_posted for recent in ['today', 'idag', 'yesterday', 'igår', '1 day', 'recent']):
            score += 3
        
        return score
    
    async def _send_real_job_email(self, job: Dict, cv_pdf: bytes, cl_pdf: bytes) -> bool:
        """
        Send personalized job email with real job information
        """
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.target_email
            msg['Subject'] = f"🎯 REAL Job Opportunity: {job['title']} at {job['company']}"
            
            # Create enhanced email body for real jobs
            email_body = self._create_real_job_email_body(job)
            msg.attach(MIMEText(email_body, 'html'))
            
            # Attach customized CV
            if cv_pdf:
                cv_attachment = MIMEApplication(cv_pdf, _subtype='pdf')
                cv_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f"CV_{job['company']}_{job['title'].replace(' ', '_')}_Customized.pdf"
                )
                msg.attach(cv_attachment)
            
            # Attach customized Cover Letter
            if cl_pdf:
                cl_attachment = MIMEApplication(cl_pdf, _subtype='pdf')
                cl_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f"CoverLetter_{job['company']}_{job['title'].replace(' ', '_')}_Customized.pdf"
                )
                msg.attach(cl_attachment)
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            text = msg.as_string()
            server.sendmail(self.sender_email, self.target_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending real job email: {e}")
            return False
    
    def _create_real_job_email_body(self, job: Dict) -> str:
        """
        Create enhanced HTML email body for real job opportunities
        """
        # Source badge styling
        source_colors = {
            'gmail_real': '#EA4335',
            'linkedin_real': '#0077B5', 
            'indeed_real': '#2164F3',
            'arbetsformedlingen_real': '#0052CC'
        }
        
        source_names = {
            'gmail_real': 'Gmail',
            'linkedin_real': 'LinkedIn',
            'indeed_real': 'Indeed',
            'arbetsformedlingen_real': 'Arbetsförmedlingen'
        }
        
        source = job.get('source', 'unknown')
        source_color = source_colors.get(source, '#666666')
        source_name = source_names.get(source, 'Job Board')
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 650px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 20px; position: relative;">
                    <div style="position: absolute; top: 15px; right: 15px; background: {source_color}; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold;">
                        📍 {source_name}
                    </div>
                    <h1 style="margin: 0; font-size: 26px;">🎯 REAL Job Match Found!</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 14px;">Scanned from actual job advertisements</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #667eea;">
                    <h2 style="color: #2c3e50; margin-top: 0; font-size: 22px;">{job['title']}</h2>
                    <p style="font-size: 20px; color: #3498db; margin: 8px 0; font-weight: bold;">{job['company']}</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 15px; margin: 15px 0;">
                        <span style="color: #666; font-size: 14px;">📍 {job.get('location', 'Sweden')}</span>
                        {f'<span style="color: #27ae60; font-size: 14px; font-weight: bold;">💰 {job["salary"]}</span>' if job.get('salary') else ''}
                        <span style="color: #666; font-size: 14px;">⏰ {job.get('employment_type', 'Full-time')}</span>
                        {f'<span style="color: #8e44ad; font-size: 14px;">📈 {job["experience_level"]}</span>' if job.get('experience_level') else ''}
                    </div>
                </div>
                
                <div style="background: white; padding: 25px; border: 1px solid #eee; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: #2c3e50; margin-top: 0; display: flex; align-items: center;">
                        📋 Job Description 
                        <span style="background: #e8f4f8; color: #2980b9; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-left: 10px;">REAL POSTING</span>
                    </h3>
                    <p style="color: #555; line-height: 1.8; margin-bottom: 20px;">{job.get('description', 'Full job description available via application link.')[:500]}{'...' if len(job.get('description', '')) > 500 else ''}</p>
                    
                    {f'''
                    <h3 style="color: #2c3e50; margin-bottom: 10px;">📋 Requirements</h3>
                    <ul style="color: #555; padding-left: 20px;">
                        {' '.join([f'<li style="margin-bottom: 5px;">{req}</li>' for req in job.get('requirements', [])[:4]])}
                    </ul>
                    ''' if job.get('requirements') else ''}
                    
                    {f'''
                    <h3 style="color: #2c3e50; margin-bottom: 10px;">🔧 Technical Skills</h3>
                    <div style="margin: 15px 0;">
                        {' '.join([f'<span style="background: #e3f2fd; color: #1976d2; padding: 6px 12px; border-radius: 15px; font-size: 13px; margin: 3px; display: inline-block; font-weight: 500;">{kw}</span>' for kw in job.get('keywords', [])[:10]])}
                    </div>
                    ''' if job.get('keywords') else ''}
                    
                    {f'''
                    <h3 style="color: #2c3e50; margin-bottom: 10px;">🎁 Benefits</h3>
                    <ul style="color: #555; padding-left: 20px;">
                        {' '.join([f'<li style="margin-bottom: 5px;">{benefit}</li>' for benefit in job.get('benefits', [])[:3]])}
                    </ul>
                    ''' if job.get('benefits') else ''}
                </div>
                
                <div style="text-align: center; margin: 35px 0;">
                    <a href="{job.get('application_link', '#')}" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; 
                              padding: 18px 35px; 
                              text-decoration: none; 
                              border-radius: 30px; 
                              font-weight: bold; 
                              font-size: 18px;
                              display: inline-block;
                              box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
                              transition: all 0.3s ease;">
                        🚀 APPLY NOW - REAL JOB
                    </a>
                    <p style="margin-top: 10px; font-size: 12px; color: #666;">Click to go directly to the job application page</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border: 1px solid #b0e0c0; padding: 20px; border-radius: 10px; margin: 25px 0;">
                    <h3 style="color: #155724; margin-top: 0; display: flex; align-items: center;">
                        ✨ Your Customized Application Package
                    </h3>
                    <ul style="color: #155724; margin: 10px 0; padding-left: 20px;">
                        <li style="margin-bottom: 8px;"><strong>✅ Tailored CV</strong> - Optimized for this specific role and company</li>
                        <li style="margin-bottom: 8px;"><strong>✅ Custom Cover Letter</strong> - Personalized with job requirements and company research</li>
                        <li style="margin-bottom: 8px;"><strong>✅ ATS Optimized</strong> - Keywords naturally integrated for better visibility</li>
                        <li style="margin-bottom: 8px;"><strong>✅ AI Enhanced</strong> - Powered by Claude AI for maximum impact</li>
                    </ul>
                </div>
                
                <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 18px; border-radius: 10px; margin: 25px 0;">
                    <h3 style="color: #856404; margin-top: 0;">💡 Quality Assured & Ready to Submit</h3>
                    <p style="color: #856404; margin: 0; text-align: center; font-weight: 500;">
                        This is a REAL job opportunity from {source_name}. Your customized CV and Cover Letter are ready to submit. 
                        If satisfied with the quality, click "APPLY NOW" to submit your application directly!
                    </p>
                </div>
                
                <div style="margin-top: 35px; padding-top: 20px; border-top: 2px solid #eee; text-align: center; color: #666; font-size: 13px;">
                    <p style="margin: 5px 0;"><strong>📧 Source:</strong> {source_name} | <strong>🤖 AI-Enhanced Application</strong></p>
                    <p style="margin: 5px 0;"><strong>📅 Scanned:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')} | <strong>🎯 JobHunter Pro</strong></p>
                    {f'<p style="margin: 5px 0; font-size: 12px;"><strong>📞 Contact:</strong> {job["contact_person"]}</p>' if job.get('contact_person') else ''}
                    {f'<p style="margin: 5px 0; font-size: 12px;"><strong>⏰ Deadline:</strong> {job["deadline"]}</p>' if job.get('deadline') else ''}
                </div>
            </div>
        </body>
        </html>
        """

async def main():
    """Main function to run real job hunting"""
    
    print("🎯 REAL JobHunter - Scanning Actual Job Advertisements")
    print("=" * 60)
    print("📍 Sources: Gmail, LinkedIn, Indeed.se, Arbetsförmedlingen")
    print("🎯 Target: Customized CV/CL for each real job opportunity")
    print("=" * 60)
    
    # Initialize and run real job hunter
    hunter = RealJobHunter()
    results = await hunter.hunt_real_jobs()
    
    print("\n" + "="*60)
    print("📊 REAL JOB HUNTING RESULTS")
    print("="*60)
    
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
    else:
        print(f"📧 Total jobs found: {results['total_found']}")
        print(f"🎯 Quality jobs: {results['unique_jobs']}")
        print(f"✅ Successful applications: {results['successful_emails']}")
        print(f"❌ Failed applications: {results['failed_emails']}")
        
        print(f"\n📍 Source breakdown:")
        for source, count in results['source_breakdown'].items():
            print(f"   {source}: {count} jobs")
        
        if results['job_details']:
            print(f"\n📋 Jobs processed:")
            for job in results['job_details']:
                status_emoji = "✅" if job['status'] == 'success' else "❌"
                print(f"   {status_emoji} {job['company']} - {job['title']} ({job['source']})")
        
        if results['successful_emails'] > 0:
            print(f"\n💌 Check hongzhili01@gmail.com for your personalized job applications!")
            print("🎯 Each email contains customized CV/CL and direct application links")

if __name__ == "__main__":
    print("🚀 Starting REAL Job Hunter...")
    asyncio.run(main())