import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime, date, timedelta
import re
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import json

from app.services.supabase_service import supabase_service

logger = logging.getLogger(__name__)

class JobLinkFetcher:
    """Service to fetch job information from job posting URLs and save to database"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_and_save_jobs(self, job_urls: List[str]) -> List[Dict[str, Any]]:
        """Fetch job information from URLs and save to database"""
        results = []
        
        async with self:
            for url in job_urls:
                try:
                    logger.info(f"Fetching job from: {url}")
                    job_data = await self.fetch_job_from_url(url)
                    
                    if job_data:
                        # Save to database
                        saved_job = await supabase_service.create_job_application(job_data)
                        results.append(saved_job)
                        logger.info(f"Successfully saved job: {job_data.get('job_title')} at {job_data.get('company_name')}")
                    else:
                        logger.warning(f"Could not extract job data from: {url}")
                        
                except Exception as e:
                    logger.error(f"Error processing {url}: {e}")
                    continue
                    
                # Add delay to be respectful to servers
                await asyncio.sleep(2)
        
        return results

    async def fetch_job_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch job information from a single URL"""
        try:
            async with self.session.get(url, timeout=30) as response:
                if response.status != 200:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Determine the job site and use appropriate parser
                domain = urlparse(url).netloc.lower()
                
                if 'linkedin.com' in domain:
                    return await self._parse_linkedin_job(soup, url)
                elif 'indeed.com' in domain:
                    return await self._parse_indeed_job(soup, url)
                elif 'arbetsformedlingen.se' in domain:
                    return await self._parse_arbetsformedlingen_job(soup, url)
                elif 'thelocal.se' in domain:
                    return await self._parse_thelocal_job(soup, url)
                else:
                    # Generic parser for other sites
                    return await self._parse_generic_job(soup, url)
                    
        except Exception as e:
            logger.error(f"Error fetching job from {url}: {e}")
            return None

    async def _parse_linkedin_job(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Parse LinkedIn job posting"""
        try:
            job_data = {
                'application_link': url,
                'application_status': 'found',
                'work_type': 'unknown'
            }
            
            # Job title
            title_selectors = [
                'h1.t-24.t-bold.inline',
                'h1[data-automation-id="jobPostingHeader"]',
                '.jobs-unified-top-card__job-title h1',
                'h1.job-title'
            ]
            job_data['job_title'] = self._extract_text_by_selectors(soup, title_selectors)
            
            # Company name
            company_selectors = [
                '.jobs-unified-top-card__company-name a',
                '.jobs-unified-top-card__company-name',
                '[data-automation-id="jobPostingCompanyLink"]',
                '.job-company-name'
            ]
            job_data['company_name'] = self._extract_text_by_selectors(soup, company_selectors)
            
            # Location
            location_selectors = [
                '.jobs-unified-top-card__bullet',
                '.jobs-unified-top-card__location',
                '[data-automation-id="jobPostingLocation"]',
                '.job-location'
            ]
            job_data['location'] = self._extract_text_by_selectors(soup, location_selectors)
            
            # Job description
            desc_selectors = [
                '.jobs-description__content .jobs-description-content__text',
                '.jobs-box__html-content',
                '[data-automation-id="jobPostingDescription"]',
                '.job-description'
            ]
            job_data['job_description'] = self._extract_text_by_selectors(soup, desc_selectors, max_length=2000)
            
            # Work type (remote/hybrid/onsite)
            description_text = job_data.get('job_description', '').lower()
            location_text = job_data.get('location', '').lower()
            
            if 'remote' in description_text or 'remote' in location_text:
                job_data['work_type'] = 'remote'
            elif 'hybrid' in description_text or 'hybrid' in location_text:
                job_data['work_type'] = 'hybrid'
            else:
                job_data['work_type'] = 'onsite'
            
            # Try to extract posted date
            posted_selectors = [
                '.jobs-unified-top-card__posted-date',
                '.job-posted-date'
            ]
            posted_text = self._extract_text_by_selectors(soup, posted_selectors)
            job_data['published_date'] = self._parse_posted_date(posted_text)
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing LinkedIn job: {e}")
            return None

    async def _parse_indeed_job(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Parse Indeed job posting"""
        try:
            job_data = {
                'application_link': url,
                'application_status': 'found',
                'work_type': 'unknown'
            }
            
            # Job title
            title_selectors = [
                '[data-testid="jobsearch-JobInfoHeader-title"] h1',
                '.jobsearch-JobInfoHeader-title',
                'h1[data-automation-id="jobTitle"]',
                '.jobTitle h1'
            ]
            job_data['job_title'] = self._extract_text_by_selectors(soup, title_selectors)
            
            # Company name
            company_selectors = [
                '[data-testid="inlineHeader-companyName"] a',
                '[data-testid="inlineHeader-companyName"]',
                '.jobsearch-InlineCompanyRating .jobTitle',
                '.companyName'
            ]
            job_data['company_name'] = self._extract_text_by_selectors(soup, company_selectors)
            
            # Location
            location_selectors = [
                '[data-testid="job-location"]', 
                '.jobsearch-JobInfoHeader-subtitle div',
                '.jobLocation'
            ]
            job_data['location'] = self._extract_text_by_selectors(soup, location_selectors)
            
            # Job description
            desc_selectors = [
                '#jobDescriptionText',
                '.jobsearch-jobDescriptionText',
                '[data-testid="jobDescription"]',
                '.job-description'
            ]
            job_data['job_description'] = self._extract_text_by_selectors(soup, desc_selectors, max_length=2000)
            
            # Work type
            description_text = job_data.get('job_description', '').lower()
            location_text = job_data.get('location', '').lower()
            
            if 'remote' in description_text or 'remote' in location_text:
                job_data['work_type'] = 'remote'
            elif 'hybrid' in description_text or 'hybrid' in location_text:
                job_data['work_type'] = 'hybrid'
            else:
                job_data['work_type'] = 'onsite'
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing Indeed job: {e}")
            return None

    async def _parse_arbetsformedlingen_job(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Parse Arbetsförmedlingen job posting"""
        try:
            job_data = {
                'application_link': url,
                'application_status': 'found',
                'work_type': 'unknown'
            }
            
            # Job title
            title_selectors = [
                'h1.ad-title',
                '.job-ad-title h1',
                'h1'
            ]
            job_data['job_title'] = self._extract_text_by_selectors(soup, title_selectors)
            
            # Company name
            company_selectors = [
                '.employer-name',
                '.company-name',
                '[data-testid="company-name"]'
            ]
            job_data['company_name'] = self._extract_text_by_selectors(soup, company_selectors)
            
            # Location
            location_selectors = [
                '.workplace-address',
                '.job-location',
                '[data-testid="workplace-address"]'
            ]
            job_data['location'] = self._extract_text_by_selectors(soup, location_selectors)
            
            # Job description
            desc_selectors = [
                '.ad-description',
                '.job-description',
                '.description-text'
            ]
            job_data['job_description'] = self._extract_text_by_selectors(soup, desc_selectors, max_length=2000)
            
            # Swedish jobs are typically onsite unless stated otherwise
            description_text = job_data.get('job_description', '').lower()
            if 'distans' in description_text or 'remote' in description_text:
                job_data['work_type'] = 'remote'
            elif 'hybrid' in description_text:
                job_data['work_type'] = 'hybrid'
            else:
                job_data['work_type'] = 'onsite'
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing Arbetsförmedlingen job: {e}")
            return None

    async def _parse_thelocal_job(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Parse The Local Sweden job posting"""
        try:
            job_data = {
                'application_link': url,
                'application_status': 'found',
                'work_type': 'unknown'
            }
            
            # Job title
            title_selectors = [
                'h1.job-title',
                '.job-header h1',
                'h1'
            ]
            job_data['job_title'] = self._extract_text_by_selectors(soup, title_selectors)
            
            # Company name
            company_selectors = [
                '.company-name',
                '.employer-name',
                '.job-company'
            ]
            job_data['company_name'] = self._extract_text_by_selectors(soup, company_selectors)
            
            # Location
            location_selectors = [
                '.job-location',
                '.location',
                '.workplace-location'
            ]
            job_data['location'] = self._extract_text_by_selectors(soup, location_selectors)
            
            # Job description
            desc_selectors = [
                '.job-description',
                '.description',
                '.job-content'
            ]
            job_data['job_description'] = self._extract_text_by_selectors(soup, desc_selectors, max_length=2000)
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing The Local job: {e}")
            return None

    async def _parse_generic_job(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Generic parser for other job sites"""
        try:
            job_data = {
                'application_link': url,
                'application_status': 'found',
                'work_type': 'unknown'
            }
            
            # Try to find job title using common patterns
            title_selectors = [
                'h1',
                '.job-title',
                '.title',
                '[class*="title"]',
                '[class*="job-title"]'
            ]
            job_data['job_title'] = self._extract_text_by_selectors(soup, title_selectors)
            
            # Try to find company name
            company_selectors = [
                '.company',
                '.company-name',
                '.employer',
                '[class*="company"]',
                '[class*="employer"]'
            ]
            job_data['company_name'] = self._extract_text_by_selectors(soup, company_selectors)
            
            # Try to find location
            location_selectors = [
                '.location',
                '.job-location',
                '[class*="location"]'
            ]
            job_data['location'] = self._extract_text_by_selectors(soup, location_selectors)
            
            # Try to find description
            desc_selectors = [
                '.description',
                '.job-description',
                '.content',
                '[class*="description"]',
                '[class*="content"]'
            ]
            job_data['job_description'] = self._extract_text_by_selectors(soup, desc_selectors, max_length=2000)
            
            # If we couldn't find basic info, try extracting from page text
            if not job_data.get('job_title'):
                # Try to get title from page title or h1
                page_title = soup.find('title')
                if page_title:
                    job_data['job_title'] = page_title.get_text().strip()[:100]
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing generic job: {e}")
            return None

    def _extract_text_by_selectors(self, soup: BeautifulSoup, selectors: List[str], max_length: int = 200) -> str:
        """Extract text using multiple CSS selectors"""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text:
                    return text[:max_length] if max_length else text
        return ""

    def _parse_posted_date(self, posted_text: str) -> Optional[date]:
        """Parse posted date from text"""
        if not posted_text:
            return None
            
        posted_text = posted_text.lower().strip()
        
        try:
            # Handle "X days ago", "X hours ago", etc.
            if 'day' in posted_text and 'ago' in posted_text:
                days_match = re.search(r'(\d+)\s*days?\s*ago', posted_text)
                if days_match:
                    days_ago = int(days_match.group(1))
                    return (datetime.now() - timedelta(days=days_ago)).date()
            
            if 'hour' in posted_text and 'ago' in posted_text:
                return datetime.now().date()  # Posted today
            
            if 'today' in posted_text:
                return datetime.now().date()
            
            if 'yesterday' in posted_text:
                return (datetime.now() - timedelta(days=1)).date()
            
            # Try to parse specific dates (this is basic, can be enhanced)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', posted_text)
            if date_match:
                return datetime.strptime(date_match.group(1), '%Y-%m-%d').date()
                
        except Exception as e:
            logger.error(f"Error parsing posted date '{posted_text}': {e}")
        
        return None

# Create singleton instance
job_link_fetcher = JobLinkFetcher()