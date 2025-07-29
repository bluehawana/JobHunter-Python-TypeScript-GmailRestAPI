#!/usr/bin/env python3
"""
Setup Daily Job Automation
Configures cron job and environment for daily automation
"""
import os
import sys
from pathlib import Path
import subprocess
from datetime import datetime

class DailyAutomationSetup:
    """Setup and configure daily job automation"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.python_path = sys.executable
        self.script_path = self.project_dir / "daily_job_automation.py"
        
    def setup_environment_variables(self):
        """Setup required environment variables"""
        
        print("🔧 ENVIRONMENT SETUP")
        print("=" * 30)
        
        # Check existing environment variables
        required_vars = {
            'SUPABASE_URL': 'https://lgvfwkwzbdattzabvdas.supabase.co',
            'SUPABASE_ANON_KEY': 'REMOVED_SECRET',
            'ANTHROPIC_API_KEY': 'Your Claude API key here',
            'GMAIL_CREDENTIALS': 'Path to Gmail credentials JSON',
            'R2_ENDPOINT': 'Your R2 storage endpoint',
            'R2_ACCESS_KEY': 'Your R2 access key',
            'R2_SECRET_KEY': 'Your R2 secret key',
            'SMTP_PASSWORD': 'Your Gmail app password'
        }
        
        env_file = self.project_dir / ".env"
        
        print(f"📝 Creating environment file: {env_file}")
        
        with open(env_file, 'w') as f:
            f.write("# Daily Job Automation Environment Variables\n")
            f.write(f"# Generated on {datetime.now().isoformat()}\n\n")
            
            for var, default_value in required_vars.items():
                current_value = os.getenv(var, default_value)
                f.write(f"{var}={current_value}\n")
                
                if "Your" in default_value:
                    print(f"⚠️  {var}: Please update with your actual credentials")
                else:
                    print(f"✅ {var}: Configured")
        
        print(f"\n📋 Environment file created: {env_file}")
        print("⚠️  Please update the file with your actual API keys and credentials")
        
        return env_file
    
    def create_cron_job(self, run_time: str = "09:00"):
        """Create cron job for daily automation"""
        
        print(f"\n⏰ CRON JOB SETUP")
        print("=" * 20)
        
        # Parse run time
        hour, minute = run_time.split(":")
        
        # Create cron command
        cron_command = f"{self.python_path} {self.script_path}"
        cron_entry = f"{minute} {hour} * * * cd {self.project_dir} && {cron_command} >> /tmp/jobhunter_automation.log 2>&1"
        
        print(f"🕒 Scheduled for: {run_time} daily")
        print(f"📁 Working directory: {self.project_dir}")
        print(f"🐍 Python: {self.python_path}")
        print(f"📄 Script: {self.script_path}")
        
        print(f"\n📋 Cron entry:")
        print(f"   {cron_entry}")
        
        # Create cron setup script
        cron_setup_script = self.project_dir / "install_cron.sh"
        
        with open(cron_setup_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Install cron job for daily job automation\n\n")
            f.write("# Add to current user's crontab\n")
            f.write(f'(crontab -l 2>/dev/null; echo "{cron_entry}") | crontab -\n')
            f.write('echo "✅ Cron job installed successfully!"\n')
            f.write('echo "📋 Current crontab:"\n')
            f.write('crontab -l\n')
        
        # Make script executable
        os.chmod(cron_setup_script, 0o755)
        
        print(f"\n🛠️ Cron installation script created: {cron_setup_script}")
        print("Run the following to install cron job:")
        print(f"   bash {cron_setup_script}")
        
        return cron_setup_script
    
    def create_manual_run_script(self):
        """Create script for manual testing"""
        
        manual_script = self.project_dir / "run_automation_now.py"
        
        script_content = f'''#!/usr/bin/env python3
"""
Manual run script for daily job automation
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project directory to path
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(project_dir / ".env")

from daily_job_automation import DailyJobAutomation

async def main():
    """Run automation manually"""
    
    print("🚀 MANUAL AUTOMATION RUN")
    print("=" * 30)
    
    automation = DailyJobAutomation()
    result = await automation.run_daily_automation()
    
    if result['success']:
        print("\\n🎉 SUCCESS!")
        print(f"📊 Jobs found: {{result.get('jobs_found', 0)}}")
        print(f"📧 Applications generated: {{result.get('applications_generated', 0)}}")
        print(f"⏱️ Processing time: {{result.get('processing_time_seconds', 0):.1f}} seconds")
    else:
        print(f"\\n❌ FAILED: {{result.get('error', 'Unknown error')}}")

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        with open(manual_script, 'w') as f:
            f.write(script_content)
        
        os.chmod(manual_script, 0o755)
        
        print(f"\n🧪 Manual run script created: {manual_script}")
        print("Test automation with:")
        print(f"   python3 {manual_script}")
        
        return manual_script
    
    def create_systemd_service(self):
        """Create systemd service for better scheduling"""
        
        service_content = f"""[Unit]
Description=Daily Job Automation for JobHunter
After=network.target

[Service]
Type=oneshot
User={os.getenv('USER', 'user')}
WorkingDirectory={self.project_dir}
Environment=PATH={os.environ.get('PATH')}
ExecStart={self.python_path} {self.script_path}
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
        
        timer_content = """[Unit]
Description=Run Daily Job Automation every day at 9 AM
Requires=jobhunter-automation.service

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
"""
        
        service_file = self.project_dir / "jobhunter-automation.service"
        timer_file = self.project_dir / "jobhunter-automation.timer"
        
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        with open(timer_file, 'w') as f:
            f.write(timer_content)
        
        print(f"\n🔧 Systemd service files created:")
        print(f"   Service: {service_file}")
        print(f"   Timer: {timer_file}")
        
        install_script = self.project_dir / "install_systemd.sh"
        
        with open(install_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Install systemd service and timer\n\n")
            f.write(f"sudo cp {service_file} /etc/systemd/system/\n")
            f.write(f"sudo cp {timer_file} /etc/systemd/system/\n")
            f.write("sudo systemctl daemon-reload\n")
            f.write("sudo systemctl enable jobhunter-automation.timer\n")
            f.write("sudo systemctl start jobhunter-automation.timer\n")
            f.write('echo "✅ Systemd timer installed and started!"\n')
            f.write('echo "📋 Timer status:"\n')
            f.write('sudo systemctl status jobhunter-automation.timer\n')
        
        os.chmod(install_script, 0o755)
        
        print(f"   Install script: {install_script}")
        print("Install with:")
        print(f"   bash {install_script}")
        
        return service_file, timer_file, install_script
    
    def create_requirements_file(self):
        """Create requirements file for dependencies"""
        
        requirements = [
            "supabase>=2.0.0",
            "python-multipart>=0.0.6",
            "aiohttp>=3.8.0",
            "beautifulsoup4>=4.12.0",
            "httpx>=0.25.0",
            "python-dotenv>=1.0.0",
            "nltk>=3.8.0",
            "requests>=2.31.0",
            "asyncio>=3.4.3",
            "pathlib>=1.0.1"
        ]
        
        requirements_file = self.project_dir / "requirements_automation.txt"
        
        with open(requirements_file, 'w') as f:
            f.write("# Requirements for Daily Job Automation\\n")
            f.write(f"# Generated on {datetime.now().isoformat()}\\n\\n")
            for req in requirements:
                f.write(f"{req}\\n")
        
        print(f"\\n📦 Requirements file created: {requirements_file}")
        print("Install dependencies with:")
        print(f"   pip install -r {requirements_file}")
        
        return requirements_file
    
    def setup_complete_automation(self):
        """Complete setup process"""
        
        print("🚀 DAILY JOB AUTOMATION SETUP")
        print("=" * 40)
        print("Setting up complete automation system...")
        
        # 1. Environment variables
        env_file = self.setup_environment_variables()
        
        # 2. Requirements
        req_file = self.create_requirements_file()
        
        # 3. Manual run script
        manual_script = self.create_manual_run_script()
        
        # 4. Cron job
        cron_script = self.create_cron_job("09:00")  # 9 AM daily
        
        # 5. Systemd service (alternative to cron)
        service_files = self.create_systemd_service()
        
        print("\\n" + "=" * 40)
        print("🎉 SETUP COMPLETE!")
        print("=" * 40)
        
        print("\\n📋 NEXT STEPS:")
        print("1. Update environment variables:")
        print(f"   nano {env_file}")
        
        print("\\n2. Install Python dependencies:")
        print(f"   pip install -r {req_file}")
        
        print("\\n3. Test automation manually:")
        print(f"   python3 {manual_script}")
        
        print("\\n4. Choose scheduling method:")
        print(f"   Option A (Cron): bash {cron_script}")
        print(f"   Option B (Systemd): bash {service_files[2]}")
        
        print("\\n⏰ AUTOMATION SCHEDULE:")
        print("   • Every day at 9:00 AM")
        print("   • Scans email for LinkedIn/Indeed jobs")
        print("   • Fetches Arbetsförmedlingen jobs")
        print("   • Generates customized CV/CL with Sonnet 3.7")
        print("   • Uploads to R2 storage")
        print("   • Sends applications to hongzhili01@gmail.com")
        
        print("\\n🎯 CUSTOMIZATION FEATURES:")
        print("   • Role-specific project emphasis")
        print("   • ATS optimization for high pass rates")
        print("   • Hard skills focus in CV")
        print("   • Soft skills emphasis in cover letters")
        print("   • GitHub projects integration")
        
        print("\\n📧 EMAIL OUTPUT:")
        print("   • Job title and description")
        print("   • Application link")
        print("   • Customized CV PDF")
        print("   • Tailored cover letter PDF")
        print("   • R2 storage links")
        
        print("\\n🚀 System ready for daily automation!")
        
        return {
            'env_file': env_file,
            'requirements_file': req_file,
            'manual_script': manual_script,
            'cron_script': cron_script,
            'systemd_files': service_files
        }

def main():
    """Main setup function"""
    
    setup = DailyAutomationSetup()
    result = setup.setup_complete_automation()
    
    print(f"\\n✅ All files created successfully!")
    print("🎉 Daily job automation is ready to deploy!")

if __name__ == "__main__":
    main()