import logging
import asyncio
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import re
from .claude_api_service import ClaudeAPIService
from .job_analysis_service import JobRequirements

logger = logging.getLogger(__name__)

class SmartCoverLetterService:
    """
    Advanced cover letter generation service that creates highly personalized 
    cover letters based on job analysis and company research
    """
    
    def __init__(self):
        self.claude_service = ClaudeAPIService()
        
        # User profile for personalization
        self.user_profile = {
            'name': 'Hongzhi Li',
            'current_position': 'Senior Full Stack Developer',
            'years_experience': 5,
            'location': 'Stockholm, Sweden',
            'signature_achievements': [
                'Led development of microservices architecture serving 100K+ daily users',
                'Implemented CI/CD pipeline reducing deployment time by 60%',
                'Mentored junior developers and improved team productivity by 30%',
                'Optimized application performance achieving 40% improvement in response times'
            ],
            'core_strengths': [
                'Full-stack development expertise',
                'Cloud architecture and scalability',
                'Team leadership and mentoring',
                'Agile development practices',
                'Problem-solving and innovation'
            ],
            'passion_areas': [
                'Building scalable systems',
                'Mentoring and knowledge sharing',
                'Learning new technologies',
                'Solving complex technical challenges',
                'Creating user-focused solutions'
            ],
            'career_goals': 'To continue growing as a technical leader while contributing to innovative projects that make a meaningful impact',
            'availability': 'Available for immediate start with 2-week notice period'
        }
        
        # Company-specific talking points database
        self.company_insights = {
            'spotify': {
                'mission': 'democratizing music discovery and helping artists connect with fans',
                'values': ['innovation', 'collaboration', 'passion for music', 'user experience'],
                'talking_points': ['impact on music industry', 'global scale challenges', 'creative technology'],
                'tech_focus': ['microservices', 'real-time systems', 'data analytics', 'machine learning']
            },
            'klarna': {
                'mission': 'making payments smooth and creating a shopping experience that is simple, safe and above all, smoooth',
                'values': ['customer obsession', 'ownership', 'think big', 'raise the bar'],
                'talking_points': ['fintech innovation', 'payment solutions', 'user experience', 'financial inclusion'],
                'tech_focus': ['financial systems', 'security', 'scalability', 'real-time processing']
            },
            'volvo': {
                'mission': 'creating a safer, more sustainable and convenient mobility future',
                'values': ['safety', 'sustainability', 'innovation', 'human-centric design'],
                'talking_points': ['automotive innovation', 'sustainability goals', 'safety technology', 'future mobility'],
                'tech_focus': ['embedded systems', 'iot', 'machine learning', 'autonomous driving']
            },
            'ericsson': {
                'mission': 'empowering connectivity and enabling the full value of connectivity',
                'values': ['perseverance', 'respect', 'professionalism'],
                'talking_points': ['5G technology', 'telecommunications innovation', 'global connectivity', 'network solutions'],
                'tech_focus': ['networking', 'telecommunications', 'cloud infrastructure', 'iot']
            }
        }
        
        # Cover letter templates by tone and style
        self.letter_templates = {
            'professional_formal': {
                'opening': "I am writing to express my strong interest in the {job_title} position at {company}.",
                'company_connection': "I have been following {company}'s work in {industry_area} and am particularly impressed by {specific_achievement}.",
                'value_proposition': "With {years_experience} years of experience in {relevant_field}, I am confident I can contribute significantly to your team.",
                'closing': "I would welcome the opportunity to discuss how my experience and passion for {relevant_area} can benefit {company}."
            },
            'professional_enthusiastic': {
                'opening': "I am excited to apply for the {job_title} position at {company}, where I can combine my passion for {relevant_technology} with my {years_experience} years of software development experience.",
                'company_connection': "{company}'s commitment to {company_value} strongly resonates with my professional values and career aspirations.",
                'value_proposition': "My experience in {key_technologies} and proven track record of {key_achievement} make me an ideal candidate for this role.",
                'closing': "I am eager to contribute to {company}'s continued success and would love to discuss how I can add value to your team."
            },
            'technical_focused': {
                'opening': "As a {current_position} with extensive experience in {key_technologies}, I am thrilled to apply for the {job_title} position at {company}.",
                'company_connection': "I am particularly drawn to {company}'s innovative approach to {technical_area} and the opportunity to work with {specific_technologies}.",
                'value_proposition': "My hands-on experience with {matching_technologies} and successful delivery of {technical_achievement} directly align with your team's needs.",
                'closing': "I am excited about the possibility of contributing to {company}'s technical excellence and would appreciate the opportunity to discuss my qualifications further."
            }
        }

    async def create_personalized_cover_letter(self, job_data: Dict, job_requirements: JobRequirements) -> str:
        """
        Create a highly personalized cover letter based on job analysis
        """
        try:
            logger.info(f"✍️ Creating personalized cover letter for {job_data['company']} - {job_data['title']}")
            
            # Analyze company and determine approach
            company_analysis = self._analyze_company(job_data)
            
            # Select appropriate tone and template
            letter_style = self._determine_letter_style(job_requirements, company_analysis)
            
            # Research and gather talking points
            talking_points = await self._research_talking_points(job_data, job_requirements, company_analysis)
            
            # Generate personalized content sections
            letter_sections = await self._generate_letter_sections(job_data, job_requirements, talking_points, letter_style)
            
            # Assemble and polish with AI
            final_letter = await self._generate_final_letter_with_ai(job_data, letter_sections, job_requirements)
            
            logger.info(f"✅ Successfully created personalized cover letter for {job_data['company']}")
            return final_letter
            
        except Exception as e:
            logger.error(f"❌ Error creating cover letter: {e}")
            return await self._generate_fallback_cover_letter(job_data)

    def _analyze_company(self, job_data: Dict) -> Dict:
        """
        Analyze company information and determine approach
        """
        company_name = job_data['company'].lower()
        
        # Check if we have specific company insights
        for company_key, insights in self.company_insights.items():
            if company_key in company_name:
                return {
                    'known_company': True,
                    'company_data': insights,
                    'industry': self._determine_industry(company_name),
                    'size': self._estimate_company_size(company_name),
                    'culture': self._assess_company_culture(job_data, insights)
                }
        
        # Generic analysis for unknown companies
        return {
            'known_company': False,
            'industry': self._determine_industry(company_name),
            'size': self._estimate_company_size(company_name),
            'culture': self._assess_company_culture(job_data, {}),
            'talking_points': self._generate_generic_talking_points(job_data)
        }

    def _determine_industry(self, company_name: str) -> str:
        """Determine industry based on company name and context"""
        industry_keywords = {
            'fintech': ['klarna', 'payment', 'bank', 'financial'],
            'music_streaming': ['spotify', 'music', 'streaming'],
            'automotive': ['volvo', 'car', 'automotive', 'vehicle'],
            'telecom': ['ericsson', 'telecom', 'network', '5g'],
            'tech': ['technology', 'software', 'digital', 'tech'],
            'consulting': ['consulting', 'advisory', 'solutions']
        }
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in company_name for keyword in keywords):
                return industry
        
        return 'technology'

    def _estimate_company_size(self, company_name: str) -> str:
        """Estimate company size based on name recognition"""
        large_companies = ['spotify', 'klarna', 'volvo', 'ericsson', 'microsoft', 'google', 'amazon']
        
        if any(company in company_name for company in large_companies):
            return 'large'
        elif 'startup' in company_name or 'growing' in company_name:
            return 'startup'
        else:
            return 'medium'

    def _assess_company_culture(self, job_data: Dict, company_insights: Dict) -> Dict:
        """Assess company culture from job posting and known insights"""
        job_text = f"{job_data.get('description', '')} {job_data.get('company_info', '')}".lower()
        
        culture_indicators = {
            'innovative': ['innovative', 'cutting-edge', 'modern', 'latest technology'],
            'collaborative': ['team', 'collaborate', 'together', 'partnership'],
            'fast_paced': ['fast-paced', 'dynamic', 'agile', 'rapid growth'],
            'learning_focused': ['learning', 'growth', 'development', 'mentoring'],
            'user_centric': ['user experience', 'customer', 'user-focused', 'customer-centric'],
            'quality_focused': ['quality', 'excellence', 'best practices', 'high standards']
        }
        
        detected_culture = []
        for trait, indicators in culture_indicators.items():
            if any(indicator in job_text for indicator in indicators):
                detected_culture.append(trait)
        
        # Add known company values if available
        if company_insights and 'values' in company_insights:
            detected_culture.extend(company_insights['values'])
        
        return {
            'traits': detected_culture,
            'formality': 'formal' if 'corporate' in job_text else 'professional',
            'innovation_focus': 'innovative' in detected_culture or 'cutting-edge' in job_text
        }

    def _determine_letter_style(self, requirements: JobRequirements, company_analysis: Dict) -> str:
        """Determine appropriate letter style and tone"""
        
        # Technical roles at tech companies
        if (any(tech in requirements.technical_skills for tech in ['microservices', 'architecture', 'cloud']) and
            company_analysis['industry'] in ['tech', 'fintech', 'music_streaming']):
            return 'technical_focused'
        
        # Startup or fast-paced environments
        if (company_analysis['size'] == 'startup' or 
            'fast_paced' in company_analysis['culture'].get('traits', [])):
            return 'professional_enthusiastic'
        
        # Large corporate environments
        if company_analysis['size'] == 'large':
            return 'professional_formal'
        
        # Default
        return 'professional_enthusiastic'

    async def _research_talking_points(self, job_data: Dict, requirements: JobRequirements, company_analysis: Dict) -> Dict:
        """
        Research and prepare personalized talking points
        """
        talking_points = {
            'company_specific': [],
            'technical_alignment': [],
            'value_propositions': [],
            'shared_values': [],
            'growth_opportunities': []
        }
        
        # Company-specific talking points
        if company_analysis['known_company']:
            company_data = company_analysis['company_data']
            talking_points['company_specific'] = company_data.get('talking_points', [])
            talking_points['shared_values'] = company_data.get('values', [])
        else:
            talking_points['company_specific'] = company_analysis.get('talking_points', [])
        
        # Technical alignment
        user_skills = set(['java', 'javascript', 'python', 'react', 'spring boot', 'aws', 'docker', 'kubernetes'])
        required_skills = set(skill.lower() for skill in requirements.technical_skills + requirements.programming_languages)
        
        matching_skills = user_skills.intersection(required_skills)
        talking_points['technical_alignment'] = list(matching_skills)[:5]
        
        # Value propositions based on achievements
        talking_points['value_propositions'] = self._select_relevant_achievements(requirements)
        
        # Growth opportunities
        talking_points['growth_opportunities'] = self._identify_growth_opportunities(requirements, company_analysis)
        
        return talking_points

    def _select_relevant_achievements(self, requirements: JobRequirements) -> List[str]:
        """Select most relevant achievements for this job"""
        achievements = self.user_profile['signature_achievements']
        scored_achievements = []
        
        for achievement in achievements:
            score = 0
            achievement_lower = achievement.lower()
            
            # Score based on technical relevance
            for skill in requirements.technical_skills:
                if skill.lower() in achievement_lower:
                    score += 2
            
            # Score based on responsibility match
            for responsibility in requirements.job_responsibilities:
                if any(word in achievement_lower for word in responsibility.lower().split()):
                    score += 1
            
            # Score based on seniority level
            if requirements.seniority_level in ['senior', 'lead'] and 'led' in achievement_lower:
                score += 2
            
            scored_achievements.append((achievement, score))
        
        # Return top 2-3 most relevant achievements
        scored_achievements.sort(key=lambda x: x[1], reverse=True)
        return [achievement for achievement, score in scored_achievements[:3]]

    def _identify_growth_opportunities(self, requirements: JobRequirements, company_analysis: Dict) -> List[str]:
        """Identify growth opportunities to mention"""
        opportunities = []
        
        # Technical growth
        new_technologies = set(requirements.technical_skills) - set(['java', 'javascript', 'python'])
        if new_technologies:
            opportunities.append(f"expanding expertise in {', '.join(list(new_technologies)[:2])}")
        
        # Leadership growth
        if requirements.seniority_level in ['senior', 'lead']:
            opportunities.append("taking on greater technical leadership responsibilities")
        
        # Industry-specific growth
        industry = company_analysis['industry']
        if industry == 'fintech':
            opportunities.append("deepening knowledge of financial technology and payment systems")
        elif industry == 'automotive':
            opportunities.append("contributing to automotive innovation and connected vehicle technology")
        elif industry == 'music_streaming':
            opportunities.append("working on large-scale systems that impact millions of music lovers")
        
        return opportunities[:2]

    async def _generate_letter_sections(self, job_data: Dict, requirements: JobRequirements, talking_points: Dict, style: str) -> Dict:
        """
        Generate each section of the cover letter
        """
        template = self.letter_templates[style]
        
        sections = {
            'opening': self._generate_opening(job_data, template),
            'company_connection': self._generate_company_connection(job_data, talking_points, template),
            'value_proposition': self._generate_value_proposition(job_data, requirements, talking_points, template),
            'technical_fit': self._generate_technical_fit(requirements, talking_points),
            'growth_motivation': self._generate_growth_motivation(job_data, talking_points),
            'closing': self._generate_closing(job_data, template)
        }
        
        return sections

    def _generate_opening(self, job_data: Dict, template: Dict) -> str:
        """Generate personalized opening paragraph"""
        return template['opening'].format(
            job_title=job_data['title'],
            company=job_data['company'],
            relevant_technology=self._extract_key_technology(job_data),
            years_experience=self.user_profile['years_experience']
        )

    def _extract_key_technology(self, job_data: Dict) -> str:
        """Extract the most relevant technology mentioned in job"""
        job_text = f"{job_data.get('title', '')} {job_data.get('description', '')}".lower()
        
        key_technologies = ['java', 'javascript', 'python', 'react', 'spring boot', 'microservices', 'cloud', 'aws']
        
        for tech in key_technologies:
            if tech in job_text:
                return tech
        
        return 'software development'

    def _generate_company_connection(self, job_data: Dict, talking_points: Dict, template: Dict) -> str:
        """Generate company connection paragraph"""
        company_specific = talking_points.get('company_specific', [])
        shared_values = talking_points.get('shared_values', [])
        
        if company_specific:
            industry_area = company_specific[0] if company_specific else 'technology'
            specific_achievement = company_specific[1] if len(company_specific) > 1 else 'innovative solutions'
        else:
            industry_area = 'technology and innovation'
            specific_achievement = 'commitment to excellence'
        
        return template['company_connection'].format(
            company=job_data['company'],
            industry_area=industry_area,
            specific_achievement=specific_achievement,
            company_value=shared_values[0] if shared_values else 'innovation'
        )

    def _generate_value_proposition(self, job_data: Dict, requirements: JobRequirements, talking_points: Dict, template: Dict) -> str:
        """Generate value proposition paragraph"""
        technical_alignment = talking_points.get('technical_alignment', [])
        value_propositions = talking_points.get('value_propositions', [])
        
        key_technologies = ', '.join(technical_alignment[:3]) if technical_alignment else 'modern web technologies'
        key_achievement = value_propositions[0] if value_propositions else 'delivering high-quality software solutions'
        
        return template['value_proposition'].format(
            years_experience=self.user_profile['years_experience'],
            relevant_field='software development',
            key_technologies=key_technologies,
            key_achievement=key_achievement,
            matching_technologies=key_technologies
        )

    def _generate_technical_fit(self, requirements: JobRequirements, talking_points: Dict) -> str:
        """Generate technical fit paragraph"""
        technical_skills = talking_points.get('technical_alignment', [])
        
        if not technical_skills:
            return "My comprehensive technical background aligns well with your requirements."
        
        skills_text = ', '.join(technical_skills[:4])
        
        return f"My hands-on experience with {skills_text} directly matches your technical requirements. " \
               f"I have successfully applied these technologies in production environments, " \
               f"delivering scalable solutions that serve thousands of users daily."

    def _generate_growth_motivation(self, job_data: Dict, talking_points: Dict) -> str:
        """Generate growth and motivation paragraph"""
        growth_opportunities = talking_points.get('growth_opportunities', [])
        
        if growth_opportunities:
            opportunities_text = ' and '.join(growth_opportunities)
            return f"I am particularly excited about the opportunity for {opportunities_text} at {job_data['company']}. " \
                   f"This role represents the perfect next step in my career journey."
        
        return f"I am excited about the opportunity to contribute to {job_data['company']}'s continued success " \
               f"while growing my technical and leadership skills in a challenging environment."

    def _generate_closing(self, job_data: Dict, template: Dict) -> str:
        """Generate closing paragraph"""
        return template['closing'].format(
            company=job_data['company'],
            relevant_area=self._extract_key_technology(job_data),
            technical_area='software development'
        )

    async def _generate_final_letter_with_ai(self, job_data: Dict, sections: Dict, requirements: JobRequirements) -> str:
        """
        Use Claude AI to polish and finalize the cover letter
        """
        try:
            prompt = f"""
            Create a professional, compelling cover letter for this job application:
            
            JOB DETAILS:
            - Position: {job_data['title']}
            - Company: {job_data['company']}
            - Location: {job_data.get('location', 'Sweden')}
            
            APPLICANT DETAILS:
            - Name: {self.user_profile['name']}
            - Current Position: {self.user_profile['current_position']}
            - Experience: {self.user_profile['years_experience']} years
            - Location: {self.user_profile['location']}
            
            KEY REQUIREMENTS TO ADDRESS:
            - Technical Skills: {', '.join(requirements.technical_skills[:5])}
            - Programming Languages: {', '.join(requirements.programming_languages)}
            - Seniority Level: {requirements.seniority_level}
            - Key Responsibilities: {', '.join(requirements.job_responsibilities[:3])}
            
            DRAFT LETTER SECTIONS:
            
            Opening: {sections['opening']}
            
            Company Connection: {sections['company_connection']}
            
            Value Proposition: {sections['value_proposition']}
            
            Technical Fit: {sections['technical_fit']}
            
            Growth Motivation: {sections['growth_motivation']}
            
            Closing: {sections['closing']}
            
            Please create a polished, professional cover letter in LaTeX format that:
            1. Flows naturally and tells a compelling story
            2. Demonstrates genuine interest in the company and role
            3. Highlights relevant technical skills and experience
            4. Shows personality while maintaining professionalism
            5. Includes proper formatting with recipient address placeholder
            6. Uses modern business letter format
            7. Is concise but comprehensive (fits on one page)
            8. Integrates job-relevant keywords naturally
            9. Ends with a strong call to action
            
            Include contact information and professional formatting.
            Return only the complete LaTeX code ready for compilation.
            """
            
            cover_letter = await self.claude_service._make_claude_request(prompt)
            
            if cover_letter and len(cover_letter) > 500:
                return cover_letter
            else:
                logger.warning("AI-generated cover letter too short, using fallback")
                return await self._generate_fallback_cover_letter(job_data)
                
        except Exception as e:
            logger.error(f"Error generating final cover letter with AI: {e}")
            return await self._generate_fallback_cover_letter(job_data)

    async def _generate_fallback_cover_letter(self, job_data: Dict) -> str:
        """Generate fallback cover letter if AI generation fails"""
        current_date = datetime.now().strftime("%B %d, %Y")
        
        return f"""
\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{parskip}}

\\begin{{document}}

\\begin{{flushleft}}
{self.user_profile['name']}\\\\
{self.user_profile['location']}\\\\
Email: hongzhili01@gmail.com\\\\
Phone: +46 76 123 4567\\\\
\\end{{flushleft}}

\\vspace{{1cm}}

{current_date}

\\vspace{{0.5cm}}

Hiring Manager\\\\
{job_data['company']}\\\\
{job_data.get('location', 'Sweden')}

\\vspace{{0.5cm}}

Dear Hiring Manager,

I am writing to express my strong interest in the {job_data['title']} position at {job_data['company']}. With {self.user_profile['years_experience']} years of experience as a {self.user_profile['current_position']}, I am excited about the opportunity to contribute to your team's success.

My technical expertise includes comprehensive experience with modern software development technologies and frameworks. I have successfully delivered scalable applications, implemented CI/CD pipelines, and mentored development teams. My track record of {self.user_profile['signature_achievements'][0].lower()} demonstrates my ability to drive technical excellence and business results.

I am particularly drawn to {job_data['company']}'s innovative approach to technology and commitment to quality. The {job_data['title']} role represents an exciting opportunity to apply my skills in {self._extract_key_technology(job_data)} while contributing to meaningful projects that impact users globally.

I would welcome the opportunity to discuss how my experience and passion for software development can benefit {job_data['company']}. I am {self.user_profile['availability'].lower()} and look forward to hearing from you.

Sincerely,

{self.user_profile['name']}

\\end{{document}}
        """

    async def batch_create_cover_letters(self, analyzed_jobs: List[Dict]) -> List[Dict]:
        """
        Create personalized cover letters for multiple jobs in parallel
        """
        try:
            logger.info(f"✍️ Creating personalized cover letters for {len(analyzed_jobs)} jobs")
            
            # Create cover letter generation tasks
            cl_tasks = []
            for job_analysis in analyzed_jobs:
                job_data = job_analysis['job_data']
                requirements = job_analysis['requirements']
                
                task = self.create_personalized_cover_letter(job_data, requirements)
                cl_tasks.append((job_data, task))
            
            # Execute with controlled concurrency
            semaphore = asyncio.Semaphore(2)  # Limit concurrent generations
            
            async def bounded_cl_generation(job_data, task):
                async with semaphore:
                    cl_latex = await task
                    return {
                        'job_data': job_data,
                        'cover_letter_latex': cl_latex,
                        'generated_at': datetime.now().isoformat()
                    }
            
            bounded_tasks = [
                bounded_cl_generation(job_data, task) 
                for job_data, task in cl_tasks
            ]
            
            results = await asyncio.gather(*bounded_tasks, return_exceptions=True)
            
            # Filter successful results
            successful_cls = [
                result for result in results 
                if not isinstance(result, Exception)
            ]
            
            logger.info(f"✅ Successfully created {len(successful_cls)} personalized cover letters")
            return successful_cls
            
        except Exception as e:
            logger.error(f"❌ Error in batch cover letter creation: {e}")
            return []

    def get_cover_letter_insights(self, job_data: Dict, requirements: JobRequirements) -> Dict:
        """
        Get insights about cover letter customization for reporting
        """
        company_analysis = self._analyze_company(job_data)
        
        return {
            'job_title': job_data['title'],
            'company': job_data['company'],
            'letter_style': self._determine_letter_style(requirements, company_analysis),
            'company_insights_used': company_analysis['known_company'],
            'industry': company_analysis['industry'],
            'key_talking_points': company_analysis.get('company_data', {}).get('talking_points', [])[:3],
            'technical_alignment_count': len(requirements.technical_skills),
            'personalization_level': 'high' if company_analysis['known_company'] else 'medium',
            'generated_at': datetime.now().isoformat()
        }