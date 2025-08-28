#!/usr/bin/env python3
"""
Company Information Extractor
Extracts company details from job posting URLs for dynamic cover letter generation
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CompanyInfoExtractor:
    """Extracts company information from job posting URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_company_info(self, job_url: str) -> Dict[str, str]:
        """Extract company information from job posting URL"""
        try:
            # Determine the job board and use appropriate extraction method
            domain = urlparse(job_url).netloc.lower()
            
            if 'linkedin' in domain:
                return self._extract_linkedin_info(job_url)
            elif 'glassdoor' in domain:
                return self._extract_glassdoor_info(job_url)
            elif 'indeed' in domain:
                return self._extract_indeed_info(job_url)
            elif 'thelocal' in domain:
                return self._extract_thelocal_info(job_url)
            else:
                return self._extract_generic_info(job_url)
                
        except Exception as e:
            logger.error(f"Failed to extract company info from {job_url}: {e}")
            return self._get_fallback_company_info()
    
    def _extract_linkedin_info(self, url: str) -> Dict[str, str]:
        """Extract company info from LinkedIn job posting"""
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # LinkedIn specific selectors
        company_name = self._find_text(soup, [
            '.jobs-unified-top-card__company-name',
            '.topcard__org-name-link',
            '.job-details-jobs-unified-top-card__company-name'
        ])
        
        company_location = self._find_text(soup, [
            '.jobs-unified-top-card__bullet',
            '.topcard__flavor--bullet',
            '.job-details-jobs-unified-top-card__primary-description'
        ])
        
        # Try to get more detailed company info
        company_page_link = soup.find('a', class_='jobs-unified-top-card__company-name')
        company_description = ""
        if company_page_link and company_page_link.get('href'):
            company_description = self._get_company_description(company_page_link['href'])
        
        return {
            'company_name': self._clean_company_name(company_name),
            'company_address': self._format_address(company_location),
            'company_description': company_description,
            'greeting': f"Dear {company_name} Hiring Team,"
        }
    
    def _extract_glassdoor_info(self, url: str) -> Dict[str, str]:
        """Extract company info from Glassdoor job posting"""
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        company_name = self._find_text(soup, [
            '[data-test="employer-name"]',
            '.employerName',
            '.employer'
        ])
        
        company_location = self._find_text(soup, [
            '[data-test="job-location"]',
            '.location',
            '.jobLocation'
        ])
        
        return {
            'company_name': self._clean_company_name(company_name),
            'company_address': self._format_address(company_location),
            'company_description': "",
            'greeting': f"Dear {company_name} Hiring Manager,"
        }
    
    def _extract_indeed_info(self, url: str) -> Dict[str, str]:
        """Extract company info from Indeed job posting"""
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        company_name = self._find_text(soup, [
            '[data-testid="inlineHeader-companyName"]',
            '.icl-u-lg-mr--sm',
            '.company'
        ])
        
        company_location = self._find_text(soup, [
            '[data-testid="job-location"]',
            '.icl-u-colorForeground--secondary',
            '.location'
        ])
        
        return {
            'company_name': self._clean_company_name(company_name),
            'company_address': self._format_address(company_location),
            'company_description': "",
            'greeting': f"Dear {company_name} Hiring Manager,"
        }
    
    def _extract_thelocal_info(self, url: str) -> Dict[str, str]:
        """Extract company info from The Local job posting"""
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        company_name = self._find_text(soup, [
            '.company-name',
            '.employer-name',
            'h2.company'
        ])
        
        company_location = self._find_text(soup, [
            '.job-location',
            '.location',
            '.workplace-location'
        ])
        
        return {
            'company_name': self._clean_company_name(company_name),
            'company_address': self._format_address(company_location),
            'company_description': "",
            'greeting': f"Dear {company_name} Hiring Manager,"
        }
    
    def _extract_generic_info(self, url: str) -> Dict[str, str]:
        """Generic extraction for unknown job boards"""
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try common patterns for company name
        company_name = self._find_text(soup, [
            '[data-testid*="company"]',
            '[class*="company"]',
            '[id*="company"]',
            'h1', 'h2', 'h3'
        ])
        
        # Try common patterns for location
        company_location = self._find_text(soup, [
            '[data-testid*="location"]',
            '[class*="location"]',
            '[id*="location"]'
        ])
        
        return {
            'company_name': self._clean_company_name(company_name),
            'company_address': self._format_address(company_location),
            'company_description': "",
            'greeting': f"Dear Hiring Manager,"
        }
    
    def _find_text(self, soup: BeautifulSoup, selectors: list) -> str:
        """Find text using multiple CSS selectors"""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text:
                    return text
        return ""
    
    def _clean_company_name(self, company_name: str) -> str:
        """Clean and standardize company name"""
        if not company_name:
            return "Technology Company"
        
        # Remove common suffixes and prefixes
        company_name = re.sub(r'\s*(AB|Inc|LLC|Ltd|Corporation|Corp|Group|Company)\.?\s*$', '', company_name, flags=re.IGNORECASE)
        company_name = re.sub(r'^\s*(The)\s+', '', company_name, flags=re.IGNORECASE)
        
        return company_name.strip()
    
    def _format_address(self, location: str) -> str:
        """Format company address for cover letter"""
        if not location:
            return "Sweden"
        
        # Clean and format location
        location = re.sub(r'\s*,\s*', '\\\\\\\\', location)
        if 'sweden' not in location.lower():
            location += "\\\\\\\\Sweden"
        
        return location
    
    def _get_company_description(self, company_url: str) -> str:
        """Get brief company description from company page"""
        try:
            response = self.session.get(company_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for company description
            description_element = soup.find('meta', attrs={'name': 'description'})
            if description_element:
                return description_element.get('content', '')[:200] + "..."
            
        except Exception as e:
            logger.error(f"Failed to get company description: {e}")
        
        return ""
    
    def _get_fallback_company_info(self) -> Dict[str, str]:
        """Return fallback company information when extraction fails"""
        return {
            'company_name': 'Technology Company',
            'company_address': 'Sweden',
            'company_description': '',
            'greeting': 'Dear Hiring Manager,'
        }

# Global instance for easy access
company_extractor = CompanyInfoExtractor()

def extract_company_info_from_url(job_url: str) -> Dict[str, str]:
    """Main function to extract company information from job URL"""
    return company_extractor.extract_company_info(job_url)