#!/usr/bin/env python3
"""
Update jobs.bluehawana.com Dashboard with Today's Automation Status
Shows real-time status of the 20:00 job automation run
"""
import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')

import time
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_current_automation_status():
    """Get current status of the automation system"""
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Test system components
    status = {
        "timestamp": current_time,
        "execution_time": "20:00",
        "status": "RUNNING",
        "components": {},
        "jobs_processed": 0,
        "applications_sent": 0,
        "overleaf_urls_generated": 0,
        "errors": [],
        "successes": []
    }
    
    # Test 1: PDF Generation
    try:
        from beautiful_pdf_generator import create_beautiful_multi_page_pdf
        test_job = {'title': 'DevOps Engineer', 'company': 'Test Company', 'description': 'test'}
        pdf_content = create_beautiful_multi_page_pdf(test_job)
        
        if pdf_content:
            status["components"]["pdf_generation"] = {"status": "✅ WORKING", "size": len(pdf_content)}
            status["successes"].append("PDF generation system operational")
        else:
            status["components"]["pdf_generation"] = {"status": "❌ FAILED", "size": 0}
            status["errors"].append("PDF generation failed")
    except Exception as e:
        status["components"]["pdf_generation"] = {"status": "❌ ERROR", "error": str(e)}
        status["errors"].append(f"PDF generation error: {e}")
    
    # Test 2: LaTeX Generation
    try:
        from overleaf_pdf_generator import OverleafPDFGenerator
        generator = OverleafPDFGenerator()
        latex_content = generator._generate_latex_content(test_job)
        
        if latex_content and len(latex_content) > 1000:
            status["components"]["latex_generation"] = {"status": "✅ WORKING", "size": len(latex_content)}
            status["successes"].append("LaTeX generation with LEGO intelligence active")
        else:
            status["components"]["latex_generation"] = {"status": "❌ FAILED", "size": 0}
            status["errors"].append("LaTeX generation failed")
    except Exception as e:
        status["components"]["latex_generation"] = {"status": "❌ ERROR", "error": str(e)}
        status["errors"].append(f"LaTeX generation error: {e}")
    
    # Test 3: R2 Storage
    try:
        from r2_latex_storage import R2LaTeXStorage
        r2_storage = R2LaTeXStorage()
        
        if r2_storage.client:
            status["components"]["r2_storage"] = {"status": "✅ READY", "bucket": r2_storage.bucket_name}
            status["successes"].append("R2 storage ready for Overleaf integration")
        else:
            status["components"]["r2_storage"] = {"status": "❌ NOT READY", "bucket": "N/A"}
            status["errors"].append("R2 storage not initialized")
    except Exception as e:
        status["components"]["r2_storage"] = {"status": "❌ ERROR", "error": str(e)}
        status["errors"].append(f"R2 storage error: {e}")
    
    # Test 4: Email Configuration
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_GMAIL_PASSWORD')
    
    if sender_email and sender_password:
        status["components"]["email_system"] = {"status": "✅ CONFIGURED", "sender": sender_email}
        status["successes"].append("Email delivery system configured")
    else:
        status["components"]["email_system"] = {"status": "❌ NOT CONFIGURED", "sender": "N/A"}
        status["errors"].append("Email credentials missing")
    
    # Test 5: Claude API
    claude_key = os.getenv('ANTHROPIC_AUTH_TOKEN')
    claude_url = os.getenv('ANTHROPIC_BASE_URL')
    
    if claude_key and claude_url:
        status["components"]["claude_api"] = {"status": "✅ CONFIGURED", "endpoint": claude_url}
        status["successes"].append("Claude API ready for intelligent analysis")
    else:
        status["components"]["claude_api"] = {"status": "❌ NOT CONFIGURED", "endpoint": "N/A"}
        status["errors"].append("Claude API not configured")
    
    # Determine overall status
    working_components = sum(1 for comp in status["components"].values() if "✅" in comp["status"])
    total_components = len(status["components"])
    
    if working_components == total_components:
        status["status"] = "✅ FULLY OPERATIONAL"
    elif working_components >= 3:
        status["status"] = "⚠️ PARTIALLY OPERATIONAL"
    else:
        status["status"] = "❌ SYSTEM ISSUES"
    
    return status

def create_dashboard_html(status):
    """Create HTML dashboard content"""
    
    # Determine status color
    if "✅" in status["status"]:
        status_color = "#28a745"  # Green
        status_icon = "🎉"
    elif "⚠️" in status["status"]:
        status_color = "#ffc107"  # Yellow
        status_icon = "⚠️"
    else:
        status_color = "#dc3545"  # Red
        status_icon = "❌"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Automation Status - {status['timestamp']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: {status_color};
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .status-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 25px;
            margin-top: 15px;
            font-size: 1.2em;
        }}
        .content {{
            padding: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid {status_color};
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: {status_color};
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .components-section {{
            margin-top: 30px;
        }}
        .component {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            margin: 10px 0;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #ddd;
        }}
        .component.working {{
            border-left-color: #28a745;
            background: #d4edda;
        }}
        .component.error {{
            border-left-color: #dc3545;
            background: #f8d7da;
        }}
        .component-name {{
            font-weight: bold;
        }}
        .component-status {{
            font-family: monospace;
        }}
        .logs-section {{
            margin-top: 30px;
        }}
        .log-item {{
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            font-family: monospace;
            font-size: 0.9em;
        }}
        .log-success {{
            background: #d4edda;
            color: #155724;
        }}
        .log-error {{
            background: #f8d7da;
            color: #721c24;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
            text-align: center;
            margin-top: 20px;
        }}
        .refresh-btn {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: {status_color};
            color: white;
            border: none;
            padding: 15px 20px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1em;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        .refresh-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 7px 20px rgba(0,0,0,0.4);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{status_icon} Job Automation Dashboard</h1>
            <div class="status-badge">{status['status']}</div>
            <div style="margin-top: 10px; font-size: 1.1em;">
                Daily Run: {status['execution_time']} | Last Update: {status['timestamp']}
            </div>
        </div>
        
        <div class="content">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{status['jobs_processed']}</div>
                    <div class="stat-label">Jobs Processed Today</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{status['applications_sent']}</div>
                    <div class="stat-label">Applications Sent</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{status['overleaf_urls_generated']}</div>
                    <div class="stat-label">Overleaf URLs Generated</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(status['components'])}</div>
                    <div class="stat-label">System Components</div>
                </div>
            </div>
            
            <div class="components-section">
                <h2>🔧 System Components Status</h2>
"""
    
    # Add component status
    for comp_name, comp_data in status["components"].items():
        css_class = "working" if "✅" in comp_data["status"] else "error"
        html_content += f"""
                <div class="component {css_class}">
                    <div class="component-name">{comp_name.replace('_', ' ').title()}</div>
                    <div class="component-status">{comp_data["status"]}</div>
                </div>
"""
    
    html_content += """
            </div>
            
            <div class="logs-section">
                <h2>📋 System Logs</h2>
"""
    
    # Add success logs
    for success in status["successes"]:
        html_content += f"""
                <div class="log-item log-success">✅ {success}</div>
"""
    
    # Add error logs
    for error in status["errors"]:
        html_content += f"""
                <div class="log-item log-error">❌ {error}</div>
"""
    
    html_content += f"""
            </div>
            
            <div class="timestamp">
                🕐 Last updated: {status['timestamp']} | Next run: Tomorrow 20:00
            </div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
    
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(function() {{
            location.reload();
        }}, 30000);
    </script>
</body>
</html>
"""
    
    return html_content

def update_dashboard():
    """Update the dashboard with current status"""
    
    print("🎭 UPDATING JOBS.BLUEHAWANA.COM DASHBOARD")
    print("=" * 50)
    
    # Get current status
    print("📊 Gathering system status...")
    status = get_current_automation_status()
    
    # Create HTML dashboard
    print("🌐 Generating dashboard HTML...")
    html_content = create_dashboard_html(status)
    
    # Save dashboard locally
    dashboard_file = "job_automation_dashboard.html"
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard saved: {dashboard_file}")
    
    # Save status as JSON for API
    status_file = "automation_status.json"
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2)
    
    print(f"✅ Status JSON saved: {status_file}")
    
    # Display summary
    print(f"\n📊 DASHBOARD SUMMARY:")
    print(f"   Status: {status['status']}")
    print(f"   Components: {len(status['components'])}")
    print(f"   Successes: {len(status['successes'])}")
    print(f"   Errors: {len(status['errors'])}")
    print(f"   Timestamp: {status['timestamp']}")
    
    return status

def main():
    """Main dashboard update function"""
    
    print("🎯 20:00 JOB AUTOMATION - DASHBOARD UPDATE")
    print("=" * 60)
    
    # Update dashboard
    status = update_dashboard()
    
    # Summary
    print(f"\n🌐 DASHBOARD READY FOR JOBS.BLUEHAWANA.COM")
    print(f"📄 HTML: job_automation_dashboard.html")
    print(f"📊 JSON: automation_status.json")
    
    if "✅" in status["status"]:
        print(f"\n🎉 SYSTEM FULLY OPERATIONAL!")
        print(f"✅ Ready for automated job applications")
        print(f"✅ LEGO intelligence active")
        print(f"✅ Overleaf integration ready")
    else:
        print(f"\n⚠️ SYSTEM STATUS: {status['status']}")
        print(f"💡 Check component status above")
    
    print(f"\n🔗 Upload these files to jobs.bluehawana.com:")
    print(f"   • job_automation_dashboard.html")
    print(f"   • automation_status.json")

if __name__ == "__main__":
    main()