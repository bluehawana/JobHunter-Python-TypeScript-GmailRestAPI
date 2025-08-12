#!/usr/bin/env python3
"""
Cloudflare R2 LaTeX Storage for Overleaf Integration
Perfect for automated job applications with temporary LaTeX file hosting
"""
import os
import boto3
import logging
from typing import Optional, Dict, Any, List
from botocore.exceptions import ClientError
import time
import hashlib

logger = logging.getLogger(__name__)

class R2LaTeXStorage:
    def __init__(self):
        """Initialize R2 client with your credentials"""
        self.access_key = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('R2_BUCKET_NAME', 'resumepot')
        self.endpoint_url = os.getenv('R2_ENDPOINT_URL')
        self.public_domain = os.getenv('R2_PUBLIC_DOMAIN')  # pub-2c3ec75a299b4921821bb5ad0f311531.r2.dev
        
        # Initialize S3 client for R2
        self.client = None
        if all([self.access_key, self.secret_key, self.endpoint_url]):
            try:
                self.client = boto3.client(
                    's3',
                    endpoint_url=self.endpoint_url,
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    region_name='auto'
                )
                logger.info("✅ R2 client initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize R2 client: {e}")
        else:
            logger.warning("⚠️ R2 credentials not configured")
    
    def upload_latex_file(self, latex_content: str, job_data: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """Upload LaTeX file to R2 and return URLs"""
        if not self.client:
            logger.error("❌ R2 client not available")
            return None
        
        try:
            # Generate unique filename
            company = job_data.get('company', 'company').lower().replace(' ', '_').replace('.', '')
            job_title = job_data.get('title', 'position').lower().replace(' ', '_').replace('/', '_')
            timestamp = int(time.time())
            
            # Add content hash for uniqueness
            content_hash = hashlib.md5(latex_content.encode()).hexdigest()[:8]
            filename = f"resume_{company}_{job_title}_{timestamp}_{content_hash}.tex"
            
            # Upload to R2
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=latex_content.encode('utf-8'),
                ContentType='text/plain; charset=utf-8',
                CacheControl='public, max-age=3600',  # Cache for 1 hour
                Metadata={
                    'company': job_data.get('company', ''),
                    'job_title': job_data.get('title', ''),
                    'created_at': str(timestamp),
                    'purpose': 'overleaf-integration'
                }
            )
            
            # Generate URLs using your public domain
            if self.public_domain:
                public_url = f"https://{self.public_domain}/{filename}"
            else:
                # Fallback to direct R2 URL
                public_url = f"{self.endpoint_url}/{filename}"
            
            overleaf_url = f"https://www.overleaf.com/docs?snip_uri={public_url}"
            
            result = {
                'filename': filename,
                'public_url': public_url,
                'overleaf_url': overleaf_url,
                'bucket': self.bucket_name,
                'size': len(latex_content),
                'company': job_data.get('company', ''),
                'job_title': job_data.get('title', '')
            }
            
            logger.info(f"✅ Uploaded LaTeX to R2: {filename}")
            logger.info(f"🔗 Overleaf URL: {overleaf_url}")
            
            return result
            
        except ClientError as e:
            logger.error(f"❌ R2 upload failed: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error uploading to R2: {e}")
            return None
    
    def list_latex_files(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List recent LaTeX files in R2"""
        if not self.client:
            return []
        
        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                MaxKeys=limit
            )
            
            files = []
            for obj in response.get('Contents', []):
                if obj['Key'].endswith('.tex'):
                    # Get metadata
                    try:
                        head_response = self.client.head_object(
                            Bucket=self.bucket_name,
                            Key=obj['Key']
                        )
                        metadata = head_response.get('Metadata', {})
                    except:
                        metadata = {}
                    
                    if self.public_domain:
                        public_url = f"https://{self.public_domain}/{obj['Key']}"
                    else:
                        account_id = self.endpoint_url.split('//')[1].split('.')[0]
                        public_url = f"https://{self.bucket_name}.{account_id}.r2.cloudflarestorage.com/{obj['Key']}"
                    
                    files.append({
                        'filename': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat(),
                        'public_url': public_url,
                        'overleaf_url': f"https://www.overleaf.com/docs?snip_uri={public_url}",
                        'company': metadata.get('company', 'Unknown'),
                        'job_title': metadata.get('job_title', 'Unknown')
                    })
            
            # Sort by last modified (newest first)
            files.sort(key=lambda x: x['last_modified'], reverse=True)
            
            logger.info(f"📋 Listed {len(files)} LaTeX files from R2")
            return files
            
        except Exception as e:
            logger.error(f"❌ Error listing R2 files: {e}")
            return []
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up LaTeX files older than specified hours"""
        if not self.client:
            return
        
        try:
            current_time = time.time()
            cutoff_time = current_time - (max_age_hours * 3600)
            
            response = self.client.list_objects_v2(Bucket=self.bucket_name)
            
            deleted_count = 0
            for obj in response.get('Contents', []):
                if obj['Key'].endswith('.tex'):
                    # Check if file is old enough
                    file_time = obj['LastModified'].timestamp()
                    if file_time < cutoff_time:
                        self.client.delete_object(
                            Bucket=self.bucket_name,
                            Key=obj['Key']
                        )
                        deleted_count += 1
                        logger.info(f"🗑️ Deleted old LaTeX file: {obj['Key']}")
            
            logger.info(f"🧹 Cleaned up {deleted_count} old LaTeX files")
            
        except Exception as e:
            logger.error(f"❌ Error cleaning up R2 files: {e}")

# Integration function for your job automation
def create_resume_with_r2_overleaf(job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create resume PDF and upload LaTeX to R2 for Overleaf integration
    Returns both PDF content and Overleaf URL
    """
    from overleaf_pdf_generator import OverleafPDFGenerator
    
    try:
        # Generate LaTeX content and PDF
        generator = OverleafPDFGenerator()
        latex_content = generator._generate_latex_content(job_data)
        pdf_content = generator._compile_latex_locally(latex_content)
        
        # Upload to R2
        r2_storage = R2LaTeXStorage()
        r2_result = r2_storage.upload_latex_file(latex_content, job_data)
        
        result = {
            'pdf_content': pdf_content,
            'latex_content': latex_content,
            'pdf_size': len(pdf_content) if pdf_content else 0,
            'latex_size': len(latex_content),
            'success': bool(pdf_content),
            'company': job_data.get('company', 'Unknown'),
            'job_title': job_data.get('title', 'Unknown')
        }
        
        if r2_result:
            result.update({
                'r2_filename': r2_result['filename'],
                'latex_url': r2_result['public_url'],
                'overleaf_url': r2_result['overleaf_url'],
                'r2_upload_success': True
            })
            logger.info(f"🎉 Complete success: PDF + R2 + Overleaf URL for {job_data.get('company')}")
        else:
            result.update({
                'r2_filename': '',
                'latex_url': '',
                'overleaf_url': '',
                'r2_upload_success': False
            })
            logger.warning(f"⚠️ PDF created but R2 upload failed for {job_data.get('company')}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in complete resume creation: {e}")
        return {
            'pdf_content': b'',
            'latex_content': '',
            'pdf_size': 0,
            'latex_size': 0,
            'success': False,
            'r2_upload_success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    # Test R2 integration
    test_job = {
        'title': 'Senior DevOps Engineer',
        'company': 'Opera',
        'description': 'Kubernetes, AWS, Docker, infrastructure automation'
    }
    
    print("🧪 Testing R2 LaTeX Storage...")
    result = create_resume_with_r2_overleaf(test_job)
    
    print(f"✅ Success: {result['success']}")
    print(f"📄 PDF Size: {result['pdf_size']} bytes")
    print(f"📝 LaTeX Size: {result['latex_size']} characters")
    print(f"☁️ R2 Upload: {result['r2_upload_success']}")
    
    if result['r2_upload_success']:
        print(f"🔗 Overleaf URL: {result['overleaf_url']}")
        print(f"📁 R2 Filename: {result['r2_filename']}")
    
    # Test listing files
    r2_storage = R2LaTeXStorage()
    files = r2_storage.list_latex_files(limit=5)
    print(f"\n📋 Recent LaTeX files: {len(files)}")
    for file_info in files[:3]:
        print(f"   📝 {file_info['filename']} - {file_info['company']}")