"""
AI-Enhanced Job Description Analyzer using Minimax M2
Provides semantic analysis beyond keyword matching
"""

import os
import json
from typing import Dict, Tuple, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import anthropic
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("anthropic package not installed. Install with: pip install anthropic")

# Load environment variables from .env files if they exist
def load_env_file():
    """Load environment variables from .env files"""
    # Try multiple locations
    env_paths = [
        Path(__file__).parent.parent / '.env',  # Root .env
        Path(__file__).parent.parent / '.idea' / '.env',  # .idea/.env
    ]
    
    for env_path in env_paths:
        if env_path.exists() and env_path.stat().st_size > 0:
            logger.debug(f"Loading env from: {env_path}")
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Support both = and : as separators
                        if '=' in line:
                            key, value = line.split('=', 1)
                        elif ':' in line:
                            key, value = line.split(':', 1)
                        else:
                            continue
                        
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and value:  # Only set if both key and value exist
                            os.environ[key] = value
                            logger.debug(f"Loaded env var: {key}")

load_env_file()


class AIAnalyzer:
    """Analyzes job descriptions using Minimax M2 AI model"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "MiniMax-M2"):
        """
        Initialize AI Analyzer with Minimax M2
        
        Args:
            api_key: Minimax API key (JWT token from env variable)
            model: Minimax model to use (MiniMax-M2 for M2)
        """
        # Try to get API key from multiple sources
        self.api_key = (
            api_key or 
            os.getenv('ANTHROPIC_API_KEY') or  # MiniMax via Anthropic SDK
            os.getenv('MINIMAX_SECRET_KEY') or  # Alternative name
            os.getenv('MINIMAX_API_KEY') or 
            os.getenv('maxmini_apikey')
        )
        self.model = model
        
        # Initialize configuration (no anthropic client needed - using HTTP requests)
        if self.api_key:
            base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
            logger.info(f"Configured for Z.AI GLM-4.7 with base_url: {base_url}")
            self.client = None  # We use HTTP requests instead
        else:
            self.client = None
            logger.warning("API key not configured")
        
        # Role categories loaded from cv_templates.py for single source of truth
        from cv_templates import CVTemplateManager
        self.template_manager = CVTemplateManager()
        self.role_categories = list(self.template_manager.ROLE_CATEGORIES.keys())

        # Role descriptions for LLM context
        self.role_descriptions = {
            'it_business_analyst': 'IT Business Analyst, business requirements, stakeholder management, gap analysis, process improvement, digitalization, bridge IT and business, Power BI, Visio, workshops',
            'android_developer': 'Android/Kotlin/mobile app development, AOSP, Android SDK, automotive infotainment',
            'devops_fintech': 'DevOps for financial/banking/trading systems, FinTech, Nasdaq, payment processing',
            'ai_product_engineer': 'AI/ML engineering, LLM, GPT, machine learning, deep learning, neural networks',
            'fullstack_developer': 'Full-stack web development with React/Vue/Angular frontend + backend, TypeScript, JavaScript',
            'backend_developer': 'Backend/API development with Java, Spring Boot, microservices, server-side',
            'devops_cloud': 'Cloud infrastructure, DevOps, AWS/Azure/GCP, Kubernetes, Docker, Terraform, CI/CD',
            'incident_management_sre': 'SRE, incident management, on-call, production support, monitoring, observability',
            'platform_engineer': 'Platform engineering, internal tools, developer experience, infrastructure platform',
            'it_support': 'IT support, customer support, technical support, helpdesk, service desk, user support, troubleshooting user issues, ITIL, ticketing systems, customer service',
            'finops': 'FinOps, cloud cost optimization, cloud economics, billing, reserved instances',
            'integration_architect': 'Solution/integration architect, API architecture, system integration, middleware',
            'cloud_engineer': 'Generic cloud engineering, cloud platform, cloud migration, cloud native'
        }
    
    def is_available(self) -> bool:
        """Check if AI analysis is available"""
        # For HTTP requests, we only need the API key and requests library
        available = bool(self.api_key)
        if available:
            logger.info("AI Analyzer is available with Z.AI GLM-4.7 (HTTP)")
        else:
            logger.warning("AI Analyzer not available - API key not configured")
        return available
    
    def analyze_job_for_ats_optimization(self, job_description: str) -> Optional[Dict]:
        """
        Analyze job description and provide ATS optimization recommendations
        
        Returns:
            Dict with:
            - recommended_template: Best template to use
            - programming_language: Primary language (java, dotnet, python, etc.)
            - critical_keywords: Must-have keywords for ATS
            - skills_to_emphasize: Skills to highlight prominently
            - experience_focus: Which work experiences to emphasize
            - customization_tips: Specific tips for this job
            - ats_score_potential: Estimated ATS match potential (0-100)
        """
        if not self.is_available():
            logger.warning("AI analysis not available for ATS optimization")
            return None
        
        try:
            prompt = f"""You are an ATS (Applicant Tracking System) optimization expert. Analyze this job description and provide specific recommendations to maximize ATS screening success.

JOB DESCRIPTION:
{job_description[:4000]}

Provide your analysis in this EXACT JSON format:
{{
    "recommended_template": "java_backend_developer|dotnet_backend_developer|python_backend_developer|fullstack_developer|devops_cloud|azure_solution_architect|android_developer|project_manager",
    "programming_language": "java|dotnet|python|javascript|kotlin|multiple",
    "critical_keywords": ["keyword1", "keyword2", "keyword3"],
    "skills_to_emphasize": ["skill1", "skill2", "skill3"],
    "experience_focus": ["company1: reason", "company2: reason"],
    "customization_tips": ["tip1", "tip2", "tip3"],
    "ats_score_potential": 85,
    "reasoning": "Brief explanation of recommendations"
}}

ANALYSIS RULES:
1. **Programming Language Detection**: Identify the PRIMARY language (Java, .NET/C#, Python, etc.)
2. **Critical Keywords**: Extract 5-10 keywords that MUST appear in the CV for ATS
3. **Skills to Emphasize**: List specific technical skills to highlight prominently
4. **Experience Focus**: Which past companies/roles to emphasize and why
5. **Customization Tips**: Specific changes to make for this job
6. **ATS Score**: Estimate match potential (0-100) based on candidate's background

IMPORTANT:
- If job mentions "Java", "Spring Boot", "Maven" -> recommend "java_backend_developer"
- If job mentions ".NET", "C#", "ASP.NET" -> recommend "dotnet_backend_developer"
- If job mentions "Azure", "Microsoft 365", "SharePoint" -> recommend "azure_solution_architect"
- If job mentions "Android", "Kotlin", "mobile" -> recommend "android_developer"
- Critical keywords should be exact phrases from the job description
- Focus on technical skills, not soft skills
- Be specific about which work experiences to emphasize

Return ONLY the JSON, no other text."""

            import requests
            
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.minimax.io/anthropic')
            
            if not api_key:
                logger.error("ANTHROPIC_API_KEY not found")
                return None
            
            url = f"{base_url}/v1/messages"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'anthropic-version': '2023-06-01'
            }
            
            payload = {
                "model": "glm-4.7",
                "max_tokens": 4096,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            http_response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if http_response.status_code == 200:
                result_data = http_response.json()
                
                # Extract text from response
                ai_response_text = ""
                if 'content' in result_data:
                    for block in result_data['content']:
                        if block.get('type') == 'text':
                            ai_response_text += block.get('text', '')
                
                # Parse JSON from response
                import re
                json_match = re.search(r'\{.*\}', ai_response_text, re.DOTALL)
                if json_match:
                    ats_recommendations = json.loads(json_match.group())
                    logger.info(f"✅ ATS optimization analysis completed: {ats_recommendations['recommended_template']}")
                    return ats_recommendations
                else:
                    logger.error("Failed to parse JSON from AI response")
                    return None
            else:
                logger.error(f"❌ ATS optimization request failed: {http_response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"ATS optimization analysis failed: {e}", exc_info=True)
            return None

    def analyze_job_description(self, job_description: str) -> Optional[Dict]:
        """
        Analyze job description using Minimax M2
        
        Args:
            job_description: The job description text
            
        Returns:
            Dict with role_category, confidence, reasoning, and keywords
        """
        if not self.is_available():
            logger.warning("AI analysis not available")
            return None
        
        try:
            # Construct prompt for Minimax M2
            prompt = self._build_analysis_prompt(job_description)
            
            # Call Minimax API via direct HTTP requests (more reliable than anthropic client)
            logger.info("Calling MiniMax M2.1 via HTTP requests...")
            
            import requests
            import os
            
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.minimax.io/anthropic')
            
            if not api_key:
                logger.error("ANTHROPIC_API_KEY not found")
                return None
            
            url = f"{base_url}/v1/messages"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'anthropic-version': '2023-06-01'
            }
            
            payload = {
                "model": "glm-4.7",  # Z.AI GLM-4.7 model
                "max_tokens": 4096,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            http_response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if http_response.status_code == 200:
                result_data = http_response.json()
                logger.info("✅ MiniMax M2.1 HTTP request successful!")
                
                # Extract text from response
                ai_response_text = ""
                if 'content' in result_data:
                    for block in result_data['content']:
                        if block.get('type') == 'text':
                            ai_response_text += block.get('text', '')
                
                # Create a mock response object for compatibility with existing parsing
                class MockBlock:
                    def __init__(self, text):
                        self.type = "text"
                        self.text = text
                
                class MockResponse:
                    def __init__(self, text):
                        self.content = [MockBlock(text)]
                
                response = MockResponse(ai_response_text)
            else:
                logger.error(f"❌ MiniMax M2.1 HTTP request failed: {http_response.status_code}")
                logger.error(f"📝 Response: {http_response.text}")
                return None
            
            # Parse response
            result = self._parse_ai_response(response)
            
            logger.info(f"AI analysis completed: {result['role_category']} (confidence: {result['confidence']})")
            return result
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}", exc_info=True)
            return None
    
    def extract_role_type(self, job_description: str) -> Tuple[Optional[str], float]:
        """
        Extract role type and confidence from job description
        
        Args:
            job_description: The job description text
            
        Returns:
            Tuple of (role_category, confidence_score)
        """
        result = self.analyze_job_description(job_description)
        
        if result:
            return result['role_category'], result['confidence']
        
        return None, 0.0
    
    def _build_analysis_prompt(self, job_description: str) -> str:
        """Build the prompt for Minimax M2 with detailed role descriptions"""

        # Build categories with descriptions
        categories_with_desc = []
        for cat in self.role_categories:
            desc = self.role_descriptions.get(cat, cat.replace('_', ' '))
            categories_with_desc.append(f"- {cat}: {desc}")
        categories_desc = "\n".join(categories_with_desc)

        # Limit job description to avoid token limits
        jd_text = job_description[:3000] if len(job_description) > 3000 else job_description

        prompt = f"""You are a job classification expert. Analyze this job description and select the MOST appropriate role category.

AVAILABLE ROLE CATEGORIES (select ONE):
{categories_desc}

JOB DESCRIPTION:
{jd_text}

CLASSIFICATION RULES (follow strictly):
1. If job mentions "fullstack", "full-stack", "frontend AND backend", "React" + backend tech -> select 'fullstack_developer'
2. If job is primarily Java/Spring Boot backend with no frontend -> select 'backend_developer'
3. If job mentions Android, Kotlin, mobile, AOSP -> select 'android_developer'
4. If job mentions FinTech, banking, trading, payment, Nasdaq -> select 'devops_fintech'
5. ONLY select 'ai_product_engineer' if the job is PRIMARILY about BUILDING AI systems (model training, model fine-tuning, prompt engineering, RAG systems, vector databases, embeddings). Do NOT select this if the job just mentions using/integrating AI APIs (like OpenAI, Azure AI, AWS Bedrock) as one of many features.
6. If job mentions building web applications with React/Node/Flask/Django AND also mentions AI/ML integration -> select 'fullstack_developer' (software engineer with AI skills, not AI engineer)
7. IMPORTANT: If job mentions "customer support", "technical support", "support engineer", "helpdesk", "service desk", "user support" -> select 'it_support' (takes priority over DevOps even if networking/troubleshooting mentioned)
8. If job mentions DevOps, Kubernetes, Docker, Terraform, CI/CD (without customer support focus) -> select 'devops_cloud'
9. If job mentions SRE, incident, on-call, monitoring -> select 'incident_management_sre'
10. If job mentions FinOps, cloud cost optimization -> select 'finops'
11. If job mentions architect, integration, middleware -> select 'integration_architect'
12. Default to 'devops_cloud' if unclear

CUSTOMER SUPPORT vs DEVOPS DISTINCTION:
- Customer Support: Primary focus is helping users/customers with technical issues, troubleshooting user problems, providing technical assistance
- DevOps: Primary focus is infrastructure automation, CI/CD pipelines, cloud platforms, system reliability
- If job mentions BOTH customer support AND DevOps technologies -> customer support wins (it's likely a technical support role that uses DevOps tools)
- Keywords like "networking" and "troubleshooting" can apply to both, but customer-facing roles should be classified as 'it_support'

IMPORTANT DISTINCTION - AI Product Engineer vs Software Engineer with AI skills:
- AI Product Engineer: Primary focus is BUILDING AI/ML systems - model training, fine-tuning, MLOps, prompt engineering, RAG, vector databases
- Software Engineer with AI: Primary focus is building software (web apps, APIs) that USES AI APIs like OpenAI/Claude/Azure AI as a feature
- If the job requires fullstack skills (React, Node, Flask, PostgreSQL) AND mentions AI integration -> this is 'fullstack_developer', NOT 'ai_product_engineer'
- Look at the PRIMARY job responsibilities, not just the technologies listed

PRIORITY ORDER for ambiguous cases:
- If job mentions web application development + AI integration -> 'fullstack_developer' wins
- Specialized roles (android, fintech) take priority over generic roles
- Fullstack takes priority over backend when frontend is mentioned
- DevOps/Cloud is the fallback when nothing specific matches

Respond ONLY in this JSON format:
{{
    "role_category": "<exactly one category from the list>",
    "confidence": <0.0 to 1.0>,
    "reasoning": "<one sentence explaining why this category>",
    "key_technologies": ["<tech1>", "<tech2>", "<tech3>", ...]
}}"""

        return prompt
    
    def _parse_ai_response(self, response) -> Dict:
        """Parse Minimax API response (via Anthropic SDK)"""
        
        try:
            # Extract text from Anthropic response
            # response.content is a list of ContentBlock objects
            content = ""
            
            for block in response.content:
                if block.type == "text":
                    content += block.text
                elif block.type == "thinking":
                    # MiniMax M2 may include thinking blocks
                    logger.debug(f"Thinking: {block.thinking}")
            
            if not content:
                logger.error(f"No text content in response")
                return self._default_result()
            
            logger.debug(f"AI response content: {content[:200]}...")
            
            # Try to parse as JSON
            # Remove markdown code blocks if present
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            
            # Validate role category
            if result['role_category'] not in self.role_categories:
                logger.warning(f"AI returned invalid role category: {result['role_category']}, defaulting to devops_cloud")
                result['role_category'] = 'devops_cloud'
            
            # Ensure confidence is between 0 and 1
            result['confidence'] = max(0.0, min(1.0, float(result['confidence'])))
            
            return result
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Response content: {content if 'content' in locals() else 'N/A'}")
            return self._default_result()
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}", exc_info=True)
            return self._default_result()
    
    def _default_result(self) -> Dict:
        """Return default result when AI analysis fails"""
        return {
            'role_category': 'devops_cloud',
            'confidence': 0.0,
            'reasoning': 'AI analysis failed, using default',
            'key_technologies': []
        }


# Example usage and testing
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    analyzer = AIAnalyzer()
    
    print(f"API Key loaded: {bool(analyzer.api_key)}")
    if analyzer.api_key:
        print(f"API Key (first 50 chars): {analyzer.api_key[:50]}...")
    
    if analyzer.is_available():
        # Test with CI/CD job description
        test_jd = """
        The client is in Gothenburg, Sweden. Here are the requirements:
        Key skills: 
        - Master of Science in Computer Science
        - Professional knowledge in building robust CI services: Gerrit, Jenkins, Artifactory, SonarQube
        - Cloud knowledge in Azure and AWS
        - Scripting: Python, C#, Terraform
        - GitOps way of working
        - Kubernetes orchestration
        - Monitoring: Prometheus, Grafana
        """
        
        print("\n" + "="*60)
        print("Testing AI Analysis with CI/CD Job Description")
        print("="*60)
        
        result = analyzer.analyze_job_description(test_jd)
        
        if result:
            print(f"\n✓ Analysis successful!")
            print(f"Role Category: {result['role_category']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Reasoning: {result['reasoning']}")
            print(f"Key Technologies: {', '.join(result['key_technologies'])}")
        else:
            print("\n✗ Analysis failed")
    else:
        print("\n✗ AI Analyzer not available - API key not configured")
        print("Please set maxmini_apikey in .idea/.env file")
