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
        self.claude_model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
        
        # Official Anthropic API configuration (fallback)
        self.official_token = os.getenv("ANTHROPIC_API_KEY")
        self.official_base_url = "https://api.anthropic.com"
        
        # Use third-party API as primary
        self.current_api = "third_party"
        self.current_token = self.third_party_token
        self.current_base_url = self.third_party_base_url
        
        # Request headers
        self.headers = {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        logger.info(f"🚀 Claude API initialized with THIRD-PARTY configuration:")
        logger.info(f"   Model: {self.claude_model}")
        logger.info(f"   API: {self.current_api}")
        logger.info(f"   Base URL: {self.current_base_url}")
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
    
    async def _make_claude_request(self, prompt: str, max_retries: int = 2) -> str:
        """
        Make request to Claude API using CLI approach for third-party API
        """
        if not self.current_token:
            logger.warning("No Claude API token available")
            return ""
        
        # For third-party API, use CLI approach
        if self.current_api == "third_party":
            return await self._make_claude_cli_request(prompt)
        
        # For official API, use HTTP approach
        for attempt in range(max_retries):
            try:
                logger.info(f"Making Claude API request (attempt {attempt + 1}/{max_retries})")
                
                # Prepare request data with COST-EFFICIENT settings
                request_data = {
                    "model": self.claude_model,
                    "max_tokens": 4096,  # Balanced tokens for cost efficiency
                    "temperature": 0.5,  # Balanced creativity/accuracy
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
                
                # Set up headers for official API
                headers = self.headers.copy()
                headers["x-api-key"] = self.current_token
                
                # Make the request
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
                            
                            # Extract content from response
                            if "content" in response_data and response_data["content"]:
                                content = response_data["content"][0]["text"]
                                logger.info(f"✅ Claude API request successful ({len(content)} chars)")
                                return content
                            else:
                                logger.warning("Claude API returned empty content")
                                return ""
                        
                        elif response.status == 401:
                            logger.error("Claude API authentication failed")
                            return ""
                        
                        else:
                            error_text = await response.text()
                            logger.error(f"Claude API error {response.status}: {error_text}")
                            
                            if attempt < max_retries - 1:
                                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                                continue
                            return ""
                            
            except asyncio.TimeoutError:
                logger.error(f"Claude API request timeout (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                    continue
                return ""
                
            except Exception as e:
                logger.error(f"Claude API request error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                    continue
                return ""
        
        logger.error("All Claude API attempts failed")
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
            
            # Use Claude CLI
            cmd = ["claude", "--model", self.claude_model, "--print"]
            
            # Run the command
            result = subprocess.run(
                cmd,
                input=cli_prompt,
                text=True,
                capture_output=True,
                env=env,
                timeout=60  # Increased timeout for CLI
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
        Switch from third-party API to official Anthropic API with logout
        """
        try:
            # Perform logout from current session
            await self._logout_claude_session()
            
            # Switch to official API
            self.current_api = "official"
            self.current_token = self.official_token
            self.current_base_url = self.official_base_url
            
            logger.info("Successfully switched to official Anthropic API")
            
        except Exception as e:
            logger.error(f"Error switching to official API: {e}")
    
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
        logger.info("Reset to third-party API for next session")
    
    def get_current_api_info(self) -> Dict[str, str]:
        """
        Get information about currently active API
        """
        return {
            "api_type": self.current_api,
            "base_url": self.current_base_url,
            "token_prefix": self.current_token[:10] + "..." if self.current_token else "None"
        }