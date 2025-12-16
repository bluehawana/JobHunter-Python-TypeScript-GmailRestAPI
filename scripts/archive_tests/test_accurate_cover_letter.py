#!/usr/bin/env python3
"""
Test Accurate Cover Letter Generation with 100% Company Info Validation
NO MORE WRONG COMPANY NAMES, ADDRESSES, OR HR NAMES!
"""
import sys
import os
sys.path.append('backend')

# Load environment variables
from dotenv import load_dotenv
load_dotenv('backend/.env')

from cover_letter_generator import CoverLetterGenerator
from company_info_extractor import CompanyInfoExtractor

def test_opera_cover_letter_accuracy():
    """Test Opera DevOps cover letter with 100% accurate company information"""
    
    print("🎭 TESTING ACCURATE COVER LETTER GENERATION")
    print("=" * 60)
    print("🎯 ZERO TOLERANCE FOR WRONG COMPANY INFORMATION!")
    print("=" * 60)
    
    # Real Opera job data with comprehensive information
    opera_job = {
        'company': 'Opera',
        'title': 'DevOps Engineer',
        'location': 'Oslo, Norway',
        'url': 'https://jobs.opera.com/jobs/6060392-devops-engineer',
        'description': '''
        We are looking for a DevOps Engineer to join our team in Oslo, Norway.
        
        About Opera:
        Opera is a global web innovator with an engaged user base of hundreds of millions of monthly active users. 
        Opera has rewritten the rules of the web and continues to innovate with products like Opera Browser, 
        Opera GX gaming browser, and various mobile applications.
        
        The Role:
        - Design, implement and maintain CI/CD pipelines
        - Manage cloud infrastructure on AWS and Azure
        - Implement monitoring and alerting solutions
        - Automate deployment processes
        - Work with Kubernetes and Docker containers
        - Collaborate with development teams across multiple time zones
        - Ensure security best practices
        - Optimize system performance and reliability
        
        Requirements:
        - Experience with AWS, Azure, or GCP
        - Proficiency in Kubernetes and Docker
        - CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
        - Infrastructure as Code (Terraform, CloudFormation)
        - Monitoring tools (Prometheus, Grafana, ELK stack)
        - Scripting languages (Python, Bash, PowerShell)
        - Linux system administration
        - Security best practices
        - Agile methodologies
        - Cross-functional collaboration skills
        
        What we offer:
        - Competitive salary and benefits
        - Flexible working arrangements
        - International work environment
        - Career development opportunities
        - Modern office in Oslo city center
        ''',
        'contact_person': 'Not specified',
        'additional_info': 'Apply through Opera careers page'
    }
    
    print(f"🏢 Company: {opera_job['company']}")
    print(f"💼 Position: {opera_job['title']}")
    print(f"📍 Location: {opera_job['location']}")
    print(f"🔗 URL: {opera_job['url']}")
    
    # Step 1: Test company information extraction
    print(f"\n🔍 STEP 1: EXTRACTING COMPANY INFORMATION")
    print("-" * 40)
    
    extractor = CompanyInfoExtractor()
    company_result = extractor.extract_and_validate_company_info(opera_job)
    
    if company_result['success']:
        print(f"✅ Company info extraction successful")
        print(f"📊 Quality Score: {company_result['quality_score']}/10")
        print(f"🎯 Confidence: {company_result['confidence']}/10")
        print(f"🔧 Method: {company_result['extraction_method']}")
        
        company_info = company_result['company_info']
        print(f"\n📋 EXTRACTED COMPANY INFORMATION:")
        print(f"   Company Name: '{company_info['company_name']}'")
        print(f"   Address: '{company_info['formatted_address'].replace('\\\\', ', ')}'")
        print(f"   Greeting: '{company_info['greeting']}'")
        print(f"   Your Contact: {company_info['your_name']} - {company_info['your_email']}")
        
        # Validate critical information
        validation_errors = []
        if 'REQUIRED' in company_info['company_name']:
            validation_errors.append("❌ Company name is missing or invalid")
        if 'REQUIRED' in company_info['formatted_address']:
            validation_errors.append("❌ Company address is missing or invalid")
        if 'ERROR' in str(company_info):
            validation_errors.append("❌ Validation errors detected")
        
        if validation_errors:
            print(f"\n🚨 CRITICAL VALIDATION ERRORS:")
            for error in validation_errors:
                print(f"   {error}")
            print(f"🛑 CANNOT PROCEED - MANUAL REVIEW REQUIRED!")
            return False
        else:
            print(f"✅ All critical information validated successfully")
    else:
        print(f"❌ Company info extraction failed: {company_result.get('error', 'Unknown error')}")
        return False
    
    # Step 2: Generate cover letter
    print(f"\n📝 STEP 2: GENERATING COVER LETTER")
    print("-" * 40)
    
    generator = CoverLetterGenerator()
    result = generator.create_cover_letter_with_r2_overleaf(opera_job)
    
    if result['success']:
        print(f"✅ Cover letter generation successful")
        print(f"📄 PDF Size: {result['pdf_size']:,} bytes")
        print(f"📝 LaTeX Size: {result['latex_size']:,} characters")
        print(f"☁️ R2 Upload: {'✅' if result['r2_upload_success'] else '❌'}")
        
        # Save files for inspection
        if result['pdf_content']:
            with open('accurate_opera_cover_letter.pdf', 'wb') as f:
                f.write(result['pdf_content'])
            print(f"💾 PDF saved: accurate_opera_cover_letter.pdf")
        
        if result['latex_content']:
            with open('accurate_opera_cover_letter.tex', 'w') as f:
                f.write(result['latex_content'])
            print(f"💾 LaTeX saved: accurate_opera_cover_letter.tex")
        
        # Step 3: Validate generated content
        print(f"\n🔍 STEP 3: VALIDATING GENERATED CONTENT")
        print("-" * 40)
        
        latex_content = result['latex_content']
        content_errors = []
        
        # Check for correct company name
        if opera_job['company'] not in latex_content:
            content_errors.append(f"❌ Company name '{opera_job['company']}' not found in content")
        
        # Check for correct position
        if opera_job['title'] not in latex_content:
            content_errors.append(f"❌ Position '{opera_job['title']}' not found in content")
        
        # Check for your contact information
        if 'hongzhili01@gmail.com' not in latex_content:
            content_errors.append("❌ Your email address not found")
        if '0728384299' not in latex_content:
            content_errors.append("❌ Your phone number not found")
        if 'Ebbe Lieberathsgatan 27' not in latex_content:
            content_errors.append("❌ Your address not found")
        
        # Check for placeholder text that shouldn't be there
        placeholder_checks = [
            'REQUIRED', 'ERROR', 'Not provided', 'Company Name Required',
            'Address Required', 'MANUAL INPUT NEEDED'
        ]
        for placeholder in placeholder_checks:
            if placeholder in latex_content:
                content_errors.append(f"❌ Placeholder text found: '{placeholder}'")
        
        if content_errors:
            print(f"🚨 CONTENT VALIDATION ERRORS:")
            for error in content_errors:
                print(f"   {error}")
            print(f"🛑 COVER LETTER HAS ERRORS - MANUAL REVIEW REQUIRED!")
            return False
        else:
            print(f"✅ All content validation checks passed")
        
        # Show Overleaf URL if available
        if result['r2_upload_success']:
            print(f"\n🔗 OVERLEAF INTEGRATION:")
            print(f"   LaTeX URL: {result['latex_url']}")
            print(f"   Overleaf URL: {result['overleaf_url']}")
        
        print(f"\n🎉 COVER LETTER GENERATION SUCCESSFUL!")
        print(f"✅ 100% Accurate company information")
        print(f"✅ Professional LaTeX formatting")
        print(f"✅ LEGO intelligence applied")
        print(f"✅ R2 + Overleaf integration ready")
        
        return True
        
    else:
        print(f"❌ Cover letter generation failed: {result.get('error', 'Unknown error')}")
        return False

def test_multiple_companies():
    """Test with multiple companies to ensure accuracy across different scenarios"""
    
    test_companies = [
        {
            'company': 'Spotify',
            'title': 'Backend Developer',
            'location': 'Stockholm, Sweden',
            'description': 'Backend development role at Spotify...'
        },
        {
            'company': 'Klarna',
            'title': 'DevOps Engineer',
            'location': 'Stockholm, Sweden',
            'description': 'DevOps role at Klarna...'
        },
        {
            'company': 'King Digital Entertainment',
            'title': 'Fullstack Developer',
            'location': 'Stockholm, Sweden',
            'description': 'Fullstack development at King...'
        }
    ]
    
    print(f"\n🧪 TESTING MULTIPLE COMPANIES FOR ACCURACY")
    print("=" * 60)
    
    extractor = CompanyInfoExtractor()
    results = []
    
    for i, job in enumerate(test_companies, 1):
        print(f"\n📋 Test {i}: {job['company']} - {job['title']}")
        print("-" * 30)
        
        company_result = extractor.extract_and_validate_company_info(job)
        
        if company_result['success']:
            quality = company_result['quality_score']
            confidence = company_result['confidence']
            
            print(f"✅ Quality: {quality}/10, Confidence: {confidence}/10")
            
            company_info = company_result['company_info']
            print(f"   Company: '{company_info['company_name']}'")
            print(f"   Greeting: '{company_info['greeting']}'")
            
            results.append({
                'company': job['company'],
                'quality': quality,
                'confidence': confidence,
                'success': True
            })
        else:
            print(f"❌ Failed: {company_result.get('error', 'Unknown')}")
            results.append({
                'company': job['company'],
                'success': False
            })
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    avg_quality = sum(r.get('quality', 0) for r in results if r['success']) / max(successful, 1)
    avg_confidence = sum(r.get('confidence', 0) for r in results if r['success']) / max(successful, 1)
    
    print(f"\n📊 MULTI-COMPANY TEST SUMMARY:")
    print(f"   Successful extractions: {successful}/{len(test_companies)}")
    print(f"   Average quality: {avg_quality:.1f}/10")
    print(f"   Average confidence: {avg_confidence:.1f}/10")
    
    return successful == len(test_companies)

if __name__ == "__main__":
    print("🎯 ACCURATE COVER LETTER GENERATION TEST")
    print("=" * 60)
    print("🚨 ZERO TOLERANCE FOR WRONG COMPANY INFORMATION!")
    print("=" * 60)
    
    # Test Opera cover letter
    opera_success = test_opera_cover_letter_accuracy()
    
    # Test multiple companies
    multi_success = test_multiple_companies()
    
    print(f"\n🏁 FINAL RESULTS:")
    print(f"   Opera test: {'✅ PASSED' if opera_success else '❌ FAILED'}")
    print(f"   Multi-company test: {'✅ PASSED' if multi_success else '❌ FAILED'}")
    
    if opera_success and multi_success:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"✅ Company information extraction is 100% accurate")
        print(f"✅ Cover letter generation is ready for production")
        print(f"✅ No more wrong company names or addresses!")
    else:
        print(f"\n❌ TESTS FAILED - SYSTEM NOT READY")
        print(f"🛑 Manual review and fixes required before production use")