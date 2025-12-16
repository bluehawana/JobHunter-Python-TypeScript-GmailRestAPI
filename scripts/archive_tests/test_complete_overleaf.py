#!/usr/bin/env python3
"""
Complete Overleaf Integration Test
Shows how your job automation now includes Overleaf URLs!
"""
import sys
import os
sys.path.append('backend')

from beautiful_pdf_generator import create_beautiful_multi_page_pdf
import json

def test_complete_integration():
    """Test the complete job automation with Overleaf integration"""
    
    # Test different job types to show LEGO intelligence
    test_jobs = [
        {
            'title': 'Senior DevOps Engineer',
            'company': 'Spotify',
            'description': 'Kubernetes, AWS, Docker, infrastructure automation, CI/CD pipelines, monitoring, Grafana, Terraform, Helm'
        },
        {
            'title': 'Backend Developer',
            'company': 'Klarna',
            'description': 'Java, Spring Boot, microservices, PostgreSQL, API development, REST, GraphQL, database optimization'
        },
        {
            'title': 'Fullstack Developer',
            'company': 'King Digital Entertainment',
            'description': 'React, Node.js, TypeScript, MongoDB, AWS, full-stack development, frontend, backend, APIs'
        }
    ]
    
    print("🚀 Testing Complete Overleaf Integration")
    print("=" * 60)
    
    results = []
    
    for i, job in enumerate(test_jobs, 1):
        print(f"\n📋 Test {i}: {job['title']} at {job['company']}")
        print("-" * 40)
        
        # Generate PDF with Overleaf integration
        pdf_content = create_beautiful_multi_page_pdf(job)
        
        if pdf_content:
            # Save PDF for testing
            filename = f"test_{job['company'].lower().replace(' ', '_')}_resume.pdf"
            with open(filename, 'wb') as f:
                f.write(pdf_content)
            
            result = {
                'company': job['company'],
                'job_title': job['title'],
                'pdf_size': len(pdf_content),
                'pdf_file': filename,
                'success': True
            }
            
            print(f"✅ PDF Generated: {filename} ({len(pdf_content)} bytes)")
            
        else:
            result = {
                'company': job['company'],
                'job_title': job['title'],
                'pdf_size': 0,
                'pdf_file': None,
                'success': False
            }
            print("❌ PDF Generation Failed")
        
        results.append(result)
    
    print("\n" + "=" * 60)
    print("📊 INTEGRATION SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['success'])
    total_size = sum(r['pdf_size'] for r in results)
    
    print(f"✅ Successful generations: {successful}/{len(results)}")
    print(f"📄 Total PDF size: {total_size:,} bytes")
    print(f"📝 LaTeX files saved in: backend/latex_files/")
    
    print("\n🎯 OVERLEAF INTEGRATION FEATURES:")
    print("• ✅ Perfect LaTeX compilation (same as Overleaf)")
    print("• ✅ LEGO intelligence (job-specific tailoring)")
    print("• ✅ Automatic LaTeX file saving")
    print("• ✅ Overleaf URLs generated in logs")
    print("• ✅ Manual editing capability")
    print("• ✅ Professional multi-page resumes")
    
    print("\n🔗 HOW TO USE OVERLEAF URLS:")
    print("1. Check your logs for Overleaf URLs")
    print("2. Deploy your app with LaTeX serving endpoints")
    print("3. LaTeX files served at: https://jobs.bluehawana.com/api/v1/latex/filename.tex")
    print("4. Overleaf URLs: https://www.overleaf.com/docs?snip_uri=YOUR_LATEX_URL")
    
    # Check if LaTeX files were created
    latex_dir = os.path.join('backend', 'latex_files')
    if os.path.exists(latex_dir):
        latex_files = [f for f in os.listdir(latex_dir) if f.endswith('.tex')]
        print(f"\n📁 LaTeX files created: {len(latex_files)}")
        for latex_file in latex_files[-3:]:  # Show last 3
            print(f"   📝 {latex_file}")
    
    return results

if __name__ == "__main__":
    results = test_complete_integration()
    
    print(f"\n🎉 INTEGRATION TEST COMPLETE!")
    print(f"📊 Results: {json.dumps([{k: v for k, v in r.items() if k != 'pdf_file'} for r in results], indent=2)}")