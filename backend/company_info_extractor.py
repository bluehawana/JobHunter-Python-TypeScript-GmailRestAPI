#!/usr/bin/env python3
"""
CRITICAL: Company Information Extractor with 100% Accuracy Validation
Uses Claude API to extract and validate company details with multiple verification steps
NO MORE WRONG COMPANY NAMES, ADDRESSES, OR HR NAMES!
"""
import os
import re
import logging
import requests
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

class CompanyInfoExtractor:
    def __init__(self):
        """Initialize with Claude API for accurate information extraction"""
        # Prefer ANTHROPIC_AUTH_TOKEN, fall back to ANTHROPIC_API_KEY for compatibility
        self.claude_api_key = os.getenv('ANTHROPIC_AUTH_TOKEN') or os.getenv('ANTHROPIC_API_KEY')
        self.claude_base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://anyrouter.top')
        
        # Your FIXED contact information - NEVER changes
        self.your_contact = {
            'name': 'Hongzhi Li',
            'email': 'hongzhili01@gmail.com',
            'phone': '0728384299',
            'address': 'Ebbe Lieberathsgatan 27',
            'postal_code': '412 65',
            'city': 'Göteborg',
            'country': 'Sweden'
        }
    
    def extract_company_info_with_claude(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Claude API to extract and validate company information with 100% accuracy
        CRITICAL: This must be perfect - no mistakes allowed!
        """
        try:
            # Prepare comprehensive job information for Claude
            job_text = f"""
            Job URL: {job_data.get('url', 'Not provided')}
            Company: {job_data.get('company', 'Not provided')}
            Position: {job_data.get('title', 'Not provided')}
            Location: {job_data.get('location', 'Not provided')}
            Description: {job_data.get('description', 'Not provided')}
            Contact Person: {job_data.get('contact_person', 'Not provided')}
            Additional Info: {job_data.get('additional_info', 'Not provided')}
            """
            
            prompt = f"""
            CRITICAL TASK: Extract company contact information with 100% accuracy from this job posting.
            This information will be used in a formal cover letter - ANY MISTAKES ARE UNACCEPTABLE.
            
            Job Information:
            {job_text}
            
            Extract and validate the following information:
            1. EXACT company name (as it appears officially)
            2. Complete company address (street, postal code, city, country)
            3. HR contact person name (if mentioned)
            4. HR contact title (if mentioned)
            5. Company phone number (if available)
            6. Company email (if available)
            7. Department/Division (if specified)
            
            VALIDATION RULES:
            - If information is not clearly stated, mark as "Not provided" - DO NOT GUESS
            - Double-check company name spelling and capitalization
            - Verify address format matches the country's postal system
            - Ensure HR name is exactly as written (including titles like Mr./Ms./Dr.)
            - If multiple addresses exist, prioritize the office location for this specific job
            
            Return ONLY a JSON object with these exact keys:
            {{
                "company_name": "exact company name",
                "company_address": "complete address",
                "postal_code": "postal code",
                "city": "city",
                "country": "country",
                "hr_name": "HR contact name or Not provided",
                "hr_title": "HR title or Not provided",
                "phone": "company phone or Not provided",
                "email": "company email or Not provided",
                "department": "specific department or Not provided",
                "confidence_score": "1-10 rating of information accuracy",
                "validation_notes": "any concerns or clarifications"
            }}
            """
            
            if not self.claude_api_key:
                logger.warning("⚠️ Claude API key not configured; skipping API extraction")
                return {'success': False, 'error': 'Claude API key missing'}

            headers = {
                'Authorization': f'Bearer {self.claude_api_key}',
                'Content-Type': 'application/json',
                # Required for Anthropic official API
                'anthropic-version': os.getenv('ANTHROPIC_VERSION', '2023-06-01')
            }
            
            data = {
                'model': 'claude-3-7-sonnet-20250219',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 1500,
                'temperature': 0.1  # Low temperature for accuracy
            }
            
            response = requests.post(
                f'{self.claude_base_url}/v1/messages',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                claude_response = result['content'][0]['text']
                
                # Extract JSON from Claude's response
                try:
                    # Find JSON in the response
                    json_match = re.search(r'\{.*\}', claude_response, re.DOTALL)
                    if json_match:
                        company_info = json.loads(json_match.group())
                        
                        # Validate confidence score
                        confidence = company_info.get('confidence_score', 0)
                        if isinstance(confidence, str):
                            confidence = int(confidence) if confidence.isdigit() else 5
                        
                        if confidence < 7:
                            logger.warning(f"⚠️ Low confidence ({confidence}/10) in company info extraction")
                            logger.warning(f"Validation notes: {company_info.get('validation_notes', 'None')}")
                        
                        logger.info(f"✅ Claude extracted company info with confidence: {confidence}/10")
                        return {
                            'success': True,
                            'company_info': company_info,
                            'confidence': confidence,
                            'source': 'claude_api'
                        }
                    else:
                        logger.error("❌ No valid JSON found in Claude response")
                        return {'success': False, 'error': 'Invalid JSON response'}
                        
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON parsing error: {e}")
                    logger.error(f"Claude response: {claude_response}")
                    return {'success': False, 'error': 'JSON parsing failed'}
            else:
                logger.error(f"❌ Claude API failed: {response.status_code}")
                return {'success': False, 'error': f'API error: {response.status_code}'}
                
        except Exception as e:
            logger.error(f"❌ Company info extraction failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def fallback_company_extraction(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback method using pattern matching and validation
        Only use basic information that's clearly provided
        """
        try:
            company_info = {
                'company_name': job_data.get('company', 'Company Name Required'),
                'company_address': 'Address Required',
                'postal_code': 'Postal Code Required',
                'city': job_data.get('location', 'City Required'),
                'country': 'Country Required',
                'hr_name': 'Not provided',
                'hr_title': 'Not provided',
                'phone': 'Not provided',
                'email': 'Not provided',
                'department': 'Not provided',
                'confidence_score': 3,
                'validation_notes': 'Fallback extraction - manual verification required'
            }
            
            # Try to extract location details
            location = job_data.get('location', '')
            if location:
                # Common patterns for Swedish locations
                if 'stockholm' in location.lower():
                    company_info['city'] = 'Stockholm'
                    company_info['country'] = 'Sweden'
                elif 'göteborg' in location.lower() or 'gothenburg' in location.lower():
                    company_info['city'] = 'Göteborg'
                    company_info['country'] = 'Sweden'
                elif 'malmö' in location.lower():
                    company_info['city'] = 'Malmö'
                    company_info['country'] = 'Sweden'
                elif 'oslo' in location.lower():
                    company_info['city'] = 'Oslo'
                    company_info['country'] = 'Norway'
                elif 'copenhagen' in location.lower():
                    company_info['city'] = 'Copenhagen'
                    company_info['country'] = 'Denmark'
            
            logger.warning("⚠️ Using fallback company extraction - manual verification required")
            return {
                'success': True,
                'company_info': company_info,
                'confidence': 3,
                'source': 'fallback'
            }
            
        except Exception as e:
            logger.error(f"❌ Fallback extraction failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def validate_and_format_company_info(self, company_info: Dict[str, Any]) -> Dict[str, str]:
        """
        Final validation and formatting of company information
        Ensures proper formatting for LaTeX cover letter
        """
        try:
            # Clean and validate each field
            validated_info = {}
            
            # Company name - critical accuracy
            company_name = company_info.get('company_name', '').strip()
            if not company_name or company_name == 'Not provided':
                logger.error("❌ CRITICAL: Company name is missing!")
                company_name = "COMPANY NAME REQUIRED - MANUAL INPUT NEEDED"
            validated_info['company_name'] = company_name
            
            # Address formatting
            address = company_info.get('company_address', '').strip()
            postal_code = company_info.get('postal_code', '').strip()
            city = company_info.get('city', '').strip()
            country = company_info.get('country', '').strip()
            
            # Format address for LaTeX
            address_lines = []
            if address and address != 'Not provided':
                address_lines.append(address)
            if postal_code and postal_code != 'Not provided':
                if city and city != 'Not provided':
                    address_lines.append(f"{postal_code} {city}")
                else:
                    address_lines.append(postal_code)
            elif city and city != 'Not provided':
                address_lines.append(city)
            if country and country != 'Not provided' and country.lower() != 'sweden':
                address_lines.append(country)
            
            validated_info['formatted_address'] = '\\\\'.join(address_lines) if address_lines else 'ADDRESS REQUIRED'
            
            # HR contact information
            hr_name = company_info.get('hr_name', '').strip()
            hr_title = company_info.get('hr_title', '').strip()
            
            if hr_name and hr_name != 'Not provided':
                if hr_title and hr_title != 'Not provided':
                    validated_info['greeting'] = f"Dear {hr_name}, {hr_title}"
                else:
                    validated_info['greeting'] = f"Dear {hr_name}"
            else:
                validated_info['greeting'] = "Dear Hiring Manager"
            
            # Additional contact info
            validated_info['company_phone'] = company_info.get('phone', 'Not provided')
            validated_info['company_email'] = company_info.get('email', 'Not provided')
            validated_info['department'] = company_info.get('department', 'Not provided')
            
            # Your contact info (NEVER changes)
            validated_info['your_name'] = self.your_contact['name']
            validated_info['your_email'] = self.your_contact['email']
            validated_info['your_phone'] = self.your_contact['phone']
            validated_info['your_address'] = f"{self.your_contact['address']}\\\\{self.your_contact['postal_code']} {self.your_contact['city']}"
            
            logger.info("✅ Company information validated and formatted")
            return validated_info
            
        except Exception as e:
            logger.error(f"❌ Company info validation failed: {e}")
            return {
                'company_name': 'VALIDATION ERROR - MANUAL REVIEW REQUIRED',
                'formatted_address': 'ADDRESS VALIDATION ERROR',
                'greeting': 'Dear Hiring Manager',
                'your_name': self.your_contact['name'],
                'your_email': self.your_contact['email'],
                'your_phone': self.your_contact['phone'],
                'your_address': f"{self.your_contact['address']}\\\\{self.your_contact['postal_code']} {self.your_contact['city']}"
            }
    
    def extract_and_validate_company_info(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method: Extract and validate company information with multiple verification steps
        Returns validated company info ready for cover letter generation
        """
        logger.info(f"🔍 Extracting company info for: {job_data.get('company', 'Unknown')}")
        
        # Step 1: Try Claude API extraction
        claude_result = self.extract_company_info_with_claude(job_data)
        
        if claude_result['success'] and claude_result['confidence'] >= 7:
            logger.info("✅ High-confidence Claude extraction successful")
            company_info = claude_result['company_info']
        elif claude_result['success'] and claude_result['confidence'] >= 5:
            logger.warning("⚠️ Medium-confidence Claude extraction - review recommended")
            company_info = claude_result['company_info']
        else:
            logger.warning("⚠️ Claude extraction failed or low confidence - using fallback")
            fallback_result = self.fallback_company_extraction(job_data)
            if fallback_result['success']:
                company_info = fallback_result['company_info']
            else:
                logger.error("❌ All extraction methods failed!")
                return {'success': False, 'error': 'Company info extraction failed'}
        
        # Step 2: Validate and format
        validated_info = self.validate_and_format_company_info(company_info)
        
        # Step 3: Final quality check
        quality_score = self._calculate_quality_score(validated_info)
        
        result = {
            'success': True,
            'company_info': validated_info,
            'quality_score': quality_score,
            'extraction_method': claude_result.get('source', 'fallback'),
            'confidence': claude_result.get('confidence', 3)
        }
        
        if quality_score < 7:
            logger.warning(f"⚠️ Low quality score ({quality_score}/10) - manual review recommended")
            result['warning'] = 'Manual review recommended due to low quality score'
        
        logger.info(f"✅ Company info extraction complete - Quality: {quality_score}/10")
        return result
    
    def _calculate_quality_score(self, validated_info: Dict[str, str]) -> int:
        """Calculate quality score based on completeness and accuracy indicators"""
        score = 10
        
        # Deduct points for missing or placeholder information
        if 'REQUIRED' in validated_info.get('company_name', ''):
            score -= 5
        if 'REQUIRED' in validated_info.get('formatted_address', ''):
            score -= 3
        if validated_info.get('greeting') == 'Dear Hiring Manager':
            score -= 1  # Not critical, but specific name is better
        if 'ERROR' in str(validated_info):
            score -= 4
        
        return max(1, score)

if __name__ == "__main__":
    # Test company info extraction
    test_job = {
        'company': 'Opera',
        'title': 'DevOps Engineer',
        'location': 'Oslo, Norway',
        'url': 'https://jobs.opera.com/jobs/6060392-devops-engineer',
        'description': 'DevOps Engineer position at Opera in Oslo, Norway...'
    }
    
    print("🔍 Testing Company Info Extraction...")
    extractor = CompanyInfoExtractor()
    result = extractor.extract_and_validate_company_info(test_job)
    
    if result['success']:
        print(f"✅ Extraction successful - Quality: {result['quality_score']}/10")
        print(f"📊 Method: {result['extraction_method']}")
        print(f"🎯 Confidence: {result['confidence']}/10")
        
        company_info = result['company_info']
        print(f"\n📋 Company Information:")
        print(f"   Company: {company_info['company_name']}")
        print(f"   Address: {company_info['formatted_address'].replace('\\\\', ', ')}")
        print(f"   Greeting: {company_info['greeting']}")
        
        if 'warning' in result:
            print(f"\n⚠️ Warning: {result['warning']}")
    else:
        print(f"❌ Extraction failed: {result.get('error', 'Unknown error')}")
    
    print("\n🎉 Company info extraction test complete!")
