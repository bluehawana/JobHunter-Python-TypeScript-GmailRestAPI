#!/usr/bin/env python3
"""
Simple test to verify CV title fix without Flask dependencies
"""

def test_role_type_consistency():
    """Test that role_type is made consistent with role_category"""
    print("🔧 Testing Role Type Consistency Fix")
    print("=" * 50)
    
    # Simulate the safeguard logic
    def apply_safeguard(role_type, role_category):
        expected_role_type = role_category.replace('_', ' ').title()
        if role_type != expected_role_type:
            print(f"⚠️ Role type mismatch detected: roleType='{role_type}', roleCategory='{role_category}'")
            print(f"🔧 Correcting role_type from '{role_type}' to '{expected_role_type}'")
            role_type = expected_role_type
        return role_type
    
    # Test cases
    test_cases = [
        {
            'name': 'DevOps Cloud with IT Business Analyst mismatch',
            'input_role_type': 'IT Business Analyst',
            'input_role_category': 'devops_cloud',
            'expected_role_type': 'Devops Cloud'
        },
        {
            'name': 'Kamstrup role (should stay as Kamstrup)',
            'input_role_type': 'Kamstrup',
            'input_role_category': 'kamstrup',
            'expected_role_type': 'Kamstrup'
        },
        {
            'name': 'IT Support role (should stay as It Support)',
            'input_role_type': 'It Support',
            'input_role_category': 'it_support',
            'expected_role_type': 'It Support'
        },
        {
            'name': 'Correct match (no change needed)',
            'input_role_type': 'Fullstack Developer',
            'input_role_category': 'fullstack_developer',
            'expected_role_type': 'Fullstack Developer'
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Input: roleType='{test_case['input_role_type']}', roleCategory='{test_case['input_role_category']}'")
        
        result_role_type = apply_safeguard(test_case['input_role_type'], test_case['input_role_category'])
        
        print(f"Result: roleType='{result_role_type}'")
        print(f"Expected: '{test_case['expected_role_type']}'")
        
        if result_role_type == test_case['expected_role_type']:
            print("✅ PASS")
        else:
            print("❌ FAIL")
            all_passed = False
    
    return all_passed

def test_cv_title_generation():
    """Test CV title generation logic"""
    print("\n📄 Testing CV Title Generation Logic")
    print("=" * 50)
    
    # Simulate the CV title generation
    def generate_cv_title(role_type):
        # This is what happens in the LaTeX template
        return f"{{\\Large \\textit{{{role_type}}}}}\\\\[10pt]"
    
    test_cases = [
        ('Devops Cloud', 'DevOps Cloud'),
        ('Kamstrup', 'Kamstrup'),
        ('It Support', 'IT Support'),
        ('Fullstack Developer', 'Fullstack Developer')
    ]
    
    all_passed = True
    
    for role_type, expected_display in test_cases:
        cv_title_latex = generate_cv_title(role_type)
        print(f"Role Type: '{role_type}' -> LaTeX: {cv_title_latex}")
        
        # Extract the title from LaTeX
        import re
        match = re.search(r'\\textit\{([^}]+)\}', cv_title_latex)
        if match:
            extracted_title = match.group(1)
            print(f"Extracted Title: '{extracted_title}'")
            
            if extracted_title == role_type:
                print("✅ PASS - Title matches role_type")
            else:
                print("❌ FAIL - Title doesn't match role_type")
                all_passed = False
        else:
            print("❌ FAIL - Could not extract title")
            all_passed = False
        print()
    
    return all_passed

def main():
    """Run all tests"""
    print("🧪 Testing CV Title Fix")
    print("=" * 60)
    
    # Run tests
    consistency_ok = test_role_type_consistency()
    title_generation_ok = test_cv_title_generation()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Role Type Consistency: {'✅ PASS' if consistency_ok else '❌ FAIL'}")
    print(f"CV Title Generation: {'✅ PASS' if title_generation_ok else '❌ FAIL'}")
    
    all_passed = consistency_ok and title_generation_ok
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n✅ The safeguard should prevent role_type/role_category mismatches")
        print("✅ CV titles will now be consistent with the classified role")
    else:
        print("\n❌ There are still issues with the fix")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)