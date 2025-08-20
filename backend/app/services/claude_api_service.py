import os
import logging
import asyncio
import aiohttp
import subprocess
from typing import Dict, Optional, Tuple
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ClaudeAPIService:
    """
    Claude API service with third-party provider fallback
    Uses anyrouter.top as primary, falls back to official Anthropic API
    """
    
    def __init__(self):
        # Third-party API configuration (primary)
        self.third_party_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
        self.third_party_base_url = os.getenv("ANTHROPIC_BASE_URL", "https://anyrouter.top")
        self.third_party_model = os.getenv("CLAUDE_MODEL", "claude-3-7-sonnet-20250219")
        
        # Official Anthropic API configuration (fallback)
        self.official_token = os.getenv("ANTHROPIC_OFFICIAL_API_KEY")
        self.official_base_url = "https://api.anthropic.com"
        self.official_model = "claude-3-5-sonnet-20241022"  # Limited to Sonnet 3.5 for cost efficiency
        
        # Use third-party API as primary (official API has low credits)
        self.current_api = "third_party"
        self.current_token = self.third_party_token
        self.current_base_url = self.third_party_base_url
        self.current_model = self.third_party_model
        
        # Retry configuration for third-party API (FREE - so we can be aggressive!)
        self.third_party_max_retries = 10  # 10 attempts since it's totally free
        self.third_party_base_delay = 3    # Start with 3 seconds
        self.third_party_max_delay = 45    # Max 45 seconds between retries
        
        # Request headers
        self.headers = {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        logger.info(f"🚀 Claude API Load Balancer initialized:")
        logger.info(f"   Primary: Third-party API ({self.third_party_base_url})")
        logger.info(f"   Fallback: Official Claude Pro API (low credits)")
        logger.info(f"   Current Model: {self.current_model}")
        logger.info(f"   Retry Strategy: {self.third_party_max_retries} attempts with backoff (FREE API!)")
        logger.info(f"   Token: {self.current_token[:20]}..." if self.current_token else "   Token: None")
        
    async def enhance_resume_content(self, job: Dict, base_resume_content: str) -> str:
        """
        Use Claude API to enhance and tailor resume content for specific job
        """
        try:
            prompt = f"""
            Please enhance and tailor this resume content for the following job application:
            
            JOB TITLE: {job.get('title', 'Software Developer')}
            COMPANY: {job.get('company', 'Target Company')}
            JOB DESCRIPTION: {job.get('description', 'No description provided')}
            
            CURRENT RESUME CONTENT:
            {base_resume_content}
            
            Please:
            1. Optimize the Profile Summary to match job requirements
            2. Emphasize relevant technical skills mentioned in job description
            3. Highlight relevant experience that aligns with the role
            4. Improve ATS compatibility by including job-relevant keywords
            5. Keep the same LaTeX structure and formatting
            6. Ensure the content fits on appropriate pages
            
            Return only the enhanced LaTeX content, ready to compile.
            """
            
            enhanced_content = await self._make_claude_request(prompt)
            
            if enhanced_content and len(enhanced_content) > 100:
                logger.info(f"Successfully enhanced resume content for {job.get('company', 'Unknown')}")
                return enhanced_content
            else:
                logger.warning("Claude API returned insufficient content, using base resume")
                return base_resume_content
                
        except Exception as e:
            logger.error(f"Error enhancing resume content: {e}")
            return base_resume_content
    
    async def enhance_cover_letter_content(self, job: Dict, base_cover_letter: str) -> str:
        """
        Use Claude API to enhance and personalize cover letter content
        """
        try:
            prompt = f"""
            Please enhance and personalize this cover letter for the following job application:
            
            JOB TITLE: {job.get('title', 'Software Developer')}
            COMPANY: {job.get('company', 'Target Company')}
            JOB DESCRIPTION: {job.get('description', 'No description provided')}
            HIRING MANAGER: {job.get('hiring_manager', 'Unknown')}
            
            CURRENT COVER LETTER:
            {base_cover_letter}
            
            Please:
            1. Personalize the greeting if hiring manager name is provided
            2. Extract and emphasize soft skills mentioned in job description
            3. Highlight technical alignment with job requirements
            4. Show passion for the company's industry/mission
            5. Demonstrate cultural fit based on company description
            6. Keep the exact LaTeX formatting and structure
            7. Ensure it fits on one page
            8. Use professional, enthusiastic tone
            
            Return only the enhanced LaTeX content, ready to compile.
            """
            
            enhanced_content = await self._make_claude_request(prompt)
            
            if enhanced_content and len(enhanced_content) > 100:
                logger.info(f"Successfully enhanced cover letter for {job.get('company', 'Unknown')}")
                return enhanced_content
            else:
                logger.warning("Claude API returned insufficient content, using base cover letter")
                return base_cover_letter
                
        except Exception as e:
            logger.error(f"Error enhancing cover letter content: {e}")
            return base_cover_letter
    
    async def optimize_for_ats(self, content: str, job_keywords: list) -> str:
        """
        Use Claude API to optimize content for ATS systems
        """
        try:
            keywords_str = ", ".join(job_keywords) if job_keywords else "general software development"
            
            prompt = f"""
            Please optimize this resume/cover letter content for ATS (Applicant Tracking System) compatibility:
            
            TARGET KEYWORDS: {keywords_str}
            
            CONTENT TO OPTIMIZE:
            {content}
            
            Please:
            1. Naturally integrate relevant keywords from the target list
            2. Ensure proper formatting for ATS parsing
            3. Use standard section headers
            4. Avoid complex formatting that might confuse ATS
            5. Include industry-standard terminology
            6. Maintain readability for human reviewers
            7. Keep the same LaTeX structure
            
            Return only the ATS-optimized content.
            """
            
            optimized_content = await self._make_claude_request(prompt)
            
            if optimized_content and len(optimized_content) > 100:
                logger.info("Successfully optimized content for ATS")
                return optimized_content
            else:
                logger.warning("ATS optimization failed, using original content")
                return content
                
        except Exception as e:
            logger.error(f"Error optimizing for ATS: {e}")
            return content
    
    async def generate_text(self, prompt: str) -> str:
        """
        Generate text using Claude API
        """
        return await self._make_claude_request(prompt)
    
    async def _make_claude_request(self, prompt: str) -> str:
        """
        Smart load balancer: Try third-party API with retries, fallback to official API
        """
        if not self.current_token:
            logger.warning("No Claude API token available")
            return ""
        
        # Try third-party API first with robust retry logic
        if self.current_api == "third_party":
            result = await self._try_third_party_api_with_retries(prompt)
            if result:
                return result
            
            # Third-party failed after 30 seconds, try official API
            logger.warning("🔄 Third-party API failed after 30s timeout, switching to official Claude API")
            if self.official_token:
                return await self._make_official_api_request(prompt)
            else:
                logger.error("❌ No official Claude API key available for fallback")
        
        # Return empty if both APIs unavailable
        return ""
    
    async def _try_third_party_api_with_retries(self, prompt: str) -> str:
        """
        Try third-party API with exponential backoff for 502/500 errors
        """
        for attempt in range(self.third_party_max_retries):
            try:
                # Progressive delay: 3s, 6s, 12s, 24s, 45s, 45s, 45s...
                delay = min(self.third_party_base_delay * (2 ** attempt), self.third_party_max_delay)
                
                if attempt > 0:
                    logger.info(f"🔄 Third-party API retry {attempt + 1}/{self.third_party_max_retries} (waiting {delay}s) - FREE API, keep trying!")
                    await asyncio.sleep(delay)
                else:
                    logger.info(f"🚀 Third-party API attempt {attempt + 1}/{self.third_party_max_retries} - FREE API advantage!")
                
                result = await self._make_claude_cli_request(prompt)
                
                if result and len(result) > 10:  # Valid response
                    logger.info(f"✅ Third-party API success on attempt {attempt + 1}")
                    return result
                else:
                    logger.warning(f"⚠️ Third-party API returned empty/short response (attempt {attempt + 1})")
                    
            except subprocess.TimeoutExpired:
                logger.warning(f"⏰ Third-party API timeout (attempt {attempt + 1}/{self.third_party_max_retries})")
            except Exception as e:
                logger.warning(f"⚠️ Third-party API error (attempt {attempt + 1}): {e}")
                
                # Check if it's a server overload error (502, 500, etc.)
                if "502" in str(e) or "500" in str(e) or "503" in str(e) or "timeout" in str(e).lower():
                    logger.info(f"🚦 Server overload/timeout detected (attempt {attempt + 1}), will retry with backoff - FREE API!")
                    continue
                elif "rate limit" in str(e).lower():
                    logger.info(f"⏱️ Rate limit hit (attempt {attempt + 1}), waiting longer - FREE API!")
                    await asyncio.sleep(delay * 2)  # Double wait for rate limits
                    continue
        
        logger.warning(f"❌ Third-party API failed after {self.third_party_max_retries} attempts (FREE API exhausted)")
        return ""
    
    async def _make_official_api_request(self, prompt: str) -> str:
        """
        Make request to official Claude Pro API with cost-efficient settings
        """
        try:
            logger.info("🔑 Using official Claude Pro API")
            
            # Cost-efficient settings for official API (limited to Sonnet 3.5)
            request_data = {
                "model": self.current_model,  # claude-3-5-sonnet-20241022
                "max_tokens": 1500,  # Reduced for cost efficiency
                "temperature": 0.2,  # Lower temperature for consistency and cost
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            headers = self.headers.copy()
            headers["x-api-key"] = self.current_token
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.current_base_url}/v1/messages"
                
                async with session.post(
                    url,
                    headers=headers,
                    json=request_data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        response_data = await response.json()
                        
                        if "content" in response_data and response_data["content"]:
                            content = response_data["content"][0]["text"]
                            logger.info(f"✅ Official Claude Pro API success ({len(content)} chars)")
                            return content
                        else:
                            logger.warning("Official API returned empty content")
                            return ""
                    
                    elif response.status == 401:
                        logger.error("❌ Official Claude Pro API authentication failed")
                        return ""
                    
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Official API error {response.status}: {error_text}")
                        return ""
                        
        except Exception as e:
            logger.error(f"❌ Official Claude Pro API error: {e}")
            return ""
    
    async def _make_claude_cli_request(self, prompt: str) -> str:
        """
        Make Claude request using CLI approach for third-party API
        """
        try:
            logger.info("🤖 Using Claude CLI for third-party API request...")
            
            # Set up environment for CLI
            env = os.environ.copy()
            env["ANTHROPIC_AUTH_TOKEN"] = self.current_token
            env["ANTHROPIC_BASE_URL"] = self.current_base_url
            
            # Prepare the prompt with clear instructions
            cli_prompt = f"""Please provide a concise, professional response to this request:

{prompt}

Important: Return only the requested content without additional commentary or formatting."""
            
            # Use Claude CLI with current model
            cmd = ["claude", "--model", self.current_model, "--print"]
            
            # Run the command with appropriate timeout
            result = subprocess.run(
                cmd,
                input=cli_prompt,
                text=True,
                capture_output=True,
                env=env,
                timeout=30  # 30 second timeout as requested
            )
            
            if result.returncode == 0 and result.stdout:
                response = result.stdout.strip()
                logger.info(f"✅ Claude CLI request successful ({len(response)} chars)")
                return response
            else:
                logger.error(f"❌ Claude CLI failed: {result.stderr}")
                logger.info("💡 You may need to run the setup script first: ./setup_claude_cli.sh")
                return ""
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Claude CLI request timeout")
            return ""
        except FileNotFoundError:
            logger.error("❌ Claude CLI not found. Please install: pip install claude-cli")
            return ""
        except Exception as e:
            logger.error(f"❌ Claude CLI error: {e}")
            return ""
    
    async def _switch_to_official_api(self):
        """
        Switch from third-party API to official Claude Pro API
        """
        try:
            # Switch to official API configuration
            self.current_api = "official"
            self.current_token = self.official_token
            self.current_base_url = self.official_base_url
            self.current_model = self.official_model
            
            logger.info(f"🔄 Switched to official Claude Pro API (model: {self.current_model})")
            
        except Exception as e:
            logger.error(f"❌ Error switching to official API: {e}")
    
    async def _logout_claude_session(self):
        """
        Perform logout from current Claude session
        """
        try:
            # Method 1: Try HTTP logout if endpoint exists
            if self.current_base_url != self.official_base_url:
                try:
                    async with aiohttp.ClientSession() as session:
                        logout_url = f"{self.current_base_url}/logout"
                        async with session.post(
                            logout_url,
                            headers={"x-api-key": self.current_token},
                            timeout=aiohttp.ClientTimeout(total=5)
                        ) as response:
                            if response.status == 200:
                                logger.info("Successfully logged out from third-party API")
                            else:
                                logger.info(f"Logout attempt returned {response.status}")
                except Exception:
                    pass  # Logout endpoint might not exist, continue anyway
            
            # Method 2: Environment variable cleanup and reset
            try:
                # Clear environment variables
                if "ANTHROPIC_AUTH_TOKEN" in os.environ:
                    del os.environ["ANTHROPIC_AUTH_TOKEN"]
                if "ANTHROPIC_BASE_URL" in os.environ:
                    del os.environ["ANTHROPIC_BASE_URL"]
                
                # Run shell logout command if available
                result = subprocess.run(
                    ["bash", "-c", "unset ANTHROPIC_AUTH_TOKEN; unset ANTHROPIC_BASE_URL"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                logger.info("Environment variables cleared for API switch")
                
            except Exception as e:
                logger.warning(f"Environment cleanup warning: {e}")
            
            # Small delay to ensure clean session switch
            await asyncio.sleep(0.5)
            
        except Exception as e:
            logger.warning(f"Logout process warning (continuing anyway): {e}")
    
    def reset_to_third_party(self):
        """
        Reset back to third-party API (for next session)
        """
        self.current_api = "third_party"
        self.current_token = self.third_party_token
        self.current_base_url = self.third_party_base_url
        self.current_model = self.third_party_model
        logger.info("🔄 Reset to third-party API for next session")
    
    def get_current_api_info(self) -> Dict[str, str]:
        """
        Get information about currently active API
        """
        return {
            "api_type": self.current_api,
            "base_url": self.current_base_url,
            "model": self.current_model,
            "token_prefix": self.current_token[:10] + "..." if self.current_token else "None"
        }