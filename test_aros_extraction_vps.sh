#!/bin/bash
# Test Aros Kapital extraction on VPS

echo "🧪 Testing Aros Kapital job extraction on VPS..."
echo "================================================"

ssh alphavps "cd /var/www/lego-job-generator/backend && source venv/bin/activate && python3 << 'PYTHON_EOF'
import sys
from app.services.job_url_extractor import JobUrlExtractor

url = 'https://career.computerswedenrecruitment.se/jobs/6602293-fullstackutvecklare-till-aros-kapital'

print('🔗 Testing URL:', url)
print('=' * 60)

extractor = JobUrlExtractor()
result = extractor.extract_job_details(url)

print('\\n📊 EXTRACTION RESULT:')
print('=' * 60)
print(f'Success: {result.get(\"success\")}')

if result.get('job_details'):
    details = result['job_details']
    print(f'✅ Company: {details.get(\"company\")}')
    print(f'✅ Title: {details.get(\"title\")}')
    print(f'✅ Location: {details.get(\"location\")}')
    print(f'✅ Source: {details.get(\"source\")}')
else:
    print(f'❌ Error: {result.get(\"error\")}')

print('=' * 60)
PYTHON_EOF
"
