#!/usr/bin/env python3
"""
Simplified Claude-powered resume test
Tests Claude API integration without Supabase dependency
"""
import asyncio
import subprocess
import tempfile
import shutil
import os
import smtplib
import json
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class ClaudeSimpleTest:
    def __init__(self):
        # Email settings
        self.sender_email = "bluehawanan@gmail.com"
        self.recipient_email = "leeharvad@gmail.com"
        self.password = os.getenv('SMTP_PASSWORD')
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        # Claude API settings - USER MUST PROVIDE THEIR OWN
        self.claude_base_url = os.getenv('ANTHROPIC_BASE_URL')
        self.claude_token = os.getenv('ANTHROPIC_AUTH_TOKEN')
        
        if not self.claude_base_url or not self.claude_token:
            raise ValueError("❌ REQUIRED: Set ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN environment variables")
        
        # Local resume data (instead of Supabase for testing)
        self.resume_data = {
            "basic_info": {
                "name": "Hongzhi Li",
                "email": "hongzhili01@gmail.com",
                "phone": "0728384299",
                "linkedin": "https://www.linkedin.com/in/hzl/",
                "github": "https://github.com/bluehawana",
                "website": "https://www.bluehawana.com",
                "address": "Ebbe Lieberathsgatan 27, 412 65 Göteborg"
            },
            "profile_summary": "Experienced Software Developer with over 5 years of hands-on experience in full-stack development, DevOps, and infrastructure management. Currently serving as IT/Infrastructure Specialist at ECARX, leading infrastructure optimization and system integration projects.",
            "technical_skills": {
                "programming_languages": "Java/J2EE, JavaScript, C#/.NET Core, Python, Bash, PowerShell",
                "cloud_platforms": "AWS, Azure, GCP",
                "containerization": "Docker, Kubernetes, Azure Kubernetes Service (AKS)",
                "cicd": "Jenkins, GitHub Actions, GitLab CI"
            }
        }
    
    async def call_claude_api(self, prompt: str, job_description: str = "") -> str:
        """Call Claude API for resume customization"""
        
        try:
            # Create environment for Claude API call
            env = os.environ.copy()
            env["ANTHROPIC_BASE_URL"] = self.claude_base_url
            env["ANTHROPIC_AUTH_TOKEN"] = self.claude_token
            
            # Prepare full prompt
            full_prompt = f"""
{prompt}

Job Description:
{job_description}

Please provide a detailed response optimized for this specific role.
"""
            
            print(f"🤖 Calling Claude API...")
            print(f"Environment: ANTHROPIC_BASE_URL={self.claude_base_url}")
            print(f"Token: {self.claude_token[:20]}...")
            
            # Call Claude via command line  
            cmd = ["claude", "--model", "claude-3-7-sonnet-20250219", "--print"]
            
            result = subprocess.run(
                cmd,
                input=full_prompt,
                text=True,
                capture_output=True,
                env=env,
                timeout=120
            )
            
            print(f"Claude API return code: {result.returncode}")
            if result.stdout:
                print(f"Claude response length: {len(result.stdout)}")
                print(f"Claude response preview: {result.stdout[:200]}...")
            if result.stderr:
                print(f"Claude stderr: {result.stderr}")
            
            if result.returncode == 0:
                print("✅ Claude API call successful")
                return result.stdout.strip()
            else:
                print(f"❌ Claude API error: {result.stderr}")
                return ""
                
        except Exception as e:
            print(f"❌ Error calling Claude API: {e}")
            return ""
    
    async def test_claude_customization(self, job_title: str, company: str, job_description: str):
        """Test Claude customization"""
        
        print(f"🎯 Testing Claude customization for {job_title} at {company}")
        
        # Simple customization prompt
        customization_prompt = f"""
Please customize this resume profile summary for a {job_title} position at {company}:

Current Profile: {self.resume_data['profile_summary']}
Technical Skills: {json.dumps(self.resume_data['technical_skills'], indent=2)}

Requirements:
1. Rewrite the profile summary to emphasize {job_title} skills
2. Match keywords from the job description
3. Keep it professional and factual
4. Return as JSON with: {{"profile_summary": "...", "key_skills": ["skill1", "skill2"]}}

Return only valid JSON.
"""
        
        # Call Claude
        claude_response = await self.call_claude_api(customization_prompt, job_description)
        
        if claude_response:
            try:
                # Extract JSON from markdown if present
                if "```json" in claude_response:
                    start = claude_response.find("```json") + 7
                    end = claude_response.find("```", start)
                    json_text = claude_response[start:end].strip()
                else:
                    json_text = claude_response
                
                customization = json.loads(json_text)
                print("✅ Claude customization successful!")
                print(f"New profile: {customization.get('profile_summary', '')[:100]}...")
                print(f"Key skills: {customization.get('key_skills', [])}")
                return customization
            except json.JSONDecodeError:
                print("❌ Failed to parse Claude response as JSON")
                print(f"Response: {claude_response[:300]}...")
                return None
        else:
            print("❌ No response from Claude")
            return None
    
    async def test_cover_letter(self, job_title: str, company: str, job_description: str):
        """Test cover letter generation"""
        
        print(f"✍️ Testing cover letter generation for {job_title} at {company}")
        
        cover_letter_prompt = f"""
Write a professional cover letter for a {job_title} position at {company}.

Candidate Info:
- Name: Hongzhi Li
- Current Role: IT/Infrastructure Specialist at ECARX
- Experience: 5+ years in software development and DevOps
- Skills: {self.resume_data['technical_skills']['programming_languages']}

Requirements:
1. 3-4 paragraphs
2. Professional tone
3. Highlight relevant experience
4. Show enthusiasm for {company}
5. Include specific examples

Return only the cover letter text.
"""
        
        cover_letter = await self.call_claude_api(cover_letter_prompt, job_description)
        
        if cover_letter:
            print("✅ Cover letter generated!")
            print(f"Preview: {cover_letter[:200]}...")
            return cover_letter
        else:
            print("❌ Cover letter generation failed")
            return ""
    
    async def send_test_email(self, job_title: str, company: str, customization: dict, cover_letter: str):
        """Send test email with Claude results"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"🤖 Claude Test: {job_title} at {company} - AI Customization"
            
            body = f"""Hi!

🤖 CLAUDE-POWERED CUSTOMIZATION TEST

🏢 Company: {company}
💼 Position: {job_title}
🎯 Test Status: Claude API Integration

📝 CLAUDE CUSTOMIZED PROFILE:
{customization.get('profile_summary', 'Not generated')}

🔑 KEY SKILLS IDENTIFIED:
{', '.join(customization.get('key_skills', []))}

✍️ CLAUDE GENERATED COVER LETTER:
{cover_letter[:500]}{'...' if len(cover_letter) > 500 else ''}

🎯 This demonstrates Claude's ability to:
- Analyze job descriptions
- Customize resume content
- Generate role-specific cover letters
- Optimize for ATS keywords

Next steps: Integrate with Supabase database and PDF generation.

Best regards,
Claude Test System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            server.quit()
            
            print("✅ Test email sent!")
            return True
            
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False

async def main():
    """Test Claude integration"""
    
    tester = ClaudeSimpleTest()
    
    # Test job
    job_title = "DevOps Engineer"
    company = "Opera"
    job_description = """
    We are looking for a DevOps Engineer to join our team in Stockholm. 
    
    Requirements:
    - 3+ years experience with Kubernetes and Docker
    - Strong knowledge of CI/CD pipelines
    - Experience with AWS or Azure cloud platforms
    - Python scripting and automation experience
    - Infrastructure as Code (Terraform/Ansible)
    - Monitoring and logging systems (Grafana, Prometheus)
    
    Responsibilities:
    - Design and maintain CI/CD pipelines
    - Manage Kubernetes clusters
    - Implement infrastructure automation
    - Collaborate with development teams
    - Ensure system reliability and scalability
    """
    
    print(f"🎯 Testing Claude API integration")
    print(f"📋 Job: {job_title} at {company}")
    print()
    
    # Test customization
    customization = await tester.test_claude_customization(job_title, company, job_description)
    
    # Test cover letter
    cover_letter = await tester.test_cover_letter(job_title, company, job_description)
    
    # Send results
    if customization or cover_letter:
        await tester.send_test_email(job_title, company, customization or {}, cover_letter)
        print("🎉 Claude integration test completed!")
    else:
        print("❌ Claude integration test failed")

if __name__ == "__main__":
    asyncio.run(main())