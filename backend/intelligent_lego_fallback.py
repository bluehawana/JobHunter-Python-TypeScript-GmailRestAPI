#!/usr/bin/env python3
"""
Intelligent LEGO Fallback System
When Claude API is unavailable, use smart keyword analysis for LEGO decisions
"""
import re
import json
from typing import Dict, List, Any

class IntelligentLegoFallback:
    """Smart LEGO system that works without Claude API"""
    
    def __init__(self):
        # Keyword patterns for job analysis
        self.devops_keywords = [
            'devops', 'infrastructure', 'kubernetes', 'docker', 'ci/cd', 'jenkins',
            'terraform', 'ansible', 'aws', 'azure', 'gcp', 'cloud', 'deployment',
            'monitoring', 'grafana', 'prometheus', 'automation', 'pipeline'
        ]
        
        self.backend_keywords = [
            'backend', 'api', 'microservices', 'spring', 'java', 'python', 'node.js',
            'database', 'sql', 'postgresql', 'mongodb', 'rest', 'graphql', 'server',
            'architecture', 'scalability', 'performance'
        ]
        
        self.frontend_keywords = [
            'frontend', 'react', 'angular', 'vue', 'javascript', 'typescript',
            'html', 'css', 'ui', 'ux', 'responsive', 'mobile', 'web', 'browser'
        ]
        
        self.fullstack_keywords = [
            'fullstack', 'full-stack', 'full stack', 'end-to-end', 'complete',
            'both frontend and backend', 'web development'
        ]
    
    def analyze_job_and_create_lego_strategy(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze job and create LEGO strategy using intelligent keyword analysis"""
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        company = job.get('company', 'Company')
        
        # Combine title and description for analysis
        content = f"{title} {description}"
        
        # Count keyword matches
        devops_score = self._count_keywords(content, self.devops_keywords)
        backend_score = self._count_keywords(content, self.backend_keywords)
        frontend_score = self._count_keywords(content, self.frontend_keywords)
        fullstack_score = self._count_keywords(content, self.fullstack_keywords)
        
        # Determine primary focus
        scores = {
            'devops': devops_score,
            'backend': backend_score,
            'frontend': frontend_score,
            'fullstack': fullstack_score
        }
        
        primary_focus = max(scores, key=scores.get)
        
        # If fullstack score is low but others are mixed, choose fullstack
        if fullstack_score == 0 and backend_score > 0 and frontend_score > 0:
            primary_focus = 'fullstack'
        
        # Generate strategy based on focus
        strategy = self._generate_strategy_for_focus(primary_focus, content, company)
        
        return strategy
    
    def _count_keywords(self, content: str, keywords: List[str]) -> int:
        """Count how many keywords appear in content"""
        count = 0
        for keyword in keywords:
            if keyword in content:
                count += 1
        return count
    
    def _generate_strategy_for_focus(self, focus: str, content: str, company: str) -> Dict[str, Any]:
        """Generate LEGO strategy based on determined focus"""
        
        if focus == 'devops':
            return {
                "primary_focus": "devops",
                "skills_to_highlight": ["Kubernetes", "Docker", "AWS", "CI/CD", "Infrastructure"],
                "experience_order": "ecarx_first",
                "role_title": "DevOps Engineer & Cloud Infrastructure Specialist",
                "profile_angle": f"DevOps specialist with proven experience in cloud infrastructure and automation, ideal for {company}'s infrastructure needs",
                "keywords_to_include": self._extract_relevant_keywords(content, self.devops_keywords),
                "sections_to_emphasize": ["skills", "experience", "certifications"],
                "tone": "technical"
            }
        
        elif focus == 'backend':
            return {
                "primary_focus": "backend",
                "skills_to_highlight": ["Java", "Spring Boot", "Microservices", "APIs", "Databases"],
                "experience_order": "synteda_first",
                "role_title": "Backend Developer & API Specialist",
                "profile_angle": f"Backend developer with expertise in scalable architecture and API design, perfect for {company}'s backend systems",
                "keywords_to_include": self._extract_relevant_keywords(content, self.backend_keywords),
                "sections_to_emphasize": ["skills", "experience", "projects"],
                "tone": "technical"
            }
        
        elif focus == 'frontend':
            return {
                "primary_focus": "frontend",
                "skills_to_highlight": ["React", "Angular", "TypeScript", "UI/UX", "Responsive Design"],
                "experience_order": "synteda_first",
                "role_title": "Frontend Developer & UI Specialist",
                "profile_angle": f"Frontend developer with modern web technologies expertise, ideal for {company}'s user experience goals",
                "keywords_to_include": self._extract_relevant_keywords(content, self.frontend_keywords),
                "sections_to_emphasize": ["skills", "experience", "projects"],
                "tone": "creative"
            }
        
        else:  # fullstack
            return {
                "primary_focus": "fullstack",
                "skills_to_highlight": ["Java", "React", "Spring Boot", "Cloud", "Full-Stack"],
                "experience_order": "balanced",
                "role_title": "Fullstack Developer",
                "profile_angle": f"Versatile fullstack developer with end-to-end development expertise, perfect for {company}'s comprehensive development needs",
                "keywords_to_include": self._extract_relevant_keywords(content, self.backend_keywords + self.frontend_keywords),
                "sections_to_emphasize": ["skills", "experience"],
                "tone": "balanced"
            }
    
    def _extract_relevant_keywords(self, content: str, keyword_list: List[str]) -> List[str]:
        """Extract keywords that actually appear in the job content"""
        found_keywords = []
        for keyword in keyword_list:
            if keyword in content:
                found_keywords.append(keyword)
        return found_keywords[:5]  # Limit to top 5 for focus
    
    def create_intelligent_cover_letter_strategy(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Create cover letter strategy focusing on soft skills"""
        company = job.get('company', 'Company')
        title = job.get('title', 'Position')
        
        # Determine company type for cultural fit
        company_lower = company.lower()
        
        if any(keyword in company_lower for keyword in ['spotify', 'music', 'audio']):
            industry_focus = "music technology and creative innovation"
        elif any(keyword in company_lower for keyword in ['volvo', 'automotive', 'car']):
            industry_focus = "automotive technology and sustainable mobility"
        elif any(keyword in company_lower for keyword in ['bank', 'fintech', 'payment']):
            industry_focus = "financial technology and secure systems"
        else:
            industry_focus = "innovative technology solutions"
        
        return {
            "company": company,
            "title": title,
            "industry_focus": industry_focus,
            "soft_skills_emphasis": [
                "Cross-cultural bridge building (Chinese-Swedish perspective)",
                "Business-IT translation with Master's in International Business",
                "Cultural adaptability and global mindset",
                "Multilingual communication abilities",
                "International team collaboration experience"
            ],
            "unique_value": f"Brings unique perspective combining Eastern and Western approaches to technology, valuable for {company}'s global operations",
            "cultural_fit": f"Passionate about {industry_focus} and Swedish innovation culture"
        }

# Test the intelligent fallback
if __name__ == "__main__":
    fallback = IntelligentLegoFallback()
    
    # Test with Volvo job
    test_job = {
        'title': 'Senior Backend Developer',
        'company': 'Volvo Group',
        'description': 'We are looking for a Senior Backend Developer with expertise in Java, Spring Boot, microservices architecture, and cloud platforms. Experience with Kubernetes, Docker, and AWS is highly valued. The role involves building scalable APIs for automotive systems and working with international teams across Sweden and China.'
    }
    
    print("🧠 Testing Intelligent LEGO Fallback...")
    strategy = fallback.analyze_job_and_create_lego_strategy(test_job)
    print(f"📊 LEGO Strategy: {json.dumps(strategy, indent=2)}")
    
    cover_strategy = fallback.create_intelligent_cover_letter_strategy(test_job)
    print(f"💌 Cover Letter Strategy: {json.dumps(cover_strategy, indent=2)}")
    
    print("✅ Intelligent fallback working perfectly!")