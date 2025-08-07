#!/usr/bin/env python3
"""
Heroku JobHunter LEGO System
Automated job hunting with 6 AM weekday scheduling
"""
import os
import sys
import asyncio
import logging
from datetime import datetime, time
from pathlib import Path

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
import json

# Configure logging for Heroku
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import scheduler components after path setup
try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    import pytz
    SCHEDULER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Scheduler not available: {e}")
    SCHEDULER_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title="JobHunter LEGO System",
    description="Automated job hunting with intelligent template customization",
    version="1.0.0"
)

# Simple HTML dashboard without templates

# Statistics storage (in production, use a database)
stats = {
    "total_runs": 0,
    "jobs_fetched": 0,
    "jobs_filtered": 0,
    "resumes_generated": 0,
    "cover_letters_generated": 0,
    "emails_sent": 0,
    "last_run": None,
    "success_rate": 0.0,
    "recent_jobs": []
}

# Initialize scheduler if available
scheduler = None
if SCHEDULER_AVAILABLE:
    scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Stockholm'))

@app.on_event("startup")
async def startup_event():
    """Start the scheduler when app starts"""
    try:
        if SCHEDULER_AVAILABLE and scheduler:
            # Schedule daily job hunting at 6:00 AM Stockholm time, Monday-Friday
            scheduler.add_job(
                run_daily_lego_automation,
                CronTrigger(
                    hour=6,
                    minute=0,
                    day_of_week='mon-fri',
                    timezone=pytz.timezone('Europe/Stockholm')
                ),
                id='daily_job_hunt',
                name='Daily LEGO Job Hunting',
                replace_existing=True
            )
            
            scheduler.start()
            logger.info("🚀 JobHunter LEGO System started with 6 AM weekday scheduling")
            logger.info("📅 Next run: Monday-Friday at 6:00 AM Stockholm time")
        else:
            logger.info("🚀 JobHunter LEGO System started (scheduler disabled)")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown scheduler when app stops"""
    if scheduler:
        scheduler.shutdown()
    logger.info("🛑 JobHunter LEGO System stopped")

def generate_dashboard_html():
    """Generate dashboard HTML without templates"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JobHunter LEGO System - Dashboard</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
                padding: 20px;
            }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ text-align: center; color: white; margin-bottom: 30px; }}
            .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
            .header p {{ font-size: 1.1rem; opacity: 0.9; }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.3s ease;
            }}
            .stat-card:hover {{ transform: translateY(-5px); }}
            .stat-number {{
                font-size: 2.5rem;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 10px;
            }}
            .stat-label {{
                font-size: 1rem;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .controls {{
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }}
            .controls h3 {{ margin-bottom: 20px; color: #333; }}
            .button-group {{ display: flex; gap: 15px; flex-wrap: wrap; }}
            .btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }}
            .btn-primary {{ background: #667eea; color: white; }}
            .btn-primary:hover {{ background: #5a6fd8; }}
            .btn-secondary {{
                background: #f8f9fa;
                color: #333;
                border: 2px solid #dee2e6;
            }}
            .btn-secondary:hover {{ background: #e9ecef; }}
            .status-section {{
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }}
            .status-indicator {{
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
                background: #28a745;
            }}
            .footer {{
                text-align: center;
                color: white;
                opacity: 0.8;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 JobHunter LEGO System</h1>
                <p>Automated Job Hunting with Intelligent Template Customization</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{stats['total_runs']}</div>
                    <div class="stat-label">Total Runs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['jobs_fetched']}</div>
                    <div class="stat-label">Jobs Fetched</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['jobs_filtered']}</div>
                    <div class="stat-label">Jobs Filtered</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['resumes_generated']}</div>
                    <div class="stat-label">Resumes Generated</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['cover_letters_generated']}</div>
                    <div class="stat-label">Cover Letters</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['emails_sent']}</div>
                    <div class="stat-label">Emails Sent</div>
                </div>
            </div>
            
            <div class="status-section">
                <h3>System Status</h3>
                <p>
                    <span class="status-indicator"></span>
                    <strong>Status:</strong> Running
                </p>
                <p><strong>Service:</strong> JobHunter LEGO System</p>
                <p><strong>Schedule:</strong> Monday-Friday at 6:00 AM</p>
                <p><strong>Timezone:</strong> Europe/Stockholm</p>
                <p><strong>Next Run:</strong> {get_next_run_time() or 'Not scheduled'}</p>
                <p><strong>Last Run:</strong> {stats['last_run'] or 'Never'}</p>
                <p><strong>Success Rate:</strong> {stats['success_rate']:.1f}%</p>
            </div>
            
            <div class="controls">
                <h3>Manual Controls</h3>
                <div class="button-group">
                    <button class="btn btn-primary" onclick="runAutomation()">🚀 Run Automation Now</button>
                    <button class="btn btn-secondary" onclick="triggerManual()">⚡ Quick Trigger</button>
                    <button class="btn btn-secondary" onclick="refreshStats()">🔄 Refresh Stats</button>
                    <a href="/health" class="btn btn-secondary">📊 Health Check</a>
                    <a href="/api/status" class="btn btn-secondary">📋 API Status</a>
                </div>
            </div>
            
            <div class="footer">
                <p>Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p>🌐 <a href="https://bluehawana.com" style="color: white;">bluehawana.com</a></p>
            </div>
        </div>
        
        <script>
            async function runAutomation() {{
                const btn = event.target;
                btn.disabled = true;
                btn.textContent = '⏳ Running...';
                
                try {{
                    const response = await fetch('/run-automation', {{ method: 'POST' }});
                    const result = await response.json();
                    
                    if (result.status === 'success') {{
                        alert(`✅ Automation completed!\\n${{result.message}}`);
                    }} else {{
                        alert(`❌ Error: ${{result.message}}`);
                    }}
                }} catch (error) {{
                    alert(`❌ Network error: ${{error.message}}`);
                }}
                
                btn.disabled = false;
                btn.textContent = '🚀 Run Automation Now';
                setTimeout(() => location.reload(), 2000);
            }}
            
            async function triggerManual() {{
                const btn = event.target;
                btn.disabled = true;
                btn.textContent = '⏳ Triggering...';
                
                try {{
                    const response = await fetch('/trigger/manual-run', {{ method: 'POST' }});
                    const result = await response.json();
                    alert(`✅ ${{result.message}}`);
                }} catch (error) {{
                    alert(`❌ Network error: ${{error.message}}`);
                }}
                
                btn.disabled = false;
                btn.textContent = '⚡ Quick Trigger';
            }}
            
            function refreshStats() {{
                location.reload();
            }}
            
            // Auto-refresh every 30 seconds
            setInterval(() => {{
                location.reload();
            }}, 30000);
        </script>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard with statistics"""
    return HTMLResponse(generate_dashboard_html())

@app.get("/api/status")
async def api_status():
    """JSON API endpoint for status"""
    return {
        "status": "running",
        "service": "JobHunter LEGO System",
        "next_scheduled_run": get_next_run_time(),
        "timezone": "Europe/Stockholm",
        "schedule": "Monday-Friday at 6:00 AM",
        "timestamp": datetime.now().isoformat(),
        "stats": stats
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    scheduler_info = {
        "scheduler_available": SCHEDULER_AVAILABLE,
        "scheduler_running": scheduler.running if scheduler else False,
        "jobs_scheduled": len(scheduler.get_jobs()) if scheduler else 0,
    }
    
    return {
        "status": "healthy",
        **scheduler_info,
        "next_run": get_next_run_time(),
        "system_time": datetime.now().isoformat(),
        "stockholm_time": datetime.now(pytz.timezone('Europe/Stockholm')).isoformat() if SCHEDULER_AVAILABLE else "N/A"
    }

@app.post("/trigger/manual-run")
async def manual_trigger(background_tasks: BackgroundTasks):
    """Manual trigger for testing"""
    logger.info("🔧 Manual automation triggered via master orchestrator")
    background_tasks.add_task(run_daily_lego_automation)
    return {
        "status": "triggered",
        "message": "Manual automation started using master orchestrator",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/run-automation")
async def run_automation_sync():
    """Synchronous automation run for immediate results"""
    try:
        logger.info("🚀 Running automation synchronously...")
        
        # Import and run master orchestrator
        try:
            from master_automation_orchestrator import MasterAutomationOrchestrator
            orchestrator = MasterAutomationOrchestrator()
            
            # Run the complete automation workflow
            await orchestrator.run_complete_automation()
            
            # Update statistics
            jobs_fetched = getattr(orchestrator, 'jobs_found', 0)
            jobs_filtered = getattr(orchestrator, 'jobs_processed', 0)
            emails_sent = getattr(orchestrator, 'successful_applications', 0)
            
            # Create recent jobs list
            recent_jobs = []
            if hasattr(orchestrator, 'processed_jobs'):
                for job in orchestrator.processed_jobs[-10:]:
                    recent_jobs.append({
                        "title": job.get('title', 'Unknown'),
                        "company": job.get('company', 'Unknown'),
                        "status": "sent" if job.get('sent', False) else "pending"
                    })
            
            update_stats(
                jobs_fetched=jobs_fetched,
                jobs_filtered=jobs_filtered,
                resumes_generated=emails_sent,  # Assume 1 resume per email
                cover_letters_generated=emails_sent,  # Assume 1 cover letter per email
                emails_sent=emails_sent,
                recent_jobs=recent_jobs
            )
            
            return {
                "status": "success",
                "message": f"Automation completed: {emails_sent} applications sent",
                "successful_applications": emails_sent,
                "failed_applications": getattr(orchestrator, 'failed_applications', 0),
                "jobs_fetched": jobs_fetched,
                "jobs_filtered": jobs_filtered,
                "execution_time": getattr(orchestrator, '_get_execution_time', lambda: "N/A")(),
                "timestamp": datetime.now().isoformat()
            }
        except ImportError as e:
            logger.error(f"❌ Import error: {e}")
            return {
                "status": "error",
                "message": f"Import error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error(f"❌ Automation failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/status/next-jobs")
async def get_scheduled_jobs():
    """Get information about scheduled jobs"""
    if not scheduler:
        return {
            "scheduled_jobs": [],
            "scheduler_running": False,
            "scheduler_available": SCHEDULER_AVAILABLE,
            "timezone": "Europe/Stockholm"
        }
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger)
        })
    
    return {
        "scheduled_jobs": jobs,
        "scheduler_running": scheduler.running,
        "scheduler_available": SCHEDULER_AVAILABLE,
        "timezone": "Europe/Stockholm"
    }

def get_next_run_time():
    """Get next scheduled run time"""
    if not scheduler:
        return None
    jobs = scheduler.get_jobs()
    if jobs:
        next_run = jobs[0].next_run_time
        return next_run.strftime("%Y-%m-%d %H:%M:%S") if next_run else None
    return None

def update_stats(jobs_fetched=0, jobs_filtered=0, resumes_generated=0, cover_letters_generated=0, emails_sent=0, recent_jobs=None):
    """Update statistics"""
    global stats
    stats["total_runs"] += 1
    stats["jobs_fetched"] += jobs_fetched
    stats["jobs_filtered"] += jobs_filtered
    stats["resumes_generated"] += resumes_generated
    stats["cover_letters_generated"] += cover_letters_generated
    stats["emails_sent"] += emails_sent
    stats["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if emails_sent > 0 and jobs_filtered > 0:
        stats["success_rate"] = (stats["emails_sent"] / max(stats["jobs_filtered"], 1)) * 100
    
    if recent_jobs:
        stats["recent_jobs"].extend(recent_jobs)
        # Keep only last 50 jobs
        stats["recent_jobs"] = stats["recent_jobs"][-50:]

@app.get("/api/stats")
async def get_stats():
    """Get current statistics"""
    return stats

@app.post("/api/stats/reset")
async def reset_stats():
    """Reset all statistics"""
    global stats
    stats = {
        "total_runs": 0,
        "jobs_fetched": 0,
        "jobs_filtered": 0,
        "resumes_generated": 0,
        "cover_letters_generated": 0,
        "emails_sent": 0,
        "last_run": None,
        "success_rate": 0.0,
        "recent_jobs": []
    }
    return {"status": "success", "message": "Statistics reset"}

async def run_daily_lego_automation():
    """Daily automation task using master orchestrator"""
    try:
        logger.info("🎯 Starting daily automation at 6 AM via master orchestrator...")
        
        # Import and run master orchestrator
        try:
            from master_automation_orchestrator import MasterAutomationOrchestrator
            
            orchestrator = MasterAutomationOrchestrator()
            await orchestrator.run_complete_automation()
            
            # Update statistics for daily run
            jobs_fetched = getattr(orchestrator, 'jobs_found', 0)
            jobs_filtered = getattr(orchestrator, 'jobs_processed', 0)
            emails_sent = getattr(orchestrator, 'successful_applications', 0)
            
            # Create recent jobs list
            recent_jobs = []
            if hasattr(orchestrator, 'processed_jobs'):
                for job in orchestrator.processed_jobs[-10:]:
                    recent_jobs.append({
                        "title": job.get('title', 'Unknown'),
                        "company": job.get('company', 'Unknown'),
                        "status": "sent" if job.get('sent', False) else "pending"
                    })
            
            update_stats(
                jobs_fetched=jobs_fetched,
                jobs_filtered=jobs_filtered,
                resumes_generated=emails_sent,
                cover_letters_generated=emails_sent,
                emails_sent=emails_sent,
                recent_jobs=recent_jobs
            )
            
            logger.info(f"🎉 Daily automation completed: {emails_sent} applications sent")
        except ImportError as e:
            logger.error(f"❌ Import error in daily automation: {e}")
        
    except Exception as e:
        logger.error(f"❌ Daily automation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Get port from environment (Heroku sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Run the app
    uvicorn.run(
        "heroku_app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )