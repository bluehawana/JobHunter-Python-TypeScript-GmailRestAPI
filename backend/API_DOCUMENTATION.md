# JobHunter Dashboard API Documentation

## 🎯 Overview
RESTful API endpoints for the JobHunter Dashboard at `bluehawana.com/jobs`

## 📋 Base URL
```
Production: https://jobs.bluehawana.com
Development: http://localhost:8000
```

## 🔗 Endpoints

### GET `/`
**Main Dashboard Page**
- Returns: HTML dashboard interface
- Purpose: Primary user interface

### GET `/api/status`
**System Status**
```json
{
  "status": {
    "automation_running": false,
    "scheduler_active": true,
    "next_scheduled_run": "2025-08-06T06:00:00+02:00",
    "last_execution": {
      "timestamp": "2025-08-05T06:00:00",
      "duration": "2m 34s",
      "jobs_found": 5,
      "successful_applications": 4,
      "failed_applications": 1,
      "success_rate": "80.0%"
    }
  },
  "stats": {
    "total_jobs_found": 25,
    "total_applications_sent": 20,
    "success_rate": 80.0,
    "last_run": "2025-08-05T06:00:00"
  }
}
```

### POST `/api/run-automation`
**Trigger Manual Automation**
- Purpose: Start automation immediately
- Returns: Execution results
- Status Codes:
  - `200`: Success
  - `409`: Automation already running
  - `500`: Internal error

```json
{
  "status": "success",
  "message": "Automation completed successfully",
  "result": {
    "timestamp": "2025-08-05T14:30:00",
    "duration": "3m 12s",
    "jobs_found": 3,
    "successful_applications": 3,
    "failed_applications": 0,
    "success_rate": "100.0%"
  }
}
```

### GET `/api/history`
**Execution History**
```json
{
  "executions": [
    {
      "timestamp": "2025-08-05T06:00:00",
      "duration": "2m 34s",
      "jobs_found": 5,
      "successful_applications": 4,
      "failed_applications": 1,
      "success_rate": "80.0%"
    }
  ],
  "total_count": 10
}
```

### GET `/api/stats`
**Overall Statistics**
```json
{
  "total_jobs_found": 25,
  "total_applications_sent": 20,
  "success_rate": 80.0,
  "last_run": "2025-08-05T06:00:00"
}
```

### GET `/health`
**Health Check**
```json
{
  "status": "healthy",
  "service": "JobHunter Dashboard",
  "version": "2.0.0",
  "scheduler_running": true,
  "automation_running": false,
  "timestamp": "2025-08-05T14:30:00"
}
```

## 🔧 Integration Examples

### JavaScript Fetch
```javascript
// Get current status
const response = await fetch('/api/status');
const data = await response.json();
console.log('Jobs found:', data.stats.total_jobs_found);

// Trigger automation
const runResponse = await fetch('/api/run-automation', {
  method: 'POST'
});
const result = await runResponse.json();
```

### Python Requests
```python
import requests

# Get status
response = requests.get('https://jobs.bluehawana.com/api/status')
data = response.json()
print(f"Success rate: {data['stats']['success_rate']}%")

# Trigger automation
run_response = requests.post('https://jobs.bluehawana.com/api/run-automation')
result = run_response.json()
```

### cURL Examples
```bash
# Get status
curl https://jobs.bluehawana.com/api/status

# Trigger automation
curl -X POST https://jobs.bluehawana.com/api/run-automation

# Get execution history
curl https://jobs.bluehawana.com/api/history
```

## 📊 Response Formats

All API responses use JSON format with consistent structure:

**Success Response:**
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2025-08-05T14:30:00"
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Error description",
  "timestamp": "2025-08-05T14:30:00"
}
```

## 🔒 Authentication

Currently, the API is open for your personal use. For production deployment with public access, consider adding:
- API key authentication
- Rate limiting
- IP whitelisting

## 📈 Rate Limits

- Manual automation triggers: 1 per 5 minutes
- Status checks: 100 per hour
- History requests: 50 per hour

## 🚀 WebSocket Support (Future)

Real-time updates for:
- Automation progress
- Live status changes
- Execution notifications

## 🛠️ Error Handling

Common error scenarios:
- `409 Conflict`: Automation already running
- `500 Internal Server Error`: System error
- `503 Service Unavailable`: Scheduler not running

## 📱 CORS Support

Cross-origin requests are enabled for integration with your main website at `bluehawana.com`.

Perfect for embedding in your personal website or creating mobile apps! 🌟