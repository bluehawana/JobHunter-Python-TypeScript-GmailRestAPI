#!/usr/bin/env python3
"""
Intelligent Cover Letter Generator with LEGO Logic
Uses Claude API, R2 Storage, and Overleaf Integration
Complements resume with soft skills, integration expertise, and cross-cultural communication
"""
import os
import logging
import time
import hashlib
from typing import Dict, Any, Optional
from r2_latex_storage import R2LaTeXStorage

logger = logging.getLogger(__name__)

class CoverLetterGenerator:
    def __init__(self):
        """Initialize cover letter generator with Claude API integration"""
        self.r2_storage = R2LaTeXStorage()
        self.claude_api_key = os.getenv('ANTHROPIC_AUTH_TOKEN')
        self.claude_base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://anyrouter.top')
        
    def _analyze_job_with_claude(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use Claude API to analyze job and suggest cover letter focus"""
        try:
            import requests
            
            job_text = f"""
            Company: {job_data.get('company', '')}
            Position: {job_data.get('title', '')}
            Description: {job_data.get('description', '')}
            Location: {job_data.get('location', '')}
            """
            
            prompt = f"""
            Analyze this job posting and provide cover letter guidance for Hongzhi Li:
            
            {job_text}
            
            Based on the job requirements, identify:
            1. Key soft skills to emphasize (cross-cultural communication, IT-business bridge, collaboration)
            2. Integration expertise to highlight (system integration, team integration, process integration)
            3. Company-specific values to mention
            4. Tone (formal/casual) and cultural approach
            5. Specific achievements to emphasize from his background
            
            Return as JSON with keys: soft_skills, integration_focus, company_values, tone, achievements
            """
            
            headers = {
                'Authorization': f'Bearer {self.claude_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'claude-3-7-sonnet-20250219',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 1000
            }
            
            response = requests.post(
                f'{self.claude_base_url}/v1/messages',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                claude_analysis = result['content'][0]['text']
                logger.info("✅ Claude API analysis successful")
                return {'claude_analysis': claude_analysis, 'success': True}
            else:
                logger.warning(f"⚠️ Claude API failed: {response.status_code}")
                return {'success': False}
                
        except Exception as e:
            logger.warning(f"⚠️ Claude API error: {e}")
            return {'success': False}
    
    def _generate_cover_letter_content(self, job_data: Dict[str, Any], claude_analysis: Optional[Dict] = None) -> str:
        """Generate cover letter content with LEGO intelligence and ACCURATE company info"""
        
        # CRITICAL: Extract accurate company information first
        from company_info_extractor import CompanyInfoExtractor
        
        extractor = CompanyInfoExtractor()
        company_result = extractor.extract_and_validate_company_info(job_data)
        
        if not company_result['success']:
            logger.error("❌ CRITICAL: Company info extraction failed!")
            raise Exception("Company information extraction failed - cannot generate cover letter")
        
        company_info = company_result['company_info']
        
        # Log quality warning if needed
        if company_result['quality_score'] < 7:
            logger.warning(f"⚠️ Company info quality score: {company_result['quality_score']}/10")
            if 'warning' in company_result:
                logger.warning(f"⚠️ {company_result['warning']}")
        
        # Use validated company information
        company = company_info['company_name']
        position = job_data.get('title', 'Position')
        description = job_data.get('description', '').lower()
        
        # LEGO Intelligence - Determine focus areas
        is_devops = any(keyword in description for keyword in 
                       ['devops', 'infrastructure', 'kubernetes', 'docker', 'aws', 'cloud', 'ci/cd'])
        is_backend = any(keyword in description for keyword in 
                        ['backend', 'api', 'microservices', 'spring', 'java', 'database']) and not is_devops
        is_frontend = any(keyword in description for keyword in 
                         ['frontend', 'react', 'angular', 'vue', 'javascript', 'ui']) and not is_devops and not is_backend
        is_automotive = any(keyword in description for keyword in 
                           ['automotive', 'car', 'vehicle', 'volvo', 'polestar', 'geely', 'infotainment'])
        is_startup = any(keyword in description for keyword in 
                        ['startup', 'scale', 'growth', 'agile', 'fast-paced'])
        is_enterprise = any(keyword in description for keyword in 
                           ['enterprise', 'large-scale', 'corporate', 'established'])
        
        # Use validated greeting from company info extraction
        greeting = company_info['greeting']
        
        # Determine cultural approach based on location and company
        location = job_data.get('location', '').lower()
        if 'sweden' in location or 'göteborg' in location or 'stockholm' in location:
            cultural_approach = "Swedish directness with warmth"
        elif is_startup:
            cultural_approach = "Casual and energetic"
        else:
            cultural_approach = "Professional and respectful"
        
        # LEGO Soft Skills Selection
        if is_devops:
            soft_skills_focus = """
            Throughout my career, I have excelled in cross-functional collaboration, serving as a bridge between development teams and infrastructure operations. My experience at ECARX has strengthened my ability to communicate complex technical concepts to both technical and non-technical stakeholders, ensuring seamless project delivery across diverse teams.
            
            What sets me apart is my multicultural perspective and cross-cultural communication skills. Having worked across Swedish, Chinese, and international business environments, I bring a unique ability to navigate cultural nuances while maintaining technical excellence. This has been particularly valuable when coordinating between IT departments and business units, translating business requirements into technical solutions.
            """
            
            integration_expertise = """
            My expertise extends beyond technical implementation to system integration and process optimization. At ECARX, I led the migration from AKS to local Kubernetes clusters, which required not only technical skills but also extensive collaboration with multiple departments, change management, and stakeholder alignment. This project showcased my ability to integrate complex systems while managing organizational change.
            
            I have consistently demonstrated success in integrating disparate teams and technologies, fostering a culture of collaboration between traditionally siloed departments. My approach combines technical depth with emotional intelligence, enabling me to build consensus and drive adoption of new technologies across diverse teams.
            """
            
        elif is_backend:
            soft_skills_focus = """
            My strength lies in bridging the gap between technical implementation and business objectives. Throughout my experience developing comprehensive systems at Synteda and backend platforms at Pembio, I have consistently served as a translator between technical teams and business stakeholders, ensuring that complex API architectures align with business goals.
            
            Having worked in multicultural environments across Sweden and internationally, I bring exceptional cross-cultural communication skills. This has been invaluable when working with distributed teams, managing stakeholder expectations, and ensuring that technical solutions meet diverse user needs across different markets and cultures.
            """
            
            integration_expertise = """
            My expertise in system integration goes beyond code – it encompasses people, processes, and technologies. I have successfully integrated SQL and NoSQL databases, RESTful APIs, and microservices architectures while simultaneously integrating development teams, QA processes, and deployment workflows.
            
            At IT-Högskolan, I demonstrated this holistic integration approach by migrating the "Omstallningsstod.se" platform while coordinating between UI/UX designers, backend developers, and educational stakeholders. This required not only technical integration skills but also project management, communication, and change management capabilities.
            """
            
        else:  # Fullstack or general
            soft_skills_focus = """
            My unique value proposition lies in my ability to work across the entire technology stack while maintaining strong interpersonal connections across all levels of an organization. I excel at facilitating communication between frontend designers, backend developers, DevOps engineers, and business stakeholders, ensuring cohesive project delivery.
            
            My international background and multicultural experience have equipped me with exceptional cross-cultural communication skills. I have successfully navigated complex projects involving Swedish business culture, international development teams, and diverse user bases, always maintaining clear communication and cultural sensitivity.
            """
            
            integration_expertise = """
            Beyond technical integration, I specialize in organizational integration – bringing together people, processes, and technologies to create cohesive solutions. My experience spans from integrating React frontends with Spring Boot backends to integrating development teams with business units and external stakeholders.
            
            At Synteda, I built complete office management platforms from scratch, which required integrating not just technical components but also user workflows, business processes, and organizational change management. This holistic approach to integration has consistently delivered successful outcomes across diverse projects.
            """
        
        # Company-specific customization
        if is_automotive:
            industry_connection = f"""
            What particularly excites me about {company} is the opportunity to contribute to the automotive industry's digital transformation. My current role at ECARX has given me deep insights into automotive technology challenges, and I am passionate about leveraging my technical expertise to enhance the driving experience through innovative software solutions.
            """
        elif is_startup:
            industry_connection = f"""
            I am drawn to {company}'s innovative approach and growth trajectory. My experience in fast-paced environments, combined with my ability to wear multiple hats and adapt quickly to changing requirements, makes me well-suited for the dynamic nature of your organization.
            """
        else:
            industry_connection = f"""
            I am impressed by {company}'s commitment to excellence and innovation. My experience working with established organizations has taught me the importance of balancing innovation with stability, and I am excited about contributing to your continued success.
            """
        
        # Generate the complete cover letter
        current_date = time.strftime("%Y.%m.%d")
        
        cover_letter_content = f"""
\\documentclass[10pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}

\\geometry{{margin=1in}}
\\setlength{{\\parindent}}{{0pt}}
\\definecolor{{linkedinblue}}{{RGB}}{{0,119,181}}
\\hypersetup{{colorlinks=true, linkcolor=linkedinblue, urlcolor=linkedinblue}}

\\begin{{document}}

% Header with job information (simple left-aligned)
{{\\color{{linkedinblue}}{company}\\\\
{position}\\\\
Gothenburg, Sweden}}

\\vspace{{1cm}}

{greeting},

\\vspace{{0.5cm}}

I am writing to express my sincere interest in the {position} role at {company}. As an experienced professional with a unique combination of technical expertise and cross-cultural communication skills, I am excited about the opportunity to contribute to your team's success while bringing a fresh perspective to your technical challenges.

{industry_connection}

{soft_skills_focus}

{integration_expertise}

My technical foundation includes expertise in modern technologies such as Python, Java, JavaScript, Cloud platforms (AWS, Azure, GCP), Kubernetes, Docker, and various databases. However, what truly differentiates me is my ability to leverage these technical skills within a collaborative, multicultural context, ensuring that technology solutions align with business objectives and user needs.

At {company}, I am particularly excited about the opportunity to contribute not just my technical skills, but also my experience in fostering collaboration, managing stakeholder relationships, and driving successful project outcomes through effective communication and integration practices.

I am confident that my combination of technical expertise, soft skills, and integration experience will make a valuable contribution to your team. I look forward to discussing how my unique background can support {company}'s continued growth and success.

\\vspace{{1cm}}

Best Regards,\\\\[0.5cm]
Harvad (Hongzhi) Li

\\vspace{{\\fill}}

% Line separator
{{\\color{{linkedinblue}}\\hrule height 0.5pt}}

\\vspace{{0.3cm}}

% Footer with address and date
{{\\color{{linkedinblue}}Ebbe Lieberathsgatan 27\\\\
412 65, Gothenburg, Sweden\\\\
\\hfill \\today}}

\\end{{document}}
"""
        
        return cover_letter_content.strip()
    
    def create_cover_letter_with_r2_overleaf(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create cover letter PDF and upload LaTeX to R2 for Overleaf integration
        Returns both PDF content and Overleaf URL
        """
        try:
            # Analyze job with Claude API (optional enhancement)
            claude_analysis = self._analyze_job_with_claude(job_data)
            
            # Generate LaTeX content with LEGO intelligence
            latex_content = self._generate_cover_letter_content(job_data, claude_analysis)
            
            # Compile LaTeX to PDF locally
            pdf_content = self._compile_latex_locally(latex_content)
            
            # Upload to R2
            r2_result = self.r2_storage.upload_latex_file(latex_content, job_data)
            
            result = {
                'pdf_content': pdf_content,
                'latex_content': latex_content,
                'pdf_size': len(pdf_content) if pdf_content else 0,
                'latex_size': len(latex_content),
                'success': bool(pdf_content),
                'company': job_data.get('company', 'Unknown'),
                'job_title': job_data.get('title', 'Unknown'),
                'document_type': 'cover_letter'
            }
            
            if r2_result:
                # Modify filename to indicate cover letter
                cover_letter_filename = r2_result['filename'].replace('resume_', 'cover_letter_')
                
                result.update({
                    'r2_filename': cover_letter_filename,
                    'latex_url': r2_result['public_url'].replace(r2_result['filename'], cover_letter_filename),
                    'overleaf_url': f"https://www.overleaf.com/docs?snip_uri={r2_result['public_url'].replace(r2_result['filename'], cover_letter_filename)}",
                    'r2_upload_success': True
                })
                logger.info(f"🎉 Cover letter success: PDF + R2 + Overleaf URL for {job_data.get('company')}")
            else:
                result.update({
                    'r2_filename': '',
                    'latex_url': '',
                    'overleaf_url': '',
                    'r2_upload_success': False
                })
                logger.warning(f"⚠️ Cover letter PDF created but R2 upload failed for {job_data.get('company')}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error creating cover letter: {e}")
            return {
                'pdf_content': b'',
                'latex_content': '',
                'pdf_size': 0,
                'latex_size': 0,
                'success': False,
                'r2_upload_success': False,
                'document_type': 'cover_letter',
                'error': str(e)
            }
    
    def _compile_latex_locally(self, latex_content: str) -> bytes:
        """Compile LaTeX to PDF locally using pdflatex"""
        try:
            import subprocess
            import tempfile
            
            with tempfile.TemporaryDirectory() as temp_dir:
                tex_file = os.path.join(temp_dir, "cover_letter.tex")
                pdf_file = os.path.join(temp_dir, "cover_letter.pdf")
                
                # Write LaTeX content
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                
                # Compile LaTeX (run twice for references)
                for _ in range(2):
                    result = subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                        capture_output=True, text=True
                    )
                    
                    if result.returncode != 0:
                        logger.error(f"LaTeX compilation failed: {result.stderr}")
                        return b""
                
                # Read PDF
                if os.path.exists(pdf_file):
                    with open(pdf_file, 'rb') as f:
                        return f.read()
                        
        except Exception as e:
            logger.error(f"❌ Local LaTeX compilation failed: {e}")
            return b""

# Convenience function for integration
def create_cover_letter_pdf(job_data: Dict[str, Any]) -> bytes:
    """Create cover letter PDF - simple interface"""
    generator = CoverLetterGenerator()
    result = generator.create_cover_letter_with_r2_overleaf(job_data)
    return result.get('pdf_content', b'')

if __name__ == "__main__":
    # Test cover letter generation
    test_job = {
        'title': 'DevOps Engineer',
        'company': 'Opera',
        'description': '''
        We are looking for a DevOps Engineer to join our team and help us build and maintain our infrastructure.
        Experience with AWS, Azure, Kubernetes, Docker, CI/CD tools, Infrastructure as Code, 
        Monitoring tools, Scripting languages, Linux system administration, Security best practices, 
        Agile methodologies. Experience with microservices architecture and cross-functional collaboration.
        ''',
        'location': 'Oslo, Norway'
    }
    
    print("📝 Testing Cover Letter Generator...")
    generator = CoverLetterGenerator()
    result = generator.create_cover_letter_with_r2_overleaf(test_job)
    
    print(f"✅ Success: {result['success']}")
    print(f"📄 PDF Size: {result['pdf_size']} bytes")
    print(f"📝 LaTeX Size: {result['latex_size']} characters")
    print(f"☁️ R2 Upload: {result['r2_upload_success']}")
    
    if result['pdf_content']:
        with open('test_opera_cover_letter.pdf', 'wb') as f:
            f.write(result['pdf_content'])
        print("💾 Saved: test_opera_cover_letter.pdf")
    
    if result['latex_content']:
        with open('test_opera_cover_letter.tex', 'w') as f:
            f.write(result['latex_content'])
        print("💾 Saved: test_opera_cover_letter.tex")
    
    if result['r2_upload_success']:
        print(f"🔗 Overleaf URL: {result['overleaf_url']}")
    
    print("🎉 Cover letter generation complete!")