# bluehawana.com Domain Integration Guide
## Setting up Professional Subdomains for Your Projects

### 🎯 Overview
This guide helps you set up professional subdomains for your projects:
- `bluehawana.com/jobs` - JobHunter Dashboard
- `bluehawana.com/weather` - Weather Anywhere App

### 🏗️ Architecture Options

#### Option 1: Subdirectory Routing (Recommended)
```
bluehawana.com/jobs → JobHunter Dashboard (Heroku)
bluehawana.com/weather → Weather App (Heroku/Alibaba Cloud)
```

#### Option 2: Subdomain Routing
```
jobs.bluehawana.com → JobHunter Dashboard
weather.bluehawana.com → Weather App
```

### 🚀 Setup Steps

#### 1. Deploy JobHunter Dashboard
```bash
cd backend
./deploy_dashboard_to_heroku.sh
```

#### 2. Configure Main Website Routing

**If using Nginx (Recommended):**
```nginx
# /etc/nginx/sites-available/bluehawana.com
server {
    listen 80;
    listen 443 ssl;
    server_name bluehawana.com www.bluehawana.com;
    
    # SSL configuration
    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/private.key;
    
    # Main website
    location / {
        root /var/www/bluehawana.com;
        index index.html index.php;
        try_files $uri $uri/ =404;
    }
    
    # JobHunter Dashboard
    location /jobs {
        proxy_pass https://jobhunter-dashboard.herokuapp.com;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Handle WebSocket connections
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Weather App
    location /weather {
        proxy_pass https://weather-anywhere.herokuapp.com;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

**If using Apache:**
```apache
# /etc/apache2/sites-available/bluehawana.com.conf
<VirtualHost *:80>
    ServerName bluehawana.com
    ServerAlias www.bluehawana.com
    DocumentRoot /var/www/bluehawana.com
    
    # Redirect HTTP to HTTPS
    Redirect permanent / https://bluehawana.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName bluehawana.com
    ServerAlias www.bluehawana.com
    DocumentRoot /var/www/bluehawana.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/ssl/cert.pem
    SSLCertificateKeyFile /path/to/ssl/private.key
    
    # Main website
    <Location />
        DirectoryIndex index.html index.php
    </Location>
    
    # JobHunter Dashboard
    ProxyPreserveHost On
    ProxyPass /jobs https://jobhunter-dashboard.herokuapp.com/
    ProxyPassReverse /jobs https://jobhunter-dashboard.herokuapp.com/
    
    # Weather App
    ProxyPass /weather https://weather-anywhere.herokuapp.com/
    ProxyPassReverse /weather https://weather-anywhere.herokuapp.com/
</VirtualHost>
```

#### 3. Update Heroku Apps for Custom Domains

**JobHunter Dashboard:**
```bash
# Add custom domain support
heroku config:set CUSTOM_DOMAIN=bluehawana.com --app jobhunter-dashboard
heroku config:set BASE_PATH=/jobs --app jobhunter-dashboard
```

**Weather App (if on Heroku):**
```bash
# If your weather app is on Heroku
heroku config:set CUSTOM_DOMAIN=bluehawana.com --app weather-anywhere
heroku config:set BASE_PATH=/weather --app weather-anywhere
```

### 🔧 Code Updates for Path-based Routing

#### Update JobHunter Dashboard
```python
# In dashboard_app.py, add base path support
import os

BASE_PATH = os.getenv('BASE_PATH', '')

app = FastAPI(
    title="JobHunter Dashboard",
    description="Professional job hunting automation dashboard",
    version="2.0.0",
    root_path=BASE_PATH  # This handles the /jobs prefix
)

# Update template references
@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    dashboard_data = await dashboard.get_dashboard_data()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "data": dashboard_data,
        "page_title": "JobHunter Dashboard",
        "base_path": BASE_PATH
    })
```

#### Update HTML Template
```html
<!-- In templates/dashboard.html -->
<head>
    <base href="{{ base_path }}/">
    <!-- Rest of head content -->
</head>

<!-- Update asset paths -->
<link href="{{ base_path }}/static/dashboard.css" rel="stylesheet">

<!-- Update API calls -->
<script>
    const basePath = '{{ base_path }}';
    
    // Update fetch calls
    fetch(`${basePath}/api/status`)
    fetch(`${basePath}/api/run-automation`, { method: 'POST' })
</script>
```

### 🌐 DNS Configuration

If you want to use subdomains instead:

```
Type: CNAME
Name: jobs
Value: jobhunter-dashboard.herokuapp.com
TTL: 300

Type: CNAME  
Name: weather
Value: weather-anywhere.herokuapp.com
TTL: 300
```

### 📱 Mobile Navigation Integration

Add to your main website's navigation:
```html
<!-- Main website navigation -->
<nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/projects">Projects</a>
    <a href="/jobs">Job Hunter</a>
    <a href="/weather">Weather</a>
    <a href="/contact">Contact</a>
</nav>
```

### 🎨 Consistent Branding

Update both apps to match your personal brand:

**CSS Variables (shared across apps):**
```css
:root {
    --primary-color: #your-brand-color;
    --secondary-color: #your-secondary-color;
    --font-family: 'Your-Brand-Font', sans-serif;
    --border-radius: 8px;
}
```

### 🔒 SSL Certificate

Ensure your SSL certificate covers:
- `bluehawana.com`
- `www.bluehawana.com`
- `jobs.bluehawana.com` (if using subdomains)
- `weather.bluehawana.com` (if using subdomains)

### 📊 Analytics Integration

Add Google Analytics or similar to track usage:
```html
<!-- Add to both dashboard templates -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 🚀 Deployment Checklist

- [ ] Deploy JobHunter Dashboard to Heroku
- [ ] Deploy Weather App to Heroku (if not already)
- [ ] Configure reverse proxy on main server
- [ ] Update DNS records
- [ ] Test SSL certificates
- [ ] Update app configurations for custom domains
- [ ] Test all routes and functionality
- [ ] Update navigation on main website
- [ ] Configure analytics tracking

### 🧪 Testing

Test all routes:
```bash
# Test main site
curl -I https://bluehawana.com

# Test job hunter dashboard
curl -I https://bluehawana.com/jobs

# Test weather app
curl -I https://bluehawana.com/weather

# Test API endpoints
curl https://bluehawana.com/jobs/api/status
```

### 📈 Benefits

- **Professional URLs** - Clean, branded paths
- **SEO Benefits** - All under your main domain
- **Unified Analytics** - Track all projects together
- **Brand Consistency** - Cohesive user experience
- **Portfolio Integration** - Showcase your technical skills

Your professional domain setup is ready! This gives you a cohesive web presence with all your projects under the bluehawana.com umbrella. 🌟