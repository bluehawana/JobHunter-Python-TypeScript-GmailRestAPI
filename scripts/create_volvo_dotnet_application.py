#!/usr/bin/env python3
"""
Generate tailored CV for Volvo Group Full-Stack Consultant (C# .NET) position
Direct contact: Linda Redgård (SW Manager Configurator at Volvo Digital & IT)
Highlights: Ecarx automotive experience, Synteda .NET development, Xamarin graduate project, hobby projects
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.lego_api import analyze_job_description, build_lego_cv, generate_ai_enhancement_prompts
import subprocess

# Job description from LinkedIn post by Linda Redgård
job_description = """
Volvo Group Digital & IT - Full-Stack Consultant (C# .NET)
Posted by: Linda Redgård, SW Manager Configurator
Location: Lindholmen, Gothenburg (Waterfront office)
Department: Volvo Digital & IT

About the Opportunity:
Linda Redgård just joined Volvo Digital & IT as SW Manager Configurator and is building her team. 
She's looking for TWO full-stack consultants with C# .NET expertise:

Position 1: Full-Stack Consultant with Infrastructure Focus
- C# .NET development
- Infrastructure expertise
- Full-stack capabilities
- Team collaboration

Position 2: Full-Stack Consultant with Testing & Quality Focus
- C# .NET development
- Testing and quality assurance
- Full-stack capabilities
- Team collaboration

What Makes This Role Special:
- Human-centric focus with strong people management
- New team with great energy and trust
- Amazing waterfront office at Lindholmen
- Walk & talk by the water with fresh air
- Great lunch spots
- Collaborative and welcoming environment

Required Skills:
- Strong C# .NET development experience
- Full-stack development (frontend + backend)
- Either infrastructure expertise OR testing/quality focus
- Team collaboration and communication
- Passion for learning and growth

Nice to Have:
- Experience with Xamarin or mobile development
- Cloud platforms (Azure, AWS)
- Microservices architecture
- DevOps practices
- Automotive or transport industry knowledge
- Agile/Scrum methodologies

Company Culture:
- Human-centric approach
- Trust and empowerment
- Continuous learning
- Positive energy
- Team collaboration
- Work-life balance (waterfront location!)

Contact: Linda Redgård (SW Manager Configurator, Volvo Digital & IT)
Location: Lindholmen, Gothenburg, Sweden
Type: Consultant position
"""

print("="*80)
print("VOLVO GROUP DIGITAL & IT - FULL-STACK CONSULTANT (C# .NET)")
print("Direct Contact: Linda Redgård (SW Manager Configurator)")
print("="*80)
print("\n📋 Job Analysis...")

# Step 1: Analyze job description
analysis = analyze_job_description(job_description)

print(f"\n✓ Analysis Complete:")
print(f"  Role Type: {analysis['roleType']}")
print(f"  Role Category: {analysis['roleCategory']}")
print(f"  Company: Volvo Group Digital & IT")
print(f"  Title: Full-Stack Consultant (C# .NET)")
print(f"  Contact: Linda Redgård (SW Manager)")
print(f"  Keywords: {', '.join(analysis['keywords'][:10])}")

# Override company and title
analysis['company'] = 'Volvo Group Digital & IT'
analysis['title'] = 'Full-Stack Consultant (C# .NET)'

# Step 2: Generate CV with emphasis on relevant experience
print("\n📝 Generating Tailored CV...")
print("   Positioning for: Infrastructure Focus OR Testing/Quality Focus")
print("   Highlighting:")
print("   ✓ Ecarx automotive/transport industry (Oct 2024 - Nov 2025)")
print("   ✓ Synteda C#/.NET Core + Azure infrastructure (Aug 2023 - Sep 2024)")
print("   ✓ Full-stack: Frontend (React, Vue.js) + Backend (.NET, Java)")
print("   ✓ Xamarin mobile development (graduate project)")
print("   ✓ Infrastructure: Kubernetes, Docker, Terraform, CI/CD")
print("   ✓ Testing: Quality assurance, monitoring, observability")
print("   ✓ .NET and Java hobby projects")
print("   ✓ International team collaboration (4 global offices)")

cv_latex = build_lego_cv(
    analysis['roleType'],
    'Volvo Group Digital & IT',
    'Full-Stack Consultant (C# .NET)',
    analysis['roleCategory'],
    job_description
)

print(f"✓ CV Generated: {len(cv_latex)} characters")

# Step 3: Save CV
output_dir = Path('job_applications/volvo_fullstack_dotnet')
output_dir.mkdir(exist_ok=True)

cv_path = output_dir / 'Volvo_FullStack_DotNet_Consultant_CV.tex'
with open(cv_path, 'w', encoding='utf-8') as f:
    f.write(cv_latex)

print(f"\n✓ Saved CV to: {cv_path}")

# Step 4: Compile to PDF
print("\n📄 Compiling to PDF...")
try:
    result = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cv_path)],
        capture_output=True,
        timeout=30,
        text=True
    )
    
    pdf_path = output_dir / 'Volvo_FullStack_DotNet_Consultant_CV.pdf'
    if pdf_path.exists():
        print(f"✓ PDF compiled: {pdf_path}")
        
        # Clean up auxiliary files
        for ext in ['.aux', '.log', '.out']:
            for file in output_dir.glob(f'*{ext}'):
                file.unlink()
    else:
        print("⚠ PDF compilation failed")
        print(result.stdout[-500:] if result.stdout else "")
except Exception as e:
    print(f"⚠ PDF compilation error: {e}")

# Step 5: Generate AI enhancement prompts
print("\n🎯 Generating AI Enhancement Prompts...")
prompts = generate_ai_enhancement_prompts(
    job_description,
    cv_latex,
    'Volvo Group Digital & IT',
    'Full-Stack Consultant (C# .NET)'
)

import json
prompts_path = output_dir / 'ai_enhancement_prompts.json'
with open(prompts_path, 'w', encoding='utf-8') as f:
    json.dump(prompts, f, indent=2, ensure_ascii=False)

print(f"✓ Saved AI prompts to: {prompts_path}")

# Step 6: Create application summary
summary = f"""# Volvo Group Digital & IT - Full-Stack Consultant (C# .NET) Application

## 🎯 Direct Contact Opportunity!
**Posted by**: Linda Redgård (SW Manager Configurator)  
**LinkedIn**: Direct post from Linda - she's actively building her team!  
**Location**: Lindholmen, Gothenburg (Waterfront office 🌊)

## Two Positions Available

### Position 1: Full-Stack Consultant with Infrastructure Focus ✅
**Perfect fit for your profile!**
- C# .NET development ✅ (Synteda experience)
- Infrastructure expertise ✅ (Ecarx: Kubernetes, Docker, Terraform, CI/CD)
- Full-stack capabilities ✅ (React, Vue.js, .NET, Java)
- Cloud platforms ✅ (Azure at Synteda, AWS at Ecarx)

### Position 2: Full-Stack Consultant with Testing & Quality Focus ✅
**Also a strong fit!**
- C# .NET development ✅ (Synteda experience)
- Testing and quality ✅ (Ecarx: Quality assurance, monitoring, observability)
- Full-stack capabilities ✅ (React, Vue.js, .NET, Java)
- Team collaboration ✅ (4 global offices at Ecarx)

## Why You're a Perfect Match

### 1. C# .NET Expertise ✅
**Synteda AB | Azure Developer (Freelance)**
- August 2023 - September 2024
- C#/.NET Core development with microservices
- Azure cloud platform
- Application support and maintenance
- **Direct .NET professional experience**

### 2. Full-Stack Capabilities ✅
**Frontend**:
- React, TypeScript, JavaScript
- Vue.js (Pembio AB project)
- Modern web frameworks

**Backend**:
- C#/.NET Core (Synteda)
- Java/Spring Boot (Pembio, hobby projects)
- Python (automation, scripting)
- RESTful APIs, microservices

### 3. Infrastructure Focus ✅
**Ecarx (Geely Automotive) | IT/Infrastructure Specialist**
- October 2024 - November 2025
- Kubernetes, Docker, Helm
- Terraform IaC, CloudFormation
- CI/CD pipelines (GitHub Actions, GitLab CI)
- Azure AKS to on-premise Kubernetes migration
- Infrastructure automation
- **Strong infrastructure background**

### 4. Testing & Quality Focus ✅
**Ecarx Experience**:
- Quality assurance and runtime stability
- Monitoring: Prometheus, Grafana, ELK Stack
- 24/7 on-call support
- Incident resolution and RCA
- MTTR optimization
- **Quality-first mindset**

### 5. Automotive/Transport Industry ✅
**Ecarx (Geely Automotive)**:
- 1+ year in automotive industry
- Understanding of transport solutions
- Global team collaboration
- **Aligns with Volvo Group's mission**

### 6. Xamarin Mobile Development ✅
**IT-Högskolan Graduate Project**:
- Xamarin cross-platform mobile development
- Modern .NET frameworks
- **Nice-to-have requirement met**

### 7. International Team Collaboration ✅
**Ecarx**:
- Worked across 4 global offices (Gothenburg, London, Stuttgart, San Diego)
- Cross-functional collaboration
- Agile/Scrum methodologies
- **Proven international experience**

## Application Strategy

### Approach: Direct LinkedIn Outreach + Formal Application

**Step 1: LinkedIn Message to Linda Redgård**
```
Hi Linda,

Congratulations on your new role as SW Manager Configurator at Volvo Digital & IT! 

I saw your post about looking for two full-stack consultants (C# .NET), and I believe I'd be a strong fit for the infrastructure-focused position.

Quick background:
• 1+ year C#/.NET Core development at Synteda (Azure, microservices)
• 1+ year infrastructure at Ecarx/Geely Automotive (Kubernetes, Terraform, CI/CD)
• Full-stack: React/TypeScript frontend + .NET/Java backend
• Xamarin mobile development (graduate project)
• Currently in Gothenburg - would love to work at the Lindholmen waterfront!

I'd love to chat over lunch at Lindholmen or a quick call to discuss how I can contribute to your team.

Best regards,
Harvad Li
[Your LinkedIn Profile]
[Your Phone: +46 72 838 4299]
```

**Step 2: Follow Up with CV**
Attach the generated CV after initial contact

**Step 3: Mention Both Positions**
Express interest in infrastructure focus primarily, but highlight quality/testing experience as well

## Key Talking Points for Interview

### Infrastructure Focus
1. **Ecarx Infrastructure**: "At Ecarx, I managed Kubernetes clusters, implemented Terraform IaC, and built CI/CD pipelines that reduced deployment time by 25%."

2. **Azure Migration**: "I led the Azure AKS to on-premise Kubernetes migration, reducing cloud costs by 45% while improving efficiency."

3. **Full-Stack + Infrastructure**: "I combine full-stack development skills with deep infrastructure knowledge, allowing me to build and deploy scalable solutions end-to-end."

### Testing & Quality Focus
1. **Quality Mindset**: "At Ecarx, I focused on quality assurance and runtime stability, implementing Prometheus/Grafana monitoring that reduced MTTR by 35%."

2. **24/7 Support**: "I provided 24/7 on-call support, resolving critical incidents including a 26-server recovery in 5 hours."

3. **Testing Experience**: "I've worked with automated testing, monitoring, and observability tools to ensure production reliability."

### .NET Expertise
1. **Synteda .NET**: "At Synteda, I developed cloud applications using C#/.NET Core with microservices architecture on Azure."

2. **Graduate Project**: "My graduate degree focused on .NET Cloud Development, including a Xamarin mobile project."

3. **Continuous Learning**: "I continuously expand my .NET skills through hobby projects and staying current with modern frameworks."

### Cultural Fit
1. **Human-Centric**: "I value trust, collaboration, and positive energy - exactly what you mentioned about your team culture."

2. **Lindholmen Location**: "I'm excited about the waterfront office! I believe the environment plays a big role in creativity and team collaboration."

3. **Learning Mindset**: "I'm passionate about continuous learning and would love to grow with your new team."

## Application Materials
- ✅ CV: `{cv_path}`
- ✅ PDF: `{output_dir / 'Volvo_FullStack_DotNet_Consultant_CV.pdf'}`
- ✅ AI Prompts: `{prompts_path}`

## Next Steps
1. ✅ Connect with Linda Redgård on LinkedIn
2. ✅ Send personalized message highlighting infrastructure + .NET experience
3. ✅ Mention you're in Gothenburg and available for lunch at Lindholmen
4. ✅ Follow up with CV after initial contact
5. ✅ Prepare for interview using AI prompts
6. ✅ Emphasize both infrastructure AND quality/testing capabilities

## Why This is a Great Opportunity
- 🌊 **Location**: Lindholmen waterfront office in Gothenburg (where you already are!)
- 🚀 **New Team**: Join at the beginning, shape the team culture
- 👥 **Human-Centric**: Linda emphasizes people management and trust
- 🎯 **Direct Contact**: You have a warm lead through LinkedIn
- 💼 **Perfect Fit**: Your experience matches both positions
- 🏢 **Volvo Group**: Prestigious company, sustainable transport mission
- 🌍 **International**: Global team, English-speaking environment

## Contact Information
**Linda Redgård**
- Title: SW Manager Configurator
- Company: Volvo Group Digital & IT
- Location: Lindholmen, Gothenburg
- LinkedIn: [Find her post about hiring]

**Your Contact**
- Email: hongzhili01@gmail.com
- Phone: +46 72 838 4299
- LinkedIn: [Your Profile]
- Location: Gothenburg (ready to start immediately!)

## Timeline
- **Now**: Connect on LinkedIn and send message
- **This Week**: Follow up with CV and schedule lunch/call
- **Next Week**: Interview preparation using AI prompts
- **Goal**: Join the team at Lindholmen waterfront! 🌊

Good luck! This is a fantastic opportunity with a direct contact. 🚀
"""

summary_path = output_dir / 'APPLICATION_SUMMARY.md'
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(summary)

print(f"✓ Saved application summary to: {summary_path}")

print("\n" + "="*80)
print("✅ APPLICATION PACKAGE COMPLETE!")
print("="*80)
print(f"\n📦 Files created in: {output_dir}/")
print(f"   1. CV (LaTeX): Volvo_FullStack_DotNet_Consultant_CV.tex")
print(f"   2. CV (PDF): Volvo_FullStack_DotNet_Consultant_CV.pdf")
print(f"   3. AI Prompts: ai_enhancement_prompts.json")
print(f"   4. Summary: APPLICATION_SUMMARY.md")
print(f"\n🎯 DIRECT CONTACT: Linda Redgård (SW Manager Configurator)")
print(f"📍 Location: Lindholmen, Gothenburg (Waterfront office!)")
print(f"💼 Positions: Infrastructure Focus OR Testing/Quality Focus")
print(f"\n💡 Next Steps:")
print(f"   1. Connect with Linda on LinkedIn")
print(f"   2. Send personalized message (template in summary)")
print(f"   3. Mention you're in Gothenburg and available for lunch")
print(f"   4. Follow up with CV")
print(f"   5. Prepare for interview using AI prompts")
print(f"\n🌊 This is a fantastic opportunity - direct contact + perfect location!")
