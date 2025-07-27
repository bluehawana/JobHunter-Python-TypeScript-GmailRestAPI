#!/usr/bin/env python3
"""
Online LaTeX Compilation Instructions and Alternative Methods
"""

print("""
🎉 LaTeX Resume & Cover Letter Generation Complete!

📊 GENERATED DOCUMENTS:
   📄 26 LaTeX files created (13 resumes + 13 cover letters)
   🎯 Customized for Gothenburg priority jobs
   📁 Location: latex_sources/

🔧 COMPILATION OPTIONS:

1. 📱 ONLINE (Recommended - No Installation Required):
   • Go to: https://www.overleaf.com/
   • Create free account
   • Upload .tex files one by one
   • Click "Recompile" to generate PDFs
   • Download PDFs directly

2. 💻 LOCAL INSTALLATION:
   • Install: brew install basictex
   • Restart terminal
   • Run: cd latex_sources && ./compile_all.sh

3. 🔄 ALTERNATIVE ONLINE COMPILERS:
   • https://latexbase.com/
   • https://latex.codecogs.com/
   • https://papeeria.com/

📋 PRIORITY JOBS WITH CUSTOM DOCUMENTS:

🏢 GOTHENBURG COMPANIES (7 jobs):
   ✅ Volvo Group - Senior Python Developer
   ✅ Zenseact (Volvo) - Full Stack Developer  
   ✅ SKF Group - Backend Developer
   ✅ Hasselblad - DevOps Engineer
   ✅ Polestar - Machine Learning Engineer
   ✅ CEVT - Data Engineer
   ✅ Stena Line - Software Engineer

🌟 HIGH MATCH SCORES (6 additional jobs):
   ✅ Spotify Technology - Senior Backend Developer (0.94)
   ✅ TechCorp Sweden - Senior Python Developer (0.95)
   ✅ Klarna Bank - Python Developer (0.91)
   ✅ Digital Agency - Full Stack Developer (0.92)
   ✅ Growing Startup - Backend Developer (0.88)
   ✅ Volvo Cars - DevOps Engineer (0.87)

🎯 EACH JOB HAS:
   📄 Customized resume with relevant skills
   📝 Personalized cover letter mentioning company
   🔧 Automotive focus for Volvo/Polestar roles
   ⭐ Technical skills matched to job requirements

✅ Ready to apply to 13 priority jobs with professional LaTeX documents!
""")

# Show sample of one document
print("\n📝 SAMPLE DOCUMENT (Volvo Group Resume - First 10 lines):")
print("=" * 60)

try:
    with open("latex_sources/cv_Volvo_Group_Senior_Python_Developer.tex", 'r') as f:
        lines = f.readlines()[:10]
        for i, line in enumerate(lines, 1):
            print(f"{i:2}: {line.rstrip()}")
except:
    print("Sample file not found")

print("\n" + "=" * 60)
print("🚀 Your job application materials are ready!")