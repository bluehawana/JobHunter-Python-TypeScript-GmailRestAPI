#!/usr/bin/env python3
"""
Test Overleaf Integration - Generate LaTeX and create Overleaf URL
"""
import json
from backend.overleaf_pdf_generator import OverleafPDFGenerator

def test_overleaf_integration():
    """Test the complete Overleaf integration workflow"""
    
    # Test job data
    test_job = {
        'title': 'Senior DevOps Engineer',
        'company': 'Spotify',
        'description': 'Kubernetes, AWS, Docker, infrastructure automation, CI/CD pipelines, monitoring, Grafana, Terraform'
    }
    
    print("🚀 Testing Overleaf Integration...")
    print(f"📋 Job: {test_job['title']} at {test_job['company']}")
    
    # Create generator
    generator = OverleafPDFGenerator()
    
    # Generate LaTeX content
    latex_content = generator._generate_latex_content(test_job)
    
    # Save LaTeX file locally for testing
    with open('test_resume_for_overleaf.tex', 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"✅ Generated LaTeX file: test_resume_for_overleaf.tex ({len(latex_content)} characters)")
    
    # Create a simple HTTP server URL (you would replace this with your actual server)
    # For now, let's simulate what the URL would look like
    latex_url = "https://your-domain.com/latex/resume_spotify_1234567890.tex"
    overleaf_url = f"https://www.overleaf.com/docs?snip_uri={latex_url}"
    
    print(f"📝 LaTeX URL: {latex_url}")
    print(f"🔗 Overleaf URL: {overleaf_url}")
    
    # Also generate PDF locally for comparison
    pdf_content = generator.create_overleaf_pdf(test_job)
    
    if pdf_content:
        with open('test_overleaf_comparison.pdf', 'wb') as f:
            f.write(pdf_content)
        print(f"✅ Local PDF generated: test_overleaf_comparison.pdf ({len(pdf_content)} bytes)")
    
    print("\n🎯 OVERLEAF INTEGRATION READY!")
    print("📋 Steps to use:")
    print("1. Upload LaTeX file to a public URL (your server, GitHub, etc.)")
    print("2. Use: https://www.overleaf.com/docs?snip_uri=YOUR_LATEX_URL")
    print("3. Overleaf will load and compile your LaTeX automatically!")
    
    return {
        'latex_content': latex_content,
        'latex_url': latex_url,
        'overleaf_url': overleaf_url,
        'pdf_size': len(pdf_content) if pdf_content else 0
    }

if __name__ == "__main__":
    result = test_overleaf_integration()
    print(f"\n📊 Results: {json.dumps({k: v for k, v in result.items() if k != 'latex_content'}, indent=2)}")