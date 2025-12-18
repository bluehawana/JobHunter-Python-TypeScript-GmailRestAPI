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
    ROLE_CATEGORIES = {
        'android_developer': {
            'keywords': ['android', 'kotlin', 'java', 'mobile', 'aosp', 'automotive', 'infotainment'],
            'template_path': 'job_applications/ecarx_android_developer',  # Ecarx Android developer resume
            'priority': 1
        },
        'devops_cloud': {
            'keywords': ['devops', 'cloud', 'aws', 'azure', 'gcp', 'kubernetes', 'docker', 'terraform', 'ci/cd', 'infrastructure'],
            'template_path': 'job_applications/nasdaq_devops_cloud',
            'priority': 2
        },
        'incident_management_sre': {
            'keywords': ['incident', 'sre', 'site reliability', 'on-call', 'monitoring', 'observability', 'mttr', 'production support'],
            'template_path': 'job_applications/tata_incident_management',
            'priority': 3
        },
        'fullstack_developer': {
            'keywords': ['fullstack', 'full-stack', 'full stack', 'react', 'vue', 'angular', 'node.js', 'frontend', 'backend'],
            'template_path': 'job_applications/doit_international',
            'priority': 4
        },
        'ict_software_engineer': {
            'keywords': ['ict', 'software engineer', 'application', '.net', 'c#', 'java', 'spring boot'],
            'template_path': 'job_applications/Ascom_ICT_Software_Engineer.tex',
            'priority': 5
        },
        'platform_engineer': {
            'keywords': ['platform engineer', 'platform', 'infrastructure', 'internal tools', 'developer experience'],
            'template_path': 'job_applications/Thomson_Reuters_Platform_Engineer.tex',
            'priority': 6
        },
        'integration_architect': {
            'keywords': ['integration', 'architect', 'api', 'microservices', 'system integration', 'middleware'],
            'template_path': 'job_applications/VFS_Integration_Architect.tex',
            'priority': 7
        },
        'backend_developer': {
            'keywords': ['backend', 'api', 'database', 'server', 'microservices', 'rest', 'graphql'],
            'template_path': 'job_applications/Telia_Backend_Developer.tex',
            'priority': 8
        }
    }
    
    def __init__(self, templates_dir: str = 'job_applications'):
        # Get absolute path relative to this file's location
        base_dir = Path(__file__).parent
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
        
        # Return role with highest score
        if role_scores:
            best_role = max(role_scores, key=role_scores.get)
            if role_scores[best_role] > 0:
                return best_role
        
        # Default to devops_cloud if no clear match
        return 'devops_cloud'
    
    def get_template_path(self, role_category: str) -> Optional[Path]:
        """Get the template path for a given role category"""
        if role_category in self.ROLE_CATEGORIES:
            template_path = self.ROLE_CATEGORIES[role_category]['template_path']
            full_path = Path(template_path)
            
            # Check if it's a directory or file
            if full_path.is_dir():
                # Look for CV tex file in directory
                cv_files = list(full_path.glob('*_CV.tex'))
                if cv_files:
                    return cv_files[0]
            elif full_path.exists():
                return full_path
        
        return None
    
    def load_template(self, role_category: str) -> Optional[str]:
        """Load template content for a given role category"""
        template_path = self.get_template_path(role_category)
        
        if template_path and template_path.exists():
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error loading template: {e}")
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
        """List all available templates"""
        templates = []
        
        for role_key, role_data in self.ROLE_CATEGORIES.items():
            template_path = self.get_template_path(role_key)
            templates.append({
                'role': role_key,
                'display_name': role_key.replace('_', ' ').title(),
                'keywords': role_data['keywords'],
                'template_exists': template_path is not None and template_path.exists(),
                'template_path': str(template_path) if template_path else None
            })
        
        return templates


# Example usage
if __name__ == '__main__':
    manager = CVTemplateManager()
    
    # Test with Android job
    android_jd = """
    We are looking for an Android Platform Developer to work on automotive infotainment systems.
    You will work with Kotlin, Java, and AOSP to build cutting-edge mobile experiences.
    """
    
    role = manager.analyze_job_role(android_jd)
    print(f"Detected role: {role}")
    print(f"Role info: {manager.get_role_info(role)}")
    
    # List all templates
    print("\nAvailable templates:")
    for template in manager.list_available_templates():
        print(f"  - {template['display_name']}: {template['template_exists']}")
