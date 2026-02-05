# 🚀 Quick Deploy Reference

## One-Command Deploy (Recommended)

```bash
./deploy/deploy_with_consistency.sh && sleep 5 && ./deploy/verify_consistency.sh
```

**What happens:**
1. Commits & pushes to git
2. SSH to server (ONE MFA prompt!)
3. Pulls code, installs deps, atomic restart
4. Waits 5 seconds
5. Verifies consistency with 20 test requests

**Expected output:**
```
✅ Code pushed to git
📥 Pulling latest code from git...
📦 Installing dependencies...
🔄 Atomic restart...
✅ Service is healthy!
✅ DEPLOYMENT COMPLETE!

✅ NVIDIA: All 10 requests returned consistent results
✅ Microsoft: All 10 requests returned consistent results
✅ ALL TESTS PASSED - 100% consistency achieved!
```

## Troubleshooting

### If deployment fails:
```bash
# Check what went wrong
ssh root@jobs.bluehawana.com 'sudo journalctl -u lego-job-generator -n 50'
```

### If consistency test fails:
```bash
# Run atomic restart only
ssh root@jobs.bluehawana.com 'bash -s' < deploy/atomic_restart.sh

# Test again
./deploy/verify_consistency.sh
```

### Nuclear option (if everything is broken):
```bash
ssh root@jobs.bluehawana.com << 'EOF'
sudo systemctl stop lego-job-generator
sudo pkill -9 -f gunicorn
sleep 2
cd /var/www/lego-job-generator
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl start lego-job-generator
EOF
```

## Quick Tests

### Test NVIDIA:
```bash
curl -X POST http://jobs.bluehawana.com/api/analyze-job \
  -H 'Content-Type: application/json' \
  -d '{"job_description":"NVIDIA\nCloud Solution Architect"}' | jq .company_name
```

### Test Microsoft:
```bash
curl -X POST http://jobs.bluehawana.com/api/analyze-job \
  -H 'Content-Type: application/json' \
  -d '{"job_description":"Microsoft\nCloud Solution Architect"}' | jq .company_name
```

Both should return the correct company name consistently.

## MFA Count

| Old Method (rsync) | New Method (git) |
|-------------------|------------------|
| 3-5 MFA prompts 😫 | 1 MFA prompt 😊 |

## Why This Works

**Problem:** Multiple gunicorn workers reload at different times
- Worker 1: New code ✅
- Worker 2: Old code ❌  
- Worker 3: Old code ❌

**Solution:** Atomic restart stops ALL workers, then starts fresh
- All workers: New code ✅
- All workers: New code ✅
- All workers: New code ✅

**Result:** 100% consistency guaranteed! 🎯
