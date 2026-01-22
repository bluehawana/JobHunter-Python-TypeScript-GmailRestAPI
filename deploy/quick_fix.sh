#!/bin/bash
# One-command fix for VPS

echo "🚑 Quick Fix for VPS..."

ssh -p 1025 harvad@94.72.141.71 'cd /var/www/lego-job-generator && git pull origin main && sudo systemctl restart lego-job-generator && echo "✅ Done! Test at http://jobs.bluehawana.com"'
