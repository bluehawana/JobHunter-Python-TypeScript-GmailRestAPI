#!/usr/bin/env python3
"""
ECARX Infotainment Software Developer - Honest Application Generator
Updated to reflect accurate C/C++ experience level
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from true_template_automation import TrueTemplateAutomation

async def create_honest_ecarx_application():
    """Generate honest CV and cover letter for ECARX role"""
    
    # Updated job details with honest technical assessment
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
- Experience in C/C++ is a strong advantage (but not mandatory)
- Corporate language is English and proficiency in Mandarin Chinese is highly desirable

You will design and develop native platform software for AOSP based infotainment solutions and develop Android applications and services for the next-generation automotive solutions.""",
        'raw_content': 'ECARX Infotainment Software Developer R&D Gothenburg Android AOSP automotive Kotlin Java',
        
        # Honest technical profile
        'honest_profile': {
            'c_cpp_level': 'basic',  # Be honest about limited C/C++ experience
            'strengths': [
                'Android development (5+ years)',
                'Kotlin and Java expertise',
                'Android Studio proficiency',
                'Cross-cultural communication',
                'Automotive passion with hobby projects',
                'Problem-solving in ambiguous environments'
            ],
            'learning_areas': [
                'Native AOSP development',
                'C/C++ for performance-critical components',
                'Automotive communication protocols'
            ]
        }
    }
    
    automation = TrueTemplateAutomation()
    
    print("🚗 Generating Honest ECARX Application Package...")
    print("📝 Creating CV and Cover Letter with accurate technical profile...")
    
    try:
        # Generate CV
        print("\n1️⃣ Generating CV...")
        cv_latex = await automation._generate_true_cv(job_details)
        
        if cv_latex:
            cv_pdf = await automation._compile_latex_to_pdf(cv_latex, "ecarx_honest_cv")
            if cv_pdf:
                with open("ECARX_Honest_CV.pdf", 'wb') as f:
                    f.write(cv_pdf)
                print(f"✅ CV saved: ECARX_Honest_CV.pdf ({len(cv_pdf)/1024:.1f} KB)")
            else:
                print("❌ Failed to compile CV")
                return None
        
        # Generate Cover Letter
        print("\n2️⃣ Generating Cover Letter...")
        cl_latex = await automation._generate_true_cover_letter(job_details)
        
        if cl_latex:
            cl_pdf = await automation._compile_latex_to_pdf(cl_latex, "ecarx_honest_cover_letter")
            if cl_pdf:
                with open("ECARX_Honest_Cover_Letter.pdf", 'wb') as f:
                    f.write(cl_pdf)
                print(f"✅ Cover Letter saved: ECARX_Honest_Cover_Letter.pdf ({len(cl_pdf)/1024:.1f} KB)")
            else:
                print("❌ Failed to compile Cover Letter")
                return None
        
        # Send email
        print("\n3️⃣ Sending application to hongzhili01@gmail.com...")
        email_sent = await automation._send_true_email(
            job_details, 
            cv_pdf, 
            cl_pdf
        )
        
        if email_sent:
            print("✅ Application sent successfully to hongzhili01@gmail.com!")
            print("\n📋 Application Summary:")
            print("• CV: Highlights Android expertise, honest about C/C++ learning curve")
            print("• Cover Letter: Emphasizes automotive passion, cross-cultural skills")
            print("• Technical Focus: Kotlin/Java strength, willingness to learn native development")
            print("• Cultural Fit: Eastern-Western communication bridge, Mandarin advantage")
            return True
        else:
            print("❌ Failed to send email")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    asyncio.run(create_honest_ecarx_application())