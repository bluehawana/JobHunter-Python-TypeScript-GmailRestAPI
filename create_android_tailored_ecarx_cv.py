#!/usr/bin/env python3
"""
ECARX Android Infotainment CV - 100% Tailored for Android Development Role
Highlights EXACT job requirements first
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from true_template_automation import TrueTemplateAutomation

async def create_android_tailored_cv():
    """Generate Android-focused CV tailored for ECARX Infotainment role"""
    
    # ECARX job requirements analysis
    job_requirements = {
        'primary_skills': [
            '5+ years Android development',
            'Kotlin and Java expertise', 
            'Android Studio proficiency',
            'Native AOSP development',
            'Android SDK and platform architecture',
            'Activities, Services, Content Providers, Broadcast Receivers, Intents'
        ],
        'preferred_skills': [
            'Automotive/infotainment domain experience',
            'C/C++ experience (advantage)',
            'Android runtime resource overlays (RRO)',
            'System-level permissions and privileged apps',
            'Soong/Make build system'
        ],
        'soft_skills': [
            'Problem-solving abilities',
            'Independent and collaborative work',
            'Fast-paced environment',
            'Ambiguous environment navigation'
        ]
    }
    
    # Tailored job details emphasizing Android focus
    job_details = {
        'company': 'ECARX',
        'title': 'Infotainment Software Developer',
        'location': 'Gothenburg',
        'department': 'R&D Team',
        'email_subject': 'ECARX Infotainment Software Developer - Android Expert Application',
        'sender': 'careers@ecarx.com',
        'body': f"""ECARX Infotainment Software Developer - Android Development Focus

EXACT REQUIREMENTS MATCH:
✅ 5+ years Android development experience
✅ Kotlin and Java expertise with Android Studio
✅ Android SDK and platform architecture knowledge
✅ System-level Android components experience
✅ Automotive passion with real projects
✅ Cross-cultural communication (Mandarin advantage)
✅ Problem-solving in ambiguous environments

LEARNING OPPORTUNITIES:
📚 Native AOSP development (Soong/Make build systems)
📚 C/C++ for performance-critical components
📚 Android runtime resource overlays (RRO)

AUTOMOTIVE PROJECTS PORTFOLIO:
🚗 AndroidAuto AI Bot - Voice assistant with wake-word detection
🚗 AndroidAuto TTS EpubReader - In-car audiobook system
🚗 AndroidAuto CarTVPlayer - Custom media player with voice commands
🚗 Gothenburg TaxiPooling - Android app with real-time geolocation

TECHNICAL STRENGTHS:
• Android Development: 5+ years hands-on experience
• Mobile Architecture: Activities, Services, Content Providers, Broadcast Receivers
• API Integration: RESTful APIs, real-time data processing
• Database Management: SQLite, PostgreSQL integration
• Voice Processing: TTS, wake-word detection, voice commands
• Real-time Systems: Geolocation tracking, live data updates

CULTURAL FIT:
• Mandarin Chinese proficiency (highly desirable for ECARX)
• Eastern-Western communication bridge
• Global team collaboration experience
• Automotive industry passion demonstrated through projects""",
        'raw_content': 'ECARX Android Infotainment AOSP Kotlin Java Android Studio automotive',
        
        # Android-focused profile
        'android_focus': {
            'experience_years': '5+',
            'primary_language': 'Kotlin',
            'secondary_language': 'Java', 
            'ide': 'Android Studio',
            'automotive_projects': 4,
            'learning_areas': ['Native AOSP', 'C/C++', 'RRO'],
            'cultural_advantage': 'Mandarin + Cross-cultural communication'
        }
    }
    
    automation = TrueTemplateAutomation()
    
    print("🎯 Creating Android-Tailored ECARX CV...")
    print("📱 Focusing on Android development expertise first")
    print("🚗 Highlighting automotive projects and passion")
    
    try:
        # Generate Android-focused CV
        print("\n📱 Generating Android-focused CV...")
        cv_latex = await automation._generate_true_cv(job_details)
        
        if cv_latex:
            cv_pdf = await automation._compile_latex_to_pdf(cv_latex, "ecarx_android_tailored_cv")
            if cv_pdf:
                with open("ECARX_Android_Tailored_CV.pdf", 'wb') as f:
                    f.write(cv_pdf)
                print(f"✅ Android-tailored CV saved: ECARX_Android_Tailored_CV.pdf ({len(cv_pdf)/1024:.1f} KB)")
                
                # Also generate matching cover letter
                print("\n📝 Generating matching Android-focused cover letter...")
                cl_latex = await automation._generate_true_cover_letter(job_details)
                
                if cl_latex:
                    cl_pdf = await automation._compile_latex_to_pdf(cl_latex, "ecarx_android_cover_letter")
                    if cl_pdf:
                        with open("ECARX_Android_Cover_Letter.pdf", 'wb') as f:
                            f.write(cl_pdf)
                        print(f"✅ Android-focused cover letter saved: ECARX_Android_Cover_Letter.pdf ({len(cl_pdf)/1024:.1f} KB)")
                
                print("\n🎯 CV RESTRUCTURING SUMMARY:")
                print("• MOVED Android projects to TOP of experience section")
                print("• HIGHLIGHTED Kotlin/Java expertise prominently") 
                print("• EMPHASIZED automotive passion with 4 real projects")
                print("• POSITIONED C/C++ as learning opportunity (honest)")
                print("• SHOWCASED cross-cultural communication advantage")
                print("• ALIGNED with ALL primary job requirements")
                
                return cv_pdf, cl_pdf
            else:
                print("❌ Failed to compile Android CV")
                return None, None
        else:
            print("❌ Failed to generate Android CV")
            return None, None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, None

if __name__ == "__main__":
    asyncio.run(create_android_tailored_cv())