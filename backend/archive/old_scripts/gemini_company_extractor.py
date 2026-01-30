#!/usr/bin/env python3
"""
Company Information Extractor using Google Gemini API
"""
import os
import re
import logging
import requests
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)


class GeminiCompanyExtractor:
    def __init__(self):
        """Initialize with Gemini API"""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.base_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent'

        self.your_contact = {
            'name': 'Hongzhi Li',
            'email': 'hongzhili01@gmail.com',
            'phone': '0728384299',
            'address': 'Ebbe Lieberathsgatan 27',
            'postal_code': '412 65',
            'city': 'Göteborg',
            'country': 'Sweden'
        }

    def extract_company_info_with_gemini(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini API to extract company information"""
        try:
            job_text = f"""
            Job URL: {job_data.get('url', 'Not provided')}
            Company: {job_data.get('company', 'Not provided')}
            Position: {job_data.get('title', 'Not provided')}
            Location: {job_data.get('location', 'Not provided')}
            Description: {job_data.get('description', 'Not provided')}
            """

            prompt = f"""
            Extract company contact information from this job posting for a formal cover letter.
            
            Job Information:
            {job_text}
            
            Extract:
            1. Exact company name
            2. Complete company address (street, postal code, city, country)
            3. HR contact person name (if mentioned)
            4. HR contact title (if mentioned)
            
            IMPORTANT: If information is not clearly stated, mark as "Not provided" - DO NOT GUESS.
            
            Return ONLY a JSON object:
            {{
                "company_name": "exact company name",
                "company_address": "complete address",
                "postal_code": "postal code",
                "city": "city",
                "country": "country",
                "hr_name": "HR contact name or Not provided",
                "hr_title": "HR title or Not provided",
                "confidence_score": "1-10 rating"
            }}
            """

            if not self.api_key:
                logger.warning("⚠️ Gemini API key not configured")
                return {'success': False, 'error': 'Gemini API key missing'}

            headers = {'Content-Type': 'application/json'}

            data = {
                'contents': [{
                    'parts': [{'text': prompt}]
                }],
                'generationConfig': {
                    'temperature': 0.1,
                    'maxOutputTokens': 1500
                }
            }

            response = requests.post(
                f'{self.base_url}?key={self.api_key}',
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                gemini_response = result['candidates'][0]['content']['parts'][0]['text']

                # Extract JSON from response
                json_match = re.search(r'\{.*\}', gemini_response, re.DOTALL)
                if json_match:
                    company_info = json.loads(json_match.group())
                    confidence = int(company_info.get('confidence_score', 5))

                    logger.info(
                        f"✅ Gemini extracted company info with confidence: {confidence}/10")
                    return {
                        'success': True,
                        'company_info': company_info,
                        'confidence': confidence,
                        'source': 'gemini_api'
                    }
                else:
                    logger.error("❌ No valid JSON in Gemini response")
                    return {'success': False, 'error': 'Invalid JSON response'}
            else:
                logger.error(f"❌ Gemini API failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return {'success': False, 'error': f'API error: {response.status_code}'}

        except Exception as e:
            logger.error(f"❌ Gemini extraction failed: {e}")
            return {'success': False, 'error': str(e)}

    def fallback_extraction(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback method"""
        company_info = {
            'company_name': job_data.get('company', 'Company Name Required'),
            'company_address': 'Address Required',
            'postal_code': 'Postal Code Required',
            'city': job_data.get('location', 'City Required'),
            'country': 'Country Required',
            'hr_name': 'Not provided',
            'hr_title': 'Not provided',
            'confidence_score': 3
        }

        location = job_data.get('location', '')
        if 'gothenburg' in location.lower() or 'göteborg' in location.lower():
            company_info['city'] = 'Göteborg'
            company_info['country'] = 'Sweden'
        elif 'stockholm' in location.lower():
            company_info['city'] = 'Stockholm'
            company_info['country'] = 'Sweden'

        return {
            'success': True,
            'company_info': company_info,
            'confidence': 3,
            'source': 'fallback'
        }

    def extract_and_validate(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main extraction method"""
        logger.info(
            f"🔍 Extracting company info for: {job_data.get('company', 'Unknown')}")

        # Try Gemini first
        gemini_result = self.extract_company_info_with_gemini(job_data)

        if gemini_result['success'] and gemini_result['confidence'] >= 5:
            company_info = gemini_result['company_info']
        else:
            logger.warning("⚠️ Using fallback extraction")
            fallback_result = self.fallback_extraction(job_data)
            company_info = fallback_result['company_info']

        # Format for LaTeX
        validated_info = self._format_for_latex(company_info)

        return {
            'success': True,
            'company_info': validated_info,
            'quality_score': self._calculate_quality(validated_info),
            'extraction_method': gemini_result.get('source', 'fallback')
        }

    def _format_for_latex(self, company_info: Dict[str, Any]) -> Dict[str, str]:
        """Format company info for LaTeX cover letter"""
        validated = {}

        validated['company_name'] = company_info.get(
            'company_name', 'COMPANY NAME REQUIRED').strip()

        # Address formatting
        address = company_info.get('company_address', '').strip()
        postal_code = company_info.get('postal_code', '').strip()
        city = company_info.get('city', '').strip()
        country = company_info.get('country', '').strip()

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

        validated['formatted_address'] = '\\\\'.join(
            address_lines) if address_lines else 'ADDRESS REQUIRED'

        # Greeting
        hr_name = company_info.get('hr_name', '').strip()
        hr_title = company_info.get('hr_title', '').strip()

        if hr_name and hr_name != 'Not provided':
            if hr_title and hr_title != 'Not provided':
                validated['greeting'] = f"Dear {hr_name}, {hr_title}"
            else:
                validated['greeting'] = f"Dear {hr_name}"
        else:
            validated['greeting'] = "Dear Hiring Manager"

        return validated

    def _calculate_quality(self, validated_info: Dict[str, str]) -> int:
        """Calculate quality score"""
        score = 10
        if 'REQUIRED' in validated_info.get('company_name', ''):
            score -= 5
        if 'REQUIRED' in validated_info.get('formatted_address', ''):
            score -= 3
        if validated_info.get('greeting') == 'Dear Hiring Manager':
            score -= 1
        return max(1, score)


if __name__ == "__main__":
    test_job = {
        'company': 'Kollmorgen',
        'title': 'Junior Software Engineer - Operation & Visualization',
        'location': 'Gothenburg, Sweden',
        'url': 'https://career-agv.kollmorgen.com/jobs/5973951',
        'description': 'Visualization software for AGV operations'
    }

    print("🔍 Testing Gemini Company Info Extraction...")
    extractor = GeminiCompanyExtractor()
    result = extractor.extract_and_validate(test_job)

    if result['success']:
        print(f"✅ Success - Quality: {result['quality_score']}/10")
        print(f"📊 Method: {result['extraction_method']}")
        info = result['company_info']
        print(f"\n📋 Company: {info['company_name']}")
        print(
            f"   Address: {info['formatted_address'].replace(chr(92)+chr(92), ', ')}")
        print(f"   Greeting: {info['greeting']}")
    else:
        print(f"❌ Failed: {result.get('error')}")
