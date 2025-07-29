#!/usr/bin/env python3
"""
Advanced ATS (Applicant Tracking System) Analyzer
Comprehensive ATS compatibility checker with detailed scoring and recommendations
"""
import re
import logging
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from collections import Counter, defaultdict
import math
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class ATSAnalysisResult:
    """Comprehensive ATS analysis result"""
    overall_score: float
    passing_threshold: bool  # True if score >= 75
    detailed_scores: Dict[str, float]
    recommendations: List[str]
    critical_issues: List[str]
    keyword_analysis: Dict
    format_analysis: Dict
    content_analysis: Dict
    improvement_suggestions: List[str]

@dataclass
class KeywordDensity:
    """Keyword density analysis"""
    keyword: str
    count: int
    density: float  # percentage
    relevance_score: float
    position_weight: float  # keywords in important sections get higher weight

class ATSAnalyzer:
    """Advanced ATS compatibility analyzer with industry-standard scoring"""
    
    def __init__(self):
        self.industry_keywords = self._load_industry_keywords()
        self.ats_requirements = self._load_ats_requirements()
        self.scoring_weights = {
            'keyword_optimization': 0.35,
            'format_compatibility': 0.25,
            'content_structure': 0.20,
            'readability': 0.10,
            'length_optimization': 0.10
        }
        
    def _load_industry_keywords(self) -> Dict[str, Dict[str, int]]:
        """Load industry-specific keywords with importance weights"""
        return {
            'software_development': {
                # Programming languages (high importance)
                'python': 10, 'java': 10, 'javascript': 10, 'typescript': 9,
                'c#': 8, '.net': 8, 'php': 7, 'ruby': 7, 'go': 7, 'rust': 6,
                # Frameworks (high importance)
                'react': 10, 'angular': 9, 'vue': 8, 'spring': 10, 'django': 9,
                'flask': 8, 'express': 8, 'laravel': 7, 'rails': 7,
                # Databases (medium-high importance)
                'postgresql': 9, 'mysql': 8, 'mongodb': 8, 'redis': 7,
                'elasticsearch': 6, 'oracle': 6,
                # Cloud & DevOps (high importance)
                'aws': 10, 'azure': 10, 'gcp': 8, 'docker': 9, 'kubernetes': 9,
                'terraform': 8, 'ansible': 7, 'jenkins': 7,
                # Tools & Methodologies (medium importance)
                'git': 8, 'agile': 8, 'scrum': 7, 'ci/cd': 8, 'microservices': 9,
                'api': 8, 'rest': 8, 'graphql': 7, 'websocket': 6
            },
            'devops': {
                # Core DevOps tools (very high importance)
                'kubernetes': 10, 'docker': 10, 'terraform': 10, 'ansible': 9,
                'jenkins': 9, 'gitlab': 8, 'github': 8,
                # Cloud platforms (very high importance)
                'aws': 10, 'azure': 10, 'gcp': 9,
                # Monitoring & Logging (high importance)
                'prometheus': 9, 'grafana': 9, 'elk': 8, 'splunk': 7,
                'datadog': 7, 'newrelic': 6,
                # Infrastructure (high importance)
                'linux': 9, 'bash': 8, 'powershell': 7, 'python': 8,
                'yaml': 7, 'json': 6,
                # CI/CD & Automation (high importance)
                'ci/cd': 10, 'automation': 9, 'pipeline': 8, 'deployment': 8,
                'infrastructure as code': 9, 'gitops': 8
            },
            'cloud_engineering': {
                # Cloud platforms (very high importance)
                'aws': 10, 'azure': 10, 'gcp': 9,
                # Core services (high importance)
                'ec2': 9, 's3': 8, 'lambda': 9, 'vpc': 8, 'rds': 8,
                'kubernetes': 10, 'docker': 9,
                # Infrastructure as Code (high importance)
                'terraform': 10, 'cloudformation': 9, 'arm': 7,
                # Security & Networking (medium-high importance)
                'iam': 8, 'security groups': 7, 'load balancer': 8,
                'cdn': 7, 'dns': 6,
                # Monitoring & Cost (medium importance)
                'cloudwatch': 7, 'cost optimization': 8, 'monitoring': 8
            }
        }
    
    def _load_ats_requirements(self) -> Dict[str, Dict]:
        """Load ATS system requirements and compatibility rules"""
        return {
            'format_requirements': {
                'acceptable_formats': ['pdf', 'docx', 'doc'],
                'avoid_formats': ['png', 'jpg', 'gif', 'html'],
                'font_requirements': {
                    'readable_fonts': ['arial', 'calibri', 'times new roman', 'helvetica'],
                    'avoid_fonts': ['comic sans', 'papyrus', 'wingdings'],
                    'min_font_size': 10,
                    'max_font_size': 14
                }
            },
            'structure_requirements': {
                'required_sections': ['contact', 'experience', 'skills', 'education'],
                'optional_sections': ['summary', 'certifications', 'projects'],
                'section_order_importance': True,
                'clear_headings': True
            },
            'content_requirements': {
                'optimal_length': {
                    'cv': {'min': 300, 'max': 800, 'optimal': 600},
                    'cover_letter': {'min': 150, 'max': 400, 'optimal': 300}
                },
                'keyword_density': {'min': 2, 'max': 8, 'optimal': 5},
                'bullet_points': True,
                'quantified_achievements': True
            }
        }
    
    async def analyze_document(self, document_content: str, job_description: str, 
                             job_title: str, document_type: str = 'cv') -> ATSAnalysisResult:
        """Perform comprehensive ATS analysis on document"""
        
        logger.info(f"Starting ATS analysis for {document_type} - {job_title}")
        
        # Determine industry/role category
        industry = self._determine_industry(job_title, job_description)
        
        # Perform individual analyses
        keyword_analysis = self._analyze_keywords(document_content, job_description, job_title, industry)
        format_analysis = self._analyze_format_compatibility(document_content, document_type)
        content_analysis = self._analyze_content_structure(document_content, document_type)
        readability_analysis = self._analyze_readability(document_content)
        length_analysis = self._analyze_length_optimization(document_content, document_type)
        
        # Calculate component scores
        scores = {
            'keyword_optimization': keyword_analysis['score'],
            'format_compatibility': format_analysis['score'],
            'content_structure': content_analysis['score'],
            'readability': readability_analysis['score'],
            'length_optimization': length_analysis['score']
        }
        
        # Calculate overall score
        overall_score = sum(
            scores[component] * self.scoring_weights[component]
            for component in scores
        )
        
        # Generate recommendations and critical issues
        recommendations = []
        critical_issues = []
        improvement_suggestions = []
        
        # Collect recommendations from each analysis
        recommendations.extend(keyword_analysis.get('recommendations', []))
        recommendations.extend(format_analysis.get('recommendations', []))
        recommendations.extend(content_analysis.get('recommendations', []))
        recommendations.extend(readability_analysis.get('recommendations', []))
        recommendations.extend(length_analysis.get('recommendations', []))
        
        # Identify critical issues (score < 60)
        for component, score in scores.items():
            if score < 60:
                critical_issues.append(f"Critical: {component.replace('_', ' ').title()} needs immediate attention (score: {score:.1f})")
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(scores, keyword_analysis, content_analysis)
        
        return ATSAnalysisResult(
            overall_score=round(overall_score, 1),
            passing_threshold=overall_score >= 75,
            detailed_scores=scores,
            recommendations=recommendations[:10],  # Top 10 recommendations
            critical_issues=critical_issues,
            keyword_analysis=keyword_analysis,
            format_analysis=format_analysis,
            content_analysis=content_analysis,
            improvement_suggestions=improvement_suggestions
        )
    
    def _determine_industry(self, job_title: str, job_description: str) -> str:
        """Determine industry/role category from job posting"""
        combined_text = f"{job_title} {job_description}".lower()
        
        industry_scores = {}
        for industry, keywords in self.industry_keywords.items():
            score = 0
            for keyword, weight in keywords.items():
                if keyword in combined_text:
                    score += weight
            industry_scores[industry] = score
        
        if not industry_scores:
            return 'software_development'  # Default
        
        best_industry = max(industry_scores, key=industry_scores.get)
        logger.info(f"Determined industry: {best_industry} (score: {industry_scores[best_industry]})")
        return best_industry
    
    def _analyze_keywords(self, document: str, job_description: str, 
                         job_title: str, industry: str) -> Dict:
        """Comprehensive keyword analysis"""
        
        doc_lower = document.lower()
        job_lower = f"{job_title} {job_description}".lower()
        
        # Get industry-specific keywords
        industry_keywords = self.industry_keywords.get(industry, {})
        
        # Extract job-specific keywords
        job_keywords = self._extract_job_specific_keywords(job_lower)
        
        # Analyze keyword presence and density
        keyword_analysis = {
            'industry_matches': {},
            'job_specific_matches': {},
            'density_analysis': [],
            'missing_critical_keywords': [],
            'keyword_distribution': {},
            'score': 0.0
        }
        
        # Industry keyword analysis
        industry_matches = 0
        total_industry_weight = sum(industry_keywords.values()) if industry_keywords else 1
        
        for keyword, weight in industry_keywords.items():
            count = doc_lower.count(keyword)
            if count > 0:
                industry_matches += weight
                density = (count / len(document.split())) * 100
                keyword_analysis['industry_matches'][keyword] = {
                    'count': count,
                    'weight': weight,
                    'density': round(density, 2)
                }
            else:
                if weight >= 8:  # Critical keywords
                    keyword_analysis['missing_critical_keywords'].append(keyword)
        
        # Job-specific keyword analysis
        job_matches = 0
        for keyword in job_keywords:
            count = doc_lower.count(keyword)
            if count > 0:
                job_matches += 1
                keyword_analysis['job_specific_matches'][keyword] = count
        
        # Calculate keyword scores
        industry_score = (industry_matches / total_industry_weight) * 100 if total_industry_weight > 0 else 0
        job_score = (job_matches / len(job_keywords)) * 100 if job_keywords else 0
        
        # Overall keyword score (weighted average)
        keyword_score = (industry_score * 0.6) + (job_score * 0.4)
        keyword_analysis['score'] = min(100, keyword_score)
        
        # Generate recommendations
        recommendations = []
        if keyword_score < 70:
            recommendations.append("Increase keyword density by adding more relevant technical terms")
        if keyword_analysis['missing_critical_keywords']:
            recommendations.append(f"Add missing critical keywords: {', '.join(keyword_analysis['missing_critical_keywords'][:3])}")
        if job_matches < len(job_keywords) * 0.5:
            recommendations.append("Include more job-specific terms from the job description")
        
        keyword_analysis['recommendations'] = recommendations
        
        return keyword_analysis
    
    def _extract_job_specific_keywords(self, job_text: str) -> List[str]:
        """Extract job-specific technical keywords"""
        
        # Technical keyword patterns
        patterns = [
            r'\b(?:programming|coding|development|software|application|system|platform|framework|library|database|cloud|devops|infrastructure|deployment|monitoring|testing|automation|integration|architecture|design|security|performance|optimization|scalability|reliability|maintenance|troubleshooting|debugging|documentation|collaboration|leadership|mentoring|training|project management|agile|scrum|kanban|ci/cd|version control|api|microservices|containerization|virtualization|networking|storage|backup|disaster recovery|compliance|governance|best practices|standards|methodologies|tools|technologies|solutions|innovations|improvements|enhancements|migrations|upgrades|implementations|configurations|customizations|integrations|optimizations|automations|streamlining|efficiency|productivity|quality|standards|guidelines|procedures|processes|workflows|pipelines|deployment|delivery|operations|maintenance|support|troubleshooting|monitoring|alerting|logging|reporting|analytics|metrics|dashboards|visualizations|insights|recommendations|strategies|planning|roadmaps|architectures|designs|specifications|requirements|analysis|research|evaluation|assessment|review|audit|validation|verification|testing|quality assurance|quality control|performance testing|load testing|stress testing|security testing|penetration testing|vulnerability assessment|risk assessment|threat modeling|incident response|disaster recovery|business continuity|compliance|governance|risk management|change management|configuration management|release management|deployment management|environment management|capacity planning|resource management|cost optimization|budget management|vendor management|contract management|procurement|sourcing|evaluation|selection|implementation|onboarding|training|support|maintenance|operations|monitoring|reporting|analysis|optimization|improvement|innovation|transformation|modernization|migration|upgrade|consolidation|standardization|automation|streamlining|efficiency|productivity|quality|reliability|security|performance|scalability|availability|disaster recovery|business continuity|compliance|governance|risk management|change management|configuration management|release management|deployment management|environment management|capacity planning|resource management|cost optimization|budget management)\b',
            r'\b(?:java|python|javascript|typescript|c#|\.net|php|ruby|go|rust|scala|kotlin|swift|objective-c|c\+\+|c|perl|bash|powershell|sql|nosql|html|css|xml|json|yaml|toml|markdown|latex|regex|linux|unix|windows|macos|ios|android|web|mobile|desktop|server|client|frontend|backend|fullstack|database|api|rest|graphql|soap|microservices|monolith|containerization|virtualization|cloud|aws|azure|gcp|docker|kubernetes|terraform|ansible|chef|puppet|jenkins|gitlab|github|bitbucket|git|svn|mercurial|bazaar|maven|gradle|npm|yarn|pip|composer|bundler|cargo|nuget|webpack|babel|eslint|prettier|jest|mocha|junit|testng|selenium|cypress|postman|insomnia|swagger|openapi|jira|confluence|slack|teams|zoom|skype|email|phone|chat|video|audio|text|voice|data|file|image|video|audio|document|spreadsheet|presentation|pdf|word|excel|powerpoint|outlook|gmail|calendar|task|project|issue|bug|feature|enhancement|improvement|fix|patch|update|upgrade|migration|deployment|release|rollback|hotfix|maintenance|support|training|documentation|wiki|knowledge base|faq|tutorial|guide|manual|handbook|policy|procedure|standard|guideline|best practice|framework|methodology|process|workflow|pipeline|automation|scripting|coding|programming|development|design|architecture|engineering|analysis|research|planning|strategy|roadmap|vision|mission|goal|objective|target|milestone|deliverable|requirement|specification|acceptance criteria|user story|epic|feature|task|subtask|bug|defect|issue|incident|problem|change request|enhancement|improvement|optimization|refactoring|cleanup|maintenance|support|troubleshooting|debugging|monitoring|alerting|logging|reporting|analytics|metrics|dashboard|visualization|insight|recommendation|action item|follow-up|next step|todo|backlog|sprint|iteration|release|version|branch|tag|commit|merge|pull request|code review|pair programming|mob programming|test-driven development|behavior-driven development|domain-driven design|event-driven architecture|service-oriented architecture|microservices architecture|serverless architecture|cloud-native architecture|distributed systems|high availability|fault tolerance|disaster recovery|business continuity|scalability|performance|security|privacy|compliance|governance|risk management|change management|configuration management|release management|deployment management|environment management|capacity planning|resource management|cost optimization|budget management|vendor management|contract management|procurement|sourcing|evaluation|selection|implementation|onboarding|training|support|maintenance|operations|monitoring|reporting|analysis|optimization|improvement|innovation|transformation|modernization|migration|upgrade|consolidation|standardization|automation|streamlining|efficiency|productivity|quality|reliability|security|performance|scalability|availability)\b'
        ]
        
        keywords = set()
        for pattern in patterns:
            matches = re.findall(pattern, job_text, re.IGNORECASE)
            keywords.update(match.lower() for match in matches)
        
        return list(keywords)[:25]  # Return top 25 most relevant
    
    def _analyze_format_compatibility(self, document: str, document_type: str) -> Dict:
        """Analyze format compatibility with ATS systems"""
        
        analysis = {
            'score': 0.0,
            'issues': [],
            'recommendations': [],
            'format_elements': {}
        }
        
        score = 0.0
        
        # Check for LaTeX formatting (good for PDF generation)
        if '\\' in document and 'documentclass' in document:
            score += 25
            analysis['format_elements']['latex_formatted'] = True
        else:
            analysis['issues'].append("Document not in structured format")
            analysis['recommendations'].append("Use structured formatting (LaTeX or proper markup)")
        
        # Check for proper sections
        section_indicators = ['\\section', '\\subsection', '#', '##']
        has_sections = any(indicator in document for indicator in section_indicators)
        if has_sections:
            score += 20
            analysis['format_elements']['has_sections'] = True
        else:
            analysis['issues'].append("Missing clear section headers")
            analysis['recommendations'].append("Add clear section headers for better ATS parsing")
        
        # Check for bullet points
        bullet_indicators = ['\\item', '•', '*', '-']
        has_bullets = any(indicator in document for indicator in bullet_indicators)
        if has_bullets:
            score += 20
            analysis['format_elements']['has_bullets'] = True
        else:
            analysis['recommendations'].append("Use bullet points for better readability")
        
        # Check for emphasis/formatting
        emphasis_indicators = ['\\textbf', '\\textit', '**', '*', '_']
        has_emphasis = any(indicator in document for indicator in emphasis_indicators)
        if has_emphasis:
            score += 15
            analysis['format_elements']['has_emphasis'] = True
        
        # Check for contact information
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        has_email = bool(re.search(email_pattern, document))
        has_phone = bool(re.search(phone_pattern, document))
        
        if has_email and has_phone:
            score += 20
            analysis['format_elements']['complete_contact'] = True
        elif has_email or has_phone:
            score += 10
            analysis['recommendations'].append("Include complete contact information")
        else:
            analysis['issues'].append("Missing contact information")
            analysis['recommendations'].append("Add email and phone number")
        
        analysis['score'] = min(100, score)
        return analysis
    
    def _analyze_content_structure(self, document: str, document_type: str) -> Dict:
        """Analyze content structure and organization"""
        
        analysis = {
            'score': 0.0,
            'structure_elements': {},
            'issues': [],
            'recommendations': []
        }
        
        score = 0.0
        doc_lower = document.lower()
        
        # Required sections for CV
        if document_type == 'cv':
            required_sections = ['experience', 'skills', 'education']
            optional_sections = ['summary', 'profile', 'projects', 'certifications']
        else:  # cover letter
            required_sections = ['dear', 'sincerely']
            optional_sections = ['paragraph']
        
        # Check for required sections
        found_required = 0
        for section in required_sections:
            if section in doc_lower:
                found_required += 1
                analysis['structure_elements'][f'has_{section}'] = True
        
        section_score = (found_required / len(required_sections)) * 50
        score += section_score
        
        if found_required < len(required_sections):
            missing = [s for s in required_sections if s not in doc_lower]
            analysis['recommendations'].append(f"Add missing sections: {', '.join(missing)}")
        
        # Check for optional sections (bonus points)
        found_optional = sum(1 for section in optional_sections if section in doc_lower)
        bonus_score = min(20, found_optional * 5)
        score += bonus_score
        
        # Check for quantified achievements
        number_pattern = r'\b\d+[\%\+]?\b'
        numbers = re.findall(number_pattern, document)
        if len(numbers) >= 3:
            score += 15
            analysis['structure_elements']['quantified_achievements'] = True
        else:
            analysis['recommendations'].append("Add quantified achievements with numbers/percentages")
        
        # Check for action verbs
        action_verbs = ['developed', 'implemented', 'created', 'managed', 'led', 'designed', 
                       'built', 'optimized', 'improved', 'reduced', 'increased', 'achieved']
        found_verbs = sum(1 for verb in action_verbs if verb in doc_lower)
        if found_verbs >= 5:
            score += 15
            analysis['structure_elements']['strong_action_verbs'] = True
        else:
            analysis['recommendations'].append("Use more strong action verbs to describe achievements")
        
        analysis['score'] = min(100, score)
        return analysis
    
    def _analyze_readability(self, document: str) -> Dict:
        """Analyze document readability and clarity"""
        
        analysis = {
            'score': 0.0,
            'readability_metrics': {},
            'recommendations': []
        }
        
        # Clean text for analysis
        clean_text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', document)  # Remove LaTeX commands
        clean_text = re.sub(r'[{}\\]', '', clean_text)  # Remove LaTeX symbols
        
        words = clean_text.split()
        sentences = re.split(r'[.!?]+', clean_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not words or not sentences:
            analysis['score'] = 0
            return analysis
        
        # Calculate metrics
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        avg_chars_per_word = sum(len(word) for word in words) / len(words) if words else 0
        
        analysis['readability_metrics'] = {
            'total_words': len(words),
            'total_sentences': len(sentences),
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'avg_chars_per_word': round(avg_chars_per_word, 1)
        }
        
        score = 100  # Start with perfect score and deduct
        
        # Penalize overly long sentences
        if avg_words_per_sentence > 25:
            score -= 20
            analysis['recommendations'].append("Break down long sentences for better readability")
        elif avg_words_per_sentence > 20:
            score -= 10
        
        # Penalize overly complex words
        if avg_chars_per_word > 6:
            score -= 15
            analysis['recommendations'].append("Use simpler, more direct language")
        
        # Check for passive voice (simplified detection)
        passive_indicators = ['was', 'were', 'been', 'being']
        passive_count = sum(clean_text.lower().count(indicator) for indicator in passive_indicators)
        if passive_count > len(words) * 0.1:  # More than 10% passive voice
            score -= 15
            analysis['recommendations'].append("Reduce passive voice usage")
        
        analysis['score'] = max(0, score)
        return analysis
    
    def _analyze_length_optimization(self, document: str, document_type: str) -> Dict:
        """Analyze document length optimization"""
        
        analysis = {
            'score': 0.0,
            'length_metrics': {},
            'recommendations': []
        }
        
        # Count words (excluding LaTeX commands)
        clean_text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', document)
        words = clean_text.split()
        word_count = len(words)
        
        # Get optimal length requirements
        requirements = self.ats_requirements['content_requirements']['optimal_length'][document_type]
        min_words = requirements['min']
        max_words = requirements['max']
        optimal_words = requirements['optimal']
        
        analysis['length_metrics'] = {
            'word_count': word_count,
            'min_required': min_words,
            'max_recommended': max_words,
            'optimal_range': optimal_words,
            'length_category': 'unknown'
        }
        
        # Calculate score based on length
        if optimal_words * 0.9 <= word_count <= optimal_words * 1.1:
            score = 100
            analysis['length_metrics']['length_category'] = 'optimal'
        elif min_words <= word_count <= max_words:
            score = 80
            analysis['length_metrics']['length_category'] = 'acceptable'
        elif word_count < min_words:
            score = max(40, 80 - (min_words - word_count))
            analysis['length_metrics']['length_category'] = 'too_short'
            analysis['recommendations'].append(f"Document is too short. Add {min_words - word_count} more words")
        else:  # word_count > max_words
            score = max(40, 80 - (word_count - max_words) * 0.5)
            analysis['length_metrics']['length_category'] = 'too_long'
            analysis['recommendations'].append(f"Document is too long. Remove {word_count - max_words} words")
        
        analysis['score'] = score
        return analysis
    
    def _generate_improvement_suggestions(self, scores: Dict[str, float], 
                                        keyword_analysis: Dict, content_analysis: Dict) -> List[str]:
        """Generate prioritized improvement suggestions"""
        
        suggestions = []
        
        # Priority 1: Critical issues (score < 60)
        critical_components = [comp for comp, score in scores.items() if score < 60]
        
        if 'keyword_optimization' in critical_components:
            suggestions.append("🔑 CRITICAL: Add more relevant keywords from the job description")
            missing_keywords = keyword_analysis.get('missing_critical_keywords', [])
            if missing_keywords:
                suggestions.append(f"   → Focus on these missing keywords: {', '.join(missing_keywords[:3])}")
        
        if 'format_compatibility' in critical_components:
            suggestions.append("📄 CRITICAL: Improve document formatting for ATS compatibility")
            suggestions.append("   → Use clear section headers and bullet points")
        
        if 'content_structure' in critical_components:
            suggestions.append("📝 CRITICAL: Enhance content structure and organization")
            suggestions.append("   → Add quantified achievements with numbers and percentages")
        
        # Priority 2: Significant improvements (score 60-75)
        moderate_components = [comp for comp, score in scores.items() if 60 <= score < 75]
        
        for component in moderate_components:
            if component == 'keyword_optimization':
                suggestions.append("🎯 Moderate: Increase keyword density strategically")
            elif component == 'readability':
                suggestions.append("📖 Moderate: Improve readability with shorter sentences")
            elif component == 'length_optimization':
                suggestions.append("📏 Moderate: Optimize document length")
        
        # Priority 3: Fine-tuning (score 75-85)
        good_components = [comp for comp, score in scores.items() if 75 <= score < 85]
        
        if good_components:
            suggestions.append("✨ Fine-tuning opportunities:")
            for component in good_components:
                suggestions.append(f"   → Enhance {component.replace('_', ' ')}")
        
        return suggestions[:8]  # Return top 8 suggestions
    
    async def generate_ats_report(self, analysis_result: ATSAnalysisResult, 
                                job_title: str, company: str) -> Dict:
        """Generate comprehensive ATS compatibility report"""
        
        report = {
            'report_id': f"ats_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'job_details': {
                'title': job_title,
                'company': company,
                'analysis_date': datetime.now().isoformat()
            },
            'overall_assessment': {
                'score': analysis_result.overall_score,
                'grade': self._get_score_grade(analysis_result.overall_score),
                'passing': analysis_result.passing_threshold,
                'ats_ready': analysis_result.overall_score >= 80
            },
            'detailed_scores': analysis_result.detailed_scores,
            'score_breakdown': {
                component: {
                    'score': score,
                    'weight': self.scoring_weights[component],
                    'contribution': score * self.scoring_weights[component],
                    'status': self._get_component_status(score)
                }
                for component, score in analysis_result.detailed_scores.items()
            },
            'critical_issues': analysis_result.critical_issues,
            'recommendations': {
                'immediate_actions': analysis_result.critical_issues,
                'improvements': analysis_result.recommendations,
                'next_steps': analysis_result.improvement_suggestions
            },
            'keyword_insights': {
                'industry_matches': len(analysis_result.keyword_analysis.get('industry_matches', {})),
                'job_specific_matches': len(analysis_result.keyword_analysis.get('job_specific_matches', {})),
                'missing_critical': analysis_result.keyword_analysis.get('missing_critical_keywords', [])
            },
            'action_plan': self._create_action_plan(analysis_result),
            'benchmarks': {
                'minimum_passing_score': 75,
                'good_score': 85,
                'excellent_score': 95,
                'current_percentile': self._calculate_percentile(analysis_result.overall_score)
            }
        }
        
        return report
    
    def _get_score_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 95:
            return 'A+'
        elif score >= 90:
            return 'A'
        elif score >= 85:
            return 'B+'
        elif score >= 80:
            return 'B'
        elif score >= 75:
            return 'C+'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _get_component_status(self, score: float) -> str:
        """Get status description for component score"""
        if score >= 85:
            return 'Excellent'
        elif score >= 75:
            return 'Good'
        elif score >= 60:
            return 'Needs Improvement'
        else:
            return 'Critical'
    
    def _calculate_percentile(self, score: float) -> int:
        """Calculate approximate percentile based on score"""
        # Simplified percentile calculation
        if score >= 95:
            return 95
        elif score >= 90:
            return 85
        elif score >= 85:
            return 75
        elif score >= 80:
            return 65
        elif score >= 75:
            return 50
        elif score >= 70:
            return 35
        elif score >= 60:
            return 20
        else:
            return 10
    
    def _create_action_plan(self, analysis_result: ATSAnalysisResult) -> List[Dict]:
        """Create prioritized action plan for improvements"""
        
        actions = []
        
        # Critical actions (score < 60)
        for component, score in analysis_result.detailed_scores.items():
            if score < 60:
                actions.append({
                    'priority': 'Critical',
                    'component': component.replace('_', ' ').title(),
                    'current_score': score,
                    'target_score': 75,
                    'impact': 'High',
                    'effort': 'Medium',
                    'timeline': '1-2 days'
                })
        
        # Important actions (score 60-75)
        for component, score in analysis_result.detailed_scores.items():
            if 60 <= score < 75:
                actions.append({
                    'priority': 'Important',
                    'component': component.replace('_', ' ').title(),
                    'current_score': score,
                    'target_score': 85,
                    'impact': 'Medium',
                    'effort': 'Low',
                    'timeline': '2-4 hours'
                })
        
        # Enhancement actions (score 75-85)
        for component, score in analysis_result.detailed_scores.items():
            if 75 <= score < 85:
                actions.append({
                    'priority': 'Enhancement',
                    'component': component.replace('_', ' ').title(),
                    'current_score': score,
                    'target_score': 95,
                    'impact': 'Low',
                    'effort': 'Low',
                    'timeline': '1-2 hours'
                })
        
        return sorted(actions, key=lambda x: {'Critical': 0, 'Important': 1, 'Enhancement': 2}[x['priority']])