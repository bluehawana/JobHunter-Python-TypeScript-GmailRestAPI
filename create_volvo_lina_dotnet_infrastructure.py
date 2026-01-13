#!/usr/bin/env python3
"""
🧱 LEGO Bricks + AI: Volvo Lina .NET Infrastructure Developer
Creates perfectly tailored resume using our intelligent system
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))
sys.path.append(str(Path(__file__).parent / 'backend' / 'app'))

from lego_api import analyze_job_description, build_lego_cv, generate_ai_enhancement_prompts
from ai_resume_prompts import AIResumePrompts
from cv_templates import CVTemplateManager
import json

def main():
    """Generate Volvo Lina .NET Infrastructure Developer application"""
    
    # Job Description from Lina (Volvo Group Manager)
    job_description = """
    Full Stack Developer – C# / .NET – (Infrastructure experience)

    We are looking for a Full Stack Developer with strong experience in C# and .NET 
    with an infrastructure experience, to join a team responsible for systems handling 
    part number setup and lifecycle management within an automotive environment. 
    The team develops business-critical applications that support product 
    configuration, manufacturing, and enterprise integrations.

    The role spans the full stack, covering backend services, frontend user interfaces, 
    and relational databases. The ideal candidate has hands-on experience with Azure-
    based solutions, works comfortably in a DevOps-oriented setup, and has exposure 
    to Infrastructure as Code (IaC) for provisioning and maintaining environments. 
    Practical use of AI-assisted development and infrastructure tools is beneficial.

    We are seeking someone proactive, collaborative, and adaptable, who thrives in a 
    high-delivery agile team, takes ownership from development through deployment, 
    and brings curiosity and a continuous-improvement mindset, including 
    responsible adoption of AI in engineering and platform work.

    Key skills:
    C# / .NET (ASP.NET Core) and REST API development
    Frontend experience with Angular, Blazor, or similar SPA frameworks
    Databases: SQL Server / PostgreSQL and NoSQL (Azure Cosmos DB)
    Cloud-native development on Kubernetes, ideally Azure Red Hat OpenShift (ARO)
    Azure platform services such as Key Vault, API Management (APIM), and Entra ID 
    (Identity & access management)
    Infrastructure as Code using Terraform
    CI/CD pipelines, GitOps with Argo CD, and containerization (Docker)
    """
    
    company = "Volvo Group"
    position = "Full Stack Developer – C# / .NET – (Infrastructure experience)"
    
    print("🧱 LEGO Bricks + AI: Volvo .NET Infrastructure Developer")
    print("=" * 60)
    
    # Step 1: Analyze job description with AI
    print("\n1️⃣ Analyzing job description with AI...")
    analysis = analyze_job_description(job_description)
    
    print(f"   Role Type: {analysis['roleType']}")
    print(f"   Role Category: {analysis['roleCategory']}")
    print(f"   Company: {analysis['company']}")
    print(f"   Key Technologies: {', '.join(analysis['keywords'][:8])}")
    print(f"   AI Analysis: {analysis['aiAnalysis']['model']} (confidence: {analysis['aiAnalysis']['confidence']:.0%})")
    
    # Step 2: Build customized CV using LEGO bricks
    print("\n2️⃣ Building CV with LEGO bricks...")
    cv_content = build_lego_cv(
        role_type=analysis['roleType'],
        company=company,
        title=position,
        role_category=analysis['roleCategory'],
        job_description=job_description
    )
    
    # Step 3: Create output directory
    output_dir = Path("job_applications/volvo_lina_dotnet_infrastructure")
    output_dir.mkdir(exist_ok=True)
    
    # Step 4: Save CV
    cv_filename = "Volvo_Lina_DotNet_Infrastructure_CV.tex"
    cv_path = output_dir / cv_filename
    
    with open(cv_path, 'w', encoding='utf-8') as f:
        f.write(cv_content)
    
    print(f"   ✅ CV saved: {cv_path}")
    
    # Step 5: Generate AI enhancement prompts
    print("\n3️⃣ Generating AI enhancement prompts...")
    ai_prompts = generate_ai_enhancement_prompts(
        job_description=job_description,
        customized_cv_text=cv_content,
        company=company,
        position=position
    )
    
    # Save AI prompts
    prompts_file = output_dir / "AI_Enhancement_Prompts.md"
    
    with open(prompts_file, 'w', encoding='utf-8') as f:
        f.write("# 🤖 AI Enhancement Prompts for Volvo .NET Infrastructure Role\n\n")
        f.write(f"**Position**: {position}\n")
        f.write(f"**Company**: {company}\n")
        f.write(f"**Generated**: {analysis['aiAnalysis']['model']}\n\n")
        
        f.write("## 1. Resume Rewrite (Get More Interviews)\n")
        f.write("```\n")
        f.write(ai_prompts['resume_rewrite'])
        f.write("\n```\n\n")
        
        f.write("## 2. JD Match Check (Aim for 90% Match)\n")
        f.write("```\n")
        f.write(ai_prompts['jd_match'])
        f.write("\n```\n\n")
        
        f.write("## 3. Interview Preparation (15 Questions + Answers)\n")
        f.write("```\n")
        f.write(ai_prompts['interview_prep'])
        f.write("\n```\n\n")
        
        f.write("## 4. Proof Projects (Complete This Week)\n")
        f.write("```\n")
        f.write(ai_prompts['proof_projects'])
        f.write("\n```\n\n")
        
        f.write("## 5. Cover Letter Generator\n")
        f.write("```\n")
        f.write(ai_prompts['cover_letter'])
        f.write("\n```\n\n")
        
        f.write("## 6. LinkedIn Optimization\n")
        f.write("```\n")
        f.write(ai_prompts['linkedin_optimization'])
        f.write("\n```\n\n")
        
        f.write("## 7. Salary Negotiation Strategy\n")
        f.write("```\n")
        f.write(ai_prompts['salary_negotiation'])
        f.write("\n```\n\n")
    
    print(f"   ✅ AI prompts saved: {prompts_file}")
    
    # Step 6: Create application summary
    print("\n4️⃣ Creating application summary...")
    
    summary_content = f"""# 🎯 Volvo Lina .NET Infrastructure Developer Application

## Job Analysis
- **Position**: {position}
- **Company**: {company}
- **Role Category**: {analysis['roleCategory']}
- **AI Confidence**: {analysis['aiAnalysis']['confidence']:.0%}

## Key Requirements Match
✅ **C# / .NET (ASP.NET Core)**: 1+ year professional experience at Synteda
✅ **Infrastructure Experience**: Current role at Ecarx with Kubernetes, Terraform, Azure
✅ **Azure Platform**: Azure AKS, App Services, Functions experience
✅ **DevOps**: CI/CD pipelines, GitHub Actions, GitLab CI
✅ **Databases**: SQL Server, PostgreSQL, Entity Framework
✅ **Frontend**: React experience (can adapt to Angular/Blazor)
✅ **Containerization**: Docker, Kubernetes expertise
✅ **Infrastructure as Code**: Terraform experience

## Competitive Advantages
1. **Professional .NET Experience**: Synteda (C# .NET Core, Azure, microservices)
2. **Infrastructure Expertise**: Ecarx (Kubernetes, Terraform, CI/CD, 24/7 support)
3. **Automotive Industry**: 1+ year at Ecarx/Geely (aligns with Volvo)
4. **Cost Optimization**: 45% cloud cost reduction, 35% MTTR improvement
5. **Full-Stack**: React frontend + .NET backend combination
6. **Gothenburg Location**: Already local, no relocation needed

## Skills We Don't Have (Skip These)
❌ **Azure Red Hat OpenShift (ARO)**: No experience - skip this
❌ **Blazor**: No experience - emphasize React instead
❌ **Argo CD**: No experience - emphasize GitHub Actions/GitLab CI
❌ **Azure Cosmos DB**: No experience - emphasize SQL Server/PostgreSQL

## Application Strategy
1. **Lead with .NET**: Professional experience at Synteda
2. **Emphasize Infrastructure**: Current Ecarx role shows DevOps/Infrastructure skills
3. **Highlight Automotive**: Ecarx/Geely experience aligns with Volvo
4. **Show Full-Stack**: React + .NET combination
5. **Demonstrate Results**: Quantified achievements (45% cost reduction, etc.)

## Files Generated
- `{cv_filename}`: Tailored CV with LEGO bricks + AI optimization
- `AI_Enhancement_Prompts.md`: 7 AI prompts for further optimization
- `APPLICATION_SUMMARY.md`: This summary file

## Next Steps
1. **Review CV**: Check the generated LaTeX file
2. **Use AI Prompts**: Copy prompts to ChatGPT/Claude for further enhancement
3. **Compile PDF**: Use Overleaf or local LaTeX to generate PDF
4. **LinkedIn Message**: Use cover letter prompt to craft LinkedIn message to Lina
5. **Prepare Interview**: Use interview prep prompts to practice

## Key Talking Points for Lina
- "I have 1+ year professional C# .NET Core experience from Synteda"
- "Currently at Ecarx doing infrastructure work - Kubernetes, Terraform, Azure"
- "Automotive industry experience aligns with Volvo's transport solutions"
- "Full-stack developer who can handle both .NET backend and React frontend"
- "Based in Gothenburg, ready to start immediately"
"""
    
    summary_path = output_dir / "APPLICATION_SUMMARY.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"   ✅ Summary saved: {summary_path}")
    
    # Step 7: Final output
    print("\n🎉 Application Generated Successfully!")
    print("=" * 60)
    print(f"📁 Output Directory: {output_dir}")
    print(f"📄 CV File: {cv_filename}")
    print(f"🤖 AI Prompts: AI_Enhancement_Prompts.md")
    print(f"📋 Summary: APPLICATION_SUMMARY.md")
    print("\n💡 Next Steps:")
    print("1. Review the generated CV")
    print("2. Use AI prompts for further optimization")
    print("3. Compile PDF using Overleaf")
    print("4. Send LinkedIn message to Lina using cover letter prompt")

if __name__ == "__main__":
    main()