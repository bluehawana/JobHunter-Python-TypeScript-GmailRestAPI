#!/usr/bin/env python3
"""
Specialized ECARX Infotainment Cover Letter Generator
Emphasizes automotive passion, innovative projects, and cross-cultural strengths
"""
import os
import time
import requests
import json
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv('backend/.env')

def generate_ecarx_infotainment_cover_letter(job_data):
    """Generate specialized cover letter for ECARX Infotainment role"""
    
    # Use official Claude API
    claude_api_key = os.getenv('ANTHROPIC_AUTH_TOKEN')
    claude_base_url = "https://api.anthropic.com"
    
    if not claude_api_key:
        print("❌ Claude API key not found")
        return None
    
    # Comprehensive prompt for Claude
    prompt = f"""
    Create a compelling cover letter for Hongzhi Li applying for the Infotainment Software Developer position at ECARX. 

    KEY CONTEXT:
    - Hongzhi is CURRENTLY working at ECARX as IT/Infrastructure Specialist (internal candidate advantage!)
    - This is a perfect career progression within the same company
    - He has deep passion for automotive industry and software development
    - He has innovative hobby projects related to Android Auto and automotive infotainment
    - He excels at cross-cultural communication and bridging gaps

    JOB REQUIREMENTS:
    {job_data.get('description', '')}

    HONGZHI'S UNIQUE STRENGTHS TO EMPHASIZE:

    1. AUTOMOTIVE PASSION & INNOVATION:
    - Deep passion for automotive industry and software development
    - Personal hobby projects demonstrating automotive infotainment innovation:
      * AndroidAuto_CarTVPlayer_KOTLIN: Custom Android Auto media player with enhanced audio controls and intuitive UI
      * AndroidAuto_TTS_EpubReader: EPUB-to-MP3 audiobook generator using Microsoft Edge TTS for Android Auto playback
      * AndroidAuto_AI_Bot: In-car AI voice assistant activated via custom wake-word "Hi Car" as smarter alternative to Google Assistant
    - These projects show genuine passion and practical innovation in automotive infotainment space
    - Ideas for new features and competitive advantages for ECARX Android Auto products

    2. CROSS-CULTURAL COMMUNICATION EXCELLENCE:
    - Fluent in both Mandarin Chinese and English (perfect for global collaboration requirement)
    - Experienced in bridging the gap between IT and business stakeholders
    - Expert at bridging Eastern and Western cultural approaches in software development
    - Strong listener and communicator with international business background
    - Master's in International Business and Trade + technical expertise = unique combination

    3. INTERNAL CANDIDATE ADVANTAGES:
    - Already at ECARX - understands company culture, values, and automotive focus
    - Current IT/Infrastructure role provides system-level understanding
    - Experience with Kubernetes, AWS, system integration - valuable for infotainment architecture
    - Proven ability to work in ECARX's dynamic, fast-paced environment

    4. TECHNICAL ALIGNMENT:
    - Java/J2EE development experience (5+ years)
    - System integration and architecture experience
    - Cross-platform development (React Native, mobile apps)
    - Infrastructure and DevOps knowledge valuable for AOSP development
    - AI tools experience (mentioned in job requirements)

    COVER LETTER STRUCTURE:
    1. Opening: Express genuine excitement about this internal opportunity and automotive passion
    2. Automotive Innovation: Highlight hobby projects and ideas for ECARX products
    3. Cross-Cultural Value: Emphasize communication strengths and cultural bridging
    4. Technical Fit: Connect current experience to infotainment development
    5. Internal Advantage: Leverage ECARX knowledge and commitment
    6. Closing: Enthusiasm for contributing to ECARX's automotive infotainment leadership

    TONE: Professional yet passionate, showing genuine excitement for automotive technology and ECARX's mission.

    Generate a compelling, personalized cover letter that positions Hongzhi as the ideal internal candidate who brings both technical skills and innovative automotive passion to drive ECARX's infotainment solutions forward.
    """
    
    try:
        headers = {
            'Authorization': f'Bearer {claude_api_key}',
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': 'claude-3-5-sonnet-20241022',
            'max_tokens': 2000,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        }
        
        print(f"🔑 Using API key: {claude_api_key[:20]}...")
        print(f"🌐 API URL: {claude_base_url}/v1/messages")
        
        print("🤖 Generating specialized cover letter with Claude API...")
        response = requests.post(
            f'{claude_base_url}/v1/messages',
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            cover_letter_content = result['content'][0]['text']
            
            print("✅ Claude API generated specialized cover letter successfully!")
            return cover_letter_content
        else:
            print(f"❌ Claude API error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error generating cover letter: {e}")
        return None

def create_latex_cover_letter(content):
    """Convert cover letter content to LaTeX format"""
    
    current_date = datetime.now().strftime("%B %d, %Y")
    
    latex_template = f"""\\documentclass[a4paper,11pt]{{article}}
\\usepackage[left=1in,right=1in,top=1in,bottom=1in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}

% Define colors
\\definecolor{{darkblue}}{{rgb}}{{0.0, 0.2, 0.6}}

% Section formatting
\\titleformat{{\\section}}{{\\large\\bfseries\\raggedright\\color{{black}}}}{{}}{{0em}}{{}}[\\titlerule]

% Remove paragraph indentation
\\setlength{{\\parindent}}{{0pt}}

\\begin{{document}}
\\pagestyle{{empty}}

% Header
\\begin{{center}}
{{\\Large \\textbf{{Hongzhi Li}}}}\\\\[5pt]
{{\\color{{darkblue}} Ebbe Lieberathsgatan 27, 412 65 Göteborg, Sweden}}\\\\
{{\\color{{darkblue}} hongzhili01@gmail.com | +46 728 384 299}}\\\\
{{\\color{{darkblue}} \\href{{https://www.linkedin.com/in/hzl/}}{{LinkedIn}} | \\href{{https://github.com/bluehawana}}{{GitHub}}}}
\\end{{center}}

\\vspace{{20pt}}

% Date and Address
{current_date}

\\vspace{{10pt}}

ECARX Technology\\\\
R\\&D Department\\\\
Gothenburg, Sweden

\\vspace{{20pt}}

% Cover Letter Content
{content}

\\vspace{{20pt}}

Sincerely,

\\vspace{{20pt}}

Hongzhi Li

\\end{{document}}"""
    
    return latex_template

if __name__ == "__main__":
    # Test the specialized cover letter generator
    test_job = {
        'title': 'Infotainment Software Developer',
        'company': 'ECARX',
        'description': '''
        We are seeking an experienced Infotainment software developer who combines strong technical skills with a pragmatic and proactive mindset. You will be part of a dynamic development environment where not everything is fully defined, and your ability to move forward despite ambiguity will be key to success.

        You will be part of the R&D team in Gothenburg and contribute to evolving, developing and maintaining our infotainment solution. Our products are already available on the market and more to come.

        Key Requirements:
        - 5+ years of hands-on experience in Android development, ideally within the automotive or infotainment domain
        - Proven expertise in Kotlin and Java with strong proficiency in Android Studio
        - Deep experience with native AOSP development using the Soong/Make build system
        - Solid understanding of the Android SDK and platform architecture
        - Experience in C/C++ is a strong advantage
        - Knowledge in automotive communication protocols and/or QNX is a strong advantage
        - Proficiency in Mandarin Chinese is highly desirable
        - Design and implement native platform software for AOSP based infotainment solutions
        - Develop Android applications and services for next-generation automotive solutions
        - Collaborate with global cross-functional teams
        - Troubleshoot issues and optimize performance
        - Contribute to Android development processes, tooling, and architecture
        '''
    }
    
    content = generate_ecarx_infotainment_cover_letter(test_job)
    if content:
        latex_content = create_latex_cover_letter(content)
        
        # Save LaTeX file
        with open('ECARX_Infotainment_CoverLetter_Specialized.tex', 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print("✅ Specialized cover letter saved: ECARX_Infotainment_CoverLetter_Specialized.tex")
        print("\n📄 COVER LETTER PREVIEW:")
        print("-" * 50)
        print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print("❌ Failed to generate cover letter")