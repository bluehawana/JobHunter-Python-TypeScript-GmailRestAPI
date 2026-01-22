#!/usr/bin/env python3
"""
Test script for Göteborgs Stad Azure Specialist job application
"""

import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from app.lego_api import analyze_job_description, build_lego_cv, build_lego_cover_letter

def test_goteborg_azure_specialist():
    """Process the Göteborgs Stad Azure Specialist job posting"""
    
    job_description = """
Om jobbet
Du kommer vara en del av teamet som bygger och driver Microsoft Azure-plattformen i Göteborgs stad. 
Teamet ansvarar bland annat för att tillse att en central och delad infrastruktur i Azure efterlevs och 
man ansvarar också för plattformens arkitektur och styrning. Ytterligare ett ansvar som ligger på teamet 
är att säkerställa en stabil drift, dess prestanda, säkerhet samt kostnader för plattformen.

Som Azure Specialist kommer du bland annat att:
- designa, bygga och förvalta plattformen med Infrastructure as Code (IaC) med hjälp av Bicep och Azure DevOps
- ansvara för drift, utveckling och optimering av centrala plattformsförmågor såsom nätverk, säkerhet, 
  identitet, policy, övervakning och kostnadskontroll
- automatisera deployment, skalning, compliance-rutiner och incidenthantering
- introducera och stötta kunder och interna team i hur plattformen används på ett säkert och effektivt sätt

Om dig
Vi ser att du har:
- någon form av högskoleutbildning inom IT, alternativt har annan förvärvad erfarenhet som vi bedömer likvärdig
- minst 3 års erfarenhet av arbete med Microsoft Azure och djup förståelse av Azure-tjänster 
  (nätverk, RBAC, identitet, policy och säkerhet)
- god kunskap om principer som Cloud Adoption Framework, Well-Architected Framework och Azure Landing Zone
- erfarenhet av traditionell infrastruktur on-prem, inklusive drift och förvaltning av Windows- och Linux-servrar

Det är meriterande om du har erfarenhet av:
- Infrastructure as Code (IaC) t ex Bicep, ARM, Terraform
- CI/CD-processer med Azure DevOps eller liknande verktyg
- containeriserade arbetslaster (Kubernetes, Docker)
- övervakning och loggning samt larmstrategier
- skriptvana i PowerShell/Bash/Ansible
- Relevant certifiering (som AZ-104, AZ-400 eller AZ-305)

Vi ser att du som ansöker är en driven och ansvarsfull person som både tar ansvar för att tjänsten 
förvaltas på rätt sätt men även driver utvecklingen och nya arbetssätt framåt. Du har ett kommunikativt 
förhållningssätt till dina kunder, kollegor och övriga intressenter.

Övrigt
Tjänsten kan eventuellt innefattas av beredskapstjänstgöring. Du kommer att få befattningen systemspecialist hos oss.

Om oss
Intraservice levererar tjänster och digital infrastruktur som hjälper medarbetare och chefer i Göteborgs 
Stad att arbeta smart och effektivt. Vi har en central roll i stadens digitalisering och automatisering 
och våra kunder är Göteborgs alla förvaltningar och bolag. Vi är drygt 700 medarbetare som arbetar i 
centrala Göteborg.

Sista ansökningsdag: 15 februari 2026
Anställningsform: Tillsvidareanställning
Referensnummer: 2026/184
    """
    
    company_name = "Göteborgs Stad"
    job_title = "Azure Specialist"
    job_url = "https://goteborg.se/wps/portal/start/jobba-i-goteborgs-stad/lediga-jobb?id=893909"
    
    print("=" * 80)
    print("PROCESSING: Göteborgs Stad - Azure Specialist")
    print("=" * 80)
    
    # Step 1: Analyze the job
    print("\n[STEP 1] Analyzing job posting...")
    analysis = analyze_job_description(job_description, job_url)
    
    print(f"\nJob Analysis Results:")
    print(f"  Role Category: {analysis.get('roleCategory', 'N/A')}")
    print(f"  Role Type: {analysis.get('roleType', 'N/A')}")
    print(f"  Extraction Success: {analysis.get('extractionStatus', {}).get('success', 'N/A')}")
    print(f"  Key Technologies: {analysis.get('keywords', [])[:10]}")
    
    # Step 2: Generate CV
    print("\n[STEP 2] Generating CV...")
    cv_content = build_lego_cv(
        role_type=analysis.get('roleType', 'Azure Specialist'),
        company=company_name,
        title=job_title,
        role_category=analysis.get('roleCategory', 'devops_cloud'),
        job_description=job_description
    )
    
    print(f"  ✓ CV generated ({len(cv_content)} characters)")
    
    # Step 3: Generate Cover Letter
    print("\n[STEP 3] Generating Cover Letter...")
    cl_content = build_lego_cover_letter(
        role_type=analysis.get('roleType', 'Azure Specialist'),
        company=company_name,
        title=job_title,
        role_category=analysis.get('roleCategory', 'devops_cloud'),
        job_description=job_description
    )
    
    print(f"  ✓ Cover Letter generated ({len(cl_content)} characters)")
    
    # Step 4: Save outputs
    print("\n[STEP 4] Saving application documents...")
    
    output_dir = "job_applications/goteborg_azure_specialist"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save CV
    cv_filename = f"{output_dir}/Goteborg_Azure_Specialist_CV.tex"
    with open(cv_filename, 'w', encoding='utf-8') as f:
        f.write(cv_content)
    print(f"  ✓ CV saved: {cv_filename}")
    
    # Save Cover Letter
    cl_filename = f"{output_dir}/Goteborg_Azure_Specialist_CL.tex"
    with open(cl_filename, 'w', encoding='utf-8') as f:
        f.write(cl_content)
    print(f"  ✓ Cover Letter saved: {cl_filename}")
    
    # Save job info
    info_filename = f"{output_dir}/job_info.txt"
    with open(info_filename, 'w', encoding='utf-8') as f:
        f.write(f"Company: {company_name}\n")
        f.write(f"Position: {job_title}\n")
        f.write(f"Location: Göteborg, Sweden\n")
        f.write(f"URL: https://goteborg.se/wps/portal/start/jobba-i-goteborgs-stad/lediga-jobb?id=893909\n")
        f.write(f"Application Deadline: 15 februari 2026\n")
        f.write(f"Reference Number: 2026/184\n")
        f.write(f"\nAnalysis:\n")
        f.write(f"  Role Category: {analysis.get('roleCategory', 'N/A')}\n")
        f.write(f"  Role Type: {analysis.get('roleType', 'N/A')}\n")
    print(f"  ✓ Job info saved: {info_filename}")
    
    # Verification
    print("\n[STEP 5] Verification...")
    issues = []
    
    if company_name not in cl_content:
        issues.append(f"Cover letter missing company name: {company_name}")
    if job_title not in cl_content:
        issues.append(f"Cover letter missing job title: {job_title}")
    if 'COMPANY_NAME' in cl_content or 'JOB_TITLE' in cl_content:
        issues.append("Cover letter has unreplaced placeholders")
    
    if issues:
        print("  ⚠️ Issues found:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("  ✅ All checks passed!")
    
    print("\n" + "=" * 80)
    print("✓ APPLICATION GENERATION COMPLETE")
    print("=" * 80)
    print(f"\nOutput directory: {output_dir}/")
    print(f"  - CV: Goteborg_Azure_Specialist_CV.tex")
    print(f"  - Cover Letter: Goteborg_Azure_Specialist_CL.tex")
    print(f"  - Job Info: job_info.txt")
    print("\nNext steps:")
    print("  1. Review the generated LaTeX files")
    print("  2. Compile to PDF using your LaTeX compiler")
    print("  3. Submit before deadline: 15 februari 2026")
    print("  4. Apply at: https://goteborg.se/wps/portal/start/jobba-i-goteborgs-stad/lediga-jobb?id=893909")
    
    return {
        'analysis': analysis,
        'output_dir': output_dir,
        'issues': issues
    }

if __name__ == "__main__":
    try:
        result = test_goteborg_azure_specialist()
        print("\n✓ Test completed successfully!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
