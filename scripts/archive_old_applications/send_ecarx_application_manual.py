#!/usr/bin/env python3
"""
Manual Email Sender for ECARX Application
Sends the honest CV and cover letter to hongzhili01@gmail.com
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

def send_ecarx_application():
    """Send ECARX application via email"""
    
    # Email configuration
    sender_email = "leeharvad@gmail.com"
    sender_password = "vsdclxhjnklrccsf"  # App password
    target_email = "hongzhili01@gmail.com"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = f"ECARX Application <{sender_email}>"
    msg['To'] = target_email
    msg['Subject'] = "🚗 ECARX Infotainment Developer Application - Honest Technical Profile"
    
    # Email body
    email_body = f"""Hi Hongzhi,

🚗 ECARX INFOTAINMENT SOFTWARE DEVELOPER APPLICATION

Your application package is ready with an honest technical profile:

📋 POSITION DETAILS:
• Role: Infotainment Software Developer
• Company: ECARX
• Location: Gothenburg, Sweden
• Department: R&D Team

🎯 HONEST TECHNICAL PROFILE:
✅ Strong Android Development (5+ years)
✅ Kotlin & Java Expertise
✅ Android Studio Proficiency
✅ Cross-Cultural Communication Skills
✅ Automotive Industry Passion
✅ Innovative Hobby Projects (Car TV Player, Android Auto eBook Reader, Car Voice Bot)

📚 LEARNING OPPORTUNITIES:
• Native AOSP Development (Soong/Make build systems)
• C/C++ for Performance-Critical Components
• Automotive Communication Protocols

🌍 CULTURAL ADVANTAGES:
• Eastern-Western Communication Bridge
• Mandarin Chinese Proficiency
• Experience in Global Teams

📄 ATTACHED DOCUMENTS:
1. ECARX_Honest_CV.pdf - Complete technical profile with accurate skill levels
2. ECARX_Honest_Cover_Letter.pdf - Emphasizes automotive passion and learning mindset

💡 APPLICATION STRATEGY:
This honest approach positions you as:
- A strong Android developer ready to grow into automotive/AOSP
- Someone with genuine automotive passion (hobby projects prove this)
- A cultural bridge for ECARX's global operations
- A proactive learner who thrives in ambiguous environments

🎯 KEY SELLING POINTS:
• 5+ years Android development experience
• Proven automotive interest through personal projects
• Cross-cultural communication skills (perfect for ECARX)
• Willingness to learn and grow in native development
• Problem-solving in dynamic, undefined environments

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Ready to submit! The honest approach shows integrity and growth mindset. 🚀

Best regards,
JobHunter Application System
"""
    
    msg.attach(MIMEText(email_body, 'plain'))
    
    # Attach CV
    try:
        with open("ECARX_Honest_CV.pdf", "rb") as f:
            cv_attachment = MIMEApplication(f.read(), _subtype="pdf")
            cv_attachment.add_header('Content-Disposition', 'attachment', filename="ECARX_Honest_CV.pdf")
            msg.attach(cv_attachment)
        print("✅ CV attached")
    except FileNotFoundError:
        print("❌ CV file not found")
        return False
    
    # Attach Cover Letter
    try:
        with open("ECARX_Honest_Cover_Letter.pdf", "rb") as f:
            cl_attachment = MIMEApplication(f.read(), _subtype="pdf")
            cl_attachment.add_header('Content-Disposition', 'attachment', filename="ECARX_Honest_Cover_Letter.pdf")
            msg.attach(cl_attachment)
        print("✅ Cover Letter attached")
    except FileNotFoundError:
        print("❌ Cover Letter file not found")
        return False
    
    # Send email
    try:
        print("📧 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        print("📤 Sending email...")
        text = msg.as_string()
        server.sendmail(sender_email, target_email, text)
        server.quit()
        
        print("✅ Email sent successfully to hongzhili01@gmail.com!")
        print("\n📊 Application Summary:")
        print("• CV: 113.8 KB - Honest technical profile")
        print("• Cover Letter: 26.7 KB - Automotive passion focus")
        print("• Strategy: Growth mindset with strong Android foundation")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚗 Sending ECARX Application with Honest Technical Profile...")
    send_ecarx_application()