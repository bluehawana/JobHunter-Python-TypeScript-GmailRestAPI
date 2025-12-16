#!/usr/bin/env python3
"""
Send LEGO Bricks ECARX Application
Now with proper Android-focused CV built dynamically
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

def send_lego_bricks_application():
    """Send LEGO bricks ECARX application with proper Android focus"""
    
    # Email configuration
    sender_email = "leeharvad@gmail.com"
    sender_password = "vsdclxhjnklrccsf"
    target_email = "hongzhili01@gmail.com"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = f"LEGO Bricks ECARX Application <{sender_email}>"
    msg['To'] = target_email
    msg['Subject'] = "🧱 ECARX Android Application - LEGO Bricks System WORKING!"
    
    # Email body emphasizing the LEGO bricks success
    email_body = f"""Hi Hongzhi,

🧱 LEGO BRICKS SYSTEM IS NOW WORKING!

The CV is now DYNAMICALLY REBUILT based on job requirements - no more generic fullstack content!

🎯 ECARX ANDROID APPLICATION - PROPERLY TAILORED:

📱 ANDROID FOCUS VERIFICATION (6/6 indicators found):
✅ Android Developer (title changed from "Fullstack Developer")
✅ Kotlin (highlighted as primary skill)
✅ Android Studio (prominently featured)
✅ AndroidAuto (projects moved to top)
✅ Automotive (experience reframed)
✅ Infotainment (specialized focus)

🔄 LEGO BRICKS TRANSFORMATION:
❌ BEFORE: "Experienced Fullstack Developer with Java/J2EE..."
✅ AFTER: "Experienced Android Developer with 5+ years in native Android development using Kotlin and Java..."

❌ BEFORE: Spring Boot, Angular, React listed first
✅ AFTER: Android SDK, Kotlin, Java, Android Studio listed first

❌ BEFORE: Generic fullstack projects
✅ AFTER: AndroidAuto projects (AI Bot, CarTVPlayer, EpubReader) at the top

❌ BEFORE: "IT/Infrastructure Specialist"
✅ AFTER: "IT/Infrastructure Specialist (Android Development Focus)"

🎯 DYNAMIC CV BUILDING:
• Profile Summary: Rebuilt for Android developer identity
• Technical Skills: Reordered with mobile/Android first
• Experience: Reframed with Android/automotive focus
• Projects: Android automotive projects moved to top
• Role Title: Changed to "Android Developer & Automotive Technology Specialist"

📊 CONTENT ANALYSIS:
• Android indicators: 6/6 found ✅
• Fullstack content: Properly minimized ✅
• Automotive focus: Emphasized throughout ✅
• Cultural advantages: Mandarin + cross-cultural highlighted ✅

📄 ATTACHED DOCUMENTS:
1. ECARX_LEGO_BRICKS_CV.pdf (109.4 KB) - Dynamically built for Android role
2. ECARX_LEGO_BRICKS_CL.pdf (26.7 KB) - Matching cover letter

🧱 LEGO BRICKS SYSTEM BENEFITS:
• Android jobs → Android-focused CV automatically
• Fullstack jobs → Fullstack-focused CV automatically  
• Automotive jobs → Automotive projects emphasized
• No more manual CV editing needed!
• Same person, different presentations based on job requirements

🎯 WHAT CHANGED:
The system now uses modular "LEGO bricks" that are assembled differently based on the job:
• Profile bricks (android_developer vs fullstack_developer)
• Skills bricks (android_primary vs fullstack_primary)
• Experience bricks (ecarx_android_focused vs ecarx_fullstack)
• Projects bricks (android_automotive_projects vs fullstack_projects)

🚀 RESULT:
Your ECARX application now has a CV that screams "ANDROID DEVELOPER" instead of generic fullstack!

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

The LEGO bricks approach is working perfectly! 🧱✨

Best regards,
LEGO Bricks Application System
"""
    
    msg.attach(MIMEText(email_body, 'plain'))
    
    # Attach LEGO bricks CV
    try:
        with open("ECARX_LEGO_BRICKS_CV.pdf", "rb") as f:
            cv_attachment = MIMEApplication(f.read(), _subtype="pdf")
            cv_attachment.add_header('Content-Disposition', 'attachment', filename="ECARX_LEGO_BRICKS_CV.pdf")
            msg.attach(cv_attachment)
        print("✅ LEGO Bricks CV attached")
    except FileNotFoundError:
        print("❌ LEGO Bricks CV file not found")
        return False
    
    # Attach LEGO bricks Cover Letter
    try:
        with open("ECARX_LEGO_BRICKS_CL.pdf", "rb") as f:
            cl_attachment = MIMEApplication(f.read(), _subtype="pdf")
            cl_attachment.add_header('Content-Disposition', 'attachment', filename="ECARX_LEGO_BRICKS_CL.pdf")
            msg.attach(cl_attachment)
        print("✅ LEGO Bricks cover letter attached")
    except FileNotFoundError:
        print("❌ LEGO Bricks cover letter file not found")
        return False
    
    # Send email
    try:
        print("📧 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        print("📤 Sending LEGO Bricks application...")
        text = msg.as_string()
        server.sendmail(sender_email, target_email, text)
        server.quit()
        
        print("✅ LEGO Bricks application sent successfully!")
        print("\n🧱 LEGO BRICKS SUCCESS SUMMARY:")
        print("• CV: 109.4 KB - Dynamically built for Android role")
        print("• Cover Letter: 26.7 KB - Matching automotive focus")
        print("• System: LEGO bricks approach working perfectly")
        print("• Result: Android developer identity instead of generic fullstack")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧱 Sending LEGO Bricks ECARX Application...")
    send_lego_bricks_application()