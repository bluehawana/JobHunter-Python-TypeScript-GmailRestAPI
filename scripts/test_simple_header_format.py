#!/usr/bin/env python3
"""
Test the simple header format: Company // Job Title // Location
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.template_customizer import TemplateCustomizer

def test_simple_header():
    """Test the simple header format customization"""
    
    # Sample template with the new simple header format
    sample_template = r"""
\begin{center}
{\LARGE \textbf{Harvad (Hongzhi) Li}}\\[8pt]
{\Large \textbf{COMPANY_NAME // JOB_TITLE // Gothenburg, Sweden}}\\[8pt]
\textcolor{linkedinblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com}}
\end{center}

\section*{Profile Summary}
Experienced developer applying for JOB_TITLE position at COMPANY_NAME.
"""
    
    print("🔍 Testing Simple Header Format")
    print("=" * 50)
    
    customizer = TemplateCustomizer()
    
    # Test with Meltwater job
    print("Testing with Meltwater Software Engineer job...")
    
    customized = customizer.customize_template(
        sample_template,
        company="Meltwater",
        title="Software Engineer", 
        role_type="backend_developer"
    )
    
    print("\nCustomized Header:")
    # Extract just the header line
    lines = customized.split('\n')
    for line in lines:
        if 'Meltwater //' in line:
            print(f"  {line.strip()}")
            break
    
    # Check if it matches the expected format
    expected = "Meltwater // Software Engineer // Gothenburg, Sweden"
    if expected in customized:
        print(f"\n✅ SUCCESS! Header format is correct:")
        print(f"   {expected}")
    else:
        print(f"\n❌ Issue with header format")
        print("Expected: Meltwater // Software Engineer // Gothenburg, Sweden")
        
        # Show what we got instead
        for line in lines:
            if '//' in line and 'Meltwater' in line:
                print(f"Got: {line.strip()}")
    
    return expected in customized

def test_different_jobs():
    """Test with different job combinations"""
    
    test_cases = [
        ("Volvo Cars", "Senior DevOps Engineer"),
        ("Spotify", "Backend Developer"),
        ("IKEA", "Fullstack Developer"),
        ("Klarna", "Platform Engineer")
    ]
    
    customizer = TemplateCustomizer()
    sample_template = r"{\Large \textbf{COMPANY_NAME // JOB_TITLE // Gothenburg, Sweden}}"
    
    print(f"\n🧪 Testing Different Job Combinations:")
    print("-" * 40)
    
    for company, title in test_cases:
        customized = customizer.customize_template(
            sample_template,
            company=company,
            title=title,
            role_type="backend_developer"
        )
        
        expected = f"{company} // {title} // Gothenburg, Sweden"
        if expected in customized:
            print(f"  ✅ {expected}")
        else:
            print(f"  ❌ Failed for {company} - {title}")

if __name__ == '__main__':
    print("🚀 Testing Simple Header Format: Company // Job Title // Location\n")
    
    success = test_simple_header()
    test_different_jobs()
    
    print(f"\n" + "=" * 50)
    if success:
        print("🎉 Simple header format is working!")
        print("✅ Format: Company // Job Title // Gothenburg, Sweden")
        print("✅ Ready for Meltwater job application")
    else:
        print("⚠️ Header format needs adjustment")
    
    print(f"\n💡 The header will now show:")
    print("   Meltwater // Software Engineer // Gothenburg, Sweden")
    print("   Instead of complex role descriptions")