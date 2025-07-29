#!/usr/bin/env python3
"""
Enhanced CV/CL Optimizer Service
Provides intelligent document customization with ATS optimization and quality scoring
"""
import asyncio
import json
import re
import logging
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime
from dataclasses import dataclass
from collections import Counter
import hashlib
import tempfile
import subprocess
import os

logger = logging.getLogger(__name__)

@dataclass
class ATSScore:
    """ATS compatibility score breakdown"""
    overall_score: float  # 0-100
    keyword_match: float  # 0-100
    format_score: float   # 0-100
    length_score: float   # 0-100
    structure_score: float # 0-100
    recommendations: List[str]

@dataclass
class DocumentTemplate:
    """Reusable document template with versioning"""
    template_id: str
    template_type: str  # 'cv' or 'cover_letter'
    content: str
    last_modified: datetime
    usage_count: int
    ats_keywords: List[str]
    success_rate: float

class EnhancedCVOptimizer:
    """Enhanced CV and Cover Letter optimization service with ATS scoring"""
    
    def __init__(self):
        self.templates_cache = {}
        self.keyword_database = self._initialize_keyword_database()
        self.ats_weights = {
            'keyword_match': 0.4,
            'format_score': 0.2,
            'length_score': 0.2,
            'structure_score': 0.2
        }
        
    def _initialize_keyword_database(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize comprehensive keyword database for different roles"""
        return {
            'software_engineer': {
                'primary': ['python', 'java', 'javascript', 'react', 'angular', 'spring', 'django', 'flask'],
                'secondary': ['git', 'docker', 'kubernetes', 'aws', 'azure', 'postgresql', 'mongodb'],
                'soft_skills': ['agile', 'scrum', 'teamwork', 'problem-solving', 'communication']
            },
            'devops_engineer': {
                'primary': ['kubernetes', 'docker', 'aws', 'azure', 'terraform', 'ansible', 'jenkins'],
                'secondary': ['python', 'bash', 'linux', 'monitoring', 'grafana', 'prometheus'],
                'soft_skills': ['automation', 'ci/cd', 'infrastructure', 'scalability', 'reliability']
            },
            'fullstack_developer': {
                'primary': ['react', 'node.js', 'javascript', 'typescript', 'python', 'java', 'spring boot'],
                'secondary': ['postgresql', 'mongodb', 'redis', 'docker', 'aws', 'rest api'],
                'soft_skills': ['full-stack', 'responsive design', 'user experience', 'api development']
            },
            'backend_developer': {
                'primary': ['java', 'spring boot', 'python', 'django', 'flask', 'node.js', 'c#', '.net'],
                'secondary': ['postgresql', 'mysql', 'mongodb', 'redis', 'microservices', 'kafka'],
                'soft_skills': ['scalability', 'performance', 'api design', 'database optimization']
            },
            'cloud_engineer': {
                'primary': ['aws', 'azure', 'gcp', 'terraform', 'cloudformation', 'kubernetes'],
                'secondary': ['docker', 'monitoring', 'security', 'networking', 'storage'],
                'soft_skills': ['cloud architecture', 'cost optimization', 'disaster recovery']
            }
        }
    
    def analyze_job_role(self, job_title: str, job_description: str) -> str:
        """Analyze job posting to determine primary role category"""
        title_lower = job_title.lower()
        desc_lower = job_description.lower()
        combined_text = f"{title_lower} {desc_lower}"
        
        role_scores = {}
        for role, keywords in self.keyword_database.items():
            score = 0
            all_keywords = keywords['primary'] + keywords['secondary'] + keywords['soft_skills']
            
            for keyword in all_keywords:
                if keyword in combined_text:
                    # Primary keywords get higher weight
                    if keyword in keywords['primary']:
                        score += 3
                    elif keyword in keywords['secondary']:
                        score += 2
                    else:
                        score += 1
            
            role_scores[role] = score
        
        # Return the role with highest score
        best_role = max(role_scores, key=role_scores.get)
        logger.info(f"Identified job role: {best_role} (score: {role_scores[best_role]})")
        return best_role
    
    def calculate_ats_score(self, document_content: str, job_description: str, 
                           job_title: str, document_type: str = 'cv') -> ATSScore:
        """Calculate comprehensive ATS compatibility score"""
        
        recommendations = []
        
        # 1. Keyword Match Score (40% weight)
        keyword_score = self._calculate_keyword_match(document_content, job_description, job_title)
        if keyword_score < 70:
            recommendations.append("Increase keyword density - add more relevant technical terms from job description")
        
        # 2. Format Score (20% weight)
        format_score = self._calculate_format_score(document_content, document_type)
        if format_score < 80:
            recommendations.append("Improve document structure - use clear headings and bullet points")
        
        # 3. Length Score (20% weight)
        length_score = self._calculate_length_score(document_content, document_type)
        if length_score < 80:
            recommendations.append(f"Optimize document length for {document_type}")
        
        # 4. Structure Score (20% weight)
        structure_score = self._calculate_structure_score(document_content, document_type)
        if structure_score < 80:
            recommendations.append("Enhance document structure with proper sections and formatting")
        
        # Calculate overall score
        overall_score = (
            keyword_score * self.ats_weights['keyword_match'] +
            format_score * self.ats_weights['format_score'] +
            length_score * self.ats_weights['length_score'] +
            structure_score * self.ats_weights['structure_score']
        )
        
        return ATSScore(
            overall_score=round(overall_score, 1),
            keyword_match=round(keyword_score, 1),
            format_score=round(format_score, 1),
            length_score=round(length_score, 1),
            structure_score=round(structure_score, 1),
            recommendations=recommendations
        )
    
    def _calculate_keyword_match(self, document: str, job_description: str, job_title: str) -> float:
        """Calculate keyword matching score"""
        doc_lower = document.lower()
        job_lower = f"{job_title} {job_description}".lower()
        
        # Extract key terms from job description
        job_keywords = self._extract_job_keywords(job_lower)
        
        # Count matches in document
        matches = 0
        total_keywords = len(job_keywords)
        
        for keyword in job_keywords:
            if keyword in doc_lower:
                matches += 1
        
        # Calculate percentage with bonus for critical keywords
        base_score = (matches / total_keywords) * 100 if total_keywords > 0 else 0
        
        # Bonus for role-specific keywords
        role = self.analyze_job_role(job_title, job_description)
        role_keywords = self.keyword_database.get(role, {}).get('primary', [])
        
        role_matches = sum(1 for keyword in role_keywords if keyword in doc_lower)
        role_bonus = (role_matches / len(role_keywords)) * 20 if role_keywords else 0
        
        return min(100, base_score + role_bonus)
    
    def _extract_job_keywords(self, job_text: str) -> List[str]:
        """Extract relevant keywords from job description"""
        # Common technical terms and skills
        tech_patterns = [
            r'\b(java|python|javascript|typescript|c#|\.net|php|ruby|go|rust)\b',
            r'\b(react|angular|vue|svelte|next\.js|nuxt\.js)\b',
            r'\b(spring|django|flask|express|laravel|rails)\b',
            r'\b(aws|azure|gcp|cloud|kubernetes|docker)\b',
            r'\b(postgresql|mysql|mongodb|redis|elasticsearch)\b',
            r'\b(git|jenkins|ci/cd|devops|agile|scrum)\b',
            r'\b(microservices|api|rest|graphql|websocket)\b'
        ]
        
        keywords = []
        for pattern in tech_patterns:
            matches = re.findall(pattern, job_text, re.IGNORECASE)
            keywords.extend([match.lower() for match in matches])
        
        # Remove duplicates and return top keywords  
        return list(set(keywords))[:20]
    
    def _calculate_format_score(self, document: str, doc_type: str) -> float:
        """Calculate format and structure score"""
        score = 0
        
        # Check for proper sections
        sections = ['experience', 'skills', 'education', 'summary', 'profile']
        if doc_type == 'cover_letter':
            sections = ['dear', 'sincerely', 'paragraph']
        
        doc_lower = document.lower()
        section_count = sum(1 for section in sections if section in doc_lower)
        
        # Base score from sections
        score += (section_count / len(sections)) * 50
        
        # Check for bullet points
        if '•' in document or '\\item' in document:
            score += 20
        
        # Check for proper formatting indicators
        if '\\textbf' in document or '**' in document:
            score += 15
        
        # Check for contact information
        if '@' in document and any(char.isdigit() for char in document):
            score += 15
        
        return min(100, score)
    
    def _calculate_length_score(self, document: str, doc_type: str) -> float:
        """Calculate optimal length score"""
        word_count = len(document.split())
        
        if doc_type == 'cv':
            # Optimal CV length: 300-800 words
            if 300 <= word_count <= 800:
                return 100
            elif 200 <= word_count < 300 or 800 < word_count <= 1000:
                return 80
            elif 100 <= word_count < 200 or 1000 < word_count <= 1200:
                return 60
            else:
                return 40
        else:  # cover_letter
            # Optimal cover letter: 150-400 words
            if 150 <= word_count <= 400:
                return 100
            elif 100 <= word_count < 150 or 400 < word_count <= 500:
                return 80
            else:
                return 60
    
    def _calculate_structure_score(self, document: str, doc_type: str) -> float:
        """Calculate document structure quality"""
        score = 0.0
        
        # Check for clear hierarchy
        if '\\section' in document or '#' in document:
            score += 25
        
        # Check for consistent formatting
        if '\\textbf' in document or '**' in document:
            score += 25
        
        # Check for proper spacing and organization
        lines = document.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        if len(non_empty_lines) > 10:  # Well-structured document
            score += 25
        
        # Check for contact information placement
        first_few_lines = '\n'.join(lines[:5]).lower()
        if '@' in first_few_lines:
            score += 25
        
        return score
    
    def generate_template_id(self, job_title: str, company: str, role_type: str) -> str:
        """Generate unique template ID for caching"""
        content = f"{job_title}_{company}_{role_type}_{datetime.now().date()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    async def optimize_cv_incrementally(self, base_cv: str, job_data: Dict, 
                                      previous_score: Optional[ATSScore] = None) -> Tuple[str, ATSScore]:
        """Optimize CV with incremental improvements rather than full regeneration"""
        
        job_title = job_data.get('title', '')
        job_description = job_data.get('description', '')
        company = job_data.get('company', '')
        
        logger.info(f"Starting incremental CV optimization for {job_title} at {company}")
        
        # Analyze job requirements
        role_type = self.analyze_job_role(job_title, job_description)
        target_keywords = self._get_target_keywords(role_type, job_description)
        
        # Get current ATS score
        current_score = self.calculate_ats_score(base_cv, job_description, job_title, 'cv')
        
        # If score is already high, minimal changes needed
        if current_score.overall_score >= 85:
            logger.info(f"CV already optimized (score: {current_score.overall_score})")
            return await self._apply_minimal_customization(base_cv, job_data, target_keywords), current_score
        
        # Apply targeted improvements
        optimized_cv = base_cv
        
        # 1. Optimize profile summary
        if current_score.keyword_match < 70:
            optimized_cv = self._enhance_profile_summary(optimized_cv, job_data, target_keywords)
        
        # 2. Reorder skills based on job relevance
        optimized_cv = self._reorder_skills_section(optimized_cv, target_keywords)
        
        # 3. Highlight relevant experience
        optimized_cv = self._emphasize_relevant_experience(optimized_cv, job_data, target_keywords)
        
        # 4. Add missing keywords strategically
        optimized_cv = self._inject_strategic_keywords(optimized_cv, target_keywords, job_description)
        
        # Calculate new score
        new_score = self.calculate_ats_score(optimized_cv, job_description, job_title, 'cv')
        
        logger.info(f"CV optimization complete. Score improved: {current_score.overall_score} → {new_score.overall_score}")
        
        return optimized_cv, new_score
    
    def _get_target_keywords(self, role_type: str, job_description: str) -> List[str]:
        """Get target keywords for optimization"""
        role_keywords = self.keyword_database.get(role_type, {})
        base_keywords = (role_keywords.get('primary', []) + 
                        role_keywords.get('secondary', []))
        
        # Add job-specific keywords
        job_keywords = self._extract_job_keywords(job_description)
        
        # Combine and prioritize
        all_keywords = list(set(base_keywords + job_keywords))
        return all_keywords[:15]  # Top 15 most relevant
    
    def _enhance_profile_summary(self, cv_content: str, job_data: Dict, keywords: List[str]) -> str:
        """Enhance profile summary with job-relevant keywords"""
        # Find profile summary section
        lines = cv_content.split('\n')
        summary_start = -1
        summary_end = -1
        
        for i, line in enumerate(lines):
            if 'profile' in line.lower() or 'summary' in line.lower():
                summary_start = i
            elif summary_start != -1 and line.strip().startswith('\\section') and i > summary_start:
                summary_end = i
                break
        
        if summary_start == -1:
            return cv_content
        
        if summary_end == -1:
            summary_end = len(lines)
        
        # Extract current summary
        current_summary = '\n'.join(lines[summary_start:summary_end])
        
        # Enhance with keywords
        enhanced_summary = self._inject_keywords_naturally(current_summary, keywords[:5])
        
        # Replace in CV
        lines[summary_start:summary_end] = enhanced_summary.split('\n')
        return '\n'.join(lines)
    
    def _reorder_skills_section(self, cv_content: str, keywords: List[str]) -> str:
        """Reorder skills to prioritize job-relevant ones"""
        # This is a simplified implementation
        # In practice, you'd parse the skills section and reorder based on keyword relevance
        return cv_content
    
    def _emphasize_relevant_experience(self, cv_content: str, job_data: Dict, keywords: List[str]) -> str:
        """Emphasize experience items that match job requirements"""
        # Add emphasis markers to relevant experience bullets
        for keyword in keywords:
            pattern = rf'(\\item.*{re.escape(keyword)}.*)'
            replacement = r'\\item \\textbf{\1}'
            cv_content = re.sub(pattern, replacement, cv_content, flags=re.IGNORECASE)
        
        return cv_content
    
    def _inject_strategic_keywords(self, cv_content: str, keywords: List[str], job_description: str) -> str:
        """Strategically inject missing keywords"""
        cv_lower = cv_content.lower()
        missing_keywords = [kw for kw in keywords if kw not in cv_lower]
        
        if not missing_keywords:
            return cv_content
        
        # Find a good place to inject keywords (usually in skills section)
        skills_section_pattern = r'(\\section\*?\{.*?[Ss]kills.*?\}.*?)(\\section|\Z)'
        match = re.search(skills_section_pattern, cv_content, re.DOTALL)
        
        if match:
            skills_content = match.group(1)
            # Add missing keywords to skills section
            additional_skills = f"\\item \\textbf{{Additional Technologies:}} {', '.join(missing_keywords[:3])}\n"
            enhanced_skills = skills_content + additional_skills
            cv_content = cv_content.replace(skills_content, enhanced_skills)
        
        return cv_content
    
    def _inject_keywords_naturally(self, text: str, keywords: List[str]) -> str:
        """Inject keywords naturally into text"""
        # Simple implementation - would use NLP for better results
        for keyword in keywords:
            if keyword not in text.lower():
                # Find a suitable place to inject the keyword
                sentences = text.split('.')
                if len(sentences) > 1:
                    # Inject into first sentence if possible
                    first_sentence = sentences[0]
                    if 'experience' in first_sentence.lower():
                        first_sentence += f" specializing in {keyword}"
                        sentences[0] = first_sentence
                        text = '.'.join(sentences)
                        break
        
        return text
    
    async def _apply_minimal_customization(self, cv_content: str, job_data: Dict, keywords: List[str]) -> str:
        """Apply minimal customization for already good CVs"""
        # Just customize the job title in header and add company name context
        job_title = job_data.get('title', 'Software Developer')
        company = job_data.get('company', '')
        
        # Update job role in header
        role_pattern = r'(\\Large \\textit\{)([^}]+)(\})'
        cv_content = re.sub(role_pattern, rf'\1{job_title}\3', cv_content)
        
        return cv_content
    
    async def optimize_cover_letter_incrementally(self, base_cl: str, job_data: Dict) -> Tuple[str, ATSScore]:
        """Optimize cover letter with incremental improvements"""
        
        job_title = job_data.get('title', '')
        job_description = job_data.get('description', '')
        company = job_data.get('company', '')
        
        logger.info(f"Starting incremental cover letter optimization for {job_title} at {company}")
        
        # Get current score
        current_score = self.calculate_ats_score(base_cl, job_description, job_title, 'cover_letter')
        
        # Apply customizations
        optimized_cl = base_cl
        
        # 1. Customize company and role references
        optimized_cl = optimized_cl.replace('{company}', company)
        optimized_cl = optimized_cl.replace('{job_title}', job_title)
        optimized_cl = optimized_cl.replace('{company_name}', company)
        
        # 2. Add job-specific keywords
        role_type = self.analyze_job_role(job_title, job_description)
        keywords = self._get_target_keywords(role_type, job_description)
        
        # 3. Enhance with specific achievements relevant to job
        optimized_cl = self._add_relevant_achievements(optimized_cl, job_data, keywords)
        
        # Calculate new score
        new_score = self.calculate_ats_score(optimized_cl, job_description, job_title, 'cover_letter')
        
        logger.info(f"Cover letter optimization complete. Score: {current_score.overall_score} → {new_score.overall_score}")
        
        return optimized_cl, new_score
    
    def _add_relevant_achievements(self, cover_letter: str, job_data: Dict, keywords: List[str]) -> str:
        """Add relevant achievements and soft skills based on job requirements"""
        paragraphs = cover_letter.split('\n\n')
        
        if len(paragraphs) >= 2:
            # Enhance paragraphs with achievements and soft skills
            main_paragraph = paragraphs[1]
            soft_skills_paragraph = "\n\nAs a lifelong learner passionate about technology, I consistently stay ahead of industry trends, particularly in AI and emerging technologies. My experience as a team leader has enabled me to effectively bridge communication gaps between Chinese and international teams, fostering collaboration across geographical, temporal, and cultural boundaries. Through my various hobby projects and continuous learning initiatives, I demonstrate both technical expertise and adaptability.\n\n"
            
            # Add technical achievement based on keywords
            if 'kubernetes' in keywords or 'devops' in keywords:
                achievement = " I successfully led infrastructure optimization projects at ECARX, implementing Kubernetes clusters and establishing robust CI/CD pipelines, resulting in improved deployment efficiency and system reliability."
            elif 'microservices' in keywords or 'spring boot' in keywords:
                achievement = " I architected and implemented scalable microservices solutions using Spring Boot, significantly improving system modularity and maintainability while reducing deployment complexities."
            elif 'cloud' in keywords:
                achievement = " I have demonstrated expertise in cloud platforms including AWS and Azure, successfully migrating and optimizing applications for cloud environments while ensuring cost-effectiveness and performance."
            else:
                achievement = " My extensive full-stack development experience includes delivering high-impact solutions using modern frameworks and best practices, consistently meeting both technical requirements and business objectives."
            
            main_paragraph += achievement
            paragraphs[1] = main_paragraph
            
            # Insert soft skills paragraph before the closing
            if len(paragraphs) > 2:
                paragraphs.insert(-1, soft_skills_paragraph)
            else:
                paragraphs.append(soft_skills_paragraph)
            
            cover_letter = '\n\n'.join(paragraphs)
        
        return cover_letter
    
    def generate_optimization_report(self, before_score: ATSScore, after_score: ATSScore, 
                                   job_title: str, company: str) -> Dict:
        """Generate comprehensive optimization report"""
        
        improvement = after_score.overall_score - before_score.overall_score
        
        return {
            'job_title': job_title,
            'company': company,
            'optimization_date': datetime.now().isoformat(),
            'scores': {
                'before': {
                    'overall': before_score.overall_score,
                    'keyword_match': before_score.keyword_match,
                    'format_score': before_score.format_score,
                    'length_score': before_score.length_score,
                    'structure_score': before_score.structure_score
                },
                'after': {
                    'overall': after_score.overall_score,
                    'keyword_match': after_score.keyword_match,
                    'format_score': after_score.format_score,
                    'length_score': after_score.length_score,
                    'structure_score': after_score.structure_score
                },
                'improvement': round(improvement, 1)
            },
            'recommendations_addressed': before_score.recommendations,
            'remaining_recommendations': after_score.recommendations,
            'success_indicators': {
                'ats_ready': after_score.overall_score >= 80,
                'keyword_optimized': after_score.keyword_match >= 70,
                'well_formatted': after_score.format_score >= 80
            }
        }
    
    async def batch_optimize_applications(self, jobs_data: List[Dict], 
                                        base_cv: str, base_cl: str) -> List[Dict]:
        """Optimize multiple applications efficiently"""
        
        results = []
        
        for job_data in jobs_data:
            try:
                # Optimize CV
                optimized_cv, cv_score = await self.optimize_cv_incrementally(base_cv, job_data)
                
                # Optimize Cover Letter
                optimized_cl, cl_score = await self.optimize_cover_letter_incrementally(base_cl, job_data)
                
                # Generate report
                report = {
                    'job': job_data,
                    'optimized_cv': optimized_cv,
                    'optimized_cover_letter': optimized_cl,
                    'cv_ats_score': cv_score,
                    'cl_ats_score': cl_score,
                    'optimization_success': cv_score.overall_score >= 80 and cl_score.overall_score >= 80,
                    'processing_time': datetime.now()
                }
                
                results.append(report)
                
                logger.info(f"Optimized application for {job_data.get('title')} at {job_data.get('company')} - CV: {cv_score.overall_score}, CL: {cl_score.overall_score}")
                
            except Exception as e:
                logger.error(f"Error optimizing application for {job_data.get('title', 'Unknown')}: {e}")
                results.append({
                    'job': job_data,
                    'error': str(e),
                    'optimization_success': False
                })
        
        return results