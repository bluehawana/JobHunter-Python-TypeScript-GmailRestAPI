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
        self.api_key = api_key or os.getenv('MINIMAX_API_KEY') or os.getenv('maxmini_apikey')
        self.model = model
        
        # Initialize Anthropic client with MiniMax base URL
        if ANTHROPIC_AVAILABLE and self.api_key:
            # For international users
            base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://api.minimax.io/anthropic')
            # For China users, use: https://api.minimaxi.com/anthropic
            
            self.client = anthropic.Anthropic(
                api_key=self.api_key,
                base_url=base_url
            )
            logger.info(f"Initialized Anthropic client with base_url: {base_url}")
        else:
            self.client = None
            if not ANTHROPIC_AVAILABLE:
                logger.warning("Anthropic SDK not available")
            if not self.api_key:
                logger.warning("API key not configured")
        
        # Role categories that the AI can select from
        self.role_categories = [
            'android_developer',
            'devops_cloud',
            'incident_management_sre',
            'fullstack_developer',
            'ict_software_engineer',
            'platform_engineer',
            'integration_architect',
            'backend_developer'
        ]
    
    def is_available(self) -> bool:
        """Check if AI analysis is available"""
        available = bool(self.api_key and self.client and ANTHROPIC_AVAILABLE)
        if available:
            logger.info("AI Analyzer is available with Minimax M2")
        else:
            if not ANTHROPIC_AVAILABLE:
                logger.warning("AI Analyzer not available - anthropic package not installed")
            elif not self.api_key:
                logger.warning("AI Analyzer not available - API key not configured")
            else:
                logger.warning("AI Analyzer not available - client not initialized")
        return available
    
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
            
            # Call Minimax API via Anthropic SDK
            logger.info("Calling MiniMax M2 via Anthropic SDK...")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
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
        """Build the prompt for Minimax M2"""
        
        categories_desc = "\n".join([f"- {cat}" for cat in self.role_categories])
        
        # Limit job description to avoid token limits
        jd_text = job_description[:2000] if len(job_description) > 2000 else job_description
        
        prompt = f"""Analyze this job description and determine the most appropriate role category.

Available role categories:
{categories_desc}

Job Description:
{jd_text}

Please respond in JSON format with:
{{
    "role_category": "<one of the categories above>",
    "confidence": <0.0 to 1.0>,
    "reasoning": "<brief explanation>",
    "key_technologies": ["<tech1>", "<tech2>", ...]
}}

Focus on:
1. Primary technical skills required (e.g., Android, Kubernetes, CI/CD tools)
2. Job responsibilities (e.g., incident management, full-stack development)
3. Specific tools mentioned (e.g., Jenkins, Gerrit, React, Kotlin)

Important: 
- For CI/CD DevOps roles emphasizing Jenkins, Gerrit, Artifactory, select 'devops_cloud'
- For Android/mobile development, select 'android_developer'
- For incident management/SRE roles, select 'incident_management_sre'
- Avoid selecting roles with irrelevant focus (e.g., don't select FinTech-focused templates for pure DevOps roles)"""
        
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
