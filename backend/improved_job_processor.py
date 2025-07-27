#!/usr/bin/env python3
"""
Improved Job Processor - Sends both TEX and PDF files with preview
1. Compiles LaTeX to PDF (tries multiple times with error handling)
2. Sends both .tex source files AND .pdf files
3. Includes content preview in email
4. Provides clear editing/compilation instructions
"""
import asyncio
import subprocess
import tempfile
import shutil
import os
import smtplib
import re
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Import our smart editor
import sys
sys.path.append(str(Path(__file__).parent))
from smart_latex_editor import SmartLaTeXEditor

class ImprovedJobProcessor(SmartLaTeXEditor):
    def __init__(self):
        super().__init__()
    
    def compile_latex_with_fallback(self, tex_content, output_name):
        """Compile LaTeX with multiple fallback attempts"""
        
        # First, try to save and see the content
        print(f"🔍 Checking LaTeX content for {output_name}...")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / f"{output_name}.tex"
            
            try:
                # Write the LaTeX file
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(tex_content)
                
                print(f"✅ LaTeX file written: {tex_file}")
                
                # Try compilation with different approaches
                compilation_attempts = [
                    # Attempt 1: Standard compilation
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(temp_path), str(tex_file)],
                    # Attempt 2: With halt-on-error
                    ['pdflatex', '-halt-on-error', '-output-directory', str(temp_path), str(tex_file)],
                    # Attempt 3: With different interaction mode
                    ['pdflatex', '-interaction=batchmode', '-output-directory', str(temp_path), str(tex_file)]
                ]
                
                for attempt, cmd in enumerate(compilation_attempts, 1):
                    print(f"🔨 Compilation attempt {attempt}/3...")
                    
                    try:
                        # Run compilation twice for references
                        for run in range(2):
                            result = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_path, timeout=30)
                            
                            if result.returncode == 0:
                                print(f"✅ Compilation successful on attempt {attempt}, run {run+1}")
                                break
                            elif run == 0:
                                print(f"⚠️  First run had issues, trying second run...")
                            else:
                                print(f"❌ Attempt {attempt} failed")
                                if attempt < len(compilation_attempts):
                                    print(f"Trying different compilation method...")
                                break
                        else:
                            # Both runs completed successfully
                            pdf_file = temp_path / f"{output_name}.pdf"
                            if pdf_file.exists():
                                final_path = f"{output_name}.pdf"
                                shutil.copy2(pdf_file, final_path)
                                size = os.path.getsize(final_path) / 1024
                                print(f"🎉 PDF successfully generated: {final_path} ({size:.1f} KB)")
                                return final_path
                    
                    except subprocess.TimeoutExpired:
                        print(f"⏰ Compilation attempt {attempt} timed out")
                        continue
                    except Exception as e:
                        print(f"❌ Error in attempt {attempt}: {e}")
                        continue
                
                # If all compilation attempts failed, still return the tex file info
                print("⚠️  PDF compilation failed, but LaTeX source is available")
                print("📝 You can compile manually with: pdflatex filename.tex")
                return None
                
            except Exception as e:
                print(f"❌ Error writing/compiling LaTeX: {e}")
                return None
    
    def extract_preview_content(self, tex_content, content_type="CV"):
        """Extract preview content from LaTeX for email"""
        
        try:
            # Extract job title
            title_match = re.search(r'\\textit\{([^}]+)\}', tex_content)
            job_title = title_match.group(1) if title_match else "Position"
            
            if content_type == "CV":
                # Extract profile summary
                profile_match = re.search(r'\\section\*\{Profile Summary\}\\s*([^\\]+)', tex_content)
                profile = profile_match.group(1).strip() if profile_match else "Profile summary tailored for this role..."
                
                # Extract first few skills
                skills_section = re.search(r'\\section\*\{Core Technical Skills\}.*?\\begin\{itemize\}.*?(\\item[^\\]*){3}', tex_content, re.DOTALL)
                skills_preview = "• Programming Languages, Frameworks, Cloud Platforms..." if not skills_section else "Skills section tailored..."
                
                preview = f"""
📋 Job Title: {job_title}

📝 Profile Summary Preview:
{profile[:200]}...

🔧 Technical Skills:
{skills_preview}

💼 Experience: 6 positions highlighted (ECARX, Synteda, IT-Högskolan, etc.)
🚀 Hobby Projects: 3 major projects (TaxiCarPooling, SmartTV, E-commerce)
🎓 Education: IT Högskolan, University of Gothenburg
📜 Certifications: AWS, Azure certifications
"""
            
            else:  # Cover Letter
                # Extract company and content preview
                company_match = re.search(r'\\\\([^\\]+)\\\\', tex_content)
                company = company_match.group(1) if company_match else "Company"
                
                # Extract opening paragraph
                content_match = re.search(r'I am writing to express.*?\.', tex_content)
                opening = content_match.group(0) if content_match else "Professional introduction tailored for this role..."
                
                preview = f"""
🏢 Company: {company}
💼 Position: {job_title}

📝 Opening Paragraph:
{opening}

✅ Content includes:
• Role-specific introduction and interest
• Technical expertise alignment
• Project examples and achievements  
• Company-specific motivation
• Professional closing
"""
            
            return preview.strip()
            
        except Exception as e:
            print(f"Warning: Could not extract preview - {e}")
            return f"Preview not available - {content_type} file ready for review"
    
    def send_improved_review_email(self, job_title, company, cv_tex, cl_tex, cv_pdf=None, cl_pdf=None, role_focus="fullstack"):
        """Send improved email with both files and preview"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        try:
            # Read LaTeX content for preview
            cv_content = ""
            cl_content = ""
            
            if cv_tex and Path(cv_tex).exists():
                with open(cv_tex, 'r', encoding='utf-8') as f:
                    cv_content = f.read()
            
            if cl_tex and Path(cl_tex).exists():
                with open(cl_tex, 'r', encoding='utf-8') as f:
                    cl_content = f.read()
            
            # Extract previews
            cv_preview = self.extract_preview_content(cv_content, "CV")
            cl_preview = self.extract_preview_content(cl_content, "Cover Letter")
            
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"JobHunter Complete: {job_title} at {company} - PDF + LaTeX Ready"
            
            # Create comprehensive email body
            pdf_status = "✅ Included" if cv_pdf and cl_pdf else "❌ Compilation failed - manual compilation needed"
            
            body = f"""Hi,

Complete job application package ready for your review:

🏢 Company: {company}
💼 Position: {job_title}
🎯 Role Focus: {role_focus.title()}
📍 Priority: {'🏢 Gothenburg' if 'gothenburg' in company.lower() or 'volvo' in company.lower() else '🌐 Remote/Other'}

📎 Files attached:
   • CV (PDF): {pdf_status}
   • Cover Letter (PDF): {pdf_status}
   • CV (LaTeX source): ✅ Always included for editing
   • Cover Letter (LaTeX source): ✅ Always included for editing

📋 CV PREVIEW:
{cv_preview}

📋 COVER LETTER PREVIEW:  
{cl_preview}

🔧 IF YOU NEED TO EDIT:
1. Download the .tex files (LaTeX source)
2. Open in any text editor (VS Code, Sublime, Notepad++)
3. Make your changes to the text content
4. Compile to PDF:
   - Method 1: pdflatex filename.tex (run twice)
   - Method 2: Use online LaTeX editor (Overleaf.com)
   - Method 3: Use LaTeX software (MiKTeX, TeX Live)

🔧 COMPILATION COMMANDS:
   pdflatex {cv_tex}
   pdflatex {cv_tex}  # Run twice for references
   pdflatex {cl_tex}
   pdflatex {cl_tex}  # Run twice for references

📤 READY TO SEND:
If PDFs look good, you can send them directly to employers.
If you made edits, recompile and then send.

🎯 This application uses your original LaTeX templates with smart edits for {role_focus} focus.

Best regards,
JobHunter Complete System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach all available files
            attachments = []
            
            # Add PDFs if available
            if cv_pdf and Path(cv_pdf).exists():
                attachments.append((cv_pdf, f"CV_{company}_{job_title}_READY.pdf"))
            if cl_pdf and Path(cl_pdf).exists():
                attachments.append((cl_pdf, f"CoverLetter_{company}_{job_title}_READY.pdf"))
            
            # Always add LaTeX source files
            if cv_tex and Path(cv_tex).exists():
                attachments.append((cv_tex, f"CV_{company}_{job_title}_SOURCE.tex"))
            if cl_tex and Path(cl_tex).exists():
                attachments.append((cl_tex, f"CoverLetter_{company}_{job_title}_SOURCE.tex"))
            
            for file_path, filename in attachments:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            server.quit()
            
            print(f"✅ Complete review email sent!")
            print(f"📎 Attached: {len(attachments)} files")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False

async def main():
    """Test improved processor with both PDF and LaTeX files"""
    processor = ImprovedJobProcessor()
    
    # Test jobs
    test_jobs = [
        ("Solution Developer", "Volvo Group", "Onsite Infrastructure", "Sven Erikssons gata 7", "Göteborg"),
        ("DevOps Engineer", "Spotify", "Infrastructure Team", "", "Stockholm"),
        ("Senior Backend Developer", "SKF Group", "Software Development", "", "Gothenburg")
    ]
    
    print("🎯 Improved JobHunter - PDF + LaTeX with Previews")
    print("=" * 60)
    print("📝 Sending both compiled PDFs AND LaTeX source files")
    print("👁️  Including content previews in email")
    print()
    
    for job_title, company, department, address, city in test_jobs:
        print(f"📋 Processing: {job_title} at {company}")
        
        role_focus = processor.determine_role_focus(job_title)
        print(f"🎯 Role Focus: {role_focus}")
        
        try:
            # Generate content
            print("✏️  Creating tailored content...")
            cv_content = processor.edit_cv_for_job(job_title, company, role_focus)
            cl_content = processor.edit_cover_letter_for_job(job_title, company, department, address, city)
            
            # Save LaTeX files
            cv_tex, cl_tex = processor.save_latex_files(cv_content, cl_content, job_title, company)
            print(f"💾 LaTeX saved: {cv_tex}, {cl_tex}")
            
            # Try to compile PDFs
            print("🔨 Compiling PDFs...")
            cv_pdf = processor.compile_latex_with_fallback(cv_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cv")
            cl_pdf = processor.compile_latex_with_fallback(cl_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cl")
            
            # Send comprehensive email
            print("📧 Sending complete package...")
            success = processor.send_improved_review_email(job_title, company, cv_tex, cl_tex, cv_pdf, cl_pdf, role_focus)
            
            if success:
                print(f"🎉 SUCCESS: Complete package sent!")
                
                # Clean up PDF files but keep LaTeX
                try:
                    if cv_pdf:
                        os.remove(cv_pdf)
                    if cl_pdf:
                        os.remove(cl_pdf)
                except:
                    pass
            else:
                print(f"❌ FAILED: Email not sent")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        print()
        await asyncio.sleep(2)
    
    print(f"📧 Check {processor.recipient_email} for complete packages!")
    print("👁️  Each email includes content previews and clear instructions")

if __name__ == "__main__":
    asyncio.run(main())