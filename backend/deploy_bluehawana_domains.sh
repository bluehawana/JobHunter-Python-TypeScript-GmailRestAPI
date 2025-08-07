#!/bin/bash
# Deploy both JobHunter and Weather apps with bluehawana.com domain integration

echo "🌐 Setting up bluehawana.com domain integration"
echo "🎯 Jobs: bluehawana.com/jobs"
echo "🌤️  Weather: bluehawana.com/weather"
echo "=" * 50

# Check Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first."
    exit 1
fi

# Login check
echo "🔐 Checking Heroku authentication..."
heroku auth:whoami || heroku login

# Deploy JobHunter Dashboard
echo "🚀 Deploying JobHunter Dashboard..."
APP_NAME_JOBS="jobhunter-dashboard"
heroku create $APP_NAME_JOBS --region eu || echo "App already exists"

# Set environment variables for JobHunter
echo "⚙️ Configuring JobHunter Dashboard..."
heroku config:set ANTHROPIC_AUTH_TOKEN=sk-wldqMp1L48Uh85iQWgv05sRuUgtZxqyJAH92mW476z0SyiG4 --app $APP_NAME_JOBS
heroku config:set ANTHROPIC_BASE_URL=https://anyrouter.top --app $APP_NAME_JOBS
heroku config:set CLAUDE_MODEL=claude-3-7-sonnet-20250219 --app $APP_NAME_JOBS
heroku config:set SENDER_EMAIL=leeharvad@gmail.com --app $APP_NAME_JOBS
heroku config:set SENDER_GMAIL_PASSWORD=vsdclxhjnklrccsf --app $APP_NAME_JOBS
heroku config:set TARGET_EMAIL=hongzhili01@gmail.com --app $APP_NAME_JOBS
heroku config:set TZ=Europe/Stockholm --app $APP_NAME_JOBS
heroku config:set CUSTOM_DOMAIN=bluehawana.com --app $APP_NAME_JOBS
heroku config:set BASE_PATH=/jobs --app $APP_NAME_JOBS
heroku config:set ENVIRONMENT=production --app $APP_NAME_JOBS

# Add buildpacks for JobHunter
heroku buildpacks:clear --app $APP_NAME_JOBS
heroku buildpacks:add --index 1 https://github.com/Thermondo/heroku-buildpack-texlive.git --app $APP_NAME_JOBS
heroku buildpacks:add --index 2 heroku/python --app $APP_NAME_JOBS

# Create Procfile for dashboard
echo "web: python dashboard_app.py" > Procfile

# Deploy JobHunter
echo "📤 Deploying JobHunter Dashboard..."
git add .
git commit -m "Deploy JobHunter Dashboard for bluehawana.com/jobs" || echo "No changes to commit"
git push heroku main

# Scale JobHunter
heroku ps:scale web=1 --app $APP_NAME_JOBS

echo "✅ JobHunter Dashboard deployed!"
echo "🌐 Direct URL: https://$APP_NAME_JOBS.herokuapp.com"

# Weather App Setup (if you want to deploy it to Heroku)
echo ""
echo "🌤️  Weather App Setup..."
read -p "Do you want to deploy Weather App to Heroku? (y/n): " deploy_weather

if [[ $deploy_weather == "y" || $deploy_weather == "Y" ]]; then
    APP_NAME_WEATHER="weather-anywhere-app"
    heroku create $APP_NAME_WEATHER --region eu || echo "Weather app already exists"
    
    # Configure weather app
    heroku config:set CUSTOM_DOMAIN=bluehawana.com --app $APP_NAME_WEATHER
    heroku config:set BASE_PATH=/weather --app $APP_NAME_WEATHER
    heroku config:set TZ=Europe/Stockholm --app $APP_NAME_WEATHER
    
    echo "✅ Weather App configured!"
    echo "🌐 Direct URL: https://$APP_NAME_WEATHER.herokuapp.com"
fi

# Generate Nginx configuration
echo ""
echo "📝 Generating Nginx configuration for your server..."
cat > nginx_bluehawana_config.conf << EOF
# Nginx configuration for bluehawana.com
server {
    listen 80;
    listen 443 ssl;
    server_name bluehawana.com www.bluehawana.com;
    
    # SSL configuration (update paths as needed)
    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/private.key;
    
    # Main website
    location / {
        root /var/www/bluehawana.com;
        index index.html index.php;
        try_files \$uri \$uri/ =404;
    }
    
    # JobHunter Dashboard
    location /jobs {
        proxy_pass https://$APP_NAME_JOBS.herokuapp.com;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        
        # Handle WebSocket connections
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
EOF

if [[ $deploy_weather == "y" || $deploy_weather == "Y" ]]; then
cat >> nginx_bluehawana_config.conf << EOF
    
    # Weather App
    location /weather {
        proxy_pass https://$APP_NAME_WEATHER.herokuapp.com;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }
EOF
fi

cat >> nginx_bluehawana_config.conf << EOF
}
EOF

echo "📄 Nginx configuration saved to: nginx_bluehawana_config.conf"

# Generate Apache configuration
echo ""
echo "📝 Generating Apache configuration..."
cat > apache_bluehawana_config.conf << EOF
# Apache configuration for bluehawana.com
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
    
    # SSL Configuration (update paths as needed)
    SSLEngine on
    SSLCertificateFile /path/to/ssl/cert.pem
    SSLCertificateKeyFile /path/to/ssl/private.key
    
    # Main website
    <Location />
        DirectoryIndex index.html index.php
    </Location>
    
    # JobHunter Dashboard
    ProxyPreserveHost On
    ProxyPass /jobs https://$APP_NAME_JOBS.herokuapp.com/
    ProxyPassReverse /jobs https://$APP_NAME_JOBS.herokuapp.com/
EOF

if [[ $deploy_weather == "y" || $deploy_weather == "Y" ]]; then
cat >> apache_bluehawana_config.conf << EOF
    
    # Weather App
    ProxyPass /weather https://$APP_NAME_WEATHER.herokuapp.com/
    ProxyPassReverse /weather https://$APP_NAME_WEATHER.herokuapp.com/
EOF
fi

cat >> apache_bluehawana_config.conf << EOF
</VirtualHost>
EOF

echo "📄 Apache configuration saved to: apache_bluehawana_config.conf"

# Summary
echo ""
echo "🎉 DEPLOYMENT SUMMARY"
echo "=" * 50
echo "✅ JobHunter Dashboard: https://$APP_NAME_JOBS.herokuapp.com"
if [[ $deploy_weather == "y" || $deploy_weather == "Y" ]]; then
    echo "✅ Weather App: https://$APP_NAME_WEATHER.herokuapp.com"
fi
echo ""
echo "📋 NEXT STEPS:"
echo "1. Copy the generated config file to your web server"
echo "2. Update SSL certificate paths in the config"
echo "3. Restart your web server (nginx/apache)"
echo "4. Test the routes:"
echo "   - https://bluehawana.com/jobs"
if [[ $deploy_weather == "y" || $deploy_weather == "Y" ]]; then
    echo "   - https://bluehawana.com/weather"
fi
echo ""
echo "🌟 Your professional domain integration is ready!"