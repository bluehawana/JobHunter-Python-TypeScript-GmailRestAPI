#!/bin/bash
# Deploy to VPS using git pull (recommended method)

echo "🚀 Deploying to jobs.bluehawana.com via Git..."
echo ""

# First, commit and push changes locally
echo "📝 Step 1: Commit and push local changes..."
echo "Current git status:"
git status --short

read -p "Do you want to commit and push changes? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter commit message: " commit_msg
    git add .
    git commit -m "$commit_msg"
    git push origin main
    echo "✅ Changes pushed to GitHub"
else
    echo "⚠️  Skipping commit. Make sure changes are already pushed!"
fi

echo ""
echo "📥 Step 2: Pull changes on VPS and restart service..."

# SSH to VPS and pull changes
ssh -p 1025 harvad@94.72.141.71 << 'EOF'
cd /var/www/lego-job-generator

echo "📥 Pulling latest changes from GitHub..."
git pull origin main

echo "🔄 Restarting service..."
sudo systemctl restart lego-job-generator

echo "✅ Service restarted"
echo ""
echo "📊 Service status:"
sudo systemctl status lego-job-generator --no-pager | head -15

echo ""
echo "✅ Deployment complete!"
EOF

echo ""
echo "🎉 Deployment finished!"
echo "🌐 Test at: http://jobs.bluehawana.com"
echo ""
echo "📝 Verification steps:"
echo "  1. Go to http://jobs.bluehawana.com"
echo "  2. Paste Göteborgs Stad job URL or description"
echo "  3. Verify company shows 'Göteborgs Stad' (not 'att')"
echo "  4. Generate cover letter and check header"
