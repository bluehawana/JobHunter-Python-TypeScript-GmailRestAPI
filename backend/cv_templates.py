"""
🧱 CV Template Manager
Manages role-specific CV templates for intelligent matching
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import logging

from job_analyzer import JobAnalyzer
from template_matcher import TemplateMatcher

# Configure logging
logger = logging.getLogger(__name__)

class CVTemplateManager:
    """Manages CV templates for different roles"""
    
    # Role categories and their keywords
    # Now using REAL templates from templates/cv_templates/ folder
    # Priority: Lower number = higher priority (checked first)
    # Tip: More specific roles should have lower priority numbers
    ROLE_CATEGORIES = {
        # === SPECIALIZED ROLES (Priority 1) - Check these first ===
        'azure_solution_architect': {
            'keywords': [
                'azure architect', 'solution architect', 'azure solution architect', 'cloud architect',
                'enterprise architect', 'azure integration', 'azure services',
                'azure devops', 'aks', 'azure kubernetes', 'bicep', 'arm template',
                'azure functions', 'logic apps', 'service bus', 'event grid',
                'azure ad', 'azure security', 'azure monitor', 'application insights',
                'sharepoint', 'dynamics 365', 'power bi', 'power platform',
                'microsoft 365', 'microsoft graph', 'azure migration',
                'finops', 'cost optimization', 'azure cost management',
                'financial services', 'banking', 'automotive finance',
                'compliance', 'psd2', 'gdpr', 'zero trust'
            ],
            'cv_template': 'templates/cv_templates/azure_solution_architect_template.tex',
            'cl_template': 'templates/cl_templates/azure_solution_architect_cl_template.tex',
            'priority': 1
        },
        'it_business_analyst': {
            'keywords': ['business analyst', 'it analyst', 'it business analyst', 'business requirements', 'stakeholder', 'business process', 'gap analysis', 'power bi', 'visio', 'workshop', 'requirements gathering', 'business case', 'process improvement', 'digitalization', 'bridge between'],
            'cv_template': 'backend/latex_sources/cv_hongzhi_li_modern.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 1
        },
        'project_manager': {
            'keywords': [
                # Explicit project manager titles (highest priority)
                'project manager', 'senior project manager', 'technical project manager', 
                'engineering project manager', 'it project manager', 'software project manager',
                'pm role', 'project lead', 'program manager', 'project coordinator',
                # Project management activities
                'project management', 'managing projects', 'lead projects', 'oversee projects',
                'project delivery', 'project execution', 'project planning',
                # PM-specific skills
                'stakeholder management', 'budget management', 'risk management', 
                'project governance', 'project portfolio', 'pmp', 'prince2',
                'agile project management', 'scrum master', 'project methodology',
                # PM responsibilities
                'coordinate project work', 'manage decision points', 'mitigate risks',
                'ensure project objectives', 'project content delivery', 'sales campaigns',
                'rfq responses', 'rfi responses', 'project issues management'
            ],
            'cv_template': 'templates/cv_templates/project_manager_template.tex',
            'cl_template': 'templates/cl_templates/project_manager_cl_template.tex',
            'priority': 1
        },
        'android_developer': {
            'keywords': ['android', 'android app', 'apk', 'mobile app', 'aosp', 'android sdk', 'jetpack', 'mobile developer', 'android studio'],
            'cv_template': 'templates/cv_templates/android_developer_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 1
        },
        'kotlin_app_developer': {
            'keywords': ['kotlin', 'android auto', 'automotive', 'in-vehicle', 'ivi', 'infotainment', 'kotlin developer', 'kotlin android', 'app developer', 'mobile developer'],
            'cv_template': 'templates/cv_templates/kotlin_app_developer_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 1
        },
        'ios_developer': {
            'keywords': ['ios', 'swift', 'swiftui', 'xcode', 'ios app', 'iphone', 'ipad', 'apple', 'cocoa', 'objective-c'],
            'cv_template': 'templates/cv_templates/kotlin_app_developer_template.tex',  # Uses same template, shows React Native + Swift
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 1
        },
        'react_native_developer': {
            'keywords': ['react native', 'cross-platform', 'expo', 'react native app', 'mobile cross-platform'],
            'cv_template': 'templates/cv_templates/kotlin_app_developer_template.tex',  # Uses same template, shows React Native
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 1
        },
        'devops_fintech': {
            'keywords': ['fintech', 'financial', 'banking', 'payment', 'trading', 'nasdaq', 'finance', 'post-trade', 'settlement', 'compliance'],
            'cv_template': 'backend/latex_sources/cv_hongzhi_li_modern.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 1
        },
        'ai_product_engineer': {
            # Keywords for BUILDING AI systems (model training, RAG, MLOps)
            'keywords': [
                'ai engineer', 'ml engineer', 'machine learning engineer',
                'model training', 'training models', 'fine-tuning', 'fine-tuning models',
                'rag', 'retrieval-augmented generation', 'vector database', 'vector databases',
                'embeddings', 'mlops', 'ml ops', 'model serving', 'model deployment',
                'deep learning', 'neural network', 'pytorch', 'tensorflow',
                'hugging face', 'langchain', 'llama', 'stable diffusion',
                'computer vision', 'nlp', 'natural language processing',
                'data science', 'feature engineering', 'model evaluation'
            ],
            'cv_template': 'templates/cv_templates/ai_product_engineer_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 1
        },

        # === LANGUAGE-SPECIFIC DEVELOPERS (Priority 2) ===
        'dotnet_developer': {
            'keywords': ['c#', '.net', 'asp.net', '.net core', 'asp.net core', 'entity framework', 'blazor', 'xamarin', 'microsoft stack', 'azure', 'c sharp'],
            'cv_template': 'templates/cv_templates/dotnet_developer_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 2
        },
        'java_developer': {
            'keywords': ['java', 'spring boot', 'spring framework', 'hibernate', 'jpa', 'maven', 'gradle', 'java developer'],
            'cv_template': 'templates/cv_templates/java_developer_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 2
        },

        # === FULLSTACK (Priority 2) - Explicit fullstack keywords win ===
        'fullstack_developer': {
            'keywords': [
                'fullstack', 'full-stack', 'full stack', 'frontend and backend', 'front-end and back-end',
                'react', 'vue', 'angular', 'next.js', 'nuxt', 'web developer', 'web application',
                'typescript', 'javascript',
                # AI integration keywords (using AI, not building AI)
                'integrating ai', 'ai integration', 'using ai', 'leverage ai',
                'ai-powered features', 'ai capabilities', 'llm integration',
                'openai api', 'claude api', 'gpt api', 'ai apis',
                'generative ai solutions', 'ai solutions', 'llm-based applications'
            ],
            'cv_template': 'templates/cv_templates/fullstack_developer_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 2
        },

        # === BACKEND-FOCUSED (Priority 3) ===
        'backend_developer': {
            'keywords': [
                'backend developer', 'back-end developer', 'api developer', 'software engineer', 'software developer',
                'microservices', 'server-side', 'restful api', 'distributed systems', 'elasticsearch',
                'cassandra', 'big data', 'search engines', 'petabyte', 'analytics systems',
                # AI integration keywords (using AI, not building AI)
                'integrating ai', 'ai integration', 'using ai', 'leverage ai',
                'ai-powered features', 'ai capabilities', 'llm integration',
                'openai api', 'claude api', 'gpt api', 'ai apis',
                'generative ai solutions', 'ai solutions', 'llm-based applications',
                'vector search', 'semantic search', 'applied use of', 'use cases powered by'
            ],
            'cv_template': 'templates/cv_templates/fullstack_developer_template.tex',  # Use fullstack as fallback
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 3
        },

        # === DEVOPS/INFRASTRUCTURE (Priority 4) ===
        'devops_cloud': {
            'keywords': ['devops', 'cloud engineer', 'aws', 'azure', 'gcp', 'kubernetes', 'docker', 'terraform', 'ci/cd', 'infrastructure as code', 'iac', 'helm', 'argocd'],
            'cv_template': 'templates/cv_templates/devops_cloud_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 4
        },
        'incident_management_sre': {
            'keywords': ['incident', 'sre', 'site reliability', 'on-call', 'monitoring', 'observability', 'mttr', 'production support', 'pagerduty', 'opsgenie', 'incident management'],
            'cv_template': 'templates/cv_templates/incident_management_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 4
        },
        'platform_engineer': {
            'keywords': ['platform engineer', 'platform team', 'internal tools', 'developer experience', 'devex', 'infrastructure platform', 'golden path'],
            'cv_template': 'templates/cv_templates/devops_cloud_template.tex',  # Use devops as fallback
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 5
        },

        # === IT SUPPORT / OPERATIONS (Priority 3) - Higher priority for customer support ===
        'it_support': {
            'keywords': ['it support', 'helpdesk', 'service desk', 'technical support', 'customer support', 'support engineer', 'it technician', 'desktop support', 'l1', 'l2', 'l3 support', 'itil', 'ticketing', 'user support', 'end user support', 'customer service'],
            'cv_template': 'templates/cv_templates/incident_management_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 3
        },

        # === KAMSTRUP (Priority 1 - Company Specific) ===
        'kamstrup': {
            'keywords': ['kamstrup', 'customer support engineer', 'kamstrup customer support'],
            'cv_template': 'templates/cv_templates/incident_management_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 1
        },

        # === FINOPS / COST OPTIMIZATION (Priority 5) ===
        'finops': {
            'keywords': ['finops', 'cloud cost', 'cost optimization', 'cloud economics', 'cloud billing', 'reserved instances', 'savings plans', 'cost management', 'cloud financial'],
            'cv_template': 'templates/cv_templates/devops_cloud_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 5
        },

        # === ARCHITECT ROLES (Priority 6) ===
        'integration_architect': {
            'keywords': ['integration architect', 'solution architect', 'enterprise architect', 'api architect', 'system integration', 'middleware', 'esb', 'mulesoft', 'api gateway'],
            'cv_template': 'templates/cv_templates/fullstack_developer_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 6
        },

        # === GENERIC CLOUD (Priority 7) - Fallback ===
        'cloud_engineer': {
            'keywords': ['cloud', 'infrastructure', 'cloud platform', 'cloud architecture', 'cloud migration', 'cloud native'],
            'cv_template': 'templates/cv_templates/devops_cloud_template.tex',
            'cl_template': 'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
            'priority': 7
        }
    }
    
    def __init__(self, templates_dir: str = 'templates/cv_templates'):
        # Get absolute path relative to project root
        base_dir = Path(__file__).parent.parent  # Go up to project root
        self.templates_dir = base_dir / templates_dir
        
        # Initialize components
        self.job_analyzer = JobAnalyzer()
        self.template_matcher = TemplateMatcher(self.ROLE_CATEGORIES)
    
    def analyze_job_role(self, job_description: str) -> str:
        """
        Analyze job description and determine the best matching role category

        Returns:
            Role category key (e.g., 'android_developer', 'devops_cloud')
        """
        logger.info("Starting job role analysis")
        logger.debug(f"Job description length: {len(job_description)} characters")
        
        # Use JobAnalyzer to extract keywords for each role
        keyword_counts = self.job_analyzer.identify_role_indicators(
            job_description, 
            self.ROLE_CATEGORIES
        )
        
        # Log keyword matches when debugging enabled
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Keyword matches by role:")
            for role_key, matches in keyword_counts.items():
                if matches:  # Only log roles with matches
                    total_matches = sum(matches.values())
                    logger.debug(f"  {role_key}: {total_matches} total matches - {matches}")
        
        # Use TemplateMatcher to calculate scores
        role_scores = self.template_matcher.calculate_scores(keyword_counts)
        
        # Calculate percentages for analysis
        role_percentages = self.template_matcher.calculate_percentages(role_scores)
        
        # Log role scores for all categories
        logger.info("Role scores for all categories:")
        for role_key, score in sorted(role_scores.items(), key=lambda x: x[1], reverse=True):
            if score > 0:  # Only log roles with non-zero scores
                percentage = role_percentages.get(role_key, 0)
                logger.info(f"  {role_key}: {score:.2f} ({percentage:.1f}%)")
        
        # Log role percentages for debugging
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Complete role percentage breakdown:")
            for role_key, percentage in sorted(role_percentages.items(), key=lambda x: x[1], reverse=True):
                logger.debug(f"  {role_key}: {percentage:.2f}%")
        
        # Select best match with template verification and content alignment
        return self._select_role_with_content_alignment_check(role_scores, role_percentages, job_description)
    
    def _select_role_with_template_verification(self, role_scores: Dict[str, float], role_percentages: Dict[str, float]) -> str:
        """
        Select the best role with template file verification and fallback logic
        
        Args:
            role_scores: Dictionary of role scores
            role_percentages: Dictionary of role percentages
            
        Returns:
            Role category key with verified template
        """
        # Get sorted list of roles by score (highest first)
        sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Try each role in order until we find one with a valid template
        for role_key, score in sorted_roles:
            if score <= 0:
                continue
                
            # Handle AI misclassification prevention
            if role_key == 'ai_product_engineer':
                ai_percentage = role_percentages.get('ai_product_engineer', 0)
                if ai_percentage < 50:
                    logger.warning(
                        f"AI Product Engineer percentage ({ai_percentage:.1f}%) is below 50% threshold. "
                        f"Skipping AI Product Engineer role."
                    )
                    continue
            
            # Verify template file exists
            template_path = self.get_template_path(role_key, 'cv')
            if template_path and template_path.exists():
                logger.info(f"Selected role category: {role_key}")
                logger.info(f"Final score: {score:.2f} ({role_percentages.get(role_key, 0):.1f}%)")
                logger.info(f"Template path used: {template_path}")
                return role_key
            else:
                # Template missing - log error and try next best
                logger.error(f"Template file missing for role {role_key}: {template_path}")
                logger.info(f"Falling back to next best template match")
                continue
        
        # No role with valid template found - use fallback
        logger.error("No role with valid template found, using fallback")
        return self._handle_template_selection_failure()
    
    def _select_role_with_content_alignment_check(self, role_scores: Dict[str, float], role_percentages: Dict[str, float], job_description: str) -> str:
        """
        Select the best role with template verification and content alignment validation
        
        Args:
            role_scores: Dictionary of role scores
            role_percentages: Dictionary of role percentages
            job_description: Job description for alignment checking
            
        Returns:
            Role category key with verified template and content alignment
        """
        # Get sorted list of roles by score (highest first)
        sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Try each role in order until we find one with valid template and alignment
        for role_key, score in sorted_roles:
            if score <= 0:
                continue
                
            # Handle AI misclassification prevention
            if role_key == 'ai_product_engineer':
                ai_percentage = role_percentages.get('ai_product_engineer', 0)
                if ai_percentage < 50:
                    logger.warning(
                        f"AI Product Engineer percentage ({ai_percentage:.1f}%) is below 50% threshold. "
                        f"Skipping AI Product Engineer role."
                    )
                    continue
            
            # Verify template content aligns with role category
            if not self._validate_template_content_alignment(role_key, job_description):
                logger.warning(f"Template content misalignment for role {role_key}, trying alternative")
                alternative_role = self._select_alternative_template_for_misalignment(role_key, job_description)
                if alternative_role != role_key:
                    # Use the alternative role
                    template_path = self.get_template_path(alternative_role, 'cv')
                    if template_path and template_path.exists():
                        logger.info(f"Using alternative role due to content misalignment: {alternative_role}")
                        logger.info(f"Alternative template path: {template_path}")
                        return alternative_role
                # Continue to next role if alternative also fails
                continue
            
            # Verify template file exists
            template_path = self.get_template_path(role_key, 'cv')
            if template_path and template_path.exists():
                logger.info(f"Selected role category: {role_key}")
                logger.info(f"Final score: {score:.2f} ({role_percentages.get(role_key, 0):.1f}%)")
                logger.info(f"Template path used: {template_path}")
                logger.info("Template content alignment validated")
                return role_key
            else:
                # Template missing - log error and try next best
                logger.error(f"Template file missing for role {role_key}: {template_path}")
                logger.info(f"Falling back to next best template match")
                continue
        
        # No role with valid template and alignment found - use fallback
        logger.error("No role with valid template and content alignment found, using fallback")
        return self._handle_template_selection_failure()
    
    def get_template_path(self, role_category: str, template_type: str = 'cv') -> Optional[Path]:
        """
        Get the template path for a given role category

        Args:
            role_category: The role category key (e.g., 'fullstack_developer')
            template_type: 'cv' or 'cl' for CV or Cover Letter template

        Returns:
            Path to the template file, or None if not found
        """
        logger.debug(f"Resolving template path for role: {role_category}, type: {template_type}")
        
        if role_category not in self.ROLE_CATEGORIES:
            logger.warning(f"Unknown role category: {role_category}")
            return None
            
        # Support both old 'template_path' key and new 'cv_template'/'cl_template' keys
        role_data = self.ROLE_CATEGORIES[role_category]

        if template_type == 'cl':
            template_path_str = role_data.get('cl_template', role_data.get('template_path'))
        else:
            template_path_str = role_data.get('cv_template', role_data.get('template_path'))

        if not template_path_str:
            logger.warning(f"No template path configured for role: {role_category}, type: {template_type}")
            return None

        # Validate path format consistency
        if not isinstance(template_path_str, str):
            logger.error(f"Invalid template path format for role {role_category}: {type(template_path_str)}")
            return None

        # Get absolute path from project root
        base_dir = Path(__file__).parent.parent  # Go up to project root
        
        # Handle both absolute and relative paths correctly
        if Path(template_path_str).is_absolute():
            full_path = Path(template_path_str)
            logger.debug(f"Using absolute path: {full_path}")
        else:
            full_path = base_dir / template_path_str
            logger.debug(f"Resolved relative path: {template_path_str} -> {full_path}")
        
        # Normalize path to handle any inconsistencies
        try:
            full_path = full_path.resolve()
            logger.debug(f"Normalized template path: {full_path}")
        except Exception as e:
            logger.error(f"Error normalizing path {full_path}: {e}")
            return None

        # Check if file exists
        if full_path.exists() and full_path.is_file():
            logger.debug(f"Template file exists: {full_path}")
            return full_path
        else:
            # Try alternative path formats for backward compatibility
            if template_type == 'cv' and not template_path_str.endswith('.tex'):
                # Try looking for *_CV.tex pattern in directory
                if full_path.is_dir():
                    cv_files = list(full_path.glob('*_CV.tex'))
                    if cv_files:
                        cv_file = cv_files[0]  # Take first match
                        logger.debug(f"Found CV file in directory: {cv_file}")
                        return cv_file
                    else:
                        logger.warning(f"No *_CV.tex files found in directory: {full_path}")
                        
            logger.warning(f"Template file does not exist: {full_path}")

        return None
    
    def load_template(self, role_category: str, template_type: str = 'cv') -> Optional[str]:
        """
        Load template content for a given role category

        Args:
            role_category: The role category key (e.g., 'fullstack_developer')
            template_type: 'cv' or 'cl' for CV or Cover Letter template

        Returns:
            Template content as string, or None if not found
        """
        logger.info(f"Loading template for role: {role_category}, type: {template_type}")
        
        template_path = self.get_template_path(role_category, template_type)

        if template_path and template_path.exists():
            try:
                logger.debug(f"Reading template file: {template_path}")
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                logger.info(f"Successfully loaded template: {template_path}")
                logger.debug(f"Template content length: {len(content)} characters")
                
                # Validate LaTeX structure after loading
                if self._validate_latex_structure(content):
                    logger.debug("Template LaTeX structure validation passed")
                    return content
                else:
                    logger.error(f"Template LaTeX structure validation failed for: {template_path}")
                    # Try fallback template loading
                    return self._load_fallback_template(role_category, template_type)
                
            except UnicodeDecodeError as e:
                logger.error(f"UTF-8 encoding error loading template from {template_path}: {e}")
                logger.error(f"Template encoding failure - Role: {role_category}, Path: {template_path}")
                return self._load_fallback_template(role_category, template_type)
                
            except Exception as e:
                # Log detailed errors for template load failures with file paths
                logger.error(f"Error loading {template_type.upper()} template from {template_path}: {e}")
                logger.error(f"Template load failure details - Role: {role_category}, Path: {template_path}, Error: {type(e).__name__}")
                return self._load_fallback_template(role_category, template_type)
        else:
            # Log template load failures with file paths
            if template_path:
                logger.error(f"Template file does not exist: {template_path}")
            else:
                logger.error(f"No template path found for role: {role_category}, type: {template_type}")
            
            logger.error(f"Template load failure - Role: {role_category}, Type: {template_type}, Path: {template_path}")
            return self._load_fallback_template(role_category, template_type)
    
    def _validate_latex_structure(self, content: str) -> bool:
        """
        Validate that template content contains required LaTeX structure
        
        Args:
            content: Template content to validate
            
        Returns:
            True if valid LaTeX structure, False otherwise
        """
        if not content:
            logger.warning("Empty template content provided for validation")
            return False
        
        # Check for required LaTeX structure markers
        required_markers = [
            r'\documentclass',
            r'\begin{document}',
            r'\end{document}'
        ]
        
        for marker in required_markers:
            if marker not in content:
                logger.warning(f"Missing required LaTeX marker: {marker}")
                return False
        
        # Check for balanced begin/end document tags
        begin_count = content.count(r'\begin{document}')
        end_count = content.count(r'\end{document}')
        
        if begin_count != end_count or begin_count == 0:
            logger.warning(f"Unbalanced document tags: {begin_count} begin, {end_count} end")
            return False
        
        # Basic LaTeX syntax validation
        if content.count('{') != content.count('}'):
            logger.warning("Unbalanced braces in LaTeX template")
            return False
        
        return True
    
    def _load_fallback_template(self, failed_role: str, template_type: str) -> Optional[str]:
        """
        Load a fallback template when primary template loading fails
        
        Args:
            failed_role: The role that failed to load
            template_type: 'cv' or 'cl'
            
        Returns:
            Fallback template content or None
        """
        logger.info(f"Attempting fallback template loading for failed role: {failed_role}")
        
        # Get fallback role
        fallback_role = self.template_matcher.get_fallback_template([failed_role])
        
        if fallback_role == failed_role:
            # Fallback is same as failed role - try default
            fallback_role = 'devops_cloud'
            logger.warning(f"Fallback role same as failed role, using default: {fallback_role}")
        
        # Try to load fallback template
        fallback_path = self.get_template_path(fallback_role, template_type)
        
        if fallback_path and fallback_path.exists():
            try:
                logger.info(f"Loading fallback template: {fallback_path}")
                with open(fallback_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Validate fallback template structure
                if self._validate_latex_structure(content):
                    logger.info(f"Successfully loaded fallback template: {fallback_role}")
                    return content
                else:
                    logger.error(f"Fallback template also has invalid LaTeX structure: {fallback_path}")
                    
            except Exception as e:
                logger.error(f"Error loading fallback template {fallback_path}: {e}")
        
        # Return detailed error information
        logger.critical(f"Critical error: Unable to load any template for role {failed_role} or fallback {fallback_role}")
        return None
    
    def get_role_info(self, role_category: str) -> Dict:
        """Get information about a role category"""
        if role_category in self.ROLE_CATEGORIES:
            role_data = self.ROLE_CATEGORIES[role_category].copy()
            role_data['category'] = role_category
            role_data['display_name'] = role_category.replace('_', ' ').title()
            return role_data
        
        return {}
    
    def get_role_scores(self, job_description: str) -> Dict[str, float]:
        """
        Get weighted scores for all role categories
        
        Args:
            job_description: The job description text to analyze
            
        Returns:
            Dictionary mapping role keys to their weighted scores
        """
        try:
            # Use JobAnalyzer to extract keywords for each role
            keyword_counts = self.job_analyzer.identify_role_indicators(
                job_description, 
                self.ROLE_CATEGORIES
            )
            
            # Use TemplateMatcher to calculate scores
            role_scores = self.template_matcher.calculate_scores(keyword_counts)
            
            return role_scores
            
        except Exception as e:
            logger.error(f"Error calculating role scores: {e}")
            logger.error(f"Role scores calculation failure - Error: {type(e).__name__}")
            # Return empty scores to prevent further errors
            return {role_key: 0.0 for role_key in self.ROLE_CATEGORIES.keys()}
    
    def get_role_percentages(self, job_description: str) -> Dict[str, float]:
        """
        Get percentage scores for all role categories (normalized to sum to 100%)
        
        Args:
            job_description: The job description text to analyze
            
        Returns:
            Dictionary mapping role keys to their percentage scores (0-100%)
        """
        try:
            # Get weighted scores
            role_scores = self.get_role_scores(job_description)
            
            # Calculate percentages
            role_percentages = self.template_matcher.calculate_percentages(role_scores)
            
            return role_percentages
            
        except Exception as e:
            logger.error(f"Error calculating role percentages: {e}")
            logger.error(f"Role percentages calculation failure - Error: {type(e).__name__}")
            # Return equal percentages to prevent further errors
            num_roles = len(self.ROLE_CATEGORIES)
            equal_percentage = 100.0 / num_roles if num_roles > 0 else 0.0
            return {role_key: equal_percentage for role_key in self.ROLE_CATEGORIES.keys()}
    
    def get_role_breakdown(
        self, 
        job_description: str, 
        threshold: float = 5.0
    ) -> List[Tuple[str, float]]:
        """
        Get a ranked list of significant role matches with their percentages
        
        Args:
            job_description: The job description text to analyze
            threshold: Minimum percentage to include in breakdown (default 5%)
            
        Returns:
            List of (role_key, percentage) tuples, sorted by percentage descending
            Only includes roles with percentage >= threshold
        """
        try:
            # Get percentages
            role_percentages = self.get_role_percentages(job_description)
            
            # Get breakdown with threshold filtering
            breakdown = self.template_matcher.get_role_breakdown(role_percentages, threshold)
            
            # Check if primary role is below 50% and log warning
            if breakdown and breakdown[0][1] < 50:
                logger.warning(
                    f"Mixed role composition detected: Primary role '{breakdown[0][0]}' "
                    f"is only {breakdown[0][1]:.1f}% of the job description. "
                    f"This job may have multiple role responsibilities."
                )
            
            return breakdown
            
        except Exception as e:
            logger.error(f"Error calculating role breakdown: {e}")
            logger.error(f"Role breakdown failure details - Threshold: {threshold}, Error: {type(e).__name__}")
            return []
    
    def list_available_templates(self) -> List[Dict]:
        """List all available templates with both CV and CL paths"""
        templates = []

        for role_key, role_data in self.ROLE_CATEGORIES.items():
            cv_path = self.get_template_path(role_key, 'cv')
            cl_path = self.get_template_path(role_key, 'cl')
            templates.append({
                'role': role_key,
                'display_name': role_key.replace('_', ' ').title(),
                'keywords': role_data['keywords'],
                'priority': role_data['priority'],
                'cv_exists': cv_path is not None and cv_path.exists(),
                'cl_exists': cl_path is not None and cl_path.exists(),
                'cv_path': str(cv_path) if cv_path else None,
                'cl_path': str(cl_path) if cl_path else None
            })

        # Sort by priority
        templates.sort(key=lambda x: x['priority'])

        return templates
    
    def _handle_template_selection_failure(self, failed_role: str = None) -> str:
        """
        Handle template selection failures with proper fallback logic and logging
        
        Args:
            failed_role: The role that failed to have a valid template (optional)
            
        Returns:
            Fallback role category key
        """
        logger.error(f"Template selection failure detected")
        if failed_role:
            logger.error(f"Failed role: {failed_role}")
        
        # Try to get fallback template
        excluded_roles = [failed_role] if failed_role else []
        fallback_role = self.template_matcher.get_fallback_template(excluded_roles)
        
        # Verify fallback template exists
        fallback_template_path = self.get_template_path(fallback_role, 'cv')
        if fallback_template_path and fallback_template_path.exists():
            logger.info(f"Using fallback role: {fallback_role}")
            logger.info(f"Fallback template path: {fallback_template_path}")
            return fallback_role
        else:
            # Fallback template also doesn't exist - critical error
            logger.error(f"Critical error: Fallback template also missing for role: {fallback_role}")
            logger.error(f"Fallback template path: {fallback_template_path}")
            
            # Try to find any working template
            for role_key in self.ROLE_CATEGORIES.keys():
                if role_key in excluded_roles:
                    continue
                    
                test_path = self.get_template_path(role_key, 'cv')
                if test_path and test_path.exists():
                    logger.warning(f"Emergency fallback: Using first available template: {role_key}")
                    logger.warning(f"Emergency template path: {test_path}")
                    return role_key
            
            # No templates available at all - return default but log critical error
            logger.critical("Critical system error: No template files found for any role category")
            logger.critical("System may not be able to generate CVs")
            return 'devops_cloud'  # Return default even if file doesn't exist
    
    def _validate_template_content_alignment(self, role_category: str, job_description: str) -> bool:
        """
        Validate that template content aligns with the detected role category
        
        Args:
            role_category: The detected role category
            job_description: The job description to check against
            
        Returns:
            True if template content aligns with role, False otherwise
        """
        # Specific check: prevent FinTech template for pure DevOps jobs
        if role_category == 'devops_fintech':
            # Check if this is actually a pure DevOps/CI/CD job without financial domain
            devops_keywords = ['ci/cd', 'jenkins', 'gerrit', 'artifactory', 'kubernetes', 'docker', 'terraform']
            fintech_keywords = ['fintech', 'financial', 'banking', 'trading', 'payment', 'nasdaq', 'finance']
            
            job_lower = job_description.lower()
            devops_count = sum(1 for keyword in devops_keywords if keyword in job_lower)
            fintech_count = sum(1 for keyword in fintech_keywords if keyword in job_lower)
            
            # If strong DevOps focus but minimal FinTech mentions, this is misaligned
            if devops_count >= 3 and fintech_count <= 1:
                logger.warning(
                    f"Template content misalignment detected: FinTech template selected for pure DevOps job "
                    f"(DevOps keywords: {devops_count}, FinTech keywords: {fintech_count})"
                )
                return False
        
        # General alignment checks
        role_keywords = self.ROLE_CATEGORIES.get(role_category, {}).get('keywords', [])
        if not role_keywords:
            return True  # Can't validate without keywords
        
        job_lower = job_description.lower()
        matching_keywords = sum(1 for keyword in role_keywords if keyword.lower() in job_lower)
        
        # Template is aligned if at least 10% of role keywords are present (minimum 2 keywords)
        alignment_threshold = max(2, len(role_keywords) * 0.1)
        is_aligned = matching_keywords >= alignment_threshold
        
        if not is_aligned:
            logger.warning(
                f"Template content alignment concern: Role '{role_category}' has only "
                f"{matching_keywords}/{len(role_keywords)} matching keywords in job description"
            )
        
        return is_aligned
    
    def _select_alternative_template_for_misalignment(self, misaligned_role: str, job_description: str) -> str:
        """
        Select an alternative template when content misalignment is detected
        
        Args:
            misaligned_role: The role that was misaligned
            job_description: The job description to analyze
            
        Returns:
            Alternative role category with better alignment
        """
        logger.info(f"Selecting alternative template for misaligned role: {misaligned_role}")
        
        # Specific case: FinTech template misalignment -> use regular DevOps
        if misaligned_role == 'devops_fintech':
            logger.info("Using devops_cloud as alternative to devops_fintech")
            return 'devops_cloud'
        
        # General case: re-analyze without the misaligned role
        try:
            # Get all role scores
            role_scores = self.get_role_scores(job_description)
            
            # Remove the misaligned role
            if misaligned_role in role_scores:
                role_scores[misaligned_role] = 0
            
            # Select next best match
            best_role, best_score = self.template_matcher.select_best_match(role_scores)
            
            if best_role and best_score > 0:
                # Validate the alternative doesn't have the same issue
                if self._validate_template_content_alignment(best_role, job_description):
                    logger.info(f"Selected alternative template: {best_role}")
                    return best_role
                else:
                    logger.warning(f"Alternative template {best_role} also has alignment issues")
            
        except Exception as e:
            logger.error(f"Error selecting alternative template: {e}")
        
        # Fallback to safe default
        logger.info("Using fallback template due to alignment issues")
        return self.template_matcher.get_fallback_template([misaligned_role])


# Example usage and tests
if __name__ == '__main__':
    # Configure logging for demo
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    manager = CVTemplateManager()

    # Test job descriptions for different role categories
    test_jobs = {
        'android': """
            We are looking for an Android Platform Developer to work on automotive infotainment systems.
            You will work with Kotlin, Java, and AOSP to build cutting-edge mobile experiences.
        """,
        'fullstack': """
            Software Developer at Benifex. We need someone with Kubernetes, Docker, Grafana,
            TypeScript, Go, Java, Spring Boot, CI/CD, Monitoring, Observability.
            Fullstack experience with React and backend development required.
        """,
        'backend_java': """
            Backend Developer needed. Strong Java and Spring Boot experience required.
            You will build microservices and RESTful APIs using Hibernate and JPA.
        """,
        'devops': """
            DevOps Engineer position. Must have experience with AWS, Kubernetes, Terraform,
            and CI/CD pipelines. Infrastructure as Code experience required.
        """,
        'fintech': """
            FinTech Engineer at Nasdaq. Experience with trading systems, payment processing,
            and financial compliance required. Banking experience is a plus.
        """,
        'it_support': """
            IT Support Specialist needed. Experience with helpdesk, service desk, ITIL.
            L2/L3 support experience required. Ticketing system knowledge needed.
        """,
        'mixed_role': """
            Senior Software Engineer position. We need someone with strong React and TypeScript
            experience for frontend work, plus Python and Flask for backend APIs. You'll also
            help with our Kubernetes deployment and CI/CD pipelines. Experience integrating
            AI features using OpenAI API is a plus.
        """
    }

    print("=" * 60)
    print("ROLE DETECTION TEST WITH PERCENTAGES")
    print("=" * 60)

    for test_name, job_desc in test_jobs.items():
        print(f"\n{test_name.upper()} job:")
        
        # Detect role
        detected = manager.analyze_job_role(job_desc)
        print(f"  Detected: {detected}")
        
        # Get percentage breakdown
        breakdown = manager.get_role_breakdown(job_desc, threshold=5.0)
        print(f"  Role breakdown (>5%):")
        for role, percentage in breakdown:
            print(f"    - {role}: {percentage:.1f}%")

    print("\n" + "=" * 60)
    print("AVAILABLE TEMPLATES (sorted by priority)")
    print("=" * 60)

    for template in manager.list_available_templates():
        cv_status = "✓" if template['cv_exists'] else "✗"
        cl_status = "✓" if template['cl_exists'] else "✗"
        print(f"  P{template['priority']} {template['display_name']}: CV={cv_status} CL={cl_status}")
