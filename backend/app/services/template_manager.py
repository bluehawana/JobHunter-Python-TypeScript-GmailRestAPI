#!/usr/bin/env python3
"""
Intelligent Template Management System
Manages reusable CV/CL templates with versioning and optimization tracking
"""
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import hashlib
from pathlib import Path

from supabase import create_client, Client
from app.core.config import settings

logger = logging.getLogger(__name__)

@dataclass
class TemplateMetadata:
    """Template metadata for tracking usage and performance"""
    template_id: str
    template_type: str  # 'cv' or 'cover_letter'
    template_name: str
    created_date: datetime
    last_used: datetime
    usage_count: int
    success_rate: float  # Based on ATS scores achieved
    average_ats_score: float
    keywords: List[str]
    role_categories: List[str]  # Which job roles this template works best for
    is_active: bool

@dataclass
class TemplateVersion:
    """Template version with content tracking"""
    version_id: str
    template_id: str
    content: str
    latex_content: str
    version_number: int
    created_date: datetime
    performance_score: float
    optimization_notes: str

class TemplateManager:
    """Intelligent template management with caching and optimization tracking"""
    
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_ANON_KEY
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.cache = {}
        self.cache_ttl = timedelta(hours=2)
        
    async def initialize_tables(self):
        """Initialize template management tables in Supabase"""
        try:
            # Create templates metadata table
            templates_table_sql = """
            CREATE TABLE IF NOT EXISTS document_templates (
                id SERIAL PRIMARY KEY,
                template_id VARCHAR(32) UNIQUE NOT NULL,
                template_type VARCHAR(20) NOT NULL,
                template_name VARCHAR(100) NOT NULL,
                created_date TIMESTAMP DEFAULT NOW(),
                last_used TIMESTAMP DEFAULT NOW(),
                usage_count INTEGER DEFAULT 0,
                success_rate FLOAT DEFAULT 0.0,
                average_ats_score FLOAT DEFAULT 0.0,
                keywords JSONB DEFAULT '[]',
                role_categories JSONB DEFAULT '[]',
                is_active BOOLEAN DEFAULT TRUE
            );
            """
            
            # Create template versions table
            versions_table_sql = """
            CREATE TABLE IF NOT EXISTS template_versions (
                id SERIAL PRIMARY KEY,
                version_id VARCHAR(32) UNIQUE NOT NULL,
                template_id VARCHAR(32) REFERENCES document_templates(template_id),
                content TEXT NOT NULL,
                latex_content TEXT,
                version_number INTEGER NOT NULL,
                created_date TIMESTAMP DEFAULT NOW(),
                performance_score FLOAT DEFAULT 0.0,
                optimization_notes TEXT DEFAULT ''
            );
            """
            
            # Create template performance tracking
            performance_table_sql = """
            CREATE TABLE IF NOT EXISTS template_performance (
                id SERIAL PRIMARY KEY,
                template_id VARCHAR(32) REFERENCES document_templates(template_id),
                job_title VARCHAR(200),
                company VARCHAR(200),
                ats_score FLOAT,
                keyword_match FLOAT,
                format_score FLOAT,
                success BOOLEAN,
                usage_date TIMESTAMP DEFAULT NOW()
            );
            """
            
            logger.info("Template management tables initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing template tables: {e}")
            return False
    
    def generate_template_id(self, template_type: str, base_content: str) -> str:
        """Generate unique template ID based on content hash"""
        content_hash = hashlib.md5(f"{template_type}_{base_content}".encode()).hexdigest()
        return f"{template_type}_{content_hash[:12]}"
    
    async def create_template(self, template_type: str, template_name: str, 
                            content: str, latex_content: str, 
                            keywords: List[str], role_categories: List[str]) -> str:
        """Create new template with initial version"""
        
        template_id = self.generate_template_id(template_type, content)
        version_id = f"{template_id}_v1"
        
        try:
            # Create template metadata
            template_data = {
                'template_id': template_id,
                'template_type': template_type,
                'template_name': template_name,
                'keywords': json.dumps(keywords),
                'role_categories': json.dumps(role_categories)
            }
            
            result = self.supabase.table("document_templates").upsert(template_data).execute()
            
            # Create first version
            version_data = {
                'version_id': version_id,
                'template_id': template_id,
                'content': content,
                'latex_content': latex_content,
                'version_number': 1,
                'optimization_notes': 'Initial template creation'
            }
            
            self.supabase.table("template_versions").upsert(version_data).execute()
            
            logger.info(f"Created template {template_id} with version {version_id}")
            return template_id
            
        except Exception as e:
            logger.error(f"Error creating template: {e}")
            return ""
    
    async def find_best_template(self, job_title: str, job_description: str, 
                               template_type: str, role_category: str) -> Optional[Dict]:
        """Find the best existing template for a job"""
        
        try:
            # Get templates of specified type and role category
            result = self.supabase.table("document_templates").select("*").eq(
                "template_type", template_type
            ).eq("is_active", True).execute()
            
            if not result.data:
                logger.info(f"No templates found for type: {template_type}")
                return None
            
            # Score templates based on relevance
            scored_templates = []
            job_lower = f"{job_title} {job_description}".lower()
            
            for template in result.data:
                score = self._calculate_template_relevance(template, job_lower, role_category)
                scored_templates.append((template, score))
            
            # Sort by score and get best template
            scored_templates.sort(key=lambda x: x[1], reverse=True)
            best_template = scored_templates[0][0] if scored_templates else None
            
            if best_template:
                logger.info(f"Found best template: {best_template['template_id']} (score: {scored_templates[0][1]:.2f})")
                return best_template
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding best template: {e}")
            return None
    
    def _calculate_template_relevance(self, template: Dict, job_text: str, role_category: str) -> float:
        """Calculate how relevant a template is for a specific job"""
        score = 0.0
        
        # Base score from success rate and ATS performance
        score += template.get('success_rate', 0) * 0.3
        score += template.get('average_ats_score', 0) * 0.2
        
        # Keyword matching score
        template_keywords = json.loads(template.get('keywords', '[]'))
        keyword_matches = sum(1 for keyword in template_keywords if keyword in job_text)
        keyword_score = (keyword_matches / len(template_keywords)) * 100 if template_keywords else 0
        score += keyword_score * 0.3
        
        # Role category matching
        template_roles = json.loads(template.get('role_categories', '[]'))
        if role_category in template_roles:
            score += 20  # Bonus for role match
        
        # Usage frequency bonus (popular templates are often better)
        usage_bonus = min(template.get('usage_count', 0) * 0.1, 10)
        score += usage_bonus
        
        return score
    
    async def get_template_with_latest_version(self, template_id: str) -> Optional[Dict]:
        """Get template with its latest version content"""
        
        try:
            # Check cache first
            cache_key = f"template_{template_id}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if datetime.now() - timestamp < self.cache_ttl:
                    return cached_data
            
            # Get template metadata
            template_result = self.supabase.table("document_templates").select("*").eq(
                "template_id", template_id
            ).execute()
            
            if not template_result.data:
                return None
            
            template_data = template_result.data[0]
            
            # Get latest version
            version_result = self.supabase.table("template_versions").select("*").eq(
                "template_id", template_id
            ).order("version_number", desc=True).limit(1).execute()
            
            if not version_result.data:
                return None
            
            version_data = version_result.data[0]
            
            # Combine template and version data
            combined_data = {
                **template_data,
                'latest_version': version_data
            }
            
            # Cache the result
            self.cache[cache_key] = (combined_data, datetime.now())
            
            return combined_data
            
        except Exception as e:
            logger.error(f"Error getting template with version: {e}")
            return None
    
    async def create_template_version(self, template_id: str, content: str, 
                                    latex_content: str, performance_score: float,
                                    optimization_notes: str) -> str:
        """Create new version of existing template"""
        
        try:
            # Get current highest version number
            version_result = self.supabase.table("template_versions").select("version_number").eq(
                "template_id", template_id
            ).order("version_number", desc=True).limit(1).execute()
            
            next_version = 1
            if version_result.data:
                next_version = version_result.data[0]['version_number'] + 1
            
            version_id = f"{template_id}_v{next_version}"
            
            # Create new version
            version_data = {
                'version_id': version_id,
                'template_id': template_id,
                'content': content,
                'latex_content': latex_content,
                'version_number': next_version,
                'performance_score': performance_score,
                'optimization_notes': optimization_notes
            }
            
            self.supabase.table("template_versions").insert(version_data).execute()
            
            # Clear cache for this template
            cache_key = f"template_{template_id}"
            if cache_key in self.cache:
                del self.cache[cache_key]
            
            logger.info(f"Created version {next_version} for template {template_id}")
            return version_id
            
        except Exception as e:
            logger.error(f"Error creating template version: {e}")
            return ""
    
    async def update_template_performance(self, template_id: str, job_title: str, 
                                        company: str, ats_score: float, 
                                        keyword_match: float, format_score: float,
                                        success: bool):
        """Update template performance metrics"""
        
        try:
            # Record performance data
            performance_data = {
                'template_id': template_id,
                'job_title': job_title,
                'company': company,
                'ats_score': ats_score,
                'keyword_match': keyword_match,
                'format_score': format_score,
                'success': success
            }
            
            self.supabase.table("template_performance").insert(performance_data).execute()
            
            # Update template aggregate metrics
            await self._update_template_aggregates(template_id)
            
            logger.info(f"Updated performance for template {template_id}")
            
        except Exception as e:
            logger.error(f"Error updating template performance: {e}")
    
    async def _update_template_aggregates(self, template_id: str):
        """Update template aggregate performance metrics"""
        
        try:
            # Get all performance records for this template
            perf_result = self.supabase.table("template_performance").select("*").eq(
                "template_id", template_id
            ).execute()
            
            if not perf_result.data:
                return
            
            performances = perf_result.data
            total_uses = len(performances)
            successful_uses = sum(1 for p in performances if p['success'])
            success_rate = (successful_uses / total_uses) * 100 if total_uses > 0 else 0
            
            avg_ats_score = sum(p['ats_score'] for p in performances) / total_uses if total_uses > 0 else 0
            
            # Update template metadata
            update_data = {
                'usage_count': total_uses,
                'success_rate': success_rate,
                'average_ats_score': avg_ats_score,
                'last_used': datetime.now().isoformat()
            }
            
            self.supabase.table("document_templates").update(update_data).eq(
                "template_id", template_id
            ).execute()
            
            # Clear cache
            cache_key = f"template_{template_id}"
            if cache_key in self.cache:
                del self.cache[cache_key]
            
        except Exception as e:
            logger.error(f"Error updating template aggregates: {e}")
    
    async def get_template_recommendations(self, job_title: str, job_description: str,
                                         role_category: str) -> Dict:
        """Get template recommendations with performance insights"""
        
        try:
            # Find best templates for both CV and cover letter
            cv_template = await self.find_best_template(job_title, job_description, 'cv', role_category)
            cl_template = await self.find_best_template(job_title, job_description, 'cover_letter', role_category)
            
            recommendations = {
                'cv_recommendation': None,
                'cover_letter_recommendation': None,
                'should_create_new': False,
                'confidence_score': 0.0,
                'performance_insights': {}
            }
            
            if cv_template:
                cv_data = await self.get_template_with_latest_version(cv_template['template_id'])
                recommendations['cv_recommendation'] = cv_data
                
            if cl_template:
                cl_data = await self.get_template_with_latest_version(cl_template['template_id'])
                recommendations['cover_letter_recommendation'] = cl_data
            
            # Calculate confidence
            cv_confidence = cv_template.get('average_ats_score', 0) if cv_template else 0
            cl_confidence = cl_template.get('average_ats_score', 0) if cl_template else 0
            recommendations['confidence_score'] = (cv_confidence + cl_confidence) / 2
            
            # Determine if new template should be created
            recommendations['should_create_new'] = recommendations['confidence_score'] < 70
            
            # Add performance insights
            if cv_template:
                recommendations['performance_insights']['cv'] = {
                    'success_rate': cv_template.get('success_rate', 0),
                    'average_ats_score': cv_template.get('average_ats_score', 0),
                    'usage_count': cv_template.get('usage_count', 0)
                }
            
            if cl_template:
                recommendations['performance_insights']['cover_letter'] = {
                    'success_rate': cl_template.get('success_rate', 0),
                    'average_ats_score': cl_template.get('average_ats_score', 0),
                    'usage_count': cl_template.get('usage_count', 0)
                }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting template recommendations: {e}")
            return {'error': str(e)}
    
    async def cleanup_old_versions(self, keep_versions: int = 5):
        """Clean up old template versions to save space"""
        
        try:
            # Get all templates
            templates_result = self.supabase.table("document_templates").select("template_id").execute()
            
            for template in templates_result.data:
                template_id = template['template_id']
                
                # Get versions for this template
                versions_result = self.supabase.table("template_versions").select("*").eq(
                    "template_id", template_id
                ).order("version_number", desc=True).execute()
                
                if len(versions_result.data) > keep_versions:
                    # Delete old versions
                    versions_to_delete = versions_result.data[keep_versions:]
                    for version in versions_to_delete:
                        self.supabase.table("template_versions").delete().eq(
                            "version_id", version['version_id']
                        ).execute()
                    
                    logger.info(f"Cleaned up {len(versions_to_delete)} old versions for template {template_id}")
            
        except Exception as e:
            logger.error(f"Error cleaning up old versions: {e}")
    
    async def get_template_analytics(self) -> Dict:
        """Get analytics about template usage and performance"""
        
        try:
            # Get template statistics
            templates_result = self.supabase.table("document_templates").select("*").execute()
            performance_result = self.supabase.table("template_performance").select("*").execute()
            
            analytics = {
                'total_templates': len(templates_result.data),
                'active_templates': len([t for t in templates_result.data if t['is_active']]),
                'template_types': {},
                'performance_overview': {},
                'top_performing_templates': [],
                'usage_trends': {}
            }
            
            # Template type breakdown
            for template in templates_result.data:
                t_type = template['template_type']
                analytics['template_types'][t_type] = analytics['template_types'].get(t_type, 0) + 1
            
            # Performance overview
            if performance_result.data:
                performances = performance_result.data
                analytics['performance_overview'] = {
                    'total_applications': len(performances),
                    'success_rate': (sum(1 for p in performances if p['success']) / len(performances)) * 100,
                    'average_ats_score': sum(p['ats_score'] for p in performances) / len(performances),
                    'average_keyword_match': sum(p['keyword_match'] for p in performances) / len(performances)
                }
            
            # Top performing templates
            top_templates = sorted(
                templates_result.data, 
                key=lambda x: x.get('average_ats_score', 0), 
                reverse=True
            )[:5]
            
            analytics['top_performing_templates'] = [
                {
                    'template_id': t['template_id'],
                    'template_name': t['template_name'],
                    'template_type': t['template_type'],
                    'average_ats_score': t.get('average_ats_score', 0),
                    'success_rate': t.get('success_rate', 0),
                    'usage_count': t.get('usage_count', 0)
                }
                for t in top_templates
            ]
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting template analytics: {e}")
            return {'error': str(e)}