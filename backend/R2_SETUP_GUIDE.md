# R2 Cloudflare Storage Setup Guide

## Overview
This guide explains how to configure R2 Cloudflare storage for automatic backup of your generated resumes and cover letters.

## R2 Storage URL
Your R2 bucket: `https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com/jobhunter`

## Required Credentials
To enable automatic backup, you need to set these environment variables in your `.env` file:

```env
# R2 Cloudflare Storage (for document backups)
R2_ACCOUNT_ID=your-cloudflare-account-id
R2_ACCESS_KEY_ID=your-r2-access-key-id
R2_SECRET_ACCESS_KEY=your-r2-secret-access-key
R2_BUCKET_NAME=jobhunter
R2_ENDPOINT=https://2a35af424f8734e497a5d707344d79d5.r2.cloudflarestorage.com
```

## How to Get R2 Credentials

### 1. Cloudflare Account ID
- Log in to Cloudflare Dashboard
- Go to the right sidebar → Account ID (copy this value)

### 2. R2 API Tokens
- In Cloudflare Dashboard, go to "R2 Object Storage"
- Click "Manage R2 API tokens"
- Click "Create API token"
- Set permissions: "Edit" for your R2 bucket
- Copy the Access Key ID and Secret Access Key

### 3. Update .env File
Replace the placeholder values in `.env`:
```env
R2_ACCOUNT_ID=your-actual-account-id-here
R2_ACCESS_KEY_ID=your-actual-access-key-here  
R2_SECRET_ACCESS_KEY=your-actual-secret-key-here
```

## Backup Structure
Documents are organized in R2 as:
```
applications/
├── 2025-01-27/
│   ├── Thomthon_Retuer_Solution_Developer/
│   │   ├── cv.pdf
│   │   ├── cv.tex
│   │   ├── cover_letter.pdf
│   │   └── cover_letter.tex
│   └── Spotify_DevOps_Engineer/
│       ├── cv.pdf
│       ├── cv.tex
│       ├── cover_letter.pdf
│       └── cover_letter.tex
└── index.html (backup index page)
```

## Benefits of R2 Backup
- ✅ **Automatic backup** of all generated documents
- ✅ **Organized storage** by date and company
- ✅ **Both PDF and LaTeX** versions saved
- ✅ **Web-accessible** backup index
- ✅ **Version history** for document revisions
- ✅ **Cost-effective** Cloudflare R2 storage

## Usage

### With R2 Backup (Recommended)
```bash
# Process jobs with automatic R2 backup
python job_processor_with_backup.py

# Process only Thomthon Retuer with backup
python job_processor_with_backup.py
# Choose option 1
```

### Test R2 Connection
```bash
# Test R2 backup service
python r2_backup_service.py
```

### Manual Backup
```bash
# Backup existing documents
python -c "
from r2_backup_service import R2BackupService
backup = R2BackupService()
backup.backup_thomthon_documents()
"
```

## Troubleshooting

### "R2 client not initialized"
- Check that R2 credentials are set in `.env`
- Verify account ID, access key, and secret key are correct

### "Upload failed"
- Check network connectivity
- Verify R2 API token has correct permissions
- Ensure bucket name is correct

### "No module named 'boto3'"
```bash
source venv/bin/activate
pip install boto3
```

## Security Notes
- R2 credentials are stored in `.env` (not committed to git)
- Credentials should have minimal required permissions
- Consider rotating API tokens regularly
- R2 bucket should have appropriate access controls

## Cost Information
- Cloudflare R2 storage is very cost-effective
- Free tier: 10GB storage, 1M Class A operations/month
- Perfect for storing application documents

## Integration with Job Processing
Once configured, R2 backup happens automatically:

1. Job application processed → PDF + LaTeX generated
2. Documents automatically uploaded to R2
3. Organized folder structure created
4. Backup index page updated
5. Local PDFs cleaned up (LaTeX sources kept)
6. Email sent with application documents

This ensures you always have a backup of all your tailored application documents!