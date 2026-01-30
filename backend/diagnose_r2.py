#!/usr/bin/env python3
"""
R2 Permissions Diagnostic Tool
Helps identify the exact R2 permission issues
"""
import boto3
import os

def diagnose_r2_permissions():
    """Diagnose R2 connection and permission issues"""
    
    print("🔍 R2 Cloudflare Storage Diagnostic Tool")
    print("=" * 60)
    
    # Get credentials from environment
    account_id = os.getenv('R2_ACCOUNT_ID')
    access_key = os.getenv('R2_ACCESS_KEY_ID') 
    secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    
    if not all([account_id, access_key, secret_key]):
        print("❌ Missing R2 credentials in environment variables")
        return False
    
    print(f"✅ Credentials found:")
    print(f"   Account ID: {account_id}")
    print(f"   Access Key: {access_key[:8]}...")
    print(f"   Secret Key: {secret_key[:8]}...")
    print()
    
    try:
        # Initialize R2 client
        print("🔧 Testing R2 connection...")
        s3_client = boto3.client(
            's3',
            endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='auto'
        )
        print("✅ R2 client initialized successfully")
        
        # Test 1: List buckets
        print("\\n🪣 Testing bucket permissions...")
        try:
            response = s3_client.list_buckets()
            buckets = [bucket['Name'] for bucket in response.get('Buckets', [])]
            print(f"✅ Can list buckets: {buckets}")
            
            if 'jobhunter' in buckets:
                print("✅ 'jobhunter' bucket exists")
                bucket_exists = True
            else:
                print("⚠️  'jobhunter' bucket not found")
                print(f"   Available buckets: {buckets}")
                bucket_exists = False
                
        except Exception as e:
            print(f"❌ Cannot list buckets: {e}")
            bucket_exists = False
        
        # Test 2: Try creating bucket if it doesn't exist
        if not bucket_exists:
            print("\\n🆕 Testing bucket creation...")
            try:
                s3_client.create_bucket(Bucket='jobhunter')
                print("✅ Successfully created 'jobhunter' bucket")
                bucket_exists = True
            except Exception as e:
                print(f"❌ Cannot create bucket: {e}")
                print("   Possible solutions:")
                print("   1. Check if bucket name 'jobhunter' is already taken globally")
                print("   2. Verify API token has 'Zone:Zone Settings:Edit' permission")
                print("   3. Try a different bucket name")
        
        # Test 3: Try uploading a small test file
        if bucket_exists:
            print("\\n📄 Testing file upload...")
            try:
                test_content = "Test file for R2 permissions"
                s3_client.put_object(
                    Bucket='jobhunter',
                    Key='test/permissions_test.txt',
                    Body=test_content.encode('utf-8'),
                    ContentType='text/plain'
                )
                print("✅ Successfully uploaded test file")
                
                # Test 4: Try downloading the file
                print("\\n📥 Testing file download...")
                try:
                    response = s3_client.get_object(Bucket='jobhunter', Key='test/permissions_test.txt')
                    content = response['Body'].read().decode('utf-8')
                    if content == test_content:
                        print("✅ Successfully downloaded test file")
                        print("🎉 R2 permissions are working correctly!")
                        
                        # Clean up test file
                        s3_client.delete_object(Bucket='jobhunter', Key='test/permissions_test.txt')
                        print("🧹 Cleaned up test file")
                        return True
                    else:
                        print("❌ Downloaded content doesn't match uploaded content")
                except Exception as e:
                    print(f"❌ Cannot download test file: {e}")
                    
            except Exception as e:
                print(f"❌ Cannot upload test file: {e}")
                print("   Possible solutions:")
                print("   1. Verify API token has 'Object Read and Write' permissions")
                print("   2. Check if the token is scoped to the correct bucket")
                print("   3. Ensure token hasn't expired")
        
        return False
        
    except Exception as e:
        print(f"❌ R2 connection failed: {e}")
        return False

def suggest_solutions():
    """Suggest solutions for common R2 issues"""
    
    print("\\n🔧 TROUBLESHOOTING GUIDE")
    print("=" * 40)
    print()
    print("If you're getting 'Unauthorized' errors, try these solutions:")
    print()
    print("1. 📝 Check API Token Permissions:")
    print("   • Go to Cloudflare Dashboard → R2 Object Storage")
    print("   • Click 'Manage R2 API tokens'")
    print("   • Edit your token and ensure it has:")
    print("     - Zone:Zone Settings:Edit (for bucket creation)")
    print("     - Zone:Zone:Read (for listing buckets)")
    print("     - Account:Cloudflare R2:Edit (for object operations)")
    print()
    print("2. 🎯 Check Token Scope:")
    print("   • Make sure the token includes your account")
    print("   • Consider creating a token with 'All accounts' scope for testing")
    print()
    print("3. 🪣 Try Different Bucket Name:")
    print("   • 'jobhunter' might be taken globally")
    print("   • Try: 'jobhunter-[your-initials]' or 'jobhunter-2025'")
    print()
    print("4. 🔄 Create New Token:")
    print("   • Sometimes recreating the token fixes permission issues")
    print("   • Use 'Custom token' with specific permissions")
    print()
    print("5. ⏰ Check Token Expiry:")
    print("   • Tokens might have expiration dates")
    print("   • Create a token that doesn't expire for testing")

def main():
    """Main diagnostic function"""
    success = diagnose_r2_permissions()
    
    if not success:
        suggest_solutions()
        
        print("\\n🚀 Next Steps:")
        print("1. Fix the API token permissions in Cloudflare Dashboard")
        print("2. Set the environment variables:")
        print("   export R2_ACCOUNT_ID='your-account-id'")
        print("   export R2_ACCESS_KEY_ID='your-access-key'") 
        print("   export R2_SECRET_ACCESS_KEY='your-secret-key'")
        print("3. Run this diagnostic again to verify")
        print("4. Then run the document upload script")

if __name__ == "__main__":
    main()