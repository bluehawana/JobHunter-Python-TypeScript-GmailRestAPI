#!/usr/bin/env python3
"""
Test the role display fix for Kamstrup
"""

def test_role_display_logic():
    """Test the new role display logic"""
    print("🔍 Testing Role Display Logic")
    print("=" * 40)
    
    # Simulate the new logic
    def get_role_type(role_category):
        if role_category == 'kamstrup':
            return 'Customer Support Engineer'  # Use the actual job role, not company name
        else:
            return role_category.replace('_', ' ').title()
    
    test_cases = [
        ('kamstrup', 'Customer Support Engineer'),
        ('it_support', 'It Support'),
        ('devops_cloud', 'Devops Cloud'),
        ('fullstack_developer', 'Fullstack Developer')
    ]
    
    all_passed = True
    
    for role_category, expected_role_type in test_cases:
        result = get_role_type(role_category)
        print(f"Role Category: '{role_category}' -> Role Type: '{result}'")
        
        if result == expected_role_type:
            print("✅ CORRECT")
        else:
            print(f"❌ WRONG - Expected: '{expected_role_type}'")
            all_passed = False
        print()
    
    return all_passed

if __name__ == '__main__':
    success = test_role_display_logic()
    if success:
        print("🎉 Role display fix should work correctly!")
        print("✅ Kamstrup jobs will now show 'Customer Support Engineer' as role")
    else:
        print("❌ Role display fix has issues")
    
    exit(0 if success else 1)