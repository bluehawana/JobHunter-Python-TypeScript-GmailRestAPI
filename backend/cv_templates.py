"""
🧱 CV Template Manager
Manages role-specific CV templates for intelligent matching
"""

from pathlib import Path
from typing import Dict, List, Optional
import re

class CVTemplateManager:
    """Manages CV templates for different roles"""
    
    # Role categories and their keywords
    # Now using REAL templates from job_applications/ folder
    # Priority: Lower number = higher priority (checked first)
    # Tip: More specific roles should have lower priority numbers
    ROLE_CATEGORIES = {
        # === SPECIALIZED ROLES (Priority 1) - Check these first ===
        'it_business_analyst': {
            'keywords': ['business analyst', 'it analyst', 'it business analyst', 'business requirements', 'stakeholder', 'business process', 'gap analysis', 'power bi', 'visio', 'workshop', 'requirements gathering', 'business case', 'process improvement', 'digitalization', 'bridge between'],
            'cv_template': 'job_applications/incluso_it_business_analyst/Incluso_IT_Business_Analyst_CV.tex',
            'cl_template': 'job_applications/incluso_it_business_analyst/Incluso_IT_Business_Analyst_CL.tex',
            'priority': 1
        },
        'android_developer': {
            'keywords': ['android', 'kotlin', 'android app', 'apk', 'mobile app', 'aosp', 'android sdk', 'jetpack', 'react native', 'mobile developer'],
            'cv_template': 'job_applications/ecarx_android_developer/Ecarx_Android_Developer_CV.tex',
            'cl_template': 'job_applications/ecarx_android_developer/Ecarx_Android_Developer_CL.tex',
            'priority': 1
        },
        'devops_fintech': {
            'keywords': ['fintech', 'financial', 'banking', 'payment', 'trading', 'nasdaq', 'finance', 'post-trade', 'settlement', 'compliance'],
            'cv_template': 'job_applications/nasdaq_devops_cloud/Nasdaq_DevOps_Cloud_Harvad_CV.tex',
            'cl_template': 'job_applications/nasdaq_devops_cloud/Nasdaq_DevOps_Cloud_Harvad_CL.tex',
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
            'cv_template': 'job_applications/omnimodular_ai_product_engineer/Omnimodular_AI_Product_Engineer_CV.tex',
            'cl_template': 'job_applications/omnimodular_ai_product_engineer/Omnimodular_AI_Product_Engineer_CL.tex',
            'priority': 1
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
            'cv_template': 'job_applications/ahlsell_fullstack/Ahlsell_Fullstack_CV.tex',
            'cl_template': 'job_applications/ahlsell_fullstack/Ahlsell_Fullstack_CL.tex',
            'priority': 2
        },

        # === BACKEND-FOCUSED (Priority 3) ===
        'backend_developer': {
            'keywords': [
                'backend developer', 'back-end developer', 'api developer',
                'java developer', 'spring boot', 'spring framework', 'hibernate', 'jpa',
                'microservices', 'server-side', 'restful api',
                # AI integration keywords (using AI, not building AI)
                'integrating ai', 'ai integration', 'using ai', 'leverage ai',
                'ai-powered features', 'ai capabilities', 'llm integration',
                'openai api', 'claude api', 'gpt api', 'ai apis',
                'generative ai solutions', 'ai solutions', 'llm-based applications'
            ],
            'cv_template': 'job_applications/eworks_java/eWorks_Complete_CV_20251120.tex',
            'cl_template': 'job_applications/eworks_java/eWorks_Complete_CL_20251120.tex',
            'priority': 3
        },

        # === DEVOPS/INFRASTRUCTURE (Priority 4) ===
        'devops_cloud': {
            'keywords': ['devops', 'cloud engineer', 'aws', 'azure', 'gcp', 'kubernetes', 'docker', 'terraform', 'ci/cd', 'infrastructure as code', 'iac', 'helm', 'argocd'],
            'cv_template': 'job_applications/alten_cloud/ALTEN_Cloud_Engineer_Harvad_CV.tex',
            'cl_template': 'job_applications/alten_cloud/ALTEN_Cloud_Engineer_Harvad_CL.tex',
            'priority': 4
        },
        'incident_management_sre': {
            'keywords': ['incident', 'sre', 'site reliability', 'on-call', 'monitoring', 'observability', 'mttr', 'production support', 'pagerduty', 'opsgenie', 'incident management'],
            'cv_template': 'job_applications/tata_incident_management/Tata_Incident_Management_Harvad_CV.tex',
            'cl_template': 'job_applications/tata_incident_management/Tata_Incident_Management_Harvad_CL.tex',
            'priority': 4
        },
        'platform_engineer': {
            'keywords': ['platform engineer', 'platform team', 'internal tools', 'developer experience', 'devex', 'infrastructure platform', 'golden path'],
            'cv_template': 'job_applications/essity/Essity_Cloud_DevOps_CV_Overleaf.tex',
            'cl_template': 'job_applications/essity/Essity_Cloud_DevOps_CL_Overleaf.tex',
            'priority': 5
        },

        # === IT SUPPORT / OPERATIONS (Priority 5) ===
        'it_support': {
            'keywords': ['it support', 'helpdesk', 'service desk', 'technical support', 'support engineer', 'it technician', 'desktop support', 'l1', 'l2', 'l3 support', 'itil', 'ticketing'],
            'cv_template': 'job_applications/tata_incident_management/Tata_Incident_Management_Harvad_CV.tex',
            'cl_template': 'job_applications/tata_incident_management/Tata_Incident_Management_Harvad_CL.tex',
            'priority': 5
        },

        # === FINOPS / COST OPTIMIZATION (Priority 5) ===
        'finops': {
            'keywords': ['finops', 'cloud cost', 'cost optimization', 'cloud economics', 'cloud billing', 'reserved instances', 'savings plans', 'cost management', 'cloud financial'],
            'cv_template': 'job_applications/alten_cloud/ALTEN_Cloud_Engineer_Harvad_CV.tex',
            'cl_template': 'job_applications/alten_cloud/ALTEN_Cloud_Engineer_Harvad_CL.tex',
            'priority': 5
        },

        # === ARCHITECT ROLES (Priority 6) ===
        'integration_architect': {
            'keywords': ['integration architect', 'solution architect', 'enterprise architect', 'api architect', 'system integration', 'middleware', 'esb', 'mulesoft', 'api gateway'],
            'cv_template': 'job_applications/gothenburg_devops_cicd/Gothenburg_DevOps_CICD_Harvad_CV.tex',
            'cl_template': 'job_applications/gothenburg_devops_cicd/Gothenburg_DevOps_CICD_Harvad_CL.tex',
            'priority': 6
        },

        # === GENERIC CLOUD (Priority 7) - Fallback ===
        'cloud_engineer': {
            'keywords': ['cloud', 'infrastructure', 'cloud platform', 'cloud architecture', 'cloud migration', 'cloud native'],
            'cv_template': 'job_applications/alten_cloud/ALTEN_Cloud_Engineer_Harvad_CV.tex',
            'cl_template': 'job_applications/alten_cloud/ALTEN_Cloud_Engineer_Harvad_CL.tex',
            'priority': 7
        }
    }
    
    def __init__(self, templates_dir: str = 'templates/cv_templates'):
        # Get absolute path relative to project root
        base_dir = Path(__file__).parent.parent  # Go up to project root
        self.templates_dir = base_dir / templates_dir
    
    def analyze_job_role(self, job_description: str) -> str:
        """
        Analyze job description and determine the best matching role category

        Returns:
            Role category key (e.g., 'android_developer', 'devops_cloud')
        """
        job_lower = job_description.lower()

        # Score each role category
        role_scores = {}

        for role_key, role_data in self.ROLE_CATEGORIES.items():
            score = 0
            keywords = role_data['keywords']

            for keyword in keywords:
                # Count occurrences of each keyword
                count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', job_lower))
                score += count

            # Apply priority weight (lower priority number = higher weight)
            weighted_score = score / role_data['priority']
            role_scores[role_key] = weighted_score

        # Calculate total score for percentage calculation
        total_score = sum(role_scores.values())
        
        # Return role with highest score
        if role_scores and total_score > 0:
            best_role = max(role_scores, key=role_scores.get)
            if role_scores[best_role] > 0:
                # Prevent AI product template from overriding software engineering roles.
                # AI Product Engineer = building AI systems (model training, RAG, MLOps)
                # Software Engineer with AI = building software that uses AI APIs
                if best_role == 'ai_product_engineer':
                    # Calculate percentage of AI Product Engineer work
                    ai_percentage = (role_scores['ai_product_engineer'] / total_score) * 100
                    
                    # AI Product Engineer requires at least 50% AI-specific work
                    if ai_percentage < 50:
                        # This is likely a software engineering role with AI integration
                        # Remove AI Product Engineer from consideration
                        role_scores['ai_product_engineer'] = 0
                        best_role = max(role_scores, key=role_scores.get)
                
                return best_role

        # Default to devops_cloud if no clear match
        return 'devops_cloud'
    
    def get_template_path(self, role_category: str, template_type: str = 'cv') -> Optional[Path]:
        """
        Get the template path for a given role category

        Args:
            role_category: The role category key (e.g., 'fullstack_developer')
            template_type: 'cv' or 'cl' for CV or Cover Letter template

        Returns:
            Path to the template file, or None if not found
        """
        if role_category in self.ROLE_CATEGORIES:
            # Support both old 'template_path' key and new 'cv_template'/'cl_template' keys
            role_data = self.ROLE_CATEGORIES[role_category]

            if template_type == 'cl':
                template_path_str = role_data.get('cl_template', role_data.get('template_path'))
            else:
                template_path_str = role_data.get('cv_template', role_data.get('template_path'))

            if not template_path_str:
                return None

            # Get absolute path from project root
            base_dir = Path(__file__).parent.parent  # Go up to project root
            full_path = base_dir / template_path_str

            # Check if file exists
            if full_path.exists() and full_path.is_file():
                return full_path

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
        template_path = self.get_template_path(role_category, template_type)

        if template_path and template_path.exists():
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error loading {template_type.upper()} template: {e}")
                return None

        return None
    
    def get_role_info(self, role_category: str) -> Dict:
        """Get information about a role category"""
        if role_category in self.ROLE_CATEGORIES:
            role_data = self.ROLE_CATEGORIES[role_category].copy()
            role_data['category'] = role_category
            role_data['display_name'] = role_category.replace('_', ' ').title()
            return role_data
        
        return {}
    
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


# Example usage and tests
if __name__ == '__main__':
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
        """
    }

    print("=" * 60)
    print("ROLE DETECTION TEST")
    print("=" * 60)

    for test_name, job_desc in test_jobs.items():
        detected = manager.analyze_job_role(job_desc)
        print(f"\n{test_name.upper()} job -> Detected: {detected}")

    print("\n" + "=" * 60)
    print("AVAILABLE TEMPLATES (sorted by priority)")
    print("=" * 60)

    for template in manager.list_available_templates():
        cv_status = "✓" if template['cv_exists'] else "✗"
        cl_status = "✓" if template['cl_exists'] else "✗"
        print(f"  P{template['priority']} {template['display_name']}: CV={cv_status} CL={cl_status}")
