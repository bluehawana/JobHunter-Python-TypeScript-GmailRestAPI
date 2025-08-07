# Custom Domain Setup Guide
## Integrating JobHunter Dashboard with bluehawana.com/jobs

### 🎯 Overview
This guide helps you set up a professional dashboard at `bluehawana.com/jobs` for your job hunting automation, similar to your other projects like weatheranywhere.

### 🚀 Deployment Steps

#### 1. Deploy Dashboard to Heroku
```bash
cd backend
./deploy_dashboard_to_heroku.sh
```

#### 2. Add Custom Domain
```bash
# Add the custom domain to your Heroku app
heroku domains:add jobs.bluehawana.com --app jobhunter-dashboard

# Get the DNS target
heroku domains --app jobhunter-dashboard
```

#### 3. Configure DNS
In your domain provider (where bluehawana.com is hosted):
```
Type: CNAME
Name: jobs
Value: jobhunter-dashboard.herokuapp.com
TTL: 300 (or default)
```

#### 4. Enable SSL
```bash
# Enable automatic SSL certificates
heroku certs:auto:enable --app jobhunter-dashboard
```

### 🌐 Alternative: Subdirectory Setup

If you prefer `bluehawana.com/jobs` instead of `jobs.bluehawana.com`:

#### Option A: Reverse Proxy (Recommended)
Add to your main website's server configuration:

**Nginx:**
```nginx
location /jobs {
    proxy_pass https://jobhunter-dashboard.herokuapp.com;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**Apache:**
```apache
ProxyPass /jobs https://jobhunter-dashboard.herokuapp.com/
ProxyPassReverse /jobs https://jobhunter-dashboard.herokuapp.com/
```

#### Option B: iframe Integration
Add to your main website:
```html
<div style="width: 100%; height: 100vh;">
    <iframe 
        src="https://jobhunter-dashboard.herokuapp.com" 
        width="100%" 
        height="100%" 
        frameborder="0">
    </iframe>
</div>
```

### 📊 Dashboard Features

Your dashboard at `bluehawana.com/jobs` will include:

- **Real-time Status** - System health and automation status
- **Statistics Dashboard** - Jobs found, applications sent, success rates
- **Manual Controls** - Trigger automation on-demand
- **Execution History** - Detailed logs of all automation runs
- **Scheduling Info** - Next run times and frequency
- **Professional UI** - Matches your personal brand

### 🔧 Configuration Options

#### Environment Variables
```bash
# Core automation settings
SENDER_EMAIL=leeharvad@gmail.com
TARGET_EMAIL=hongzhili01@gmail.com
TZ=Europe/Stockholm

# API keys
ANTHROPIC_AUTH_TOKEN=your-claude-api-key
ANTHROPIC_BASE_URL=https://anyrouter.top

# Dashboard customization
DASHBOARD_TITLE="JobHunter Dashboard"
BRAND_URL="bluehawana.com"
```

#### Custom Branding
Update `templates/dashboard.html`:
```html
<!-- Change header branding -->
<p class="text-sm text-blue-100">bluehawana.com/jobs</p>

<!-- Update footer -->
<p>&copy; 2025 bluehawana.com - Professional Job Hunting Automation</p>
```

### 🎨 Styling Integration

To match your personal website's design:

1. **Update CSS** in `static/dashboard.css`
2. **Modify colors** to match your brand
3. **Add your logo** to the header
4. **Customize fonts** to match your site

### 📱 Mobile Responsiveness

The dashboard is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

### 🔒 Security Features

- **Environment-based configuration**
- **No hardcoded credentials**
- **HTTPS enforcement**
- **Secure API endpoints**
- **Rate limiting protection**

### 📈 Monitoring & Analytics

Track your automation performance:
- **Success rates** over time
- **Job market trends** 
- **Application effectiveness**
- **System uptime** monitoring

### 🚀 Going Live

Once deployed, your professional job hunting dashboard will be available at:
- `https://jobs.bluehawana.com` (subdomain)
- `https://bluehawana.com/jobs` (subdirectory)

Perfect integration with your existing projects like weatheranywhere! 🌟

### 🛠️ Maintenance

Regular tasks:
- Monitor Heroku logs: `heroku logs --tail --app jobhunter-dashboard`
- Check automation success rates
- Update environment variables as needed
- Review execution history for optimization

Your professional job hunting automation is now ready for prime time! 🎯