# Proxy Setup for Job URL Scraping

## The Problem
Job boards like Indeed and LinkedIn block requests from datacenter/VPS IP addresses to prevent automated scraping. This causes the URL fetching feature to fail.

## Solution: Configure a Proxy

Add the `SCRAPING_PROXY` environment variable to your VPS to route scraping requests through a residential proxy.

### Step 1: Get a Proxy Service

Choose a residential proxy provider:
- **Bright Data** (formerly Luminati) - https://brightdata.com
- **Oxylabs** - https://oxylabs.io
- **Smartproxy** - https://smartproxy.com
- **IPRoyal** - https://iproyal.com (affordable option)

### Step 2: Configure the Environment Variable

On your VPS, add the proxy URL to your environment:

```bash
# Format: http://username:password@proxy-server:port
export SCRAPING_PROXY="http://user:pass@proxy.example.com:8080"
```

Or add it to your `.env` file:
```
SCRAPING_PROXY=http://user:pass@proxy.example.com:8080
```

### Step 3: Restart the Backend

```bash
# If using systemd
sudo systemctl restart jobhunter

# If using pm2
pm2 restart jobhunter-backend

# If using Docker
docker-compose restart backend
```

## Free Alternatives

If you don't want to pay for a proxy service:

### Option 1: Use Free Proxy Lists (Not Recommended)
Free proxies are unreliable and often blocked. Use at your own risk.

### Option 2: Rotate User Agents
Already implemented - the backend uses realistic browser headers.

### Option 3: Add Delays
Already implemented - requests have a 0.5s delay.

### Option 4: Use ScraperAPI (Free Tier)
ScraperAPI has a free tier with 1000 requests/month:
- Sign up: https://www.scraperapi.com
- Get API key
- Format: `http://api.scraperapi.com?api_key=YOUR_KEY&url=TARGET_URL`

## Testing the Proxy

Test if your proxy is working:

```bash
curl -X POST "https://jobs.bluehawana.com/api/analyze-job" \
  -H "Content-Type: application/json" \
  -d '{"jobUrl": "https://se.indeed.com/viewjob?jk=f3e78fb417a9af7f"}'
```

If successful, you'll get a JSON response with the job analysis.

## Troubleshooting

### Still getting 400 errors?
1. Check if the proxy URL is correct
2. Verify the proxy service is active
3. Check backend logs: `journalctl -u jobhunter -f`

### Proxy timeout?
Increase the timeout in `lego_api.py` or use a faster proxy server.
