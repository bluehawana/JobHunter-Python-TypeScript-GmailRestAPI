#!/bin/bash
# Check if VPS has git repo configured correctly

SERVER="root@jobs.bluehawana.com"
PORT="22"

echo "🔍 Checking VPS Git Configuration"
echo "=================================="
echo ""

ssh -t $SERVER -p $PORT << 'ENDSSH'
echo "📂 Checking git repository..."
cd /var/www/lego-job-generator

if [ -d .git ]; then
    echo "✅ Git repository exists"
    echo ""
    echo "📍 Current branch:"
    git branch --show-current
    echo ""
    echo "🔗 Remote URL:"
    git remote -v
    echo ""
    echo "📊 Git status:"
    git status
    echo ""
    echo "📝 Last commit:"
    git log -1 --oneline
else
    echo "❌ No git repository found!"
    echo ""
    echo "🔧 Setting up git repository..."
    git init
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    git fetch origin
    git checkout -b main origin/main
    echo "✅ Git repository initialized"
fi
ENDSSH
