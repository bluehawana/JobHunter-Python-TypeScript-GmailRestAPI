# 🔗 LinkedIn API Setup Guide

## Your Current Status
✅ **LinkedIn Client ID**: `77duha47hcbh8o` (already configured)  
❌ **LinkedIn Client Secret**: Not provided yet  
❌ **LinkedIn Access Token**: Not provided yet  

## Step 1: Get LinkedIn API Credentials

1. **Go to LinkedIn Developers**
   - Visit: https://www.linkedin.com/developers/apps
   - Sign in with your LinkedIn account

2. **Find Your Existing App**
   - Look for an app with Client ID: `77duha47hcbh8o`
   - If it doesn't exist, create a new app

3. **Get Client Secret**
   - In your app dashboard, go to "Auth" tab
   - Copy the "Client Secret" value

4. **Get Access Token**
   - In the "Auth" tab, find "Access Token" section
   - Generate or copy your access token
   - Make sure it has "r_liteprofile" and "r_emailaddress" permissions

## Step 2: Set Environment Variables

⚠️ **SECURITY WARNING**: Never commit API keys or passwords to version control!

Once you have the credentials, set them as environment variables:

```bash
export LINKEDIN_CLIENT_SECRET="your_actual_client_secret_here"
export LINKEDIN_ACCESS_TOKEN="your_actual_access_token_here"
export SMTP_PASSWORD="your_gmail_app_password"
export ANTHROPIC_AUTH_TOKEN="your_anthropic_api_token"
```

## Step 3: Test the Integration

Run the LinkedIn integration:

```bash
export SMTP_PASSWORD='your_gmail_app_password' && \\
export ANTHROPIC_BASE_URL='your_anthropic_api_base_url' && \\
export ANTHROPIC_AUTH_TOKEN='your_anthropic_api_token' && \\
export LINKEDIN_CLIENT_SECRET='your_linkedin_client_secret' && \\
export LINKEDIN_ACCESS_TOKEN='your_linkedin_access_token' && \\
python3 linkedin_real_integration.py
```

## What This Will Do

🎯 **Fetch Your Real Saved Jobs** from https://www.linkedin.com/my-items/saved-jobs/

🤖 **Process Each Job with Claude 3.7** using our improved system:
- Swedish B2 + driving licenses in resume
- AKS migration achievements (60% cost reduction) for DevOps
- Role-specific project highlights
- Powerful persuasive cover letters
- 90%+ ATS optimization

📧 **Send Applications** to leeharvad@gmail.com with:
- CV PDF (ready to submit)
- Cover Letter PDF (ready to submit)  
- LaTeX source files (for editing)
- Content previews and optimization notes

## Priority Processing

The system will process jobs in this order:
1. 🔥 **High Priority**: Gothenburg jobs (any company)
2. 🔥 **High Priority**: Remote jobs at famous IT companies (Spotify, Volvo, etc.)
3. 📋 **Medium Priority**: Other saved jobs

## If LinkedIn API Doesn't Work

Alternative: **Manual Job Input**

```bash
# Use our manual system for now
python3 quick_test.py
```

Then manually copy job details from your LinkedIn saved jobs.

## Troubleshooting

**401 Authentication Error**: Access token expired or invalid
**403 Forbidden Error**: App doesn't have required permissions  
**404 Not Found Error**: API endpoint might have changed

**Solution**: Re-generate your access token with proper permissions.

## Next Steps

1. Get your LinkedIn credentials
2. Test with one saved job first
3. Process all your saved jobs
4. Submit the applications directly to employers

Your resume system is now **dramatically more powerful** than before! 🚀