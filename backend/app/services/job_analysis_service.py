import logging
import re
import asyncio
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from .claude_api_service import ClaudeAPIService

logger = logging.getLogger(__name__)

@dataclass
class JobRequirements:
    """Structure for analyzed job requirements"""
    technical_skills: List[str]
    soft_skills: List[str]
    experience_level: str
    programming_languages: List[str]
    frameworks_tools: List[str]
    databases: List[str]
    cloud_platforms: List[str]
    methodologies: List[str]
    industry_keywords: List[str]
    required_experience_years: Optional[int]
    education_level: str
    certifications: List[str]
    job_responsibilities: List[str]
    company_culture_keywords: List[str]
    benefits_mentioned: List[str]
    job_type: str  # remote, hybrid, onsite
    seniority_level: str
    urgency_indicators: List[str]

class JobAnalysisService:
    """
    Advanced job analysis service that extracts detailed requirements from job advertisements
    to enable highly customized CV and cover letter generation
    """
    
    def __init__(self):
        self.claude_service = ClaudeAPIService()
        
        # Comprehensive keyword mappings
        self.technical_skills_map = {
            # Programming Languages
            'languages': {
                'java', 'javascript', 'python', 'typescript', 'c#', 'go', 'rust', 'kotlin', 
                'swift', 'php', 'ruby', 'scala', 'clojure', 'r', 'matlab', 'c++', 'c'
            },
            
            # Frontend Technologies
            'frontend': {
                'react', 'angular', 'vue', 'svelte', 'html', 'css', 'sass', 'less',
                'webpack', 'vite', 'parcel', 'gatsby', 'next.js', 'nuxt.js', 'tailwind'
            },
            
            # Backend Technologies  
            'backend': {
                'spring', 'spring boot', 'django', 'flask', 'fastapi', 'express',
                'nest.js', 'rails', 'laravel', 'symfony', '.net', 'asp.net'
            },
            
            # Databases
            'databases': {
                'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
                'dynamodb', 'sqlite', 'oracle', 'sql server', 'neo4j', 'influxdb'
            },
            
            # Cloud Platforms
            'cloud': {
                'aws', 'azure', 'gcp', 'google cloud', 'digitalocean', 'heroku',
                'vercel', 'netlify', 'cloudflare', 'alibaba cloud'
            },
            
            # DevOps & Tools
            'devops': {
                'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions',
                'terraform', 'ansible', 'puppet', 'chef', 'vagrant', 'helm'
            },
            
            # Testing
            'testing': {
                'junit', 'pytest', 'jest', 'cypress', 'selenium', 'testng',
                'mocha', 'karma', 'jasmine', 'cucumber'
            }
        }
        
        self.soft_skills_keywords = {
            'communication', 'teamwork', 'leadership', 'problem-solving', 
            'analytical', 'creative', 'innovative', 'collaborative', 
            'adaptable', 'flexible', 'proactive', 'self-motivated',
            'detail-oriented', 'organized', 'time management', 'multitasking'
        }
        
        self.experience_patterns = {
            'junior': ['junior', 'entry', 'graduate', '0-2 years', 'trainee', 'intern'],
            'mid': ['mid', 'intermediate', '2-5 years', '3-5 years'],  
            'senior': ['senior', 'lead', 'principal', 'expert', '5+ years', '7+ years'],
            'architect': ['architect', 'chief', 'director', '10+ years']
        }

    async def analyze_job_posting(self, job_data: Dict) -> JobRequirements:
        """
        Comprehensive analysis of a job posting to extract all relevant requirements
        """
        try:
            logger.info(f"🔍 Analyzing job: {job_data['title']} at {job_data['company']}")
            
            # Combine all text for analysis
            full_text = self._combine_job_text(job_data)
            
            # Extract basic requirements using regex patterns
            basic_requirements = self._extract_basic_requirements(full_text)
            
            # Use Claude AI for advanced analysis
            ai_enhanced_requirements = await self._ai_enhance_analysis(job_data, full_text, basic_requirements)
            
            # Combine and create final requirements object
            final_requirements = self._merge_requirements(basic_requirements, ai_enhanced_requirements)
            
            logger.info(f"✅ Job analysis completed for {job_data['company']}")
            return final_requirements
            
        except Exception as e:
            logger.error(f"❌ Error analyzing job posting: {e}")
            return self._create_fallback_requirements(job_data)

    def _combine_job_text(self, job_data: Dict) -> str:
        """Combine all available job text for analysis"""
        text_parts = [
            job_data.get('title', ''),
            job_data.get('description', ''),
            job_data.get('company', ''),
            ' '.join(job_data.get('keywords', [])),
            ' '.join(job_data.get('requirements', [])),
            job_data.get('company_info', ''),
            ' '.join(job_data.get('benefits', [])),
        ]
        return ' '.join(filter(None, text_parts))

    def _extract_basic_requirements(self, text: str) -> Dict:
        """Extract basic requirements using regex patterns"""
        text_lower = text.lower()
        
        # Extract technical skills
        technical_skills = self._extract_technical_skills(text_lower)
        
        # Extract soft skills
        soft_skills = [skill for skill in self.soft_skills_keywords if skill in text_lower]
        
        # Extract experience level
        experience_level = self._determine_experience_level(text_lower)
        
        # Extract years of experience
        years_pattern = r'(\d+)\s*\+?\s*years?\s*(?:of\s*)?experience'
        years_match = re.search(years_pattern, text_lower)
        required_years = int(years_match.group(1)) if years_match else None
        
        # Extract education requirements
        education_level = self._extract_education_level(text_lower)
        
        # Extract job type (remote/hybrid/onsite)
        job_type = self._extract_job_type(text_lower)
        
        # Extract urgency indicators
        urgency_indicators = self._extract_urgency_indicators(text_lower)
        
        return {
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'experience_level': experience_level,
            'required_experience_years': required_years,
            'education_level': education_level,
            'job_type': job_type,
            'urgency_indicators': urgency_indicators
        }

    def _extract_technical_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract categorized technical skills"""
        extracted = {category: [] for category in self.technical_skills_map.keys()}
        
        for category, keywords in self.technical_skills_map.items():
            for keyword in keywords:
                if keyword in text:
                    extracted[category].append(keyword)
        
        return extracted

    def _determine_experience_level(self, text: str) -> str:
        """Determine experience level from text"""
        for level, patterns in self.experience_patterns.items():
            if any(pattern in text for pattern in patterns):
                return level
        return 'mid'  # Default to mid-level

    def _extract_education_level(self, text: str) -> str:
        """Extract education requirements"""
        if any(term in text for term in ['phd', 'doctorate', 'doctoral']):
            return 'PhD'
        elif any(term in text for term in ['master', 'msc', 'masters']):
            return 'Masters'
        elif any(term in text for term in ['bachelor', 'bsc', 'degree', 'university']):
            return 'Bachelors'
        elif any(term in text for term in ['certification', 'certificate', 'course']):
            return 'Certification'
        return 'Not specified'

    def _extract_job_type(self, text: str) -> str:
        """Extract job type (remote, hybrid, onsite)"""
        if 'remote' in text:
            if 'hybrid' in text or 'flexible' in text:
                return 'hybrid'
            return 'remote'
        elif 'hybrid' in text:
            return 'hybrid'
        elif any(term in text for term in ['on-site', 'onsite', 'office']):
            return 'onsite'
        return 'not specified'

    def _extract_urgency_indicators(self, text: str) -> List[str]:
        """Extract urgency indicators"""
        urgency_keywords = [
            'urgent', 'asap', 'immediately', 'start immediately',
            'fast-growing', 'scaling rapidly', 'urgent need',
            'join us now', 'immediate start'
        ]
        return [keyword for keyword in urgency_keywords if keyword in text]

    async def _ai_enhance_analysis(self, job_data: Dict, full_text: str, basic_requirements: Dict) -> Dict:
        """Use Claude AI to enhance the job analysis"""
        try:
            prompt = f"""
            Analyze this job posting and extract detailed information for CV customization:
            
            JOB TITLE: {job_data.get('title', '')}
            COMPANY: {job_data.get('company', '')}
            LOCATION: {job_data.get('location', '')}
            
            JOB DESCRIPTION:
            {full_text}
            
            Please extract and categorize:
            
            1. PROGRAMMING LANGUAGES (list all mentioned)
            2. FRAMEWORKS & TOOLS (specific frameworks, libraries, tools)
            3. DATABASES (all database technologies mentioned)
            4. CLOUD PLATFORMS (AWS, Azure, GCP services mentioned)
            5. METHODOLOGIES (Agile, Scrum, DevOps practices)
            6. INDUSTRY KEYWORDS (domain-specific terms, business context)
            7. JOB RESPONSIBILITIES (main duties and responsibilities)
            8. COMPANY CULTURE KEYWORDS (values, culture, work environment)
            9. BENEFITS MENTIONED (perks, benefits, compensation details)
            10. CERTIFICATIONS (any certifications mentioned or preferred)
            11. SENIORITY LEVEL (junior/mid/senior/lead based on responsibilities)
            
            Format as JSON with these exact keys:
            {
                "programming_languages": [],
                "frameworks_tools": [],
                "databases": [],
                "cloud_platforms": [],
                "methodologies": [],
                "industry_keywords": [],
                "job_responsibilities": [],
                "company_culture_keywords": [],
                "benefits_mentioned": [],
                "certifications": [],
                "seniority_level": ""
            }
            
            Return only valid JSON.
            """
            
            ai_response = await self.claude_service._make_claude_request(prompt)
            
            # Parse JSON response
            import json
            try:
                ai_analysis = json.loads(ai_response)
                return ai_analysis
            except json.JSONDecodeError:
                logger.warning("Failed to parse AI analysis JSON, using fallback")
                return self._create_ai_fallback(job_data)
                
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            return self._create_ai_fallback(job_data)

    def _create_ai_fallback(self, job_data: Dict) -> Dict:
        """Create fallback AI analysis"""
        return {
            "programming_languages": job_data.get('keywords', [])[:3],
            "frameworks_tools": [],
            "databases": [],
            "cloud_platforms": [],
            "methodologies": ['agile'],
            "industry_keywords": [],
            "job_responsibilities": ['software development', 'code review', 'testing'],
            "company_culture_keywords": ['teamwork', 'innovation'],
            "benefits_mentioned": [],
            "certifications": [],
            "seniority_level": "mid"
        }

    def _merge_requirements(self, basic: Dict, ai_enhanced: Dict) -> JobRequirements:
        """Merge basic and AI-enhanced requirements into final structure"""
        
        # Combine technical skills from both sources
        all_technical = []
        for category_skills in basic['technical_skills'].values():
            all_technical.extend(category_skills)
        
        return JobRequirements(
            technical_skills=list(set(all_technical + ai_enhanced.get('frameworks_tools', []))),
            soft_skills=basic['soft_skills'],
            experience_level=basic['experience_level'],
            programming_languages=ai_enhanced.get('programming_languages', []),
            frameworks_tools=ai_enhanced.get('frameworks_tools', []),
            databases=ai_enhanced.get('databases', []),
            cloud_platforms=ai_enhanced.get('cloud_platforms', []),
            methodologies=ai_enhanced.get('methodologies', []),
            industry_keywords=ai_enhanced.get('industry_keywords', []),
            required_experience_years=basic['required_experience_years'],
            education_level=basic['education_level'],
            certifications=ai_enhanced.get('certifications', []),
            job_responsibilities=ai_enhanced.get('job_responsibilities', []),
            company_culture_keywords=ai_enhanced.get('company_culture_keywords', []),
            benefits_mentioned=ai_enhanced.get('benefits_mentioned', []),
            job_type=basic['job_type'],
            seniority_level=ai_enhanced.get('seniority_level', basic['experience_level']),
            urgency_indicators=basic['urgency_indicators']
        )

    def _create_fallback_requirements(self, job_data: Dict) -> JobRequirements:
        """Create fallback requirements if analysis fails"""
        return JobRequirements(
            technical_skills=job_data.get('keywords', []),
            soft_skills=['problem-solving', 'teamwork', 'communication'],
            experience_level='mid',
            programming_languages=[],
            frameworks_tools=[],
            databases=[],
            cloud_platforms=[],
            methodologies=['agile'],
            industry_keywords=[],
            required_experience_years=None,
            education_level='Bachelors',
            certifications=[],
            job_responsibilities=['software development'],
            company_culture_keywords=['innovation', 'teamwork'],
            benefits_mentioned=[],
            job_type='not specified',
            seniority_level='mid',
            urgency_indicators=[]
        )

    async def analyze_multiple_jobs(self, jobs_list: List[Dict]) -> List[Dict]:
        """Analyze multiple jobs in parallel for efficiency"""
        try:
            logger.info(f"📊 Analyzing {len(jobs_list)} job postings in parallel")
            
            # Create analysis tasks
            tasks = []
            for job in jobs_list:
                task = self.analyze_job_posting(job)
                tasks.append(task)
            
            # Execute in parallel with controlled concurrency
            semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent analyses
            
            async def bounded_analysis(job, task):
                async with semaphore:
                    requirements = await task
                    return {
                        'job_data': job,
                        'requirements': requirements
                    }
            
            bounded_tasks = [
                bounded_analysis(jobs_list[i], tasks[i]) 
                for i in range(len(tasks))
            ]
            
            results = await asyncio.gather(*bounded_tasks, return_exceptions=True)
            
            # Filter out exceptions
            successful_results = [
                result for result in results 
                if not isinstance(result, Exception)
            ]
            
            logger.info(f"✅ Successfully analyzed {len(successful_results)} job postings")
            return successful_results
            
        except Exception as e:
            logger.error(f"❌ Error in batch job analysis: {e}")
            return []

    def calculate_job_match_score(self, job_requirements: JobRequirements, user_profile: Dict) -> float:
        """
        Calculate how well a user profile matches job requirements (0-1 score)
        """
        try:
            user_skills = set(skill.lower() for skill in user_profile.get('technical_skills', []))
            user_languages = set(lang.lower() for lang in user_profile.get('programming_languages', []))
            user_experience_years = user_profile.get('years_experience', 0)
            
            # Technical skills match (40% weight)
            required_skills = set(skill.lower() for skill in job_requirements.technical_skills)
            skills_match = len(user_skills.intersection(required_skills)) / max(len(required_skills), 1)
            
            # Programming languages match (30% weight)  
            required_languages = set(lang.lower() for lang in job_requirements.programming_languages)
            languages_match = len(user_languages.intersection(required_languages)) / max(len(required_languages), 1)
            
            # Experience level match (20% weight)
            experience_match = 1.0
            if job_requirements.required_experience_years:
                if user_experience_years >= job_requirements.required_experience_years:
                    experience_match = 1.0
                else:
                    experience_match = user_experience_years / job_requirements.required_experience_years
            
            # Seniority match (10% weight)
            seniority_match = 0.8  # Default good match
            user_level = user_profile.get('seniority_level', 'mid').lower()
            required_level = job_requirements.seniority_level.lower()
            
            if user_level == required_level:
                seniority_match = 1.0
            elif (user_level == 'senior' and required_level == 'mid') or \
                 (user_level == 'mid' and required_level == 'junior'):
                seniority_match = 0.9  # Overqualified but still good
            
            # Calculate weighted score
            total_score = (
                skills_match * 0.4 + 
                languages_match * 0.3 + 
                experience_match * 0.2 + 
                seniority_match * 0.1
            )
            
            return min(total_score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            logger.error(f"Error calculating job match score: {e}")
            return 0.5  # Default neutral score

    def get_customization_priorities(self, job_requirements: JobRequirements) -> Dict[str, List[str]]:
        """
        Get prioritized customization suggestions for CV/CL generation
        """
        return {
            'high_priority_skills': job_requirements.programming_languages + job_requirements.frameworks_tools[:3],
            'emphasis_keywords': job_requirements.industry_keywords[:5],
            'highlight_responsibilities': job_requirements.job_responsibilities[:3],
            'culture_alignment': job_requirements.company_culture_keywords[:3],
            'technical_focus': job_requirements.technical_skills[:5],
            'methodologies_to_mention': job_requirements.methodologies,
            'urgency_level': 'high' if job_requirements.urgency_indicators else 'normal'
        }