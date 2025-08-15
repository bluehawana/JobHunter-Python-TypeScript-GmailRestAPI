# 📧 Real Job Setup Guide

## Email Flow
- **Job alerts arrive at**: `bluehawana@gmail.com` (LinkedIn, Indeed, company alerts)
- **Applications sent from**: `leeharvad@gmail.com` (automated sender)
- **Applications delivered to**: `hongzhili01@gmail.com` (your main inbox)

## Current Status
✅ **Sender email configured**: `leeharvad@gmail.com`  
✅ **Recipient email configured**: `hongzhili01@gmail.com`  
❌ **Job alerts email**: `bluehawana@gmail.com` (password needed)

## Option 1: Add Gmail App Password (Recommended)
1. Go to your `bluehawana@gmail.com` account
2. Enable 2-factor authentication
3. Generate an App Password for "Mail"
4. Add to `backend/.env`:
   ```
   BLUEHAWANA_GMAIL_PASSWORD=your_app_password_here
   ```

## Option 2: Manual Job Input (Current Setup)
1. Check `bluehawana@gmail.com` for job alerts
2. Edit `manual_job_input.py`
3. Add real jobs to the `real_jobs` list:

```python
real_jobs = [
    {
        'company': 'Volvo Group',
        'title': 'Senior DevOps Engineer',
        'location': 'Gothenburg, Sweden',
        'description': 'We are looking for a Senior DevOps Engineer...',
        'url': 'https://jobs.volvogroup.com/job/12345',
        'requirements': 'Kubernetes, Docker, AWS, Python, CI/CD',
        'from': 'jobs@volvogroup.com',
        'subject': 'Job Opportunity: Senior DevOps Engineer',
        'date': '2025-08-14'
    }
]
```

## Testing the System
```bash
# Test with current setup
source venv/bin/activate
python3 simple_gmail_scanner.py

# Run full automation (will only process real jobs)
python3 run_06_00_automation.py
```

## Automation Schedule
- **Runs**: Every weekday at 06:00 AM
- **Delivers**: Applications by 08:00 AM
- **Only processes**: Real jobs (no fake jobs)

## Next Steps
1. Add real jobs to `manual_job_input.py` OR configure `BLUEHAWANA_GMAIL_PASSWORD`
2. Test the automation: `python3 run_06_00_automation.py`
3. Start the scheduler: `python3 daily_06_00_scheduler.py`