#!/bin/bash
# Setup Cloudflare DNS for jobs.bluehawana.com

# You need to set these environment variables:
# CLOUDFLARE_API_TOKEN - Your Cloudflare API token
# CLOUDFLARE_ZONE_ID - Your zone ID for bluehawana.com

# Or provide them as arguments
API_TOKEN="${1:-$CLOUDFLARE_API_TOKEN}"
ZONE_ID="${2:-$CLOUDFLARE_ZONE_ID}"

if [ -z "$API_TOKEN" ] || [ -z "$ZONE_ID" ]; then
    echo "❌ Missing required parameters!"
    echo ""
    echo "Usage: $0 <API_TOKEN> <ZONE_ID>"
    echo ""
    echo "Or set environment variables:"
    echo "  export CLOUDFLARE_API_TOKEN='your-token'"
    echo "  export CLOUDFLARE_ZONE_ID='your-zone-id'"
    echo ""
    echo "To get your API token:"
    echo "  1. Go to https://dash.cloudflare.com/profile/api-tokens"
    echo "  2. Create Token → Edit zone DNS → Use template"
    echo "  3. Select your zone (bluehawana.com)"
    echo "  4. Create Token"
    echo ""
    echo "To get your Zone ID:"
    echo "  1. Go to https://dash.cloudflare.com"
    echo "  2. Select bluehawana.com"
    echo "  3. Scroll down on Overview page - Zone ID is on the right"
    exit 1
fi

echo "🌐 Setting up DNS for jobs.bluehawana.com..."

# Create DNS A record
RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
     -H "Authorization: Bearer $API_TOKEN" \
     -H "Content-Type: application/json" \
     --data '{
       "type": "A",
       "name": "jobs",
       "content": "94.72.141.71",
       "ttl": 1,
       "proxied": false
     }')

# Check if successful
if echo "$RESPONSE" | grep -q '"success":true'; then
    echo "✅ DNS record created successfully!"
    echo ""
    echo "Record details:"
    echo "$RESPONSE" | grep -o '"name":"[^"]*"' | head -1
    echo "$RESPONSE" | grep -o '"content":"[^"]*"' | head -1
    echo ""
    echo "🎉 DNS is now configured!"
    echo ""
    echo "Wait 5-30 minutes for DNS propagation, then visit:"
    echo "  http://jobs.bluehawana.com"
    echo ""
    echo "Check DNS propagation:"
    echo "  nslookup jobs.bluehawana.com"
    echo "  or visit: https://dnschecker.org/#A/jobs.bluehawana.com"
else
    echo "❌ Failed to create DNS record"
    echo ""
    echo "Response:"
    echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
    echo ""
    
    # Check if record already exists
    if echo "$RESPONSE" | grep -q "already exists"; then
        echo "ℹ️  DNS record already exists!"
        echo ""
        echo "To update it, first get the record ID:"
        echo "  curl -X GET \"https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?name=jobs.bluehawana.com\" \\"
        echo "       -H \"Authorization: Bearer $API_TOKEN\""
    fi
fi
