# ⚠️ SECURITY NOTICE - API CREDENTIALS

## 🔒 IMPORTANT: Protect Your API Keys

This system requires Claude API credentials to function. **NEVER** commit API keys to version control.

### Required Environment Variables

Users must set their own API credentials:

```bash
export ANTHROPIC_BASE_URL="your_claude_api_base_url"
export ANTHROPIC_AUTH_TOKEN="your_claude_api_token"
export SMTP_PASSWORD="your_gmail_app_password"
```

### For Open Source Usage

1. **Users must obtain their own Claude API access**
2. **Users must configure their own SMTP credentials**
3. **API keys should NEVER be hardcoded in source files**
4. **Use environment variables or secure configuration files**

### Setup Instructions for New Users

1. Get Claude API access from your provider
2. Set environment variables with your credentials
3. Configure Gmail app password for email sending
4. Run the system with your own credentials

### Git Security

- API keys have been removed from all source files
- `.gitignore` should exclude any credential files
- Never commit files containing real API tokens
- Use environment variables for all sensitive data

### Example Usage

```bash
# Set your own credentials
export ANTHROPIC_BASE_URL="https://your-claude-provider.com"
export ANTHROPIC_AUTH_TOKEN="your-api-token-here"
export SMTP_PASSWORD="your-gmail-app-password"

# Run the system
python3 claude_final_system.py
```

## 🚨 For Repository Maintainers

- Always review commits for hardcoded credentials
- Use credential scanning tools in CI/CD
- Educate contributors about security practices
- Document credential requirements clearly

This ensures the open source project remains secure while allowing users to leverage their own API access.