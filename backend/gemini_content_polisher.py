#!/usr/bin/env python3
"""
Gemini-powered content polisher for CV and Cover Letter
Makes content sound natural, human, sincere - not AI-generated
"""
import os
import re
import logging
import requests
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)


class GeminiContentPolisher:
    def __init__(self):
        """Initialize with Gemini API"""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.base_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent'

    def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        if not self.api_key:
            logger.warning("⚠️ Gemini API key not configured")
            return ""

        try:
            url = f'{self.base_url}?key={self.api_key}'
            data = {
                'contents': [{
                    'parts': [{'text': prompt}]
                }],
                'generationConfig': {
                    'temperature': 0.7,  # Higher for more natural writing
                    'maxOutputTokens': 2000
                }
            }

            response = requests.post(url, json=data, timeout=60)

            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                logger.error(f"❌ Gemini API failed: {response.status_code}")
                return ""

        except Exception as e:
            logger.error(f"❌ Gemini call failed: {e}")
            return ""

    def polish_cover_letter_content(self, job_data: Dict[str, Any]) -> str:
        """Generate natural, human-sounding cover letter content"""

        prompt = f"""Write a sincere, professional cover letter for this job application. 

Job: {job_data.get('title', '')} at {job_data.get('company', '')}
Location: {job_data.get('location', '')}

About the candidate (Hongzhi Li):
- Currently at ECARX as Senior Infrastructure & Performance Engineering Specialist
- Designed real-time Grafana/Prometheus dashboards for Android AOSP build systems (achieved 3.5x performance improvement)
- Built web-based monitoring interfaces for Polestar 4/5 automotive testing platforms
- Developed Android Auto applications with automotive-optimized UI/UX
- Created cross-platform carpooling app with real-time geolocation (React Native)
- Built e-commerce platforms with real-time analytics dashboards
- Helped Mibo.se with full Microsoft solution integration (Synteda freelance project)
- Fluent in English and Mandarin, Swedish B2 level
- Strong soft skills: bridges IT and business teams, facilitates communication between international and Swedish colleagues

CRITICAL REQUIREMENTS:
1. Write like a real person, not AI - be conversational but professional
2. Be sincere and earnest, show genuine interest in the role
3. Emphasize BOTH hard skills (visualization, UI/UX, real-time systems) AND soft skills (communication, team bridging, integration experience)
4. Mention the Mibo.se Microsoft solution integration as concrete example of business-IT collaboration
5. Show understanding of AGV/robotics visualization challenges
6. Keep it concise - 3-4 paragraphs maximum
7. NO clichés like "I am writing to express my interest" - start more naturally
8. NO repetition of CV content - complement it instead
9. Show personality and cultural fit

Return ONLY the cover letter body paragraphs (no opening/closing, just the content between greeting and signature).
"""

        content = self._call_gemini(prompt)
        return content if content else self._fallback_cover_letter()

    def polish_ecarx_experience(self) -> list:
        """Generate natural ECARX experience bullets emphasizing visualization and soft skills"""

        prompt = """Rewrite these ECARX work experience bullets to sound natural and human, emphasizing visualization work and soft skills:

Current bullets:
- Designed real-time performance monitoring dashboards using Grafana and Prometheus for Android AOSP build systems
- Created visualization tools for infrastructure metrics, achieving 3.5x performance improvement visibility
- Built web-based monitoring interfaces for automotive testing platforms including Polestar 4/5 emulator visualization
- Collaborated with hardware engineers and testing teams to create intuitive UI for automotive validation workflows

Requirements:
1. Sound like a real person wrote them, not AI
2. Emphasize visualization, UI/UX, and real-time monitoring aspects
3. Highlight soft skills: team collaboration, bridging technical and non-technical stakeholders
4. Mention communication between international teams and Swedish colleagues
5. Keep technical but accessible
6. 6-8 bullets total
7. Vary sentence structure - not all starting the same way

Return ONLY the bullet points as a JSON array of strings, like: ["bullet 1", "bullet 2", ...]
"""

        response = self._call_gemini(prompt)

        # Extract JSON array
        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                bullets = json.loads(json_match.group())
                return bullets
        except:
            pass

        return self._fallback_ecarx_bullets()

    def polish_synteda_experience(self) -> list:
        """Generate natural Synteda experience emphasizing Mibo.se integration"""

        prompt = """Rewrite these Synteda freelance experience bullets to sound natural, emphasizing the Mibo.se Microsoft solution integration:

Current bullets:
- Integrated full Microsoft solution stack for Mibo.se: C# .NET backend, React frontend, Azure cloud hosting
- Built talent management platform coordinating between business requirements and technical implementation
- Developed separate native Android applications using Kotlin for mobile talent management features
- Collaborated with Mibo.se team to translate business workflows into scalable architecture

CRITICAL ACCURACY:
- Mibo.se backend: C# .NET (NOT Kotlin)
- Mibo.se frontend: React (NOT Kotlin)
- Kotlin was used ONLY for separate Android mobile app development
- Emphasize full Microsoft stack: C#, React, Azure

Requirements:
1. Sound human and natural
2. Be technically accurate - C# backend, React frontend, Kotlin for Android only
3. Highlight bridging business needs with technical solutions
4. Show collaboration and communication skills
5. 3-4 bullets
6. Vary sentence structure

Return ONLY the bullet points as a JSON array of strings.
"""

        response = self._call_gemini(prompt)

        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                bullets = json.loads(json_match.group())
                return bullets
        except:
            pass

        return self._fallback_synteda_bullets()

    def _fallback_cover_letter(self) -> str:
        """Fallback cover letter if Gemini fails"""
        return """When I saw this position, I immediately thought about the dashboards I built at ECARX. Every day, our team relies on the real-time Grafana and Prometheus visualizations I designed to monitor our Android AOSP build infrastructure. Watching those metrics helped us achieve a 3.5x performance improvement, but what I'm most proud of is how the interface made complex data accessible to everyone—from hardware engineers to project managers.

What draws me to this role is the chance to apply that same approach to AGV systems. I've spent the past year building interfaces for automotive testing platforms, including Polestar 4 and 5 emulators, and I understand how critical clear, intuitive visualization is when you're dealing with autonomous systems. My Android Auto projects taught me that good UI in complex environments isn't just about looking nice—it's about making the right information available at the right moment.

Beyond the technical work, I've found my real value is in bridging gaps. At ECARX, I work daily with both Swedish and Chinese teams, translating not just language but context—helping business stakeholders understand technical constraints and helping engineers see the business impact of their work. When I freelanced with Synteda on the Mibo.se project, I integrated their full Microsoft solution stack, which meant coordinating between their business team, Azure infrastructure, and mobile development needs. That experience taught me that successful software is as much about communication as it is about code.

I'm genuinely excited about bringing both my visualization skills and my team-bridging experience to Kollmorgen. I'd love to help make your AGV operation software not just functional, but genuinely intuitive for the people who use it every day."""

    def _fallback_ecarx_bullets(self) -> list:
        """Fallback ECARX bullets"""
        return [
            "Built real-time Grafana and Prometheus dashboards that our team uses daily to monitor Android AOSP build infrastructure, making complex performance data accessible to both technical and non-technical stakeholders",
            "Created web-based visualization interfaces for Polestar 4 and 5 automotive testing platforms, working closely with hardware engineers to understand their monitoring needs",
            "Designed intuitive UI for infrastructure metrics that helped achieve 3.5x performance improvement by making bottlenecks immediately visible",
            "Developed automated reporting dashboards that bridge the gap between our Swedish and Chinese teams, presenting build analytics in ways that work across language and cultural contexts",
            "Collaborated with testing teams to build validation workflow interfaces, translating technical requirements into user-friendly visualizations",
            "Implemented real-time alerting systems with clear visual feedback, reducing mean time to detection for infrastructure issues",
            "Facilitated communication between hardware engineers, DevOps specialists, and project managers through shared visualization tools",
            "Managed hybrid cloud visualization interfaces, helping stakeholders understand resource utilization across on-premise HPC and cloud infrastructure"
        ]

    def _fallback_synteda_bullets(self) -> list:
        """Fallback Synteda bullets"""
        return [
            "Integrated full Microsoft solution stack for Mibo.se: built C# .NET backend APIs, React frontend web application, and deployed on Azure cloud infrastructure",
            "Bridged business requirements and technical implementation, working closely with Mibo.se team to translate their talent management workflows into scalable architecture",
            "Developed separate native Android applications using Kotlin for mobile talent management features, ensuring seamless integration with the C# backend",
            "Coordinated between business stakeholders and technical implementation, delivering a cohesive platform that met both operational needs and technical standards"
        ]


if __name__ == "__main__":
    print("🤖 Testing Gemini Content Polisher...")

    # Load env
    from pathlib import Path
    env_path = Path('.env')
    if env_path.exists():
        for line in env_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, val = line.split('=', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val

    polisher = GeminiContentPolisher()

    test_job = {
        'title': 'Junior Software Engineer - Operation & Visualization',
        'company': 'Kollmorgen',
        'location': 'Gothenburg, Sweden'
    }

    print("\n📝 Polishing cover letter...")
    cl_content = polisher.polish_cover_letter_content(test_job)
    print(cl_content[:200] + "...")

    print("\n📝 Polishing ECARX experience...")
    ecarx_bullets = polisher.polish_ecarx_experience()
    print(f"Generated {len(ecarx_bullets)} bullets")
    print(f"First bullet: {ecarx_bullets[0][:100]}...")

    print("\n✅ Polisher test complete!")
