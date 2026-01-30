#!/usr/bin/env python3
"""
Enhanced Job Processor with R2 Backup Integration
Processes jobs and automatically backs up generated documents to R2 storage
"""
import asyncio
import os
from pathlib import Path
from typing import Dict, List, Optional
from ultra_simple_generator import UltraSimpleGenerator
from r2_backup_service import R2BackupService

class JobProcessorWithBackup(UltraSimpleGenerator):
    def __init__(self):
        super().__init__()
        self.r2_backup = R2BackupService()
        self.processed_jobs = []
    
    async def process_job_with_backup(self, job_title: str, company: str, 
                                    department: str = "", address: str = "", 
                                    city: str = "Sweden", priority: str = "medium") -> Dict:
        """Process a job application and backup documents to R2"""
        
        print(f"🎯 Processing job with R2 backup: {job_title} at {company}")
        print(f"📍 Priority: {priority}")
        print("=" * 60)
        
        result = {
            "job_title": job_title,
            "company": company,
            "success": False,
            "pdf_generated": False,
            "backup_uploaded": False,
            "files": {}
        }
        
        try:
            # Determine role focus
            role_focus = self.determine_role_focus(job_title)
            print(f"🎯 Role Focus: {role_focus}")
            
            # Generate document content
            print("📝 Generating tailored documents...")
            cv_content = self.create_basic_cv_template(job_title, company, role_focus)
            cl_content = self.create_basic_cover_letter_template(job_title, company, department, address, city)
            
            # Create safe filenames
            safe_company = company.replace(" ", "_").replace("/", "_")
            safe_job = job_title.replace(" ", "_").replace("/", "_")
            
            cv_name = f"{safe_job}_{safe_company}_cv"
            cl_name = f"{safe_job}_{safe_company}_cl"
            
            # Save LaTeX files
            cv_tex = f"{cv_name}.tex"
            cl_tex = f"{cl_name}.tex"
            
            with open(cv_tex, 'w', encoding='utf-8') as f:
                f.write(cv_content)
            with open(cl_tex, 'w', encoding='utf-8') as f:
                f.write(cl_content)
            
            print(f"💾 LaTeX sources saved: {cv_tex}, {cl_tex}")
            
            # Compile PDFs
            print("🔨 Compiling PDFs...")
            cv_pdf = self.compile_ultra_basic_latex(cv_content, cv_name)
            cl_pdf = self.compile_ultra_basic_latex(cl_content, cl_name)
            
            if cv_pdf and cl_pdf:
                result["pdf_generated"] = True
                result["files"] = {
                    "cv_pdf": cv_pdf,
                    "cv_tex": cv_tex,
                    "cl_pdf": cl_pdf,
                    "cl_tex": cl_tex
                }
                print("✅ PDFs generated successfully")
                
                # Backup to R2 storage
                print("📦 Backing up to R2 storage...")
                backup_results = self.r2_backup.backup_job_documents(
                    job_title, company, cv_pdf, cv_tex, cl_pdf, cl_tex
                )
                
                # Check backup success
                backup_success = sum(1 for success in backup_results.values() if success)
                if backup_success > 0:
                    result["backup_uploaded"] = True
                    print(f"✅ Backup successful: {backup_success} files uploaded to R2")
                else:
                    print("⚠️  Backup failed or R2 credentials not configured")
                
                # Send email (if SMTP is configured)
                print("📧 Sending email...")
                try:
                    email_success = await self.send_working_email(
                        job_title, company, cv_tex, cl_tex, cv_pdf, cl_pdf, role_focus
                    )
                    if email_success:
                        print("✅ Email sent successfully")
                    else:
                        print("⚠️  Email sending failed")
                except Exception as e:
                    print(f"⚠️  Email error: {e}")
                
                result["success"] = True
                
                # Clean up local PDF files (keep LaTeX for editing)
                try:
                    if cv_pdf and Path(cv_pdf).exists():
                        os.remove(cv_pdf)
                    if cl_pdf and Path(cl_pdf).exists():
                        os.remove(cl_pdf)
                    print("🧹 Local PDFs cleaned up (kept LaTeX sources)")
                except:
                    pass
                
            else:
                print("❌ PDF compilation failed")
                
        except Exception as e:
            print(f"❌ Job processing error: {e}")
        
        print(f"📊 Job processing complete: {'✅ Success' if result['success'] else '❌ Failed'}")
        print()
        
        self.processed_jobs.append(result)
        return result
    
    async def process_multiple_jobs(self, jobs: List[Dict]) -> Dict:
        """Process multiple jobs with backup"""
        
        print("🚀 PROCESSING MULTIPLE JOBS WITH R2 BACKUP")
        print("=" * 70)
        print(f"📋 Total jobs to process: {len(jobs)}")
        print()
        
        summary = {
            "total": len(jobs),
            "successful": 0,
            "failed": 0,
            "pdf_generated": 0,
            "backup_uploaded": 0,
            "jobs": []
        }
        
        for i, job in enumerate(jobs, 1):
            print(f"📋 Processing job {i}/{len(jobs)}")
            print("-" * 50)
            
            result = await self.process_job_with_backup(
                job.get("job_title", ""),
                job.get("company", ""),
                job.get("department", ""),
                job.get("address", ""),
                job.get("city", "Sweden"),
                job.get("priority", "medium")
            )
            
            summary["jobs"].append(result)
            
            if result["success"]:
                summary["successful"] += 1
            else:
                summary["failed"] += 1
            
            if result["pdf_generated"]:
                summary["pdf_generated"] += 1
            
            if result["backup_uploaded"]:
                summary["backup_uploaded"] += 1
            
            # Small delay between jobs
            await asyncio.sleep(2)
        
        return summary
    
    def print_processing_summary(self, summary: Dict):
        """Print detailed processing summary"""
        
        print("📊 JOB PROCESSING SUMMARY")
        print("=" * 60)
        print(f"📋 Total Jobs: {summary['total']}")
        print(f"✅ Successful: {summary['successful']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"📄 PDFs Generated: {summary['pdf_generated']}")
        print(f"📦 R2 Backups: {summary['backup_uploaded']}")
        print()
        
        print("📋 Job Details:")
        for i, job in enumerate(summary["jobs"], 1):
            status = "✅" if job["success"] else "❌"
            backup = "📦" if job["backup_uploaded"] else "⚪"
            pdf = "📄" if job["pdf_generated"] else "⚪"
            
            print(f"  {i}. {status} {pdf} {backup} {job['job_title']} at {job['company']}")
        
        print()
        print("🔗 Legend:")
        print("  ✅ = Successfully processed")
        print("  📄 = PDF generated")
        print("  📦 = Backed up to R2")
        print()
        
        if summary["backup_uploaded"] > 0:
            print(f"🔗 R2 Storage: https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com")
            print("📋 View backup index: https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com/index.html")
        else:
            print("⚠️  Configure R2 credentials in .env to enable backup")
        
        print()
        print("📧 Check leeharvad@gmail.com for application emails!")

async def test_job_processing_with_backup():
    """Test job processing with R2 backup"""
    
    processor = JobProcessorWithBackup()
    
    # Test jobs (including Thomthon Retuer)
    test_jobs = [
        {
            "job_title": "Solution Developer",
            "company": "Thomthon Retuer",
            "department": "Engineering",
            "city": "Sweden",
            "priority": "high"
        },
        {
            "job_title": "DevOps Engineer",
            "company": "Spotify",
            "department": "Platform Team",
            "city": "Stockholm",
            "priority": "high"
        },
        {
            "job_title": "Backend Developer",
            "company": "King Digital Entertainment",
            "department": "Infrastructure",
            "city": "Stockholm",
            "priority": "medium"
        }
    ]
    
    # Process all jobs
    summary = await processor.process_multiple_jobs(test_jobs)
    
    # Print summary
    processor.print_processing_summary(summary)
    
    # Create backup index
    if summary["backup_uploaded"] > 0:
        print("📋 Creating backup index...")
        processor.r2_backup.create_backup_index()

async def process_thomthon_only():
    """Process only Thomthon Retuer job"""
    
    processor = JobProcessorWithBackup()
    
    print("🎯 Processing Thomthon Retuer Application with R2 Backup")
    print("=" * 60)
    
    result = await processor.process_job_with_backup(
        "Solution Developer",
        "Thomthon Retuer", 
        "Engineering Department",
        "",
        "Sweden",
        "high"
    )
    
    if result["success"]:
        print("🎉 Thomthon Retuer application processed successfully!")
        if result["backup_uploaded"]:
            print("📦 Documents backed up to R2 storage")
            print("🔗 R2 URL: https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com")
        print("📧 Check leeharvad@gmail.com for the application email")
    else:
        print("❌ Processing failed")

async def main():
    """Main function with options"""
    
    print("🎯 JobHunter with R2 Backup Integration")
    print("=" * 50)
    print("1. Process Thomthon Retuer only")
    print("2. Process multiple test jobs")
    print("3. Test R2 backup service")
    print()
    
    choice = input("Enter choice (1-3): ").strip() or "1"
    
    if choice == "1":
        await process_thomthon_only()
    elif choice == "2":
        await test_job_processing_with_backup()
    elif choice == "3":
        from r2_backup_service import test_r2_backup
        test_r2_backup()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())