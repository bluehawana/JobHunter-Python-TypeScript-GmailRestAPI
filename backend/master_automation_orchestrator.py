#!/usr/bin/env python3
"""
Master Automation Orchestrator - Single entry point for complete job hunting workflow
Executes all steps sequentially: Gmail scan → Job processing → Document generation → Email delivery
"""
import asyncio
import sys
import os
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import traceback

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
def load_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env_file()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MasterAutomationOrchestrator:
    """Master orchestrator that runs all automation steps sequentially"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.execution_log = []
        self.processed_jobs = []
        self.successful_applications = 0
        self.failed_applications = 0
        
        logger.info("🎯 Master Automation Orchestrator initialized")
        self._log_step("INITIALIZATION", "System initialized successfully")
    
    def _log_step(self, step: str, message: str, status: str = "SUCCESS"):
        """Log each step of the automation process"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "message": message,
            "status": status
        }
        self.execution_log.append(log_entry)
        
        if status == "SUCCESS":
            logger.info(f"✅ {step}: {message}")
        elif status == "ERROR":
            logger.error(f"❌ {step}: {message}")
        else:
            logger.info(f"🔄 {step}: {message}")
    
    async def run_complete_automation(self):
        """Run the complete automation workflow step by step"""
        try:
            self._log_step("WORKFLOW_START", "Starting complete job hunting automation workflow")
            
            # Step 1: Environment Validation
            await self._step_1_validate_environment()
            
            # Step 2: Gmail Authentication & Scanning
            jobs = await self._step_2_scan_gmail_jobs()
            
            # Step 3: Job Data Processing & Enhancement
            processed_jobs = await self._step_3_process_job_data(jobs)
            
            # Step 4: Document Generation (CV & Cover Letters)
            job_documents = await self._step_4_generate_documents(processed_jobs)
            
            # Step 5: Email Delivery & Application Submission
            await self._step_5_send_applications(job_documents)
            
            # Step 6: Results Summary & Cleanup
            await self._step_6_generate_summary()
            
            self._log_step("WORKFLOW_COMPLETE", f"Automation completed successfully in {self._get_execution_time()}")
            
        except Exception as e:
            self._log_step("WORKFLOW_ERROR", f"Critical error in automation workflow: {str(e)}", "ERROR")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise
    
    async def _step_1_validate_environment(self):
        """Step 1: Validate environment and dependencies"""
        self._log_step("STEP_1", "Validating environment and dependencies", "RUNNING")
        
        try:
            # Check required environment variables
            required_vars = [
                'SENDER_EMAIL',
                'SENDER_GMAIL_PASSWORD',
                'ANTHROPIC_AUTH_TOKEN'
            ]
            
            missing_vars = []
            for var in required_vars:
                if not os.getenv(var):
                    missing_vars.append(var)
            
            if missing_vars:
                raise Exception(f"Missing required environment variables: {', '.join(missing_vars)}")
            
            # Check required Python packages
            required_packages = ['reportlab', 'supabase', 'anthropic']
            missing_packages = []
            
            for package in required_packages:
                try:
                    __import__(package)
                except ImportError:
                    missing_packages.append(package)
            
            if missing_packages:
                self._log_step("STEP_1", f"Installing missing packages: {', '.join(missing_packages)}", "RUNNING")
                import subprocess
                for package in missing_packages:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
            # Validate file structure
            required_files = [
                'app/services/real_job_scanner.py',
                'templates/cv_template.py',
                'templates/cover_letter_template.py'
            ]
            
            for file_path in required_files:
                if not Path(file_path).exists():
                    raise Exception(f"Required file not found: {file_path}")
            
            self._log_step("STEP_1", "Environment validation completed successfully")
            
        except Exception as e:
            self._log_step("STEP_1", f"Environment validation failed: {str(e)}", "ERROR")
            raise
    
    async def _step_2_scan_gmail_jobs(self) -> List[Dict[str, Any]]:
        """Step 2: Scan Gmail for job opportunities"""
        self._log_step("STEP_2", "Scanning Gmail for job opportunities", "RUNNING")
        
        try:
            # Import and initialize Gmail scanner
            from app.services.real_job_scanner import RealJobScanner
            email_scanner = RealJobScanner()
            
            # Scan for jobs from last 3 days
            jobs = await email_scanner.scan_real_gmail_jobs(days_back=3)
            
            self._log_step("STEP_2", f"Found {len(jobs)} job opportunities from Gmail scan")
            
            # Log job details for tracking
            for i, job in enumerate(jobs, 1):
                job_info = f"Job {i}: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown Company')}"
                self._log_step("STEP_2", f"Discovered: {job_info}")
            
            return jobs
            
        except Exception as e:
            self._log_step("STEP_2", f"Gmail scanning failed: {str(e)}", "ERROR")
            raise
    
    async def _step_3_process_job_data(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Step 3: Process and enhance job data"""
        self._log_step("STEP_3", f"Processing and enhancing {len(jobs)} job entries", "RUNNING")
        
        try:
            processed_jobs = []
            
            for i, job in enumerate(jobs, 1):
                self._log_step("STEP_3", f"Processing job {i}/{len(jobs)}: {job.get('title', 'Unknown')}", "RUNNING")
                
                # Import job processor
                from improved_working_automation import ImprovedWorkingAutomation
                automation = ImprovedWorkingAutomation()
                
                # Enhance job data
                enhanced_job = automation._improve_job_data(job)
                
                # Add processing metadata
                enhanced_job['processed_at'] = datetime.now().isoformat()
                enhanced_job['processing_id'] = f"job_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                processed_jobs.append(enhanced_job)
                
                self._log_step("STEP_3", f"Enhanced job: {enhanced_job['title']} at {enhanced_job['company']}")
            
            self._log_step("STEP_3", f"Successfully processed {len(processed_jobs)} jobs")
            self.processed_jobs = processed_jobs
            
            return processed_jobs
            
        except Exception as e:
            self._log_step("STEP_3", f"Job data processing failed: {str(e)}", "ERROR")
            raise
    
    async def _step_4_generate_documents(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Step 4: Generate CV and Cover Letter documents for each job"""
        self._log_step("STEP_4", f"Generating documents for {len(jobs)} job applications", "RUNNING")
        
        try:
            job_documents = []
            
            for i, job in enumerate(jobs, 1):
                self._log_step("STEP_4", f"Generating documents for job {i}/{len(jobs)}: {job['company']}", "RUNNING")
                
                try:
                    # Import document generator
                    from improved_working_automation import ImprovedWorkingAutomation
                    automation = ImprovedWorkingAutomation()
                    
                    # Generate CV PDF
                    cv_pdf = automation._generate_cv_pdf(job)
                    if not cv_pdf:
                        raise Exception("CV PDF generation failed")
                    
                    # Generate Cover Letter PDF
                    cl_pdf = automation._generate_cover_letter_pdf(job)
                    if not cl_pdf:
                        raise Exception("Cover Letter PDF generation failed")
                    
                    # Create job document package
                    job_document = {
                        'job': job,
                        'cv_pdf': cv_pdf,
                        'cover_letter_pdf': cl_pdf,
                        'generated_at': datetime.now().isoformat(),
                        'cv_size': len(cv_pdf),
                        'cl_size': len(cl_pdf)
                    }
                    
                    job_documents.append(job_document)
                    
                    self._log_step("STEP_4", f"Documents generated for {job['company']} (CV: {len(cv_pdf)} bytes, CL: {len(cl_pdf)} bytes)")
                    
                except Exception as e:
                    self._log_step("STEP_4", f"Document generation failed for {job.get('company', 'Unknown')}: {str(e)}", "ERROR")
                    self.failed_applications += 1
                    continue
            
            self._log_step("STEP_4", f"Successfully generated documents for {len(job_documents)} applications")
            
            return job_documents
            
        except Exception as e:
            self._log_step("STEP_4", f"Document generation step failed: {str(e)}", "ERROR")
            raise
    
    async def _step_5_send_applications(self, job_documents: List[Dict[str, Any]]):
        """Step 5: Send application emails with generated documents"""
        self._log_step("STEP_5", f"Sending {len(job_documents)} job applications", "RUNNING")
        
        try:
            for i, job_doc in enumerate(job_documents, 1):
                job = job_doc['job']
                self._log_step("STEP_5", f"Sending application {i}/{len(job_documents)}: {job['company']}", "RUNNING")
                
                try:
                    # Import email sender
                    from improved_working_automation import ImprovedWorkingAutomation
                    automation = ImprovedWorkingAutomation()
                    
                    # Send application email
                    email_sent = await automation._send_improved_job_email(
                        job,
                        job_doc['cv_pdf'],
                        job_doc['cover_letter_pdf']
                    )
                    
                    if email_sent:
                        self.successful_applications += 1
                        self._log_step("STEP_5", f"Application sent successfully to {job['company']}")
                    else:
                        self.failed_applications += 1
                        self._log_step("STEP_5", f"Application failed for {job['company']}", "ERROR")
                    
                    # Rate limiting between emails
                    await asyncio.sleep(3)
                    
                except Exception as e:
                    self.failed_applications += 1
                    self._log_step("STEP_5", f"Email sending failed for {job.get('company', 'Unknown')}: {str(e)}", "ERROR")
                    continue
            
            self._log_step("STEP_5", f"Email sending completed: {self.successful_applications} successful, {self.failed_applications} failed")
            
        except Exception as e:
            self._log_step("STEP_5", f"Email sending step failed: {str(e)}", "ERROR")
            raise
    
    async def _step_6_generate_summary(self):
        """Step 6: Generate execution summary and cleanup"""
        self._log_step("STEP_6", "Generating execution summary and cleanup", "RUNNING")
        
        try:
            # Create execution summary
            summary = {
                "execution_id": f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "execution_time": self._get_execution_time(),
                "total_jobs_found": len(self.processed_jobs),
                "successful_applications": self.successful_applications,
                "failed_applications": self.failed_applications,
                "success_rate": f"{(self.successful_applications / max(len(self.processed_jobs), 1) * 100):.1f}%",
                "execution_log": self.execution_log,
                "processed_jobs": [
                    {
                        "title": job.get('title', 'Unknown'),
                        "company": job.get('company', 'Unknown'),
                        "processing_id": job.get('processing_id', 'Unknown')
                    }
                    for job in self.processed_jobs
                ]
            }
            
            # Save summary to file
            summary_file = f"automation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            self._log_step("STEP_6", f"Execution summary saved to {summary_file}")
            
            # Print final summary
            print("\n" + "="*60)
            print("🎉 AUTOMATION EXECUTION SUMMARY")
            print("="*60)
            print(f"⏱️  Execution Time: {self._get_execution_time()}")
            print(f"🔍 Jobs Found: {len(self.processed_jobs)}")
            print(f"✅ Successful Applications: {self.successful_applications}")
            print(f"❌ Failed Applications: {self.failed_applications}")
            print(f"📊 Success Rate: {summary['success_rate']}")
            print(f"📄 Summary File: {summary_file}")
            print("="*60)
            
            if self.successful_applications > 0:
                print(f"📧 Check hongzhili01@gmail.com for {self.successful_applications} professional job applications!")
            
            self._log_step("STEP_6", "Summary generation and cleanup completed")
            
        except Exception as e:
            self._log_step("STEP_6", f"Summary generation failed: {str(e)}", "ERROR")
            raise
    
    def _get_execution_time(self) -> str:
        """Get formatted execution time"""
        duration = datetime.now() - self.start_time
        minutes, seconds = divmod(duration.total_seconds(), 60)
        return f"{int(minutes)}m {int(seconds)}s"

async def main():
    """Main entry point for the complete automation"""
    print("🚀 MASTER JOB HUNTING AUTOMATION ORCHESTRATOR")
    print("="*60)
    print("🎯 Complete workflow execution:")
    print("   1. Environment Validation")
    print("   2. Gmail Job Scanning")
    print("   3. Job Data Processing")
    print("   4. Document Generation")
    print("   5. Application Delivery")
    print("   6. Results Summary")
    print("="*60)
    print()
    
    try:
        # Initialize and run master orchestrator
        orchestrator = MasterAutomationOrchestrator()
        await orchestrator.run_complete_automation()
        
        print("\n🎉 Automation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Automation failed: {str(e)}")
        logger.error(f"Master automation failed: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())