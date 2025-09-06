#!/usr/bin/env python3
"""
ECARX Infotainment Software Developer - Customized Cover Letter Generator
Tailored for the specific role with automotive passion and innovative projects emphasis
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from true_template_automation import TrueTemplateAutomation

async def create_ecarx_infotainment_cover_letter():
    """Generate customized cover letter for ECARX Infotainment role"""
    
    # Job-specific details matching the role requirements
    job_details = {
        'company': 'ECARX',
        'title': 'Infotainment Software Developer',
        'location': 'Gothenburg',
        'department': 'R&D Team',
        'email_subject': 'ECARX Infotainment Software Developer - Gothenburg R&D Team',
        'sender': 'careers@ecarx.com',
        'body': """We are seeking an experienced Infotainment software developer who combines strong technical skills with a pragmatic and proactive mindset. You will be part of a dynamic development environment where not everything is fully defined, and your ability to move forward despite ambiguity will be key to success.

Key Requirements:
- 5+ years of hands-on experience in Android development, ideally within the automotive or infotainment domain
- Strong problem-solving abilities and the capacity to work both independently and collaboratively
- Proven expertise in Kotlin and Java with strong proficiency in Android Studio
- Deep experience with native AOSP development using the Soong/Make build system
- Solid understanding of the Android SDK and platform architecture
- Experience in C/C++ is a strong advantage
- Corporate language is English and proficiency in Mandarin Chinese is highly desirable

You will design and develop native platform software for AOSP based infotainment solutions and develop Android applications and services for the next-generation automotive solutions.""",
        'raw_content': 'ECARX Infotainment Software Developer R&D Gothenburg Android AOSP automotive'
    }
    
    # Initialize automation system
    automation = TrueTemplateAutomation()
    
    print("🚗 Generating ECARX Infotainment Cover Letter...")
    
    try:
        # Generate cover letter using the existing automation system
        cover_letter_latex = await automation._generate_true_cover_letter(job_details)
        
        if cover_letter_latex:
            # Compile to PDF
            pdf_path = await automation._compile_latex_to_pdf(
                cover_letter_latex, 
                "ecarx_infotainment_cover_letter"
            )
            
            if pdf_path:
                print(f"✅ Cover letter generated successfully!")
                print(f"📄 PDF File: {pdf_path}")
                
                # Get file size
                if os.path.exists(pdf_path):
                    file_size = os.path.getsize(pdf_path)
                    print(f"📊 Size: {file_size} bytes ({file_size/1024:.1f} KB)")
                
                return pdf_path
            else:
                print("❌ Failed to compile LaTeX to PDF")
                return None
        else:
            print("❌ Failed to generate cover letter LaTeX")
            return None
            
    except Exception as e:
        print(f"❌ Error generating cover letter: {str(e)}")
        return None

if __name__ == "__main__":
    asyncio.run(create_ecarx_infotainment_cover_letter())