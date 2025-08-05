#!/usr/bin/env python3
"""
Comprehensive test script for the Real Job Hunter system
Tests the complete pipeline from job collection to document generation
"""

import asyncio
import logging
import json
import os
import sys
from datetime import datetime
from typing import Dict, List

# Add the backend app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.real_job_hunter_orchestrator import RealJobHunterOrchestrator
from app.services.job_analysis_service import JobAnalysisService
from app.services.smart_cv_customization_service import SmartCVCustomizationService
from app.services.smart_cover_letter_service import SmartCoverLetterService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_real_job_hunter.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class RealJobHunterTester:
    """
    Comprehensive tester for the Real Job Hunter system
    """
    
    def __init__(self):
        self.orchestrator = RealJobHunterOrchestrator()
        self.job_analyzer = JobAnalysisService()
        self.cv_customizer = SmartCVCustomizationService()
        self.cover_letter_service = SmartCoverLetterService()
        
        # Test configuration
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'test_details': [],
            'performance_metrics': {}
        }
        
        # Mock job data for testing
        self.mock_jobs = [
            {
                'source': 'linkedin_real',
                'job_id': 'test_001',
                'title': 'Senior Full Stack Developer',
                'company': 'Spotify Technology',
                'location': 'Stockholm, Sweden',
                'application_link': 'https://www.linkedin.com/jobs/view/3721234567',
                'description': 'We are looking for a passionate Senior Full Stack Developer to join our engineering team. You will be working with React, Node.js, Java, Spring Boot, and AWS cloud technologies. Experience with microservices architecture, Docker, Kubernetes, and CI/CD pipelines is highly valued. You should have 5+ years of experience in software development and strong problem-solving skills. Knowledge of music streaming or media technology is a plus.',
                'requirements': [
                    'Bachelor\'s degree in Computer Science or related field',
                    '5+ years of software development experience',
                    'Proficiency in React, Node.js, Java, Spring Boot',
                    'Experience with AWS cloud services',
                    'Knowledge of microservices architecture',
                    'Experience with Docker and Kubernetes'
                ],
                'keywords': ['javascript', 'react', 'nodejs', 'java', 'spring boot', 'aws', 'microservices', 'docker', 'kubernetes'],
                'employment_type': 'Full-time',
                'salary': '650,000 - 850,000 SEK',
                'company_info': 'Spotify is the world\'s most popular audio streaming subscription service with 456m users, including 195m subscribers, across 183 markets.',
                'benefits': ['Competitive salary', 'Equity program', 'Health insurance', 'Flexible working'],
                'seniority_level': 'Senior',
                'industry': 'Music Streaming',
                'date_posted': 'Today',
                'experience_level': 'Senior',
                'collection_source': 'linkedin',
                'collection_timestamp': datetime.now().isoformat()
            },
            {
                'source': 'indeed_real',
                'job_key': 'test_002',
                'title': 'Backend Developer',
                'company': 'Klarna Bank',
                'location': 'Stockholm, Sweden',
                'application_link': 'https://se.indeed.com/viewjob?jk=test002',
                'description': 'Join Klarna\'s engineering team as a Backend Developer. We are building the next generation of payment solutions using Python, Django, PostgreSQL, and cloud technologies. You will work on high-performance APIs, implement automated testing, and contribute to our microservices architecture. Experience with fintech, payment systems, and security best practices is highly valued.',
                'salary': '550,000 - 700,000 SEK',
                'keywords': ['python', 'django', 'postgresql', 'apis', 'microservices', 'fintech', 'testing'],
                'employment_type': 'Full-time',
                'experience_level': 'Mid-level',
                'collection_source': 'indeed',
                'collection_timestamp': datetime.now().isoformat()
            },
            {
                'source': 'arbetsformedlingen_real',
                'title': 'DevOps Engineer',
                'company': 'Volvo Group',
                'location': 'Göteborg, Sweden',
                'application_link': 'https://arbetsformedlingen.se/jobb/annons/test003',
                'description': 'Volvo Group is seeking a skilled DevOps Engineer to join our infrastructure team. You will work with Kubernetes, Docker, Jenkins, Terraform, and AWS. Responsibilities include managing CI/CD pipelines, monitoring infrastructure, and ensuring system reliability. Experience with automotive industry and IoT systems is a plus.',
                'keywords': ['devops', 'kubernetes', 'docker', 'jenkins', 'terraform', 'aws', 'cicd', 'infrastructure'],
                'employment_type': 'Permanent',
                'salary': '600,000 - 750,000 SEK',
                'experience_level': 'Senior',
                'collection_source': 'arbetsformedlingen',
                'collection_timestamp': datetime.now().isoformat()
            }
        ]

    async def run_comprehensive_tests(self) -> Dict:
        """
        Run all comprehensive tests
        """
        logger.info("🧪 Starting comprehensive Real Job Hunter tests...")
        
        try:
            # Test 1: Job Analysis Service
            await self._test_job_analysis_service()
            
            # Test 2: CV Customization Service
            await self._test_cv_customization_service()
            
            # Test 3: Cover Letter Service
            await self._test_cover_letter_service()
            
            # Test 4: Document Generation Pipeline
            await self._test_document_generation_pipeline()
            
            # Test 5: Job Prioritization
            await self._test_job_prioritization()
            
            # Test 6: Error Handling
            await self._test_error_handling()
            
            # Test 7: Performance Benchmarks
            await self._test_performance_benchmarks()
            
            # Generate final test report
            self._generate_test_report()
            
            logger.info("✅ All comprehensive tests completed!")
            return self.test_results
            
        except Exception as e:
            logger.error(f"❌ Test suite failed: {e}")
            self.test_results['error'] = str(e)
            return self.test_results

    async def _test_job_analysis_service(self):
        """Test job analysis functionality"""
        test_name = "Job Analysis Service"
        logger.info(f"🔍 Testing {test_name}...")
        
        try:
            self.test_results['tests_run'] += 1
            
            # Test single job analysis
            job = self.mock_jobs[0]
            requirements = await self.job_analyzer.analyze_job_posting(job)
            
            # Validate analysis results
            assertions = [
                (len(requirements.technical_skills) > 0, "Technical skills extracted"),
                (len(requirements.programming_languages) > 0, "Programming languages identified"),
                (requirements.seniority_level in ['junior', 'mid', 'senior', 'lead', 'architect'], "Seniority level determined"),
                (len(requirements.job_responsibilities) > 0, "Job responsibilities extracted"),
                (requirements.experience_level in ['junior', 'mid', 'senior', 'architect'], "Experience level categorized")
            ]
            
            passed_assertions = sum(1 for assertion, _ in assertions if assertion)
            
            # Test batch analysis
            batch_results = await self.job_analyzer.analyze_multiple_jobs(self.mock_jobs)
            batch_success = len(batch_results) == len(self.mock_jobs)
            
            if passed_assertions >= 4 and batch_success:
                self.test_results['tests_passed'] += 1
                logger.info(f"✅ {test_name} passed")
                
                self.test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'details': {
                        'single_job_analysis': 'Success',
                        'batch_analysis': f'Processed {len(batch_results)} jobs',
                        'technical_skills_found': len(requirements.technical_skills),
                        'programming_languages_found': len(requirements.programming_languages),
                        'seniority_level': requirements.seniority_level
                    }
                })
            else:
                raise AssertionError(f"Analysis validation failed: {passed_assertions}/5 assertions passed, batch: {batch_success}")
                
        except Exception as e:
            self.test_results['tests_failed'] += 1
            logger.error(f"❌ {test_name} failed: {e}")
            
            self.test_results['test_details'].append({
                'test_name': test_name,
                'status': 'FAILED',
                'error': str(e)
            })

    async def _test_cv_customization_service(self):
        """Test CV customization functionality"""
        test_name = "CV Customization Service"
        logger.info(f"📄 Testing {test_name}...")
        
        try:
            self.test_results['tests_run'] += 1
            
            # Analyze job first
            job = self.mock_jobs[0]
            requirements = await self.job_analyzer.analyze_job_posting(job)
            
            # Generate customized CV
            cv_latex = await self.cv_customizer.create_customized_cv(job, requirements)
            
            # Validate CV content
            cv_validations = [
                (len(cv_latex) > 1000, "CV has substantial content"),
                ('\\documentclass' in cv_latex, "LaTeX document structure present"),
                (job['company'] in cv_latex, "Company name included"),
                (job['title'].lower() in cv_latex.lower() or 'developer' in cv_latex.lower(), "Job relevance maintained"),
                ('\\section' in cv_latex, "Proper LaTeX sections"),
                ('Hongzhi Li' in cv_latex, "User name included")
            ]
            
            passed_validations = sum(1 for validation, _ in cv_validations if validation)
            
            # Test batch CV generation
            analyzed_jobs = await self.job_analyzer.analyze_multiple_jobs(self.mock_jobs[:2])
            batch_cvs = await self.cv_customizer.batch_create_customized_cvs(analyzed_jobs)
            batch_success = len(batch_cvs) == len(analyzed_jobs)
            
            if passed_validations >= 5 and batch_success:
                self.test_results['tests_passed'] += 1
                logger.info(f"✅ {test_name} passed")
                
                self.test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'details': {
                        'cv_length': len(cv_latex),
                        'validations_passed': f"{passed_validations}/6",
                        'batch_generation': f"Generated {len(batch_cvs)} CVs"
                    }
                })
            else:
                raise AssertionError(f"CV validation failed: {passed_validations}/6 validations passed, batch: {batch_success}")
                
        except Exception as e:
            self.test_results['tests_failed'] += 1
            logger.error(f"❌ {test_name} failed: {e}")
            
            self.test_results['test_details'].append({
                'test_name': test_name,
                'status': 'FAILED',
                'error': str(e)
            })

    async def _test_cover_letter_service(self):
        """Test cover letter generation functionality"""
        test_name = "Cover Letter Service"
        logger.info(f"✍️ Testing {test_name}...")
        
        try:
            self.test_results['tests_run'] += 1
            
            # Analyze job first
            job = self.mock_jobs[0]
            requirements = await self.job_analyzer.analyze_job_posting(job)
            
            # Generate cover letter
            cl_latex = await self.cover_letter_service.create_personalized_cover_letter(job, requirements)
            
            # Validate cover letter content
            cl_validations = [
                (len(cl_latex) > 800, "Cover letter has substantial content"),
                ('\\documentclass' in cl_latex, "LaTeX document structure present"),
                (job['company'] in cl_latex, "Company name mentioned"),
                (job['title'] in cl_latex or 'developer' in cl_latex.lower(), "Position referenced"),
                ('Dear' in cl_latex or 'Hiring Manager' in cl_latex, "Professional greeting"),
                ('Sincerely' in cl_latex or 'Best regards' in cl_latex, "Professional closing"),
                ('Hongzhi Li' in cl_latex, "Signature included")
            ]
            
            passed_validations = sum(1 for validation, _ in cl_validations if validation)
            
            # Test batch cover letter generation
            analyzed_jobs = await self.job_analyzer.analyze_multiple_jobs(self.mock_jobs[:2])
            batch_cls = await self.cover_letter_service.batch_create_cover_letters(analyzed_jobs)
            batch_success = len(batch_cls) == len(analyzed_jobs)
            
            if passed_validations >= 6 and batch_success:
                self.test_results['tests_passed'] += 1
                logger.info(f"✅ {test_name} passed")
                
                self.test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'details': {
                        'cover_letter_length': len(cl_latex),
                        'validations_passed': f"{passed_validations}/7",
                        'batch_generation': f"Generated {len(batch_cls)} cover letters"
                    }
                })
            else:
                raise AssertionError(f"Cover letter validation failed: {passed_validations}/7 validations passed, batch: {batch_success}")
                
        except Exception as e:
            self.test_results['tests_failed'] += 1
            logger.error(f"❌ {test_name} failed: {e}")
            
            self.test_results['test_details'].append({
                'test_name': test_name,
                'status': 'FAILED',
                'error': str(e)
            })

    async def _test_document_generation_pipeline(self):
        """Test the complete document generation pipeline"""
        test_name = "Document Generation Pipeline"
        logger.info(f"🔄 Testing {test_name}...")
        
        try:
            self.test_results['tests_run'] += 1
            start_time = datetime.now()
            
            # Test complete pipeline with mock jobs
            analyzed_jobs = await self.job_analyzer.analyze_multiple_jobs(self.mock_jobs)
            
            # Generate documents
            document_results = await self.orchestrator._generate_all_documents(analyzed_jobs)
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            # Validate pipeline results
            pipeline_validations = [
                (len(document_results) > 0, "Documents generated"),
                (all('cv_latex' in result for result in document_results), "All CVs generated"),
                (all('cover_letter_latex' in result for result in document_results), "All cover letters generated"),
                (all(len(result['cv_latex']) > 500 for result in document_results), "CVs have substantial content"),
                (all(len(result['cover_letter_latex']) > 500 for result in document_results), "Cover letters have substantial content"),
                (processing_time < 60, "Processing completed within reasonable time")
            ]
            
            passed_validations = sum(1 for validation, _ in pipeline_validations if validation)
            
            if passed_validations >= 5:
                self.test_results['tests_passed'] += 1
                logger.info(f"✅ {test_name} passed")
                
                self.test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'details': {
                        'documents_generated': len(document_results),
                        'processing_time_seconds': processing_time,
                        'validations_passed': f"{passed_validations}/6"
                    }
                })
                
                # Store performance metrics
                self.test_results['performance_metrics']['document_generation'] = {
                    'jobs_processed': len(analyzed_jobs),
                    'processing_time': processing_time,
                    'jobs_per_second': len(analyzed_jobs) / processing_time
                }
            else:
                raise AssertionError(f"Pipeline validation failed: {passed_validations}/6 validations passed")
                
        except Exception as e:
            self.test_results['tests_failed'] += 1
            logger.error(f"❌ {test_name} failed: {e}")
            
            self.test_results['test_details'].append({
                'test_name': test_name,
                'status': 'FAILED',
                'error': str(e)
            })

    async def _test_job_prioritization(self):
        """Test job prioritization functionality"""
        test_name = "Job Prioritization"
        logger.info(f"🎯 Testing {test_name}...")
        
        try:
            self.test_results['tests_run'] += 1
            
            # Create jobs with different priorities
            high_priority_job = self.mock_jobs[0].copy()  # Spotify - should be high priority
            medium_priority_job = self.mock_jobs[1].copy()  # Klarna - medium priority
            low_priority_job = {
                **self.mock_jobs[2],
                'company': 'Unknown Startup',  # Should be lower priority
                'date_posted': 'Last week'
            }
            
            test_jobs = [low_priority_job, high_priority_job, medium_priority_job]
            
            # Test prioritization
            prioritized_jobs = await self.orchestrator._prioritize_jobs(test_jobs)
            
            # Validate prioritization
            first_job_company = prioritized_jobs[0]['company']
            prioritization_validations = [
                (len(prioritized_jobs) == len(test_jobs), "All jobs returned"),
                ('Spotify' in first_job_company or 'Klarna' in first_job_company, "High-quality company prioritized"),
                (prioritized_jobs[0]['company'] != 'Unknown Startup', "Low-priority job not first")
            ]
            
            passed_validations = sum(1 for validation, _ in prioritization_validations if validation)
            
            if passed_validations >= 2:
                self.test_results['tests_passed'] += 1
                logger.info(f"✅ {test_name} passed")
                
                self.test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'details': {
                        'jobs_prioritized': len(prioritized_jobs),
                        'top_priority_company': prioritized_jobs[0]['company'],
                        'validations_passed': f"{passed_validations}/3"
                    }
                })
            else:
                raise AssertionError(f"Prioritization validation failed: {passed_validations}/3 validations passed")
                
        except Exception as e:
            self.test_results['tests_failed'] += 1
            logger.error(f"❌ {test_name} failed: {e}")
            
            self.test_results['test_details'].append({
                'test_name': test_name,
                'status': 'FAILED',
                'error': str(e)
            })

    async def _test_error_handling(self):
        """Test error handling and graceful degradation"""
        test_name = "Error Handling"
        logger.info(f"🛡️ Testing {test_name}...")
        
        try:
            self.test_results['tests_run'] += 1
            
            # Test with invalid job data
            invalid_job = {
                'title': '',  # Empty title
                'company': '',  # Empty company
                'description': '',  # Empty description
                'source': 'test'
            }
            
            # Test job analysis with invalid data
            try:
                requirements = await self.job_analyzer.analyze_job_posting(invalid_job)
                analysis_handled = requirements is not None
            except Exception:
                analysis_handled = False
            
            # Test CV generation with minimal data
            try:
                if analysis_handled:
                    cv_latex = await self.cv_customizer.create_customized_cv(invalid_job, requirements)
                    cv_generation_handled = cv_latex is not None and len(cv_latex) > 100
                else:
                    cv_generation_handled = False
            except Exception:
                cv_generation_handled = False
            
            # Test cover letter generation with minimal data
            try:
                if analysis_handled:
                    cl_latex = await self.cover_letter_service.create_personalized_cover_letter(invalid_job, requirements)
                    cl_generation_handled = cl_latex is not None and len(cl_latex) > 100
                else:
                    cl_generation_handled = False
            except Exception:
                cl_generation_handled = False
            
            error_handling_validations = [
                (analysis_handled, "Job analysis handles invalid data gracefully"),
                (cv_generation_handled, "CV generation handles invalid data gracefully"),
                (cl_generation_handled, "Cover letter generation handles invalid data gracefully")
            ]
            
            passed_validations = sum(1 for validation, _ in error_handling_validations if validation)
            
            if passed_validations >= 2:
                self.test_results['tests_passed'] += 1
                logger.info(f"✅ {test_name} passed")
                
                self.test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'details': {
                        'analysis_error_handling': analysis_handled,
                        'cv_error_handling': cv_generation_handled,
                        'cl_error_handling': cl_generation_handled,
                        'validations_passed': f"{passed_validations}/3"
                    }
                })
            else:
                raise AssertionError(f"Error handling validation failed: {passed_validations}/3 validations passed")
                
        except Exception as e:
            self.test_results['tests_failed'] += 1
            logger.error(f"❌ {test_name} failed: {e}")
            
            self.test_results['test_details'].append({
                'test_name': test_name,
                'status': 'FAILED',
                'error': str(e)
            })

    async def _test_performance_benchmarks(self):
        """Test performance benchmarks and scalability"""
        test_name = "Performance Benchmarks"
        logger.info(f"⚡ Testing {test_name}...")
        
        try:
            self.test_results['tests_run'] += 1
            start_time = datetime.now()
            
            # Create larger job set for performance testing
            performance_jobs = []
            for i in range(10):  # Test with 10 jobs
                job = self.mock_jobs[i % len(self.mock_jobs)].copy()
                job['title'] = f"{job['title']} - Test {i+1}"
                job['job_id'] = f"perf_test_{i+1}"
                performance_jobs.append(job)
            
            # Test batch processing performance
            analyzed_jobs = await self.job_analyzer.analyze_multiple_jobs(performance_jobs)
            analysis_time = (datetime.now() - start_time).total_seconds()
            
            # Test document generation performance
            doc_start = datetime.now()
            document_results = await self.orchestrator._generate_all_documents(analyzed_jobs)
            document_time = (datetime.now() - doc_start).total_seconds()
            
            total_time = (datetime.now() - start_time).total_seconds()
            
            # Performance validations
            performance_validations = [
                (analysis_time < 30, "Job analysis completed within 30 seconds"),
                (document_time < 60, "Document generation completed within 60 seconds"),
                (total_time < 90, "Total processing completed within 90 seconds"),
                (len(document_results) == len(performance_jobs), "All jobs processed successfully"),
                (total_time / len(performance_jobs) < 10, "Average processing time per job < 10 seconds")
            ]
            
            passed_validations = sum(1 for validation, _ in performance_validations if validation)
            
            if passed_validations >= 4:
                self.test_results['tests_passed'] += 1
                logger.info(f"✅ {test_name} passed")
                
                self.test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'details': {
                        'jobs_processed': len(performance_jobs),
                        'analysis_time_seconds': analysis_time,
                        'document_generation_time_seconds': document_time,
                        'total_time_seconds': total_time,
                        'average_time_per_job': total_time / len(performance_jobs),
                        'validations_passed': f"{passed_validations}/5"
                    }
                })
                
                # Store performance metrics
                self.test_results['performance_metrics']['batch_processing'] = {
                    'jobs_count': len(performance_jobs),
                    'total_time': total_time,
                    'jobs_per_second': len(performance_jobs) / total_time,
                    'analysis_time': analysis_time,
                    'document_generation_time': document_time
                }
            else:
                raise AssertionError(f"Performance validation failed: {passed_validations}/5 validations passed")
                
        except Exception as e:
            self.test_results['tests_failed'] += 1
            logger.error(f"❌ {test_name} failed: {e}")
            
            self.test_results['test_details'].append({
                'test_name': test_name,
                'status': 'FAILED',
                'error': str(e)
            })

    def _generate_test_report(self):
        """Generate comprehensive test report"""
        self.test_results['summary'] = {
            'success_rate': (self.test_results['tests_passed'] / max(self.test_results['tests_run'], 1)) * 100,
            'total_tests': self.test_results['tests_run'],
            'passed_tests': self.test_results['tests_passed'],
            'failed_tests': self.test_results['tests_failed']
        }
        
        # Save test report
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_file, 'w') as f:
                json.dump(self.test_results, f, indent=2)
            logger.info(f"📊 Test report saved to {report_file}")
        except Exception as e:
            logger.error(f"Error saving test report: {e}")
        
        # Log summary
        logger.info("🏁 TEST SUMMARY:")
        logger.info(f"   Total Tests: {self.test_results['tests_run']}")
        logger.info(f"   Passed: {self.test_results['tests_passed']}")
        logger.info(f"   Failed: {self.test_results['tests_failed']}")
        logger.info(f"   Success Rate: {self.test_results['summary']['success_rate']:.1f}%")

async def main():
    """Main test execution function"""
    print("🧪 Real Job Hunter Comprehensive Test Suite")
    print("=" * 50)
    
    tester = RealJobHunterTester()
    results = await tester.run_comprehensive_tests()
    
    print("\n" + "=" * 50)
    print("🏁 TEST RESULTS SUMMARY:")
    print(f"   Tests Run: {results['tests_run']}")
    print(f"   Tests Passed: {results['tests_passed']}")
    print(f"   Tests Failed: {results['tests_failed']}")
    
    if results['tests_run'] > 0:
        success_rate = (results['tests_passed'] / results['tests_run']) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("✅ Test suite PASSED - System ready for production!")
        elif success_rate >= 60:
            print("⚠️ Test suite PARTIALLY PASSED - Some issues need attention")
        else:
            print("❌ Test suite FAILED - Critical issues need resolution")
    
    print("=" * 50)
    
    return results

if __name__ == "__main__":
    asyncio.run(main())