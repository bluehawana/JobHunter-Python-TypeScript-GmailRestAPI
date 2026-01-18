# Deployment Guide - Intelligent CV Template Selection System

## Overview

This guide covers deploying the JobHunter application with the intelligent CV template selection system to production environments.

## System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **Python**: 3.9+
- **Node.js**: 18+

### Recommended Requirements
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 50GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Python**: 3.11+
- **Node.js**: 20+

## Environment Variables

### Required Environment Variables

Create a `.env` file in the project root:

```bash
# AI Configuration
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_GROUP_ID=your_group_id_here

# Gmail API (for job application tracking)
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
GMAIL_REFRESH_TOKEN=your_refresh_token

# Application Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your_secret_key_here

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=/var/log/jobhunter/app.log

# Template Configuration
TEMPLATES_DIR=/app/job_applications
FALLBACK_TEMPLATE=devops_cloud

# AI Analysis Configuration
AI_CONFIDENCE_THRESHOLD=0.5
AI_TIMEOUT_SECONDS=30
ENABLE_AI_ANALYSIS=true

# Performance Configuration
MAX_WORKERS=4
REQUEST_TIMEOUT=60
```

### Optional Environment Variables

```bash
# Advanced AI Configuration
AI_MODEL_VERSION=minimax-m2
AI_MAX_RETRIES=3
AI_RETRY_DELAY=1

# Template Selection Configuration
ROLE_BREAKDOWN_THRESHOLD=5.0
MIXED_ROLE_WARNING_THRESHOLD=50.0
CONTENT_ALIGNMENT_THRESHOLD=0.1

# Monitoring Configuration
ENABLE_METRICS=true
METRICS_PORT=9090
HEALTH_CHECK_ENDPOINT=/health

# Security Configuration
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
RATE_LIMIT_PER_MINUTE=60
```

## Configuration Files

### 1. Application Configuration

Create `config/production.py`:

```python
import os
from pathlib import Path

class ProductionConfig:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False
    
    # AI Configuration
    MINIMAX_API_KEY = os.environ.get('MINIMAX_API_KEY')
    MINIMAX_GROUP_ID = os.environ.get('MINIMAX_GROUP_ID')
    AI_CONFIDENCE_THRESHOLD = float(os.environ.get('AI_CONFIDENCE_THRESHOLD', '0.5'))
    AI_TIMEOUT_SECONDS = int(os.environ.get('AI_TIMEOUT_SECONDS', '30'))
    ENABLE_AI_ANALYSIS = os.environ.get('ENABLE_AI_ANALYSIS', 'true').lower() == 'true'
    
    # Template Configuration
    TEMPLATES_DIR = os.environ.get('TEMPLATES_DIR', '/app/job_applications')
    FALLBACK_TEMPLATE = os.environ.get('FALLBACK_TEMPLATE', 'devops_cloud')
    
    # Role Detection Configuration
    ROLE_BREAKDOWN_THRESHOLD = float(os.environ.get('ROLE_BREAKDOWN_THRESHOLD', '5.0'))
    MIXED_ROLE_WARNING_THRESHOLD = float(os.environ.get('MIXED_ROLE_WARNING_THRESHOLD', '50.0'))
    CONTENT_ALIGNMENT_THRESHOLD = float(os.environ.get('CONTENT_ALIGNMENT_THRESHOLD', '0.1'))
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', '/var/log/jobhunter/app.log')
    
    # Performance Configuration
    MAX_WORKERS = int(os.environ.get('MAX_WORKERS', '4'))
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', '60'))
```

### 2. Logging Configuration

Create `config/logging.yaml`:

```yaml
version: 1
disable_existing_loggers: false

formatters:
  standard:
    format: '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
  detailed:
    format: '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout
    
  file:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: detailed
    filename: /var/log/jobhunter/app.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
    
  error_file:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: detailed
    filename: /var/log/jobhunter/error.log
    maxBytes: 10485760  # 10MB
    backupCount: 5

loggers:
  cv_templates:
    level: INFO
    handlers: [console, file]
    propagate: false
    
  job_analyzer:
    level: INFO
    handlers: [console, file]
    propagate: false
    
  template_matcher:
    level: INFO
    handlers: [console, file]
    propagate: false
    
  ai_analyzer:
    level: INFO
    handlers: [console, file]
    propagate: false

root:
  level: INFO
  handlers: [console, file, error_file]
```

## Docker Deployment

### 1. Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create log directory
RUN mkdir -p /var/log/jobhunter

# Create non-root user
RUN useradd -m -u 1000 jobhunter && \
    chown -R jobhunter:jobhunter /app /var/log/jobhunter
USER jobhunter

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "60", "backend.app.app:app"]
```

### 2. Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  jobhunter:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    env_file:
      - .env
    volumes:
      - ./job_applications:/app/job_applications:ro
      - ./logs:/var/log/jobhunter
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - jobhunter
    restart: unless-stopped
```

### 3. Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream jobhunter {
        server jobhunter:5000;
    }

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        client_max_body_size 10M;
        proxy_read_timeout 60s;

        location / {
            proxy_pass http://jobhunter;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://jobhunter/health;
            access_log off;
        }
    }
}
```

## VPS Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm nginx git curl

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Application Deployment

```bash
# Clone repository
git clone https://github.com/yourusername/jobhunter.git
cd jobhunter

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your configuration

# Create log directory
sudo mkdir -p /var/log/jobhunter
sudo chown $USER:$USER /var/log/jobhunter

# Test application
python3 -m pytest backend/test_cv_template_manager_properties.py -v

# Start application
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 60 backend.app.app:app
```

### 3. Systemd Service

Create `/etc/systemd/system/jobhunter.service`:

```ini
[Unit]
Description=JobHunter Application
After=network.target

[Service]
Type=exec
User=jobhunter
Group=jobhunter
WorkingDirectory=/home/jobhunter/jobhunter
Environment=PATH=/home/jobhunter/jobhunter/venv/bin
EnvironmentFile=/home/jobhunter/jobhunter/.env
ExecStart=/home/jobhunter/jobhunter/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 60 backend.app.app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable jobhunter
sudo systemctl start jobhunter
sudo systemctl status jobhunter
```

## SSL/TLS Configuration

### Using Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## Monitoring and Logging

### 1. Log Rotation

Create `/etc/logrotate.d/jobhunter`:

```
/var/log/jobhunter/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 jobhunter jobhunter
    postrotate
        systemctl reload jobhunter
    endscript
}
```

### 2. Health Check Endpoint

The application provides a health check endpoint at `/health`:

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-17T10:30:00Z",
  "version": "1.0.0",
  "components": {
    "ai_analyzer": "available",
    "template_manager": "ready",
    "templates": "loaded"
  }
}
```

### 3. Monitoring Script

Create `scripts/monitor.sh`:

```bash
#!/bin/bash

LOG_FILE="/var/log/jobhunter/monitor.log"
HEALTH_URL="http://localhost:5000/health"

check_health() {
    response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)
    if [ $response -eq 200 ]; then
        echo "$(date): Health check passed" >> $LOG_FILE
        return 0
    else
        echo "$(date): Health check failed with code $response" >> $LOG_FILE
        return 1
    fi
}

# Check every 5 minutes
while true; do
    if ! check_health; then
        echo "$(date): Restarting jobhunter service" >> $LOG_FILE
        sudo systemctl restart jobhunter
        sleep 30
    fi
    sleep 300
done
```

## Troubleshooting

### Common Issues

1. **Template Loading Errors**
   ```bash
   # Check template directory permissions
   ls -la job_applications/
   
   # Verify template files exist
   find job_applications/ -name "*.tex" | head -10
   
   # Check logs
   tail -f /var/log/jobhunter/app.log | grep -i template
   ```

2. **AI Analysis Not Working**
   ```bash
   # Test API connectivity
   curl -X POST "https://api.minimax.chat/v1/text/chatcompletion_v2" \
     -H "Authorization: Bearer $MINIMAX_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model": "abab6.5s-chat", "messages": [{"role": "user", "content": "test"}]}'
   
   # Check environment variables
   echo $MINIMAX_API_KEY | cut -c1-10
   echo $MINIMAX_GROUP_ID
   ```

3. **High Memory Usage**
   ```bash
   # Monitor memory usage
   ps aux | grep gunicorn
   
   # Reduce workers if needed
   sudo systemctl edit jobhunter
   # Add: ExecStart=/path/to/gunicorn --workers 2 ...
   ```

4. **Slow Response Times**
   ```bash
   # Check AI timeout settings
   grep -i timeout /home/jobhunter/jobhunter/.env
   
   # Monitor request times
   tail -f /var/log/nginx/access.log | grep -E '[0-9]+\.[0-9]+$'
   ```

### Log Analysis

```bash
# Check error patterns
grep -i error /var/log/jobhunter/app.log | tail -20

# Monitor role detection accuracy
grep "Selected role category" /var/log/jobhunter/app.log | tail -10

# Check AI analysis usage
grep "AI Analysis" /var/log/jobhunter/app.log | tail -10

# Monitor template fallbacks
grep -i fallback /var/log/jobhunter/app.log | tail -10
```

### Performance Tuning

1. **Optimize Gunicorn Workers**
   ```bash
   # Formula: (2 x CPU cores) + 1
   # For 4 cores: 9 workers
   gunicorn --workers 9 --worker-class sync --timeout 60
   ```

2. **Enable Caching**
   ```python
   # Add to configuration
   CACHE_TYPE = "simple"
   CACHE_DEFAULT_TIMEOUT = 300
   ```

3. **Database Connection Pooling** (if using database)
   ```python
   # Add to configuration
   SQLALCHEMY_ENGINE_OPTIONS = {
       'pool_size': 10,
       'pool_recycle': 120,
       'pool_pre_ping': True
   }
   ```

## Security Considerations

1. **Environment Variables**: Never commit `.env` files to version control
2. **API Keys**: Rotate API keys regularly
3. **File Permissions**: Ensure template files are read-only
4. **Network Security**: Use HTTPS in production
5. **Input Validation**: Job descriptions are validated and sanitized
6. **Rate Limiting**: Implement rate limiting for API endpoints

## Backup and Recovery

### Backup Script

Create `scripts/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/backup/jobhunter"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application files
tar -czf $BACKUP_DIR/app_$DATE.tar.gz \
    --exclude=venv \
    --exclude=__pycache__ \
    --exclude=.git \
    /home/jobhunter/jobhunter/

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /var/log/jobhunter/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

### Recovery Process

1. **Stop the service**: `sudo systemctl stop jobhunter`
2. **Restore files**: `tar -xzf backup.tar.gz -C /`
3. **Update permissions**: `sudo chown -R jobhunter:jobhunter /home/jobhunter/jobhunter`
4. **Start the service**: `sudo systemctl start jobhunter`
5. **Verify health**: `curl http://localhost:5000/health`

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**: Use nginx or HAProxy to distribute requests
2. **Multiple Instances**: Run multiple application instances
3. **Shared Storage**: Use shared storage for template files
4. **Database**: Move to external database for session storage

### Vertical Scaling

1. **Increase Resources**: Add more CPU/RAM to the server
2. **Optimize Workers**: Adjust Gunicorn worker count
3. **Caching**: Implement Redis for caching analysis results
4. **CDN**: Use CDN for static assets

This deployment guide provides comprehensive instructions for deploying the intelligent CV template selection system in production environments with proper monitoring, logging, and security considerations.