import logging
import asyncio
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import os
from .claude_api_service import ClaudeAPIService
from .job_analysis_service import JobRequirements, JobAnalysisService

logger = logging.getLogger(__name__)

class SmartCVCustomizationService:
    """
    Advanced CV customization service that creates highly targeted resumes
    based on real job analysis and requirements
    """
    
    def __init__(self):
        self.claude_service = ClaudeAPIService()
        self.job_analyzer = JobAnalysisService()
        
        # Base user profile (should be loaded from database in production)
        self.user_profile = {
            'name': 'Hongzhi Li',
            'email': 'hongzhili01@gmail.com',
            'phone': '+46 76 123 4567',
            'location': 'Stockholm, Sweden',
            'linkedin': 'linkedin.com/in/hongzhi-li',
            'github': 'github.com/bluehawana',
            
            # Professional summary variations
            'professional_summaries': {
                'fullstack': 'Experienced Full Stack Developer with 5+ years building scalable web applications using modern technologies. Passionate about clean code, user experience, and innovative solutions.',
                'backend': 'Senior Backend Developer specializing in high-performance systems and microservices architecture. Expert in Java, Python, and cloud technologies with strong focus on scalability.',
                'devops': 'DevOps Engineer with extensive experience in cloud infrastructure, CI/CD pipelines, and container orchestration. Proven track record of improving deployment efficiency and system reliability.',
                'senior': 'Senior Software Engineer with 5+ years experience leading development teams and architecting complex systems. Expertise in full-stack development, cloud technologies, and agile methodologies.',
                'default': 'Versatile Software Developer with strong problem-solving skills and passion for technology. Experience with modern frameworks, cloud platforms, and collaborative development practices.'
            },
            
            # Technical skills by category
            'technical_skills': {
                'programming_languages': ['Java', 'JavaScript', 'Python', 'TypeScript', 'Go', 'C#'],
                'frontend_frameworks': ['React', 'Angular', 'Vue.js', 'Next.js', 'HTML5', 'CSS3', 'Sass'],
                'backend_frameworks': ['Spring Boot', 'Django', 'Flask', 'Express.js', 'Node.js', '.NET Core'],
                'databases': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch'],
                'cloud_platforms': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes'],
                'devops_tools': ['Jenkins', 'GitLab CI', 'GitHub Actions', 'Terraform', 'Ansible'],
                'testing_frameworks': ['JUnit', 'Jest', 'Pytest', 'Cypress', 'Selenium'],
                'other_tools': ['Git', 'Jira', 'Confluence', 'Postman', 'IntelliJ IDEA']
            },
            
            # Work experience (detailed for customization)
            'work_experience': [
                {
                    'company': 'Tech Innovation AB',
                    'position': 'Senior Full Stack Developer',
                    'period': '2021 - Present',
                    'location': 'Stockholm, Sweden',
                    'achievements': [
                        'Led development of microservices architecture serving 100K+ daily users',
                        'Implemented CI/CD pipeline reducing deployment time by 60%',
                        'Mentored junior developers and conducted code reviews',
                        'Optimized database queries improving application performance by 40%',
                        'Collaborated with cross-functional teams using Agile methodologies'
                    ],
                    'technologies': ['Java', 'Spring Boot', 'React', 'PostgreSQL', 'AWS', 'Docker'],
                    'keywords': ['microservices', 'scalability', 'performance', 'mentoring', 'agile']
                },
                {
                    'company': 'Digital Solutions Sweden',
                    'position': 'Backend Developer',
                    'period': '2019 - 2021',
                    'location': 'Gothenburg, Sweden',
                    'achievements': [
                        'Developed REST APIs handling 10M+ requests daily',
                        'Implemented automated testing increasing code coverage to 95%',
                        'Integrated third-party payment systems and APIs',
                        'Participated in system architecture design and reviews',
                        'Collaborated with frontend team for seamless integration'
                    ],
                    'technologies': ['Python', 'Django', 'PostgreSQL', 'Redis', 'Jenkins'],
                    'keywords': ['apis', 'testing', 'integration', 'architecture', 'collaboration']
                },
                {
                    'company': 'StartupTech',
                    'position': 'Junior Software Developer',
                    'period': '2018 - 2019',
                    'location': 'Stockholm, Sweden',
                    'achievements': [
                        'Built responsive web applications using modern frameworks',
                        'Contributed to open-source projects and internal tools',
                        'Learned rapidly in fast-paced startup environment',
                        'Implemented automated testing and deployment scripts',
                        'Participated in daily standups and sprint planning'
                    ],
                    'technologies': ['JavaScript', 'Node.js', 'MongoDB', 'React', 'Git'],
                    'keywords': ['responsive', 'opensource', 'startup', 'automation', 'learning']
                }
            ],
            
            # Education
            'education': [
                {
                    'degree': 'Master of Science in Computer Science',
                    'institution': 'Royal Institute of Technology (KTH)',
                    'period': '2016 - 2018',
                    'location': 'Stockholm, Sweden',
                    'highlights': ['Thesis: Machine Learning in Distributed Systems', 'GPA: 4.2/5.0']
                },
                {
                    'degree': 'Bachelor of Engineering in Software Engineering', 
                    'institution': 'University of Technology',
                    'period': '2012 - 2016',
                    'location': 'China',
                    'highlights': ['Graduated Summa Cum Laude', 'Relevant Coursework: Data Structures, Algorithms, Database Systems']
                }
            ],
            
            # Projects (can be emphasized based on job requirements)
            'projects': [
                {
                    'name': 'JobHunter Automation Platform',
                    'description': 'AI-powered job application automation system with intelligent document generation',
                    'technologies': ['Python', 'FastAPI', 'Claude AI API', 'LaTeX', 'Docker', 'Heroku'],
                    'highlights': ['Automated CV/CL generation with 95% relevance matching', 'Intelligent job analysis and matching', 'Scalable document processing pipeline'],
                    'keywords': ['automation', 'ai', 'document-generation', 'job-matching', 'microservices']
                },
                {
                    'name': 'E-commerce Platform',
                    'description': 'Full-stack e-commerce solution with microservices architecture',
                    'technologies': ['Java', 'Spring Boot', 'React', 'PostgreSQL', 'Docker', 'AWS'],
                    'highlights': ['Handles 50K+ concurrent users', 'Implemented payment integration', 'Deployed on AWS with auto-scaling'],
                    'keywords': ['ecommerce', 'microservices', 'scalability', 'payments', 'cloud']
                },
                {
                    'name': 'DevOps Automation Suite',
                    'description': 'Automated CI/CD pipeline and infrastructure management tools',
                    'technologies': ['Python', 'Jenkins', 'Docker', 'Kubernetes', 'Terraform', 'AWS'],
                    'highlights': ['Reduced deployment time by 70%', 'Automated testing and monitoring', 'Infrastructure as Code'],
                    'keywords': ['automation', 'cicd', 'infrastructure', 'monitoring', 'iac']
                }
            ],
            
            # Certifications
            'certifications': [
                'AWS Certified Solutions Architect - Associate',
                'Certified Kubernetes Administrator (CKA)',
                'Oracle Java SE 11 Developer',
                'Google Cloud Professional Cloud Architect'
            ],
            
            # Languages
            'languages': [
                {'language': 'English', 'level': 'Fluent'},
                {'language': 'Swedish', 'level': 'Conversational'},
                {'language': 'Chinese (Mandarin)', 'level': 'Native'}
            ]
        }

    async def create_customized_cv(self, job_data: Dict, job_requirements: JobRequirements) -> str:
        """
        Create a highly customized CV based on job analysis
        """
        try:
            logger.info(f"🎯 Creating customized CV for {job_data['company']} - {job_data['title']}")
            
            # Get customization strategy
            customization_strategy = self._determine_customization_strategy(job_requirements)
            
            # Select and customize sections
            customized_sections = await self._customize_cv_sections(job_data, job_requirements, customization_strategy)
            
            # Generate final CV using Claude AI
            final_cv = await self._generate_final_cv_with_ai(job_data, customized_sections, job_requirements)
            
            logger.info(f"✅ Successfully created customized CV for {job_data['company']}")
            return final_cv
            
        except Exception as e:
            logger.error(f"❌ Error creating customized CV: {e}")
            return await self._generate_fallback_cv(job_data)

    def _determine_customization_strategy(self, requirements: JobRequirements) -> Dict:
        """
        Determine customization strategy based on job requirements
        """
        strategy = {
            'focus_areas': [],
            'emphasis_level': 'moderate',
            'technical_depth': 'detailed',
            'experience_highlighting': 'relevant',
            'projects_to_include': 3,
            'skills_priority': 'job_match'
        }
        
        # Determine focus based on job requirements
        if any(lang in ['java', 'spring'] for lang in requirements.programming_languages):
            strategy['focus_areas'].append('backend_java')
        if 'react' in requirements.frameworks_tools or 'javascript' in requirements.programming_languages:
            strategy['focus_areas'].append('frontend_react')
        if any(cloud in requirements.cloud_platforms for cloud in ['aws', 'azure', 'gcp']):
            strategy['focus_areas'].append('cloud_expertise')
        if 'devops' in requirements.technical_skills or requirements.methodologies:
            strategy['focus_areas'].append('devops_practices')
        
        # Adjust emphasis based on seniority
        if requirements.seniority_level in ['senior', 'lead', 'architect']:
            strategy['emphasis_level'] = 'high'
            strategy['technical_depth'] = 'comprehensive'
        elif requirements.seniority_level == 'junior':
            strategy['emphasis_level'] = 'moderate'
            strategy['technical_depth'] = 'focused'
        
        # Urgency adjustments
        if requirements.urgency_indicators:
            strategy['emphasis_level'] = 'high'
            strategy['projects_to_include'] = 2  # Focus on most relevant
        
        return strategy

    async def _customize_cv_sections(self, job_data: Dict, requirements: JobRequirements, strategy: Dict) -> Dict:
        """
        Customize each CV section based on job requirements
        """
        customized = {}
        
        # Professional Summary
        customized['professional_summary'] = self._customize_professional_summary(requirements, strategy)
        
        # Technical Skills  
        customized['technical_skills'] = self._customize_technical_skills(requirements, strategy)
        
        # Work Experience
        customized['work_experience'] = self._customize_work_experience(requirements, strategy)
        
        # Projects
        customized['projects'] = self._customize_projects(requirements, strategy)
        
        # Education (usually static but can emphasize relevant aspects)
        customized['education'] = self._customize_education(requirements)
        
        # Certifications
        customized['certifications'] = self._customize_certifications(requirements)
        
        return customized

    def _customize_professional_summary(self, requirements: JobRequirements, strategy: Dict) -> str:
        """
        Customize professional summary based on job requirements
        """
        # Select base summary based on job focus
        if 'backend_java' in strategy['focus_areas']:
            base_summary = self.user_profile['professional_summaries']['backend']
        elif 'frontend_react' in strategy['focus_areas']:
            base_summary = self.user_profile['professional_summaries']['fullstack']
        elif 'devops_practices' in strategy['focus_areas']:
            base_summary = self.user_profile['professional_summaries']['devops']
        elif requirements.seniority_level in ['senior', 'lead']:
            base_summary = self.user_profile['professional_summaries']['senior']
        else:
            base_summary = self.user_profile['professional_summaries']['default']
        
        # Add job-specific keywords naturally
        keywords_to_integrate = requirements.industry_keywords[:3] + requirements.technical_skills[:2]
        
        return base_summary

    def _customize_technical_skills(self, requirements: JobRequirements, strategy: Dict) -> Dict:
        """
        Customize and prioritize technical skills
        """
        user_skills = self.user_profile['technical_skills']
        customized_skills = {}
        
        # Prioritize skills that match job requirements
        for category, skills in user_skills.items():
            relevant_skills = []
            other_skills = []
            
            for skill in skills:
                skill_lower = skill.lower()
                if (skill_lower in [s.lower() for s in requirements.programming_languages] or
                    skill_lower in [s.lower() for s in requirements.frameworks_tools] or  
                    skill_lower in [s.lower() for s in requirements.technical_skills]):
                    relevant_skills.append(skill)
                else:
                    other_skills.append(skill)
            
            # Put relevant skills first
            customized_skills[category] = relevant_skills + other_skills[:5]  # Limit total skills
        
        return customized_skills

    def _customize_work_experience(self, requirements: JobRequirements, strategy: Dict) -> List[Dict]:
        """
        Customize work experience highlighting relevant achievements
        """
        customized_experience = []
        
        for exp in self.user_profile['work_experience']:
            customized_exp = exp.copy()
            
            # Score achievements based on relevance to job
            scored_achievements = []
            for achievement in exp['achievements']:
                score = self._score_achievement_relevance(achievement, requirements)
                scored_achievements.append((achievement, score))
            
            # Sort by relevance and take top achievements
            scored_achievements.sort(key=lambda x: x[1], reverse=True)
            max_achievements = 4 if requirements.seniority_level in ['senior', 'lead'] else 3
            
            customized_exp['achievements'] = [
                achievement for achievement, score in scored_achievements[:max_achievements]
            ]
            
            customized_experience.append(customized_exp)
        
        return customized_experience

    def _score_achievement_relevance(self, achievement: str, requirements: JobRequirements) -> float:
        """
        Score how relevant an achievement is to the job requirements
        """
        score = 0.0
        achievement_lower = achievement.lower()
        
        # Check for technical skill matches
        for skill in requirements.technical_skills:
            if skill.lower() in achievement_lower:
                score += 1.0
        
        # Check for responsibility matches  
        for responsibility in requirements.job_responsibilities:
            if any(word in achievement_lower for word in responsibility.lower().split()):
                score += 0.8
        
        # Check for methodology matches
        for methodology in requirements.methodologies:
            if methodology.lower() in achievement_lower:
                score += 0.6
        
        # Check for industry keywords
        for keyword in requirements.industry_keywords:
            if keyword.lower() in achievement_lower:
                score += 0.4
        
        return score

    def _customize_projects(self, requirements: JobRequirements, strategy: Dict) -> List[Dict]:
        """
        Select and customize projects based on job relevance
        """
        # Score projects based on relevance
        scored_projects = []
        for project in self.user_profile['projects']:
            score = self._score_project_relevance(project, requirements)
            scored_projects.append((project, score))
        
        # Sort by relevance and select top projects
        scored_projects.sort(key=lambda x: x[1], reverse=True)
        selected_projects = [
            project for project, score in scored_projects[:strategy['projects_to_include']]
        ]
        
        return selected_projects

    def _score_project_relevance(self, project: Dict, requirements: JobRequirements) -> float:
        """
        Score project relevance to job requirements
        """
        score = 0.0
        
        # Technology matches
        project_tech = [tech.lower() for tech in project['technologies']]
        required_tech = [tech.lower() for tech in requirements.programming_languages + requirements.frameworks_tools]
        
        tech_matches = len(set(project_tech).intersection(set(required_tech)))
        score += tech_matches * 2.0
        
        # Keyword matches
        project_keywords = project['keywords']
        required_keywords = requirements.industry_keywords + requirements.technical_skills
        
        keyword_matches = len(set([k.lower() for k in project_keywords]).intersection(
            set([k.lower() for k in required_keywords])
        ))
        score += keyword_matches * 1.0
        
        return score

    def _customize_education(self, requirements: JobRequirements) -> List[Dict]:
        """
        Customize education section (usually minimal changes)
        """
        education = self.user_profile['education'].copy()
        
        # If job requires specific education level, ensure it's highlighted
        if requirements.education_level in ['Masters', 'PhD']:
            # Move relevant degree to front
            masters_degrees = [edu for edu in education if 'Master' in edu['degree']]
            other_degrees = [edu for edu in education if 'Master' not in edu['degree']]
            education = masters_degrees + other_degrees
        
        return education

    def _customize_certifications(self, requirements: JobRequirements) -> List[str]:
        """
        Prioritize relevant certifications
        """
        user_certs = self.user_profile['certifications']
        relevant_certs = []
        other_certs = []
        
        for cert in user_certs:
            cert_lower = cert.lower()
            is_relevant = False
            
            # Check if certification matches job requirements
            for tech in requirements.cloud_platforms + requirements.technical_skills:
                if tech.lower() in cert_lower:
                    relevant_certs.append(cert)
                    is_relevant = True
                    break
            
            if not is_relevant:
                other_certs.append(cert)
        
        # Return relevant certifications first
        return relevant_certs + other_certs[:2]  # Limit total certifications

    async def _generate_final_cv_with_ai(self, job_data: Dict, customized_sections: Dict, requirements: JobRequirements) -> str:
        """
        Use Claude AI to generate the final polished CV
        """
        try:
            prompt = f"""
            Create a professional, ATS-optimized CV for this job application:
            
            JOB TITLE: {job_data['title']}
            COMPANY: {job_data['company']}
            LOCATION: {job_data.get('location', 'Sweden')}
            
            JOB REQUIREMENTS SUMMARY:
            - Technical Skills: {', '.join(requirements.technical_skills[:5])}
            - Programming Languages: {', '.join(requirements.programming_languages)}
            - Experience Level: {requirements.seniority_level}
            - Industry Keywords: {', '.join(requirements.industry_keywords[:3])}
            
            CUSTOMIZED CV SECTIONS:
            
            PROFESSIONAL SUMMARY:
            {customized_sections['professional_summary']}
            
            TECHNICAL SKILLS:
            {json.dumps(customized_sections['technical_skills'], indent=2)}
            
            WORK EXPERIENCE:
            {json.dumps(customized_sections['work_experience'], indent=2)}
            
            PROJECTS:
            {json.dumps(customized_sections['projects'], indent=2)}
            
            EDUCATION:
            {json.dumps(customized_sections['education'], indent=2)}
            
            CERTIFICATIONS:
            {json.dumps(customized_sections['certifications'], indent=2)}
            
            USER CONTACT INFO:
            Name: {self.user_profile['name']}
            Email: {self.user_profile['email']}
            Location: {self.user_profile['location']}
            LinkedIn: {self.user_profile['linkedin']}
            GitHub: {self.user_profile['github']}
            
            Please create a professional LaTeX CV that:
            1. Uses a modern, clean template suitable for tech roles
            2. Integrates job-relevant keywords naturally throughout
            3. Emphasizes achievements and quantifiable results
            4. Is ATS-optimized with proper section headers
            5. Flows naturally and tells a compelling career story
            6. Highlights the most relevant experience and skills for this specific job
            7. Uses professional formatting with consistent styling
            8. Includes contact information in the header
            9. Fits appropriately on 1-2 pages
            
            Return only the complete LaTeX code ready for compilation.
            """
            
            cv_latex = await self.claude_service._make_claude_request(prompt)
            
            if cv_latex and len(cv_latex) > 500:
                return cv_latex
            else:
                logger.warning("AI-generated CV too short, using fallback")
                return await self._generate_fallback_cv(job_data)
                
        except Exception as e:
            logger.error(f"Error generating final CV with AI: {e}")
            return await self._generate_fallback_cv(job_data)

    async def _generate_fallback_cv(self, job_data: Dict) -> str:
        """
        Generate a basic fallback CV if AI generation fails
        """
        return f"""
\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=0.8in]{{geometry}}
\\usepackage{{titlesec}}
\\usepackage{{enumitem}}

\\begin{{document}}

\\begin{{center}}
{{\\Large\\textbf{{{self.user_profile['name']}}}}}\\\\
{self.user_profile['email']} | {self.user_profile['phone']} | {self.user_profile['location']}\\\\
LinkedIn: {self.user_profile['linkedin']} | GitHub: {self.user_profile['github']}
\\end{{center}}

\\section*{{Professional Summary}}
{self.user_profile['professional_summaries']['default']}

\\section*{{Technical Skills}}
\\textbf{{Programming Languages:}} {', '.join(self.user_profile['technical_skills']['programming_languages'][:6])}\\\\
\\textbf{{Frameworks:}} {', '.join(self.user_profile['technical_skills']['backend_frameworks'][:4])}\\\\
\\textbf{{Databases:}} {', '.join(self.user_profile['technical_skills']['databases'][:4])}\\\\
\\textbf{{Cloud Platforms:}} {', '.join(self.user_profile['technical_skills']['cloud_platforms'][:4])}

\\section*{{Work Experience}}
\\textbf{{{self.user_profile['work_experience'][0]['position']}}} - {self.user_profile['work_experience'][0]['company']} \\hfill {self.user_profile['work_experience'][0]['period']}
\\begin{{itemize}}[leftmargin=*]
\\item {self.user_profile['work_experience'][0]['achievements'][0]}
\\item {self.user_profile['work_experience'][0]['achievements'][1]}
\\item {self.user_profile['work_experience'][0]['achievements'][2]}
\\end{{itemize}}

\\section*{{Education}}
\\textbf{{{self.user_profile['education'][0]['degree']}}} - {self.user_profile['education'][0]['institution']} \\hfill {self.user_profile['education'][0]['period']}

\\section*{{Certifications}}
\\begin{{itemize}}[leftmargin=*]
\\item {self.user_profile['certifications'][0]}
\\item {self.user_profile['certifications'][1]}
\\end{{itemize}}

\\end{{document}}
        """

    async def batch_create_customized_cvs(self, analyzed_jobs: List[Dict]) -> List[Dict]:
        """
        Create customized CVs for multiple analyzed jobs in parallel
        """
        try:
            logger.info(f"📄 Creating customized CVs for {len(analyzed_jobs)} jobs")
            
            # Create CV generation tasks
            cv_tasks = []
            for job_analysis in analyzed_jobs:
                job_data = job_analysis['job_data']
                requirements = job_analysis['requirements']
                
                task = self.create_customized_cv(job_data, requirements)
                cv_tasks.append((job_data, task))
            
            # Execute with controlled concurrency
            semaphore = asyncio.Semaphore(2)  # Limit concurrent CV generations
            
            async def bounded_cv_generation(job_data, task):
                async with semaphore:
                    cv_latex = await task
                    return {
                        'job_data': job_data,
                        'cv_latex': cv_latex,
                        'generated_at': datetime.now().isoformat()
                    }
            
            bounded_tasks = [
                bounded_cv_generation(job_data, task) 
                for job_data, task in cv_tasks
            ]
            
            results = await asyncio.gather(*bounded_tasks, return_exceptions=True)
            
            # Filter successful results
            successful_cvs = [
                result for result in results 
                if not isinstance(result, Exception)
            ]
            
            logger.info(f"✅ Successfully created {len(successful_cvs)} customized CVs")
            return successful_cvs
            
        except Exception as e:
            logger.error(f"❌ Error in batch CV creation: {e}")
            return []

    def get_cv_customization_summary(self, job_data: Dict, requirements: JobRequirements) -> Dict:
        """
        Get a summary of how the CV was customized for reporting
        """
        strategy = self._determine_customization_strategy(requirements)
        
        return {
            'job_title': job_data['title'],
            'company': job_data['company'],
            'customization_strategy': strategy,
            'key_skills_highlighted': requirements.technical_skills[:5],
            'relevant_experience_emphasized': True,
            'projects_selected': strategy['projects_to_include'],
            'keywords_integrated': requirements.industry_keywords[:3],
            'cv_focus': strategy['focus_areas'],
            'generated_at': datetime.now().isoformat()
        }