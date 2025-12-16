#!/usr/bin/env python3
"""
Send Android-Tailored ECARX Application
100% focused on Android development requirements
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

def send_android_tailored_application():
    """Send Android-tailored ECARX application"""
    
    # Email configuration
    sender_email = "leeharvad@gmail.com"
    sender_password = "vsdclxhjnklrccsf"
    target_email = "hongzhili01@gmail.com"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = f"ECARX Android Expert Application <{sender_email}>"
    msg['To'] = target_email
    msg['Subject'] = "🎯 ECARX Android Infotainment Developer - 100% Tailored Application"
    
    # Email body emphasizing Android expertise
    email_body = f"""Hi Hongzhi,

🎯 ECARX ANDROID INFOTAINMENT DEVELOPER - PERFECTLY TAILORED APPLICATION

Your application has been completely restructured to highlight Android expertise first!

📱 ANDROID DEVELOPMENT FOCUS (100% Match):
✅ 5+ Years Android Development Experience
✅ Kotlin & Java Expertise with Android Studio
✅ Android SDK & Platform Architecture Knowledge  
✅ System-Level Components (Activities, Services, Content Providers, Broadcast Receivers)
✅ Real Automotive Projects Portfolio
✅ Cross-Cultural Communication (Mandarin Advantage)

🚗 AUTOMOTIVE PASSION DEMONSTRATED:
1. AndroidAuto AI Bot - Voice assistant with "HiCar" wake-word
2. AndroidAuto TTS EpubReader - In-car audiobook system
3. AndroidAuto CarTVPlayer - Custom media player with voice commands
4. Gothenburg TaxiPooling - Android app with real-time geolocation

🎯 EXACT JOB REQUIREMENTS ALIGNMENT:

PRIMARY REQUIREMENTS (✅ FULLY QUALIFIED):
• 5+ years Android development ✅
• Kotlin and Java expertise ✅
• Android Studio proficiency ✅
• Android SDK knowledge ✅
• System components experience ✅
• Problem-solving abilities ✅
• Independent/collaborative work ✅

LEARNING OPPORTUNITIES (Honest Approach):
• Native AOSP development (Soong/Make build systems)
• C/C++ for performance-critical components
• Android runtime resource overlays (RRO)

🌍 CULTURAL ADVANTAGES:
• Mandarin Chinese proficiency (highly desirable)
• Eastern-Western communication bridge
• Global team collaboration experience
• Automotive industry genuine passion

📄 ATTACHED DOCUMENTS:
1. ECARX_Android_Tailored_CV.pdf - Android expertise highlighted first
2. ECARX_Android_Cover_Letter.pdf - Automotive passion & technical alignment

🎯 APPLICATION STRATEGY:
This tailored approach positions you as:
• PRIMARY: Android development expert (5+ years)
• SECONDARY: Automotive enthusiast with real projects
• ADVANTAGE: Cultural bridge for ECARX's global operations
• MINDSET: Growth-oriented for AOSP/native development

📊 TECHNICAL HIGHLIGHTS RESTRUCTURED:
• Android Development moved to TOP of CV
• Automotive projects prominently featured
• Kotlin/Java expertise emphasized
• Real-world Android components experience
• Voice processing and real-time systems
• Cross-platform mobile development

💡 WHY THIS APPROACH WORKS:
• Meets ALL primary job requirements
• Shows genuine automotive passion through projects
• Honest about learning opportunities (builds trust)
• Cultural fit advantage (Mandarin + communication skills)
• Demonstrates problem-solving in real projects

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

100% tailored for Android Infotainment role! 🚗📱

Best regards,
Android-Focused Application System
"""
    
    msg.attach(MIMEText(email_body, 'plain'))
    
    # Attach Android-tailored CV
    try:
        with open("ECARX_Android_Tailored_CV.pdf", "rb") as f:
            cv_attachment = MIMEApplication(f.read(), _subtype="pdf")
            cv_attachment.add_header('Content-Disposition', 'attachment', filename="ECARX_Android_Tailored_CV.pdf")
            msg.attach(cv_attachment)
        print("✅ Android-tailored CV attached")
    except FileNotFoundError:
        print("❌ Android CV file not found")
        return False
    
    # Attach Android-focused Cover Letter
    try:
        with open("ECARX_Android_Cover_Letter.pdf", "rb") as f:
            cl_attachment = MIMEApplication(f.read(), _subtype="pdf")
            cl_attachment.add_header('Content-Disposition', 'attachment', filename="ECARX_Android_Cover_Letter.pdf")
            msg.attach(cl_attachment)
        print("✅ Android-focused cover letter attached")
    except FileNotFoundError:
        print("❌ Android cover letter file not found")
        return False
    
    # Send email
    try:
        print("📧 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        print("📤 Sending Android-tailored application...")
        text = msg.as_string()
        server.sendmail(sender_email, target_email, text)
        server.quit()
        
        print("✅ Android-tailored application sent successfully!")
        print("\n🎯 FINAL APPLICATION SUMMARY:")
        print("• CV: 113.8 KB - Android expertise highlighted first")
        print("• Cover Letter: 26.7 KB - Automotive passion + technical alignment")
        print("• Strategy: 100% match for primary requirements")
        print("• Advantage: Cultural fit + genuine automotive projects")
        print("• Approach: Honest about learning opportunities")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Sending 100% Android-Tailored ECARX Application...")
    send_android_tailored_application()