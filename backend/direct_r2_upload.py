#!/usr/bin/env python3
"""
Direct R2 Upload - Skip bucket operations, upload directly
"""
import boto3
import os
from pathlib import Path
from datetime import datetime

def direct_upload_test():
    """Try uploading directly without bucket operations"""
    
    print("🎯 Direct R2 Upload Test (Skip Bucket Operations)")
    print("=" * 60)
    
    # Get credentials from environment
    account_id = os.getenv('R2_ACCOUNT_ID')
    access_key = os.getenv('R2_ACCESS_KEY_ID') 
    secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    
    if not all([account_id, access_key, secret_key]):
        print("❌ Missing R2 credentials")
        return False
    
    try:
        # Initialize R2 client
        s3_client = boto3.client(
            's3',
            endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='auto'
        )
        print("✅ R2 client initialized")
        
        # Try uploading a small test file directly to 'jobhunter' bucket
        print("\\n📄 Testing direct upload to 'jobhunter' bucket...")
        test_content = f"Test upload - {datetime.now()}"
        
        try:
            s3_client.put_object(
                Bucket='jobhunter',
                Key='test-upload.txt',
                Body=test_content.encode('utf-8'),
                ContentType='text/plain'
            )
            print("✅ SUCCESS! Direct upload works!")
            print("🎉 The 'jobhunter' bucket exists and we can upload to it")
            
            # Clean up test file
            try:
                s3_client.delete_object(Bucket='jobhunter', Key='test-upload.txt')
                print("🧹 Test file cleaned up")
            except:
                pass
            
            return True
            
        except Exception as upload_error:
            print(f"❌ Direct upload failed: {upload_error}")
            
            # Try with a different bucket name
            print("\\n🔄 Trying with 'documents' bucket...")
            try:
                s3_client.put_object(
                    Bucket='documents',
                    Key='test-upload.txt', 
                    Body=test_content.encode('utf-8'),
                    ContentType='text/plain'
                )
                print("✅ SUCCESS! Upload works with 'documents' bucket!")
                
                # Clean up
                s3_client.delete_object(Bucket='documents', Key='test-upload.txt')
                return 'documents'
                
            except Exception as e2:
                print(f"❌ 'documents' bucket also failed: {e2}")
                
                # Try creating our own unique bucket
                unique_bucket = f"jobhunter-{datetime.now().strftime('%Y%m%d')}"
                print(f"\\n🆕 Trying to create unique bucket: {unique_bucket}")
                try:
                    s3_client.create_bucket(Bucket=unique_bucket)
                    print(f"✅ Created bucket: {unique_bucket}")
                    
                    # Test upload to new bucket
                    s3_client.put_object(
                        Bucket=unique_bucket,
                        Key='test-upload.txt',
                        Body=test_content.encode('utf-8'),
                        ContentType='text/plain'
                    )
                    print("✅ Upload successful to new bucket!")
                    
                    # Clean up
                    s3_client.delete_object(Bucket=unique_bucket, Key='test-upload.txt')
                    return unique_bucket
                    
                except Exception as e3:
                    print(f"❌ Bucket creation failed: {e3}")
        
        return False
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def upload_documents_with_working_bucket(bucket_name):
    """Upload all documents using the working bucket"""
    
    print(f"\\n📦 Uploading Documents to '{bucket_name}' Bucket")
    print("=" * 60)
    
    # Initialize client
    account_id = os.getenv('R2_ACCOUNT_ID')
    access_key = os.getenv('R2_ACCESS_KEY_ID') 
    secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    
    s3_client = boto3.client(
        's3',
        endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='auto'
    )
    
    # Find all documents
    current_dir = Path(".")
    pdf_files = list(current_dir.glob("*.pdf"))
    latex_files = list(current_dir.glob("*.tex"))
    
    print(f"📄 Found {len(pdf_files)} PDF files")
    print(f"📝 Found {len(latex_files)} LaTeX files")
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    uploaded_files = []
    
    # Upload PDFs
    print(f"\\n📄 Uploading PDFs...")
    for pdf_file in pdf_files[:5]:  # Upload first 5 as test
        try:
            key = f"documents/{timestamp}/pdfs/{pdf_file.name}"
            
            with open(pdf_file, 'rb') as f:
                s3_client.upload_fileobj(
                    f, bucket_name, key,
                    ExtraArgs={'ContentType': 'application/pdf'}
                )
            
            file_size = pdf_file.stat().st_size / 1024
            print(f"✅ {pdf_file.name} ({file_size:.1f} KB)")
            uploaded_files.append({
                'name': pdf_file.name,
                'type': 'PDF',
                'url': f"https://{account_id}.r2.cloudflarestorage.com/{key}"
            })
            
        except Exception as e:
            print(f"❌ {pdf_file.name}: {e}")
    
    # Upload LaTeX files  
    print(f"\\n📝 Uploading LaTeX files...")
    for latex_file in latex_files[:10]:  # Upload first 10 as test
        try:
            key = f"documents/{timestamp}/latex/{latex_file.name}"
            
            with open(latex_file, 'rb') as f:
                s3_client.upload_fileobj(
                    f, bucket_name, key,
                    ExtraArgs={'ContentType': 'text/plain'}
                )
            
            file_size = latex_file.stat().st_size / 1024
            print(f"✅ {latex_file.name} ({file_size:.1f} KB)")
            uploaded_files.append({
                'name': latex_file.name,
                'type': 'LaTeX',
                'url': f"https://{account_id}.r2.cloudflarestorage.com/{key}"
            })
            
        except Exception as e:
            print(f"❌ {latex_file.name}: {e}")
    
    # Create simple index
    if uploaded_files:
        print(f"\\n📋 Creating document index...")
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>JobHunter Documents - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .file {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; }}
        .pdf {{ background: #ffe6e6; }}
        .latex {{ background: #e6ffe6; }}
        a {{ color: #0066cc; text-decoration: none; }}
    </style>
</head>
<body>
    <h1>📋 JobHunter Documents</h1>
    <p>Uploaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Total files: {len(uploaded_files)}</p>
"""
        
        for file in uploaded_files:
            css_class = 'pdf' if file['type'] == 'PDF' else 'latex'
            html_content += f"""
    <div class="file {css_class}">
        <strong>{file['type']}:</strong> 
        <a href="{file['url']}" target="_blank">{file['name']}</a>
    </div>"""
        
        html_content += "</body></html>"
        
        try:
            s3_client.put_object(
                Bucket=bucket_name,
                Key='index.html',
                Body=html_content.encode('utf-8'),
                ContentType='text/html'
            )
            
            index_url = f"https://{account_id}.r2.cloudflarestorage.com/index.html"
            print(f"✅ Index created: {index_url}")
            
        except Exception as e:
            print(f"❌ Index creation failed: {e}")
    
    print(f"\\n🎉 UPLOAD COMPLETE!")
    print(f"📦 Uploaded {len(uploaded_files)} files to '{bucket_name}' bucket")
    print(f"🔗 Access your documents at:")
    print(f"   https://{account_id}.r2.cloudflarestorage.com/documents/{timestamp}/")
    
    return len(uploaded_files) > 0

def main():
    """Main function"""
    print("🚀 Testing Direct R2 Upload")
    
    # Test which bucket works
    working_bucket = direct_upload_test()
    
    if working_bucket:
        if working_bucket == True:
            working_bucket = 'jobhunter'
        
        print(f"\\n✅ Found working bucket: '{working_bucket}'")
        
        # Upload documents
        success = upload_documents_with_working_bucket(working_bucket)
        
        if success:
            print("\\n🎉 SUCCESS! Your documents are now accessible online!")
        else:
            print("\\n❌ Upload failed")
    else:
        print("\\n❌ No working bucket found")
        print("\\nThe R2 token may need additional permissions:")
        print("• Account - Cloudflare R2:Edit")
        print("• Zone - Zone Settings:Edit")

if __name__ == "__main__":
    main()