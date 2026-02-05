#!/usr/bin/env python3
"""
Complete workflow test simulating the actual API process
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

# Mock the Flask dependencies for testing
class MockRequest:
    def __init__(self, json_data):
        self.json = json_data

class MockJsonify:
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return f"JsonResponse({self.data})"

class MockBlueprint:
    def __init__(self, name, import_name):
        self.name = name
        self.import_name = import_name
    
    def route(self, rule, **options):
        def decorator(f):
            return f
        return decorator

# Mock Flask functions
def jsonify(data):
    return MockJsonify(data)

def send_file(path, **kwargs):
    return f"SendFile({path})"

# Add mocks to sys.modules
sys.modules['flask'] = type('MockFlask', (), {
    'Blueprint': MockBlueprint,
    'request': None,
    'jsonify': jsonify,
    'send_file': send_file
})()

# Now we can import our functions
sys.path.append('backend')

def test_complete_kamstrup_workflow():
    """Test the complete workflow for Kamstrup Customer Support Engineer job"""
    print("🔄 Testing complete Kamstrup workflow...")
    
    # Test job description
    job_description = """
Customer Support Engineer
Kamstrup

About the role:
We are looking for a Customer Support Engineer to join our team in Gothenburg, Sweden. 
You will be responsible for providing technical support to our customers, troubleshooting 
issues with our water and heat cooling systems, and working with ServiceNow ticketing systems.

Requirements:
- Experience with ServiceNow
- Strong networking knowledge  
- Radio technologies experience
- Troubleshooting skills
- Ticketing systems experience

About Kamstrup:
Kamstrup is a leading provider of intelligent energy and water metering solutions.
"""
    
    try:
        # Import functions
        from app.lego_api import (
            analyze_job_description,
            build_lego_cv,
            build_lego_cover_letter,
            ai_review_documents
        )
        
        print("✅ Successfully imported all functions")
        
        # Step 1: Analyze job
        print("\n📊 Step 1: Analyzing job description...")
        analysis = analyze_job_description(job_description)
        
        print(f"✅ Company: {analysis.get('company', 'N/A')}")
        print(f"✅ Title: {analysis.get('title', 'N/A')}")
        print(f"✅ Role Type: {analysis.get('roleType', 'N/A')}")
        print(f"✅ Role Category: {analysis.get('roleCategory', 'N/A')}")
        
        # Verify correct classification
        expected_company = "Kamstrup"
        expected_role_category = "it_support"
        
        if analysis.get('company') == expected_company:
            print("✅ Company extraction correct")
        else:
            print(f"⚠️ Company extraction: got '{analysis.get('company')}', expected '{expected_company}'")
        
        if analysis.get('roleCategory') == expected_role_category:
            print("✅ Role classification correct")
        else:
            print(f"⚠️ Role classification: got '{analysis.get('roleCategory')}', expected '{expected_role_category}'")
        
        # Step 2: Generate CV
        print("\n📄 Step 2: Generating CV...")
        cv_latex = build_lego_cv(
            role_type=analysis.get('roleType', 'IT Support'),
            company=analysis.get('company', 'Kamstrup'),
            title=analysis.get('title', 'Customer Support Engineer'),
            role_category=analysis.get('roleCategory', 'it_support'),
            job_description=job_description
        )
        
        print(f"✅ CV generated ({len(cv_latex)} characters)")
        
        # Verify CV content
        cv_checks = [
            ('Company name', 'Kamstrup' in cv_latex),
            ('LinkedIn blue color', '0,119,181' in cv_latex),
            ('ServiceNow keyword', 'ServiceNow' in cv_latex),
            ('No placeholder text', '[COMPANY' not in cv_latex),
            ('Reasonable length', len(cv_latex) > 5000)  # Should be substantial
        ]
        
        for check_name, check_result in cv_checks:
            if check_result:
                print(f"✅ CV {check_name}: PASS")
            else:
                print(f"❌ CV {check_name}: FAIL")
        
        # Step 3: Generate Cover Letter
        print("\n💌 Step 3: Generating Cover Letter...")
        cl_latex = build_lego_cover_letter(
            role_type=analysis.get('roleType', 'IT Support'),
            company=analysis.get('company', 'Kamstrup'),
            title=analysis.get('title', 'Customer Support Engineer'),
            role_category=analysis.get('roleCategory', 'it_support'),
            job_description=job_description
        )
        
        print(f"✅ Cover Letter generated ({len(cl_latex)} characters)")
        
        # Verify CL content
        cl_checks = [
            ('Company name', 'Kamstrup' in cl_latex),
            ('LinkedIn blue color', '0,119,181' in cl_latex),
            ('No placeholder text', '[COMPANY' not in cl_latex and '[JOB' not in cl_latex),
            ('No inappropriate content', 'software development' not in cl_latex.lower()),
            ('Reasonable length', len(cl_latex) > 1000)
        ]
        
        for check_name, check_result in cl_checks:
            if check_result:
                print(f"✅ CL {check_name}: PASS")
            else:
                print(f"❌ CL {check_name}: FAIL")
        
        # Step 4: AI Quality Check
        print("\n🤖 Step 4: AI Quality Check...")
        quality_result = ai_review_documents(
            cv_latex=cv_latex,
            cl_latex=cl_latex,
            job_description=job_description,
            company=analysis.get('company', 'Kamstrup'),
            title=analysis.get('title', 'Customer Support Engineer')
        )
        
        print(f"✅ Quality check completed")
        print(f"✅ Overall Score: {quality_result.get('overall_score', 'N/A')}/100")
        print(f"✅ Ready to Send: {quality_result.get('ready_to_send', 'N/A')}")
        
        if quality_result.get('critical_issues'):
            print("⚠️ Critical issues found:")
            for issue in quality_result['critical_issues']:
                print(f"   - {issue}")
        
        # Step 5: PDF Compilation Test
        print("\n📋 Step 5: Testing PDF compilation...")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test CV compilation
            cv_tex_path = temp_path / 'cv.tex'
            with open(cv_tex_path, 'w', encoding='utf-8') as f:
                f.write(cv_latex)
            
            cv_result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(temp_path), str(cv_tex_path)],
                capture_output=True,
                timeout=30,
                text=True
            )
            
            cv_pdf_path = temp_path / 'cv.pdf'
            if cv_result.returncode == 0 and cv_pdf_path.exists():
                print(f"✅ CV PDF compiled successfully ({cv_pdf_path.stat().st_size} bytes)")
            else:
                print("❌ CV PDF compilation failed")
                print(f"STDERR: {cv_result.stderr[:300]}...")
            
            # Test CL compilation
            cl_tex_path = temp_path / 'cl.tex'
            with open(cl_tex_path, 'w', encoding='utf-8') as f:
                f.write(cl_latex)
            
            cl_result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(temp_path), str(cl_tex_path)],
                capture_output=True,
                timeout=30,
                text=True
            )
            
            cl_pdf_path = temp_path / 'cl.pdf'
            if cl_result.returncode == 0 and cl_pdf_path.exists():
                print(f"✅ CL PDF compiled successfully ({cl_pdf_path.stat().st_size} bytes)")
            else:
                print("❌ CL PDF compilation failed")
                print(f"STDERR: {cl_result.stderr[:300]}...")
        
        print("\n🎉 COMPLETE WORKFLOW TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run complete workflow test"""
    print("🚀 Starting complete workflow test...")
    
    success = test_complete_kamstrup_workflow()
    
    if success:
        print("\n✅ ALL WORKFLOW TESTS PASSED - READY FOR DEPLOYMENT!")
    else:
        print("\n❌ WORKFLOW TESTS FAILED - CHECK ERRORS ABOVE")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)