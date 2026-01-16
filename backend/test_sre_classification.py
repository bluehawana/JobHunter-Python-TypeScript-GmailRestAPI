"""
Test Site Reliability Engineer classification
"""

from cv_templates import CVTemplateManager

manager = CVTemplateManager()

# Test 1: Site Reliability Engineer
sre_jd = """
Site Reliability Engineer

We're looking for a Site Reliability Engineer to ensure system reliability and performance.

Responsibilities:
- Monitor production systems and respond to incidents
- Implement observability and monitoring solutions
- Reduce MTTR and improve system reliability
- Participate in on-call rotation
- Build automation for incident response
- Work with Prometheus, Grafana, and PagerDuty

Requirements:
- Experience with SRE practices
- Strong monitoring and observability skills
- Experience with incident management
- Knowledge of Kubernetes and cloud platforms
"""

result = manager.analyze_job_role(sre_jd)
print("Test 1 - Site Reliability Engineer:")
print(f"  Expected: incident_management_sre")
print(f"  Got: {result}")
print(f"  {'✓ PASS' if result == 'incident_management_sre' else '✗ FAIL'}")
print()

# Test 2: SRE with explicit keywords
sre_jd_2 = """
SRE - Production Support

Join our SRE team to manage production incidents and improve reliability.

Responsibilities:
- On-call support for production systems
- Incident management and resolution
- Monitoring and observability
- Reduce MTTR and improve uptime
- Work with PagerDuty and Opsgenie

Requirements:
- SRE experience
- Incident management skills
- Production support background
"""

result_2 = manager.analyze_job_role(sre_jd_2)
print("Test 2 - SRE with explicit keywords:")
print(f"  Expected: incident_management_sre")
print(f"  Got: {result_2}")
print(f"  {'✓ PASS' if result_2 == 'incident_management_sre' else '✗ FAIL'}")
print()

# Test 3: Check the keywords
print("Current incident_management_sre keywords:")
keywords = manager.ROLE_CATEGORIES['incident_management_sre']['keywords']
print(f"  {keywords}")
print()

# Check if 'sre' and 'site reliability' are in the keywords
has_sre = 'sre' in keywords
has_site_reliability = 'site reliability' in keywords
print(f"  Has 'sre': {has_sre}")
print(f"  Has 'site reliability': {has_site_reliability}")
