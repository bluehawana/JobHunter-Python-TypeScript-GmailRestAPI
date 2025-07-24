import os
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime, date
from supabase import create_client, Client
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_ANON_KEY
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        logger.info("Supabase client initialized successfully")

    async def create_job_application(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job application record"""
        try:
            # Convert date objects to strings for JSON serialization
            processed_data = self._process_data_for_insert(job_data)
            
            result = self.client.table('job_applications').insert(processed_data).execute()
            
            if result.data:
                logger.info(f"Created job application: {result.data[0].get('id')}")
                return result.data[0]
            else:
                logger.error(f"Failed to create job application: {result}")
                raise Exception("Failed to create job application")
                
        except Exception as e:
            logger.error(f"Error creating job application: {e}")
            raise

    async def update_job_application(self, application_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing job application"""
        try:
            # Convert date objects to strings for JSON serialization
            processed_data = self._process_data_for_insert(update_data)
            processed_data['updated_at'] = datetime.now().isoformat()
            
            result = self.client.table('job_applications').update(processed_data).eq('id', application_id).execute()
            
            if result.data:
                logger.info(f"Updated job application: {application_id}")
                return result.data[0]
            else:
                logger.error(f"Failed to update job application: {result}")
                raise Exception("Failed to update job application")
                
        except Exception as e:
            logger.error(f"Error updating job application: {e}")
            raise

    async def get_job_application(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get a job application by ID"""
        try:
            result = self.client.table('job_applications').select("*").eq('id', application_id).execute()
            
            if result.data:
                return result.data[0]
            return None
                
        except Exception as e:
            logger.error(f"Error fetching job application: {e}")
            return None

    async def get_job_applications(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all job applications with pagination"""
        try:
            result = self.client.table('job_applications')\
                .select("*")\
                .order('created_at', desc=True)\
                .limit(limit)\
                .offset(offset)\
                .execute()
            
            return result.data if result.data else []
                
        except Exception as e:
            logger.error(f"Error fetching job applications: {e}")
            return []

    async def search_job_applications(self, 
                                    company_name: Optional[str] = None,
                                    job_title: Optional[str] = None,
                                    application_status: Optional[str] = None,
                                    final_result: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search job applications with filters"""
        try:
            query = self.client.table('job_applications').select("*")
            
            if company_name:
                query = query.ilike('company_name', f'%{company_name}%')
            if job_title:
                query = query.ilike('job_title', f'%{job_title}%')
            if application_status:
                query = query.eq('application_status', application_status)
            if final_result:
                query = query.eq('final_result', final_result)
            
            result = query.order('created_at', desc=True).execute()
            return result.data if result.data else []
                
        except Exception as e:
            logger.error(f"Error searching job applications: {e}")
            return []

    async def update_application_status(self, application_id: str, status: str, notes: Optional[str] = None) -> bool:
        """Update application status"""
        try:
            update_data = {
                'application_status': status,
                'updated_at': datetime.now().isoformat()
            }
            
            if notes:
                update_data['memo'] = notes
            
            result = self.client.table('job_applications').update(update_data).eq('id', application_id).execute()
            return bool(result.data)
                
        except Exception as e:
            logger.error(f"Error updating application status: {e}")
            return False

    async def add_interview_round(self, application_id: str, interview_data: Dict[str, Any]) -> bool:
        """Add an interview round to the application"""
        try:
            # Get current application
            app = await self.get_job_application(application_id)
            if not app:
                return False
            
            # Get current interview rounds
            current_rounds = app.get('interview_rounds', [])
            if not isinstance(current_rounds, list):
                current_rounds = []
            
            # Add new interview round
            current_rounds.append(interview_data)
            
            # Update application
            update_data = {
                'interview_rounds': current_rounds,
                'application_status': 'interview_scheduled',
                'updated_at': datetime.now().isoformat()
            }
            
            result = self.client.table('job_applications').update(update_data).eq('id', application_id).execute()
            return bool(result.data)
                
        except Exception as e:
            logger.error(f"Error adding interview round: {e}")
            return False

    async def add_communication_log(self, application_id: str, communication_data: Dict[str, Any]) -> bool:
        """Add a communication log entry"""
        try:
            # Get current application
            app = await self.get_job_application(application_id)
            if not app:
                return False
            
            # Get current communications
            current_communications = app.get('communications', [])
            if not isinstance(current_communications, list):
                current_communications = []
            
            # Add new communication
            current_communications.append(communication_data)
            
            # Update application
            update_data = {
                'communications': current_communications,
                'updated_at': datetime.now().isoformat()
            }
            
            result = self.client.table('job_applications').update(update_data).eq('id', application_id).execute()
            return bool(result.data)
                
        except Exception as e:
            logger.error(f"Error adding communication log: {e}")
            return False

    async def get_applications_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get applications by status"""
        try:
            result = self.client.table('job_applications')\
                .select("*")\
                .eq('application_status', status)\
                .order('created_at', desc=True)\
                .execute()
            
            return result.data if result.data else []
                
        except Exception as e:
            logger.error(f"Error fetching applications by status: {e}")
            return []

    async def get_application_statistics(self) -> Dict[str, Any]:
        """Get application statistics"""
        try:
            # Get all applications
            all_apps = await self.get_job_applications(limit=1000)
            
            stats = {
                'total_applications': len(all_apps),
                'by_status': {},
                'by_result': {},
                'by_company': {},
                'recent_applications': 0
            }
            
            # Calculate statistics
            for app in all_apps:
                # Status breakdown
                status = app.get('application_status', 'unknown')
                stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
                
                # Result breakdown
                result = app.get('final_result', 'pending')
                stats['by_result'][result] = stats['by_result'].get(result, 0) + 1
                
                # Company breakdown
                company = app.get('company_name', 'Unknown')
                stats['by_company'][company] = stats['by_company'].get(company, 0) + 1
                
                # Recent applications (last 7 days)
                created_at = app.get('created_at')
                if created_at:
                    created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    days_ago = (datetime.now() - created_date.replace(tzinfo=None)).days
                    if days_ago <= 7:
                        stats['recent_applications'] += 1
            
            return stats
                
        except Exception as e:
            logger.error(f"Error calculating application statistics: {e}")
            return {}

    def _process_data_for_insert(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data for database insertion, handling date objects and None values"""
        processed = {}
        
        for key, value in data.items():
            if value is None:
                continue  # Skip None values
            elif isinstance(value, (datetime, date)):
                processed[key] = value.isoformat()
            elif isinstance(value, (list, dict)):
                processed[key] = value  # Keep as is for JSONB fields
            else:
                processed[key] = value
        
        return processed

# Create a singleton instance
supabase_service = SupabaseService()