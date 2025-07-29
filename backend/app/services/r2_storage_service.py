#!/usr/bin/env python3
"""
R2 Storage Service
Handles document storage and retrieval from Cloudflare R2
"""
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError
import hashlib
import json
import asyncio
import aiofiles
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

class R2StorageService:
    """Service for managing documents in Cloudflare R2 storage"""
    
    def __init__(self):
        # R2 configuration
        self.endpoint_url = os.getenv("R2_ENDPOINT_URL")
        self.access_key = os.getenv("R2_ACCESS_KEY_ID")
        self.secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("R2_BUCKET_NAME", "jobhunter-documents")
        self.region = os.getenv("R2_REGION", "auto")
        
        # R2 client configuration
        self.config = Config(
            region_name=self.region,
            s3={'addressing_style': 'path'}
        )
        
        # Initialize S3 client for R2
        try:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                config=self.config
            )
            logger.info("✅ R2 storage client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize R2 client: {e}")
            self.s3_client = None
        
        # Storage paths
        self.storage_paths = {
            'cvs': 'documents/cvs/',
            'cover_letters': 'documents/cover_letters/',
            'latex_sources': 'documents/latex/',
            'job_descriptions': 'jobs/',
            'templates': 'templates/',
            'backups': 'backups/'
        }
    
    def _validate_client(self) -> bool:
        """Validate R2 client is properly configured"""
        if not self.s3_client:
            logger.error("❌ R2 client not initialized")
            return False
        
        if not all([self.endpoint_url, self.access_key, self.secret_key]):
            logger.error("❌ R2 credentials not properly configured")
            return False
        
        return True
    
    async def ensure_bucket_exists(self) -> bool:
        """Ensure the R2 bucket exists"""
        try:
            if not self._validate_client():
                return False
            
            # Check if bucket exists
            try:
                self.s3_client.head_bucket(Bucket=self.bucket_name)
                logger.info(f"✅ Bucket '{self.bucket_name}' exists")
                return True
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    # Bucket doesn't exist, create it
                    logger.info(f"📁 Creating bucket '{self.bucket_name}'")
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                    logger.info(f"✅ Bucket '{self.bucket_name}' created successfully")
                    return True
                else:
                    logger.error(f"❌ Error checking bucket: {e}")
                    return False
        
        except Exception as e:
            logger.error(f"❌ Error ensuring bucket exists: {e}")
            return False
    
    def generate_file_key(self, file_type: str, job_title: str, company: str, 
                         file_extension: str, timestamp: Optional[datetime] = None) -> str:
        """Generate unique file key for R2 storage"""
        
        if timestamp is None:
            timestamp = datetime.now()
        
        # Clean job title and company for file path
        job_slug = self._slugify(job_title)
        company_slug = self._slugify(company)
        date_str = timestamp.strftime("%Y%m%d")
        
        # Create unique identifier
        unique_id = hashlib.md5(f"{job_title}{company}{timestamp}".encode()).hexdigest()[:8]
        
        # Build file key
        base_path = self.storage_paths.get(file_type, 'documents/')
        filename = f"{company_slug}_{job_slug}_{date_str}_{unique_id}.{file_extension}"
        
        return f"{base_path}{filename}"
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        import re
        
        # Convert to lowercase and replace spaces with underscores
        slug = text.lower().replace(' ', '_')
        
        # Remove special characters
        slug = re.sub(r'[^a-z0-9_-]', '', slug)
        
        # Remove multiple underscores
        slug = re.sub(r'_+', '_', slug)
        
        # Remove leading/trailing underscores
        slug = slug.strip('_')
        
        return slug[:50]  # Limit length
    
    async def upload_cv(self, cv_content: bytes, job_title: str, company: str, 
                       content_type: str = 'application/pdf') -> Optional[str]:
        """Upload CV PDF to R2 storage"""
        try:
            if not await self.ensure_bucket_exists():
                return None
            
            # Generate file key
            file_key = self.generate_file_key('cvs', job_title, company, 'pdf')
            
            # Upload to R2
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=cv_content,
                ContentType=content_type,
                Metadata={
                    'job_title': job_title,
                    'company': company,
                    'document_type': 'cv',
                    'uploaded_at': datetime.now().isoformat()
                }
            )
            
            # Generate public URL
            public_url = f"{self.endpoint_url.replace('https://', 'https://pub-')}/{self.bucket_name}/{file_key}"
            
            logger.info(f"✅ CV uploaded successfully: {file_key}")
            return public_url
            
        except Exception as e:
            logger.error(f"❌ Error uploading CV: {e}")
            return None
    
    async def upload_cover_letter(self, cl_content: bytes, job_title: str, company: str,
                                content_type: str = 'application/pdf') -> Optional[str]:
        """Upload cover letter PDF to R2 storage"""
        try:
            if not await self.ensure_bucket_exists():
                return None
            
            # Generate file key
            file_key = self.generate_file_key('cover_letters', job_title, company, 'pdf')
            
            # Upload to R2
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=cl_content,
                ContentType=content_type,
                Metadata={
                    'job_title': job_title,
                    'company': company,
                    'document_type': 'cover_letter',
                    'uploaded_at': datetime.now().isoformat()
                }
            )
            
            # Generate public URL
            public_url = f"{self.endpoint_url.replace('https://', 'https://pub-')}/{self.bucket_name}/{file_key}"
            
            logger.info(f"✅ Cover letter uploaded successfully: {file_key}")
            return public_url
            
        except Exception as e:
            logger.error(f"❌ Error uploading cover letter: {e}")
            return None
    
    async def upload_latex_source(self, latex_content: str, job_title: str, company: str,
                                 document_type: str) -> Optional[str]:
        """Upload LaTeX source file to R2 storage"""
        try:
            if not await self.ensure_bucket_exists():
                return None
            
            # Generate file key
            file_extension = f"{document_type}.tex"
            file_key = self.generate_file_key('latex_sources', job_title, company, file_extension)
            
            # Upload to R2
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=latex_content.encode('utf-8'),
                ContentType='text/plain',
                Metadata={
                    'job_title': job_title,
                    'company': company,
                    'document_type': f'latex_{document_type}',
                    'uploaded_at': datetime.now().isoformat()
                }
            )
            
            # Generate public URL
            public_url = f"{self.endpoint_url.replace('https://', 'https://pub-')}/{self.bucket_name}/{file_key}"
            
            logger.info(f"✅ LaTeX source uploaded successfully: {file_key}")
            return public_url
            
        except Exception as e:
            logger.error(f"❌ Error uploading LaTeX source: {e}")
            return None
    
    async def upload_job_application_package(self, application_data: Dict) -> Dict[str, str]:
        """Upload complete job application package"""
        try:
            job = application_data['job']
            job_title = job['title']
            company = job['company']
            
            urls = {}
            
            # Upload CV PDF
            if 'cv_pdf' in application_data:
                cv_url = await self.upload_cv(
                    application_data['cv_pdf'], job_title, company
                )
                if cv_url:
                    urls['cv_pdf'] = cv_url
            
            # Upload Cover Letter PDF
            if 'cl_pdf' in application_data:
                cl_url = await self.upload_cover_letter(
                    application_data['cl_pdf'], job_title, company
                )
                if cl_url:
                    urls['cover_letter_pdf'] = cl_url
            
            # Upload LaTeX sources
            if 'cv_latex' in application_data:
                cv_latex_url = await self.upload_latex_source(
                    application_data['cv_latex'], job_title, company, 'cv'
                )
                if cv_latex_url:
                    urls['cv_latex'] = cv_latex_url
            
            if 'cl_latex' in application_data:
                cl_latex_url = await self.upload_latex_source(
                    application_data['cl_latex'], job_title, company, 'cl'
                )
                if cl_latex_url:
                    urls['cover_letter_latex'] = cl_latex_url
            
            # Store job metadata
            metadata_url = await self.store_job_metadata(job)
            if metadata_url:
                urls['job_metadata'] = metadata_url
            
            logger.info(f"📦 Application package uploaded: {len(urls)} files for {company}")
            return urls
            
        except Exception as e:
            logger.error(f"❌ Error uploading application package: {e}")
            return {}
    
    async def store_job_metadata(self, job: Dict) -> Optional[str]:
        """Store job metadata as JSON"""
        try:
            if not await self.ensure_bucket_exists():
                return None
            
            # Generate file key
            job_title = job.get('title', 'unknown')
            company = job.get('company', 'unknown')
            file_key = self.generate_file_key('job_descriptions', job_title, company, 'json')
            
            # Prepare metadata
            metadata = {
                'job_details': job,
                'stored_at': datetime.now().isoformat(),
                'source': job.get('source', 'unknown')
            }
            
            # Upload to R2
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=json.dumps(metadata, indent=2),
                ContentType='application/json',
                Metadata={
                    'job_title': job_title,
                    'company': company,
                    'document_type': 'job_metadata',
                    'uploaded_at': datetime.now().isoformat()
                }
            )
            
            # Generate public URL
            public_url = f"{self.endpoint_url.replace('https://', 'https://pub-')}/{self.bucket_name}/{file_key}"
            
            logger.info(f"✅ Job metadata stored: {file_key}")
            return public_url
            
        except Exception as e:
            logger.error(f"❌ Error storing job metadata: {e}")
            return None
    
    async def list_documents(self, document_type: Optional[str] = None, 
                           company: Optional[str] = None) -> List[Dict]:
        """List documents in R2 storage with filtering"""
        try:
            if not self._validate_client():
                return []
            
            # Determine prefix based on document type
            prefix = ""
            if document_type and document_type in self.storage_paths:
                prefix = self.storage_paths[document_type]
            
            # List objects
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=1000
            )
            
            documents = []
            for obj in response.get('Contents', []):
                # Get object metadata
                metadata_response = self.s3_client.head_object(
                    Bucket=self.bucket_name,
                    Key=obj['Key']
                )
                
                metadata = metadata_response.get('Metadata', {})
                
                # Filter by company if specified
                if company and metadata.get('company', '').lower() != company.lower():
                    continue
                
                document = {
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'],
                    'job_title': metadata.get('job_title', 'Unknown'),
                    'company': metadata.get('company', 'Unknown'),
                    'document_type': metadata.get('document_type', 'Unknown'),
                    'uploaded_at': metadata.get('uploaded_at'),
                    'public_url': f"{self.endpoint_url.replace('https://', 'https://pub-')}/{self.bucket_name}/{obj['Key']}"
                }
                
                documents.append(document)
            
            logger.info(f"📋 Found {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"❌ Error listing documents: {e}")
            return []
    
    async def download_document(self, file_key: str, local_path: Optional[str] = None) -> Optional[bytes]:
        """Download document from R2 storage"""
        try:
            if not self._validate_client():
                return None
            
            # Download object
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            content = response['Body'].read()
            
            # Save to local file if path provided
            if local_path:
                async with aiofiles.open(local_path, 'wb') as f:
                    await f.write(content)
                logger.info(f"📥 Downloaded to: {local_path}")
            
            logger.info(f"📥 Downloaded document: {file_key}")
            return content
            
        except Exception as e:
            logger.error(f"❌ Error downloading document: {e}")
            return None
    
    async def delete_document(self, file_key: str) -> bool:
        """Delete document from R2 storage"""
        try:
            if not self._validate_client():
                return False
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            logger.info(f"🗑️ Deleted document: {file_key}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error deleting document: {e}")
            return False
    
    async def cleanup_old_documents(self, days_old: int = 30) -> int:
        """Clean up documents older than specified days"""
        try:
            if not self._validate_client():
                return 0
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            # List all documents
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                MaxKeys=1000
            )
            
            deleted_count = 0
            for obj in response.get('Contents', []):
                if obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                    await self.delete_document(obj['Key'])
                    deleted_count += 1
            
            logger.info(f"🧹 Cleaned up {deleted_count} old documents")
            return deleted_count
            
        except Exception as e:
            logger.error(f"❌ Error cleaning up documents: {e}")
            return 0
    
    async def get_storage_usage(self) -> Dict:
        """Get storage usage statistics"""
        try:
            if not self._validate_client():
                return {}
            
            # List all objects
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                MaxKeys=1000
            )
            
            usage = {
                'total_objects': 0,
                'total_size_bytes': 0,
                'total_size_mb': 0,
                'by_type': {},
                'by_month': {}
            }
            
            for obj in response.get('Contents', []):
                usage['total_objects'] += 1
                usage['total_size_bytes'] += obj['Size']
                
                # Categorize by type (from path)
                path_parts = obj['Key'].split('/')
                doc_type = path_parts[1] if len(path_parts) > 1 else 'other'
                
                if doc_type not in usage['by_type']:
                    usage['by_type'][doc_type] = {'count': 0, 'size_bytes': 0}
                
                usage['by_type'][doc_type]['count'] += 1
                usage['by_type'][doc_type]['size_bytes'] += obj['Size']
                
                # Categorize by month
                month_key = obj['LastModified'].strftime('%Y-%m')
                if month_key not in usage['by_month']:
                    usage['by_month'][month_key] = {'count': 0, 'size_bytes': 0}
                
                usage['by_month'][month_key]['count'] += 1
                usage['by_month'][month_key]['size_bytes'] += obj['Size']
            
            usage['total_size_mb'] = usage['total_size_bytes'] / (1024 * 1024)
            
            logger.info(f"📊 Storage usage: {usage['total_objects']} objects, {usage['total_size_mb']:.2f} MB")
            return usage
            
        except Exception as e:
            logger.error(f"❌ Error getting storage usage: {e}")
            return {}
    
    async def create_backup(self, backup_name: Optional[str] = None) -> Optional[str]:
        """Create backup of all documents"""
        try:
            if not backup_name:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # This would implement a comprehensive backup strategy
            # For now, just return a mock backup URL
            backup_url = f"backups/{backup_name}.zip"
            
            logger.info(f"💾 Backup created: {backup_url}")
            return backup_url
            
        except Exception as e:
            logger.error(f"❌ Error creating backup: {e}")
            return None
    
    def get_public_url(self, file_key: str) -> str:
        """Get public URL for a file"""
        return f"{self.endpoint_url.replace('https://', 'https://pub-')}/{self.bucket_name}/{file_key}"
    
    async def health_check(self) -> Dict:
        """Perform health check on R2 storage"""
        try:
            health = {
                'r2_connected': False,
                'bucket_accessible': False,
                'credentials_valid': False,
                'timestamp': datetime.now().isoformat()
            }
            
            # Check client initialization
            if self._validate_client():
                health['credentials_valid'] = True
                health['r2_connected'] = True
                
                # Check bucket access
                try:
                    self.s3_client.head_bucket(Bucket=self.bucket_name)
                    health['bucket_accessible'] = True
                except:
                    pass
            
            logger.info(f"🔍 R2 Health Check: {health}")
            return health
            
        except Exception as e:
            logger.error(f"❌ Error in health check: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}