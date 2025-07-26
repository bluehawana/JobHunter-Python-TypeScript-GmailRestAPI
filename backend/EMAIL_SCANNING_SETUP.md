# Email Job Scanning Setup

This document describes the email scanning functionality that monitors your Gmail account for job opportunities from LinkedIn, Indeed, and other job boards.

## Configuration

The email scanner uses the following environment variables from `.env`:

```
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Features

- **Daily Email Scanning**: Scans Gmail at 6am daily for job-related emails
- **Multi-Platform Support**: Parses emails from:
  - LinkedIn job alerts
  - Indeed job alerts
  - Glassdoor, Monster, ZipRecruiter, Dice, CareerBuilder, SimplyHired
- **Job Data Extraction**: Extracts:
  - Job title and company
  - Location and salary (when available)
  - Job URLs and descriptions
  - Remote work options

## Usage

### Manual Testing
```bash
# Test email scanning
python app/scheduler/job_runner.py scan_emails

# Test with daily summary
python app/scheduler/job_runner.py daily_summary
```

### Heroku Scheduler Setup
Add these commands to Heroku Scheduler:

1. **Daily Email Scan** (6:00 AM UTC):
   ```
   bash schedule_6am_email_scan.sh
   ```

2. **Daily Summary Email** (7:00 AM UTC):
   ```
   python app/scheduler/job_runner.py daily_summary
   ```

## How It Works

1. **IMAP Connection**: Connects to Gmail using app password
2. **Email Search**: Searches for recent emails from job platforms
3. **Content Parsing**: Extracts job information using regex patterns
4. **Data Processing**: Structures job data with confidence scores
5. **Summary Generation**: Sends daily summary to leeharvad@gmail.com

## Email Patterns Supported

### LinkedIn
- "Job Title at Company Name"
- "Company is hiring for Position"
- LinkedIn job alert emails with embedded job links

### Indeed
- "Job Title - Company Name"
- "Position at Company"
- Salary extraction from Indeed formats

### Other Platforms
- Generic job alert patterns
- Company hiring announcements
- Position listings with basic information

## Security Notes

- Uses Gmail app password (not OAuth2 for simplicity)
- Credentials stored in environment variables
- IMAP connection over SSL (port 993)
- Email content is processed locally, not stored permanently

## Dependencies

```
imapclient==2.3.1
email-validator==2.1.0
```

## Troubleshooting

1. **IMAP Login Issues**: Ensure Gmail app password is correct
2. **No Jobs Found**: Check if job alert subscriptions are active
3. **Pattern Matching**: Email formats may change, patterns may need updates
4. **Connection Errors**: Check network connectivity and Gmail IMAP settings