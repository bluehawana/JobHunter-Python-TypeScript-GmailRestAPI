#!/usr/bin/env python3
"""
R2 Cloudflare Storage Backup Service
Saves generated resumes and cover letters to R2 storage for backup
"""
import boto3
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import mimetypes

class R2BackupService:
    def __init__(self):
        """Initialize R2 storage client"""
        # R2 endpoint and credentials (to be set in environment variables)
        self.endpoint_url = "https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com"
        self.bucket_name = "jobhunter"
        
        # These should be set in .env file
        self.access_key = os.getenv('R2_ACCESS_KEY_ID', '')
        self.secret_key = os.getenv('R2_SECRET_ACCESS_KEY', '')
        self.account_id = os.getenv('R2_ACCOUNT_ID', '')
        
        # Initialize S3 client for R2
        self.s3_client = None
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize boto3 client for R2"""
        try:
            if self.access_key and self.secret_key and self.account_id:
                self.s3_client = boto3.client(
                    's3',
                    endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    region_name='auto'
                )
                print("✅ R2 client initialized successfully")
                
                # Try to create bucket if it doesn't exist
                self.ensure_bucket_exists()
            else:
                print("⚠️  R2 credentials not found in environment variables")
                print("   Set R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID in .env")
        except Exception as e:
            print(f"❌ Failed to initialize R2 client: {e}")
    
    def ensure_bucket_exists(self):
        """Ensure the bucket exists, create if it doesn't"""
        try:
            # Try to check if bucket exists
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"✅ Bucket '{self.bucket_name}' exists")
        except Exception as e:
            # Bucket doesn't exist or we don't have permission, try to create it
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                print(f"✅ Created bucket '{self.bucket_name}'")
            except Exception as create_error:
                print(f"⚠️  Could not create bucket '{self.bucket_name}': {create_error}")
                print("   The bucket may already exist or you may need different permissions")
    
    def upload_file(self, local_file_path: str, r2_key: str) -> bool:
        """Upload a single file to R2 storage"""
        if not self.s3_client:
            print("❌ R2 client not initialized")
            return False
        
        try:
            # Get file info
            file_path = Path(local_file_path)
            if not file_path.exists():
                print(f"❌ File not found: {local_file_path}")
                return False
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(local_file_path)
            if not content_type:
                content_type = 'application/octet-stream'
            
            # Upload file
            with open(local_file_path, 'rb') as file:
                self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    r2_key,
                    ExtraArgs={'ContentType': content_type}
                )
            
            file_size = file_path.stat().st_size / 1024  # KB
            print(f"✅ Uploaded: {local_file_path} → r2://{self.bucket_name}/{r2_key} ({file_size:.1f} KB)")
            return True
            
        except Exception as e:
            print(f"❌ Upload failed for {local_file_path}: {e}")
            return False
    
    def backup_job_documents(self, job_title: str, company: str, cv_pdf: str = None, 
                           cv_tex: str = None, cl_pdf: str = None, cl_tex: str = None) -> Dict[str, bool]:
        """Backup all documents for a job application"""
        
        # Create organized folder structure
        timestamp = datetime.now().strftime("%Y-%m-%d")
        safe_company = company.replace(" ", "_").replace("/", "_")
        safe_job_title = job_title.replace(" ", "_").replace("/", "_")
        base_path = f"applications/{timestamp}/{safe_company}_{safe_job_title}"
        
        results = {}
        files_to_upload = [
            (cv_pdf, f"{base_path}/cv.pdf"),
            (cv_tex, f"{base_path}/cv.tex"),
            (cl_pdf, f"{base_path}/cover_letter.pdf"),
            (cl_tex, f"{base_path}/cover_letter.tex")
        ]
        
        print(f"📦 Backing up documents for {job_title} at {company}")
        print(f"📁 R2 path: {base_path}")
        
        uploaded_count = 0
        for local_file, r2_key in files_to_upload:
            if local_file and Path(local_file).exists():
                success = self.upload_file(local_file, r2_key)
                results[local_file] = success
                if success:
                    uploaded_count += 1
            else:
                results[local_file] = False
        
        print(f"📊 Backup complete: {uploaded_count}/{len([f for f, _ in files_to_upload if f])} files uploaded")
        return results
    
    def backup_thomthon_documents(self) -> bool:
        """Backup the Thomthon Retuer documents"""
        
        cv_pdf = "thomthon_retuer_cv.pdf"
        cl_pdf = "thomthon_retuer_cover_letter.pdf"
        
        # Check if files exist
        if not Path(cv_pdf).exists() or not Path(cl_pdf).exists():
            print("❌ Thomthon Retuer PDF files not found")
            return False
        
        # Create LaTeX source files for backup (using the generator)
        print("📝 Creating LaTeX sources for backup...")
        
        # Import and use the LaTeX generator
        try:
            from ultra_simple_generator import UltraSimpleGenerator
            generator = UltraSimpleGenerator()
            
            # Generate LaTeX content
            cv_content = generator.create_basic_cv_template("Solution Developer", "Thomthon Retuer", "devops")
            cl_content = generator.create_basic_cover_letter_template("Solution Developer", "Thomthon Retuer", "", "", "Sweden")
            
            # Save LaTeX files
            cv_tex = "thomthon_retuer_cv.tex"
            cl_tex = "thomthon_retuer_cover_letter.tex"
            
            with open(cv_tex, 'w', encoding='utf-8') as f:
                f.write(cv_content)
            with open(cl_tex, 'w', encoding='utf-8') as f:
                f.write(cl_content)
            
            print(f"💾 Created LaTeX sources: {cv_tex}, {cl_tex}")
            
        except Exception as e:
            print(f"⚠️  Could not create LaTeX sources: {e}")
            cv_tex = None
            cl_tex = None
        
        # Backup all documents
        results = self.backup_job_documents(
            "Solution Developer", 
            "Thomthon Retuer",
            cv_pdf, cv_tex, cl_pdf, cl_tex
        )
        
        # Clean up temporary LaTeX files
        if cv_tex and Path(cv_tex).exists():
            os.remove(cv_tex)
        if cl_tex and Path(cl_tex).exists():
            os.remove(cl_tex)
        
        success_count = sum(1 for success in results.values() if success)
        return success_count > 0
    
    def list_backups(self, limit: int = 20) -> List[Dict]:
        """List recent backups in R2 storage"""
        if not self.s3_client:
            print("❌ R2 client not initialized")
            return []
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='applications/',
                MaxKeys=limit
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'modified': obj['LastModified'],
                        'url': f"https://{self.endpoint_url}/{obj['Key']}"
                    })
            
            return sorted(files, key=lambda x: x['modified'], reverse=True)
            
        except Exception as e:
            print(f"❌ Failed to list backups: {e}")
            return []
    
    def create_backup_index(self) -> bool:
        """Create an index file of all backups"""
        try:
            backups = self.list_backups(limit=100)
            
            # Create HTML index
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>JobHunter Application Backups</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .backup {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; }}
        .date {{ color: #666; font-size: 0.9em; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>JobHunter Application Backups</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Total files: {len(backups)}</p>
    
    <div id="backups">
"""
            
            for backup in backups:
                file_name = backup['key'].split('/')[-1]
                company_job = '/'.join(backup['key'].split('/')[2:-1])
                size_kb = backup['size'] / 1024
                
                html_content += f"""
        <div class="backup">
            <strong>{company_job}</strong><br>
            <a href="{backup['url']}" target="_blank">{file_name}</a> 
            ({size_kb:.1f} KB)
            <div class="date">{backup['modified'].strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
"""
            
            html_content += """
    </div>
</body>
</html>"""
            
            # Upload index file
            index_success = self.upload_file_content(html_content, "index.html", "text/html")
            if index_success:
                print(f"📋 Backup index created: https://{self.endpoint_url}/index.html")
            
            return index_success
            
        except Exception as e:
            print(f"❌ Failed to create backup index: {e}")
            return False
    
    def upload_file_content(self, content: str, r2_key: str, content_type: str = "text/plain") -> bool:
        """Upload string content directly to R2"""
        if not self.s3_client:
            return False
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=r2_key,
                Body=content.encode('utf-8'),
                ContentType=content_type
            )
            print(f"✅ Uploaded content to: r2://{self.bucket_name}/{r2_key}")
            return True
        except Exception as e:
            print(f"❌ Upload failed for {r2_key}: {e}")
            return False

def test_r2_backup():
    """Test R2 backup functionality"""
    print("🔧 Testing R2 Backup Service")
    print("=" * 50)
    
    backup = R2BackupService()
    
    # Test Thomthon Retuer backup
    print("\\n📦 Testing Thomthon Retuer backup...")
    success = backup.backup_thomthon_documents()
    
    if success:
        print("✅ Thomthon Retuer backup successful!")
        
        # Create backup index
        print("\\n📋 Creating backup index...")
        backup.create_backup_index()
        
        # List recent backups
        print("\\n📁 Recent backups:")
        backups = backup.list_backups(limit=10)
        for i, backup_file in enumerate(backups[:5], 1):
            print(f"  {i}. {backup_file['key']} ({backup_file['size']/1024:.1f} KB)")
        
    else:
        print("❌ Backup failed - check R2 credentials")
    
    print(f"\\n🔗 Your R2 storage URL: https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com")

def main():
    """Main function"""
    test_r2_backup()

if __name__ == "__main__":
    main()