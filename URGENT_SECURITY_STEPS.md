# 🚨 URGENT: Security Steps - Do This Immediately After Deployment

## Critical Security Issues

1. ❌ **Weak password:** "11" is extremely insecure
2. ❌ **Password exposed:** Shared in chat logs
3. ❌ **No SSH key protection:** Using password authentication

## Immediate Actions Required (After Deployment)

### Step 1: Change VPS Password (Do This First!)

```bash
# Connect to VPS
ssh -p 1025 harvad@94.72.141.71

# Change password
passwd

# Use a strong password:
# - At least 16 characters
# - Mix of uppercase, lowercase, numbers, symbols
# - Example: K8s#DevOps2026!Secure@VPS
```

### Step 2: Setup SSH Keys (No More Passwords)

```bash
# On your local machine:

# Generate SSH key
ssh-keygen -t ed25519 -C "harvad-vps-access"
# Save as: /Users/harvadlee/.ssh/id_ed25519_vps
# Set a strong passphrase

# Copy to VPS (use your NEW password)
ssh-copy-id -i ~/.ssh/id_ed25519_vps.pub -p 1025 harvad@94.72.141.71

# Test SSH key works
ssh -i ~/.ssh/id_ed25519_vps -p 1025 harvad@94.72.141.71

# Add to ~/.ssh/config for easy access
cat >> ~/.ssh/config << 'EOF'
Host jobhunter-vps
    HostName 94.72.141.71
    Port 1025
    User harvad
    IdentityFile ~/.ssh/id_ed25519_vps
EOF

# Now you can connect with just:
ssh jobhunter-vps
```

### Step 3: Disable Password Authentication

```bash
# Connect to VPS
ssh jobhunter-vps

# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Find and change these lines:
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes

# Save and restart SSH
sudo systemctl restart sshd
```

### Step 4: Install fail2ban (Prevent Brute Force)

```bash
# On VPS
sudo apt-get update
sudo apt-get install -y fail2ban

# Configure fail2ban
sudo nano /etc/fail2ban/jail.local

# Add this:
[sshd]
enabled = true
port = 1025
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

# Start fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Check status
sudo fail2ban-client status sshd
```

### Step 5: Setup UFW Firewall

```bash
# On VPS
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH on custom port
sudo ufw allow 1025/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

## Security Checklist

After completing the steps above:

- [ ] Changed VPS password from "11" to strong password
- [ ] Generated SSH key with passphrase
- [ ] Copied SSH key to VPS
- [ ] Tested SSH key authentication works
- [ ] Disabled password authentication in sshd_config
- [ ] Installed and configured fail2ban
- [ ] Setup UFW firewall
- [ ] Verified can still connect via SSH key
- [ ] Deleted password from any chat logs/notes

## Additional Recommendations

### 1. Enable Automatic Security Updates
```bash
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

### 2. Setup Log Monitoring
```bash
# Install logwatch
sudo apt-get install -y logwatch

# Send daily reports
sudo logwatch --output mail --mailto your@email.com --detail high
```

### 3. Regular Backups
```bash
# Backup script
cat > ~/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="$HOME/backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/lego-app.tar.gz" /var/www/lego-job-generator
echo "Backup created: $BACKUP_DIR/lego-app.tar.gz"
EOF

chmod +x ~/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup.sh") | crontab -
```

### 4. Monitor Failed Login Attempts
```bash
# View failed attempts
sudo grep "Failed password" /var/log/auth.log | tail -20

# Check who's logged in
who

# Check last logins
last -20
```

## Why This Matters for Job Hunting

A compromised VPS could:
- ❌ Take your job application site offline (miss opportunities!)
- ❌ Steal your resume data and personal information
- ❌ Use your server for malicious activities
- ❌ Damage your professional reputation

**Secure your VPS = Protect your job search!**

## Timeline

1. **NOW:** Deploy fixes (we'll do this next)
2. **Within 5 minutes:** Change password
3. **Within 30 minutes:** Setup SSH keys
4. **Within 1 hour:** Disable password auth & setup fail2ban
5. **Within 24 hours:** Complete all security steps

---

**Remember:** Your job hunting tool is only helpful if it's secure and available 24/7!
