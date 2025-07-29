#!/usr/bin/env python3
"""
Smart CV/CL Customization Service
Integrates all optimization components for intelligent document customization
"""
import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

from .enhanced_cv_optimizer import EnhancedCVOptimizer, ATSScore
from .template_manager import TemplateManager
from .ats_analyzer import ATSAnalyzer, ATSAnalysisResult
from .latex_resume_service import LaTeXResumeService

logger = logging.getLogger(__name__)

class SmartCVService:
    """
    Intelligent CV/CL customization service that:
    - Uses templates to avoid regeneration
    - Applies incremental optimizations
    - Provides ATS scoring and feedback
    - Learns from previous applications
    """
    
    def __init__(self):
        self.cv_optimizer = EnhancedCVOptimizer()
        self.template_manager = TemplateManager()
        self.ats_analyzer = ATSAnalyzer()
        self.latex_service = LaTeXResumeService()
        
        # Performance tracking
        self.optimization_history = {}
        self.success_metrics = {
            'total_applications': 0,
            'avg_ats_score': 0.0,
            'templates_reused': 0,
            'optimization_success_rate': 0.0
        }
    
    async def initialize(self):
        """Initialize all services and database tables"""
        try:
            await self.template_manager.initialize_tables()
            logger.info("Smart CV Service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing Smart CV Service: {e}")
            return False
    
    async def process_job_application(self, job_data: Dict, 
                                    force_regenerate: bool = False) -> Dict:
        """
        Process job application with intelligent customization
        
        Args:
            job_data: Job posting information
            force_regenerate: Force full regeneration instead of using templates
            
        Returns:
            Dict with optimized documents and analysis
        """
        
        job_title = job_data.get('title', '')
        company = job_data.get('company', '')
        job_description = job_data.get('description', '')
        
        logger.info(f"Processing application for {job_title} at {company}")
        
        try:
            # Step 1: Analyze job requirements
            role_category = self.cv_optimizer.analyze_job_role(job_title, job_description)
            
            # Step 2: Get template recommendations
            template_recommendations = await self.template_manager.get_template_recommendations(
                job_title, job_description, role_category
            )
            
            # Step 3: Decide on optimization strategy
            optimization_strategy = self._determine_optimization_strategy(
                template_recommendations, force_regenerate
            )
            
            # Step 4: Generate/optimize documents
            result = await self._execute_optimization_strategy(
                job_data, template_recommendations, optimization_strategy
            )
            
            # Step 5: Analyze final documents with ATS checker
            cv_analysis = await self.ats_analyzer.analyze_document(
                result['cv_content'], job_description, job_title, 'cv'
            )
            cl_analysis = await self.ats_analyzer.analyze_document(
                result['cover_letter_content'], job_description, job_title, 'cover_letter'
            )
            
            # Step 6: Update template performance
            if result.get('template_used'):
                await self._update_template_performance(
                    result['cv_template_id'], job_title, company, cv_analysis
                )
                await self._update_template_performance(
                    result['cl_template_id'], job_title, company, cl_analysis
                )
            
            # Step 7: Compile to PDF
            cv_pdf = await self.latex_service._compile_latex_to_pdf(
                result['cv_content'], f"cv_{company}_{job_title.replace(' ', '_')}"
            )
            cl_pdf = await self.latex_service._compile_latex_to_pdf(
                result['cover_letter_content'], f"cl_{company}_{job_title.replace(' ', '_')}"
            )
            
            # Step 8: Generate comprehensive report
            final_result = {
                'job_details': {
                    'title': job_title,
                    'company': company,
                    'role_category': role_category
                },
                'documents': {
                    'cv_content': result['cv_content'],
                    'cover_letter_content': result['cover_letter_content'],
                    'cv_pdf': cv_pdf,
                    'cover_letter_pdf': cl_pdf
                },
                'optimization_details': {
                    'strategy_used': optimization_strategy,
                    'template_reused': result.get('template_used', False),
                    'cv_template_id': result.get('cv_template_id'),
                    'cl_template_id': result.get('cl_template_id'),
                    'processing_time': result.get('processing_time', 0)
                },
                'ats_analysis': {
                    'cv_analysis': cv_analysis,
                    'cl_analysis': cl_analysis,
                    'overall_score': (cv_analysis.overall_score + cl_analysis.overall_score) / 2,
                    'ats_ready': cv_analysis.passing_threshold and cl_analysis.passing_threshold
                },
                'recommendations': self._generate_application_recommendations(
                    cv_analysis, cl_analysis, optimization_strategy
                ),
                'success_indicators': {
                    'high_ats_scores': cv_analysis.overall_score >= 85 and cl_analysis.overall_score >= 85,
                    'template_efficiency': result.get('template_used', False),
                    'optimization_effective': len(cv_analysis.critical_issues) == 0,
                    'ready_for_submission': cv_analysis.passing_threshold and cl_analysis.passing_threshold
                },
                'generated_at': datetime.now().isoformat()
            }
            
            # Update success metrics
            await self._update_success_metrics(final_result)
            
            logger.info(f"Successfully processed application - ATS Scores: CV:{cv_analysis.overall_score:.1f}, CL:{cl_analysis.overall_score:.1f}")
            
            return final_result
            
        except Exception as e:
            logger.error(f"Error processing job application: {e}")
            return {
                'error': str(e),
                'job_details': {'title': job_title, 'company': company},
                'success': False,
                'generated_at': datetime.now().isoformat()
            }
    
    def _determine_optimization_strategy(self, template_recommendations: Dict, 
                                       force_regenerate: bool) -> str:
        """Determine the best optimization strategy"""
        
        if force_regenerate:
            return 'full_regeneration'
        
        if template_recommendations.get('should_create_new', True):
            return 'create_new_template'
        
        confidence = template_recommendations.get('confidence_score', 0)
        
        if confidence >= 85:
            return 'minimal_customization'
        elif confidence >= 70:
            return 'incremental_optimization'
        else:
            return 'significant_customization'
    
    async def _execute_optimization_strategy(self, job_data: Dict, 
                                           template_recommendations: Dict,
                                           strategy: str) -> Dict:
        """Execute the determined optimization strategy"""
        
        start_time = datetime.now()
        
        if strategy == 'full_regeneration':
            result = await self._full_regeneration(job_data)
        elif strategy == 'create_new_template':
            result = await self._create_new_template(job_data)
        elif strategy == 'minimal_customization':
            result = await self._minimal_customization(job_data, template_recommendations)
        elif strategy == 'incremental_optimization':
            result = await self._incremental_optimization(job_data, template_recommendations)
        else:  # significant_customization
            result = await self._significant_customization(job_data, template_recommendations)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        result['processing_time'] = processing_time
        
        return result
    
    async def _full_regeneration(self, job_data: Dict) -> Dict:
        """Generate completely new documents from scratch"""
        
        logger.info("Using full regeneration strategy")
        
        # Use existing LaTeX service for full generation
        cv_pdf = await self.latex_service.generate_customized_cv(job_data)
        cl_pdf = await self.latex_service.generate_customized_cover_letter(job_data)
        
        # Extract LaTeX content (simplified - would need proper extraction)
        cv_content = self._generate_cv_latex_content(job_data)
        cl_content = self._generate_cl_latex_content(job_data)
        
        return {
            'cv_content': cv_content,
            'cover_letter_content': cl_content,
            'template_used': False,
            'optimization_method': 'full_regeneration'
        }
    
    async def _create_new_template(self, job_data: Dict) -> Dict:
        """Create new templates and optimize for job"""
        
        logger.info("Creating new templates strategy")
        
        # Generate base documents
        result = await self._full_regeneration(job_data)
        
        # Create templates for future use
        role_category = self.cv_optimizer.analyze_job_role(
            job_data.get('title', ''), job_data.get('description', '')
        )
        
        keywords = self.cv_optimizer._get_target_keywords(
            role_category, job_data.get('description', '')
        )
        
        # Create CV template
        cv_template_id = await self.template_manager.create_template(
            'cv', 
            f"CV Template - {role_category}",
            result['cv_content'],
            result['cv_content'], 
            keywords,
            [role_category]
        )
        
        # Create Cover Letter template
        cl_template_id = await self.template_manager.create_template(
            'cover_letter',
            f"CL Template - {role_category}",
            result['cover_letter_content'],
            result['cover_letter_content'],
            keywords,
            [role_category]
        )
        
        result.update({
            'cv_template_id': cv_template_id,
            'cl_template_id': cl_template_id,
            'template_created': True,
            'optimization_method': 'create_new_template'
        })
        
        return result
    
    async def _minimal_customization(self, job_data: Dict, 
                                   template_recommendations: Dict) -> Dict:
        """Apply minimal customization to existing high-quality templates"""
        
        logger.info("Using minimal customization strategy")
        
        # Get templates
        cv_template = template_recommendations.get('cv_recommendation')
        cl_template = template_recommendations.get('cover_letter_recommendation')
        
        if not cv_template or not cl_template:
            return await self._create_new_template(job_data)
        
        # Get template content
        cv_base = cv_template['latest_version']['content']
        cl_base = cl_template['latest_version']['content']
        
        # Apply minimal customizations
        cv_content = await self.cv_optimizer._apply_minimal_customization(
            cv_base, job_data, []
        )
        
        cl_content = cl_base.replace('{company}', job_data.get('company', ''))
        cl_content = cl_content.replace('{job_title}', job_data.get('title', ''))
        
        return {
            'cv_content': cv_content,
            'cover_letter_content': cl_content,
            'cv_template_id': cv_template['template_id'],
            'cl_template_id': cl_template['template_id'],
            'template_used': True,
            'optimization_method': 'minimal_customization'
        }
    
    async def _incremental_optimization(self, job_data: Dict,
                                      template_recommendations: Dict) -> Dict:
        """Apply incremental optimization to existing templates"""
        
        logger.info("Using incremental optimization strategy")
        
        cv_template = template_recommendations.get('cv_recommendation')
        cl_template = template_recommendations.get('cover_letter_recommendation')
        
        if not cv_template or not cl_template:
            return await self._create_new_template(job_data)
        
        # Get base content
        cv_base = cv_template['latest_version']['content']
        cl_base = cl_template['latest_version']['content']
        
        # Apply incremental optimizations
        cv_optimized, cv_score = await self.cv_optimizer.optimize_cv_incrementally(
            cv_base, job_data
        )
        
        cl_optimized, cl_score = await self.cv_optimizer.optimize_cover_letter_incrementally(
            cl_base, job_data
        )
        
        # Create new versions if significantly improved
        if cv_score.overall_score > cv_template.get('average_ats_score', 0) + 5:
            await self.template_manager.create_template_version(
                cv_template['template_id'],
                cv_optimized,
                cv_optimized,
                cv_score.overall_score,
                f"Incremental optimization for {job_data.get('company', 'unknown')}"
            )
        
        if cl_score.overall_score > cl_template.get('average_ats_score', 0) + 5:
            await self.template_manager.create_template_version(
                cl_template['template_id'],
                cl_optimized,
                cl_optimized,
                cl_score.overall_score,
                f"Incremental optimization for {job_data.get('company', 'unknown')}"
            )
        
        return {
            'cv_content': cv_optimized,
            'cover_letter_content': cl_optimized,
            'cv_template_id': cv_template['template_id'],
            'cl_template_id': cl_template['template_id'],
            'template_used': True,
            'optimization_method': 'incremental_optimization',
            'cv_ats_score': cv_score,
            'cl_ats_score': cl_score
        }
    
    async def _significant_customization(self, job_data: Dict,
                                       template_recommendations: Dict) -> Dict:
        """Apply significant customization for challenging jobs"""
        
        logger.info("Using significant customization strategy")
        
        # Start with templates if available, otherwise create new
        if template_recommendations.get('cv_recommendation'):
            cv_base = template_recommendations['cv_recommendation']['latest_version']['content']
            cl_base = template_recommendations['cover_letter_recommendation']['latest_version']['content']
        else:
            base_result = await self._full_regeneration(job_data)
            cv_base = base_result['cv_content']
            cl_base = base_result['cover_letter_content']
        
        # Apply comprehensive optimization
        cv_optimized, cv_score = await self.cv_optimizer.optimize_cv_incrementally(
            cv_base, job_data
        )
        
        cl_optimized, cl_score = await self.cv_optimizer.optimize_cover_letter_incrementally(
            cl_base, job_data
        )
        
        # If still not satisfactory, try different approach
        if cv_score.overall_score < 75 or cl_score.overall_score < 75:
            logger.warning("Significant customization yielding low scores, falling back to full regeneration")
            return await self._full_regeneration(job_data)
        
        return {
            'cv_content': cv_optimized,
            'cover_letter_content': cl_optimized,
            'template_used': template_recommendations.get('cv_recommendation') is not None,
            'optimization_method': 'significant_customization',
            'cv_ats_score': cv_score,
            'cl_ats_score': cl_score
        }
    
    async def _update_template_performance(self, template_id: str, job_title: str,
                                         company: str, analysis: ATSAnalysisResult):
        """Update template performance metrics"""
        
        if not template_id:
            return
        
        await self.template_manager.update_template_performance(
            template_id,
            job_title,
            company,
            analysis.overall_score,
            analysis.detailed_scores.get('keyword_optimization', 0),
            analysis.detailed_scores.get('format_compatibility', 0),
            analysis.passing_threshold
        )
    
    def _generate_application_recommendations(self, cv_analysis: ATSAnalysisResult,
                                            cl_analysis: ATSAnalysisResult,
                                            strategy: str) -> List[str]:
        """Generate actionable recommendations for the application"""
        
        recommendations = []
        
        # Overall assessment
        avg_score = (cv_analysis.overall_score + cl_analysis.overall_score) / 2
        
        if avg_score >= 90:
            recommendations.append("🎉 Excellent! Your application is highly optimized for ATS systems")
        elif avg_score >= 80:
            recommendations.append("✅ Good work! Your application should perform well with ATS systems")
        elif avg_score >= 70:
            recommendations.append("⚠️ Your application needs some improvements for better ATS compatibility")
        else:
            recommendations.append("🚨 Critical: Your application needs significant improvements for ATS systems")
        
        # CV-specific recommendations
        if cv_analysis.overall_score < 75:
            recommendations.append(f"📄 CV Priority: {cv_analysis.recommendations[0] if cv_analysis.recommendations else 'Improve keyword optimization'}")
        
        # Cover Letter-specific recommendations
        if cl_analysis.overall_score < 75:
            recommendations.append(f"✍️ CL Priority: {cl_analysis.recommendations[0] if cl_analysis.recommendations else 'Add more job-specific content'}")
        
        # Strategy-specific advice
        if strategy == 'minimal_customization':
            recommendations.append("⚡ Used high-quality template with minimal changes - very efficient!")
        elif strategy == 'create_new_template':
            recommendations.append("🆕 Created new template - future applications for similar roles will be faster")
        elif strategy == 'full_regeneration':
            recommendations.append("🔄 Used complete regeneration - consider creating templates for efficiency")
        
        return recommendations[:5]  # Top 5 recommendations
    
    async def _update_success_metrics(self, result: Dict):
        """Update overall success metrics"""
        
        self.success_metrics['total_applications'] += 1
        
        if result.get('ats_analysis'):
            current_score = result['ats_analysis']['overall_score']
            current_avg = self.success_metrics['avg_ats_score']
            total = self.success_metrics['total_applications']
            
            # Update running average
            self.success_metrics['avg_ats_score'] = (
                (current_avg * (total - 1) + current_score) / total
            )
        
        if result.get('optimization_details', {}).get('template_reused'):
            self.success_metrics['templates_reused'] += 1
        
        # Calculate success rate
        if result.get('ats_analysis', {}).get('ats_ready'):
            current_success = self.success_metrics.get('successful_applications', 0) + 1
            self.success_metrics['successful_applications'] = current_success
            self.success_metrics['optimization_success_rate'] = (
                current_success / self.success_metrics['total_applications']
            ) * 100
    
    def _generate_cv_latex_content(self, job_data: Dict) -> str:
        """Generate CV LaTeX content (simplified version)"""
        # This would use the existing LaTeX service template
        # For now, return a basic structure
        return self.latex_service.cv_template.format(
            job_role=job_data.get('title', 'Software Developer'),
            customized_profile="Experienced developer with relevant skills",
            skills_content="\\item \\textbf{Programming:} Java, Python, JavaScript"
        )
    
    def _generate_cl_latex_content(self, job_data: Dict) -> str:
        """Generate Cover Letter LaTeX content (simplified version)"""
        return self.latex_service.cover_letter_template.format(
            company_name=job_data.get('company', 'Company'),
            company_address=f"{job_data.get('company', 'Company')}\\\\Location",
            hiring_manager_greeting="Dear Hiring Manager",
            cover_letter_body="I am writing to express my interest in this position...",
            current_date=datetime.now().strftime("%Y-%m-%d")
        )
    
    async def get_service_analytics(self) -> Dict:
        """Get comprehensive service analytics"""
        
        template_analytics = await self.template_manager.get_template_analytics()
        
        return {
            'service_metrics': self.success_metrics,
            'template_analytics': template_analytics,
            'optimization_efficiency': {
                'template_reuse_rate': (
                    self.success_metrics['templates_reused'] / 
                    max(1, self.success_metrics['total_applications'])
                ) * 100,
                'avg_ats_score': self.success_metrics['avg_ats_score'],
                'success_rate': self.success_metrics.get('optimization_success_rate', 0)
            },
            'performance_insights': {
                'total_processed': self.success_metrics['total_applications'],
                'avg_quality': self.success_metrics['avg_ats_score'],
                'efficiency_score': (
                    self.success_metrics['templates_reused'] * 20 + 
                    self.success_metrics.get('optimization_success_rate', 0)
                ) / 2
            }
        }
    
    async def batch_process_applications(self, jobs_list: List[Dict]) -> List[Dict]:
        """Process multiple job applications efficiently"""
        
        logger.info(f"Starting batch processing of {len(jobs_list)} applications")
        
        results = []
        
        for i, job_data in enumerate(jobs_list):
            try:
                logger.info(f"Processing application {i+1}/{len(jobs_list)}")
                
                result = await self.process_job_application(job_data)
                results.append(result)
                
                # Add small delay to prevent overwhelming the system
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error processing job {i+1}: {e}")
                results.append({
                    'error': str(e),
                    'job_details': job_data,
                    'success': False
                })
        
        # Generate batch summary
        batch_summary = {
            'total_processed': len(results),
            'successful': len([r for r in results if not r.get('error')]),
            'failed': len([r for r in results if r.get('error')]),
            'avg_ats_score': sum(
                r.get('ats_analysis', {}).get('overall_score', 0) 
                for r in results if not r.get('error')
            ) / max(1, len([r for r in results if not r.get('error')])),
            'batch_completed_at': datetime.now().isoformat()
        }
        
        logger.info(f"Batch processing completed: {batch_summary['successful']}/{batch_summary['total_processed']} successful")
        
        return {
            'batch_summary': batch_summary,
            'individual_results': results
        }