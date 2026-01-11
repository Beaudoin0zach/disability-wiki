# Backup Agent Setup Guide

## Overview

The backup agent provides automated daily backups of your Wiki.js instance, including:
- PostgreSQL database
- Configuration files (docker-compose.yml)
- Content directories
- Automatic compression and rotation

## Quick Start

### 1. Test the Backup Script

```bash
cd /Users/zachbeaudoin/disability-wiki
./backup_agent.sh
```

This will create a backup in `/Users/zachbeaudoin/disability-wiki/backups/YYYY-MM-DD.tar.gz`

### 2. Verify the Backup

```bash
# List backups
ls -lh /Users/zachbeaudoin/disability-wiki/backups/

# Check backup contents
tar -tzf /Users/zachbeaudoin/disability-wiki/backups/YYYY-MM-DD.tar.gz

# Extract to verify (optional)
mkdir -p /tmp/backup-test
tar -xzf /Users/zachbeaudoin/disability-wiki/backups/YYYY-MM-DD.tar.gz -C /tmp/backup-test
ls -la /tmp/backup-test/
```

### 3. Schedule Daily Backups

Add to crontab to run daily at 3 AM:

```bash
crontab -e
```

Add this line:
```
0 3 * * * /Users/zachbeaudoin/disability-wiki/backup_agent.sh >> /Users/zachbeaudoin/disability-wiki/backups/backup.log 2>&1
```

To verify cron is set up:
```bash
crontab -l
```

## Backup Strategy

### Retention Policy

The script automatically retains:
- **Daily backups**: 7 days
- **Monthly backups**: 12 months (1st of each month)
- **Automatic deletion**: Backups older than 1 year

### What Gets Backed Up

1. **PostgreSQL Database** (`wikijs_db.sql`)
   - All wiki pages
   - User accounts
   - Settings and configuration

2. **Configuration Files**
   - `docker-compose.yml`

3. **Content Directories** (if they exist)
   - `/content/`
   - `/data/`

4. **Backup Manifest**
   - Timestamp
   - File list
   - Wiki.js version

### Backup Size Expectations

- Database: ~5-50 MB (depending on content volume)
- Compressed backup: ~2-20 MB
- Monthly storage: ~50-200 MB

## Cloud Upload Options

The script includes commented-out code for cloud uploads. Uncomment and configure ONE option:

### Option A: AWS S3

```bash
# Install AWS CLI
brew install awscli

# Configure credentials
aws configure

# Uncomment in backup_agent.sh (lines ~150-154)
```

### Option B: Backblaze B2 (via rclone)

```bash
# Install rclone
brew install rclone

# Configure B2
rclone config

# Uncomment in backup_agent.sh (lines ~156-161)
```

### Option C: DigitalOcean Spaces

```bash
# Install AWS CLI (compatible with Spaces)
brew install awscli

# Configure with Spaces credentials
aws configure

# Uncomment in backup_agent.sh (lines ~163-168)
```

### Option D: Remote Server (rsync)

```bash
# Set up SSH key authentication
ssh-keygen -t ed25519
ssh-copy-id user@remote-server

# Uncomment in backup_agent.sh (lines ~170-175)
```

## Restore Procedures

### Full Database Restore

```bash
# 1. Extract backup
cd /Users/zachbeaudoin/disability-wiki/backups
tar -xzf YYYY-MM-DD.tar.gz

# 2. Stop Wiki.js
cd /Users/zachbeaudoin/disability-wiki
docker compose down

# 3. Restore database
docker compose up -d wiki-db
sleep 5
docker exec -i wiki-db psql -U wikijs wikijs < backups/YYYY-MM-DD/wikijs_db.sql

# 4. Restart Wiki.js
docker compose up -d
```

### Restore Specific Tables

```bash
# Extract backup
tar -xzf backups/YYYY-MM-DD.tar.gz

# Restore specific table
docker exec -i wiki-db psql -U wikijs wikijs << EOF
DELETE FROM pages WHERE id = 123;
EOF

cat backups/YYYY-MM-DD/wikijs_db.sql | grep "INSERT INTO pages" | docker exec -i wiki-db psql -U wikijs wikijs
```

### Restore Configuration Only

```bash
# Extract backup
tar -xzf backups/YYYY-MM-DD.tar.gz

# Copy configuration
cp backups/YYYY-MM-DD/docker-compose.yml /Users/zachbeaudoin/disability-wiki/

# Restart containers
docker compose up -d
```

## Monitoring & Maintenance

### Check Backup Logs

```bash
# View recent backup logs
tail -50 /Users/zachbeaudoin/disability-wiki/backups/backup.log

# View full log
cat /Users/zachbeaudoin/disability-wiki/backups/backup.log

# Search for errors
grep ERROR /Users/zachbeaudoin/disability-wiki/backups/backup.log
```

### Manual Backup Before Updates

Always create a manual backup before major updates:

```bash
cd /Users/zachbeaudoin/disability-wiki
./backup_agent.sh
```

### Disk Space Monitoring

```bash
# Check backup directory size
du -sh /Users/zachbeaudoin/disability-wiki/backups

# Check available disk space
df -h /Users/zachbeaudoin
```

## Troubleshooting

### "PostgreSQL container (wiki-db) is not running!"

```bash
# Check container status
docker ps -a | grep wiki

# Start containers
cd /Users/zachbeaudoin/disability-wiki
docker compose up -d
```

### "Permission denied" errors

```bash
# Make script executable
chmod +x /Users/zachbeaudoin/disability-wiki/backup_agent.sh

# Fix backup directory permissions
chmod 755 /Users/zachbeaudoin/disability-wiki/backups
```

### Cron job not running

```bash
# Check if cron is running
ps aux | grep cron

# View cron logs (macOS)
log show --predicate 'eventMessage contains "cron"' --last 1d

# Test cron environment
* * * * * env > /tmp/cron-env.txt
```

### Backup file too large

```bash
# Check what's consuming space
tar -tzf backups/YYYY-MM-DD.tar.gz | xargs -I {} ls -lh {}

# Exclude large files (edit backup_agent.sh)
tar --exclude='*.log' --exclude='*.tmp' -czf ...
```

## Security Best Practices

1. **Encrypt backups** before uploading to cloud:
   ```bash
   gpg --encrypt --recipient your@email.com backup.tar.gz
   ```

2. **Restrict backup permissions**:
   ```bash
   chmod 600 /Users/zachbeaudoin/disability-wiki/backups/*.tar.gz
   ```

3. **Test restores monthly** to ensure backups are valid

4. **Store offsite backups** in at least one cloud location

5. **Keep backup credentials secure** (use keychain/vault)

## Testing Checklist

- [ ] Manual backup runs successfully
- [ ] Backup file can be extracted
- [ ] Database restore works
- [ ] Cron job runs on schedule
- [ ] Log file records all operations
- [ ] Old backups are automatically deleted
- [ ] Cloud upload works (if configured)
- [ ] Email alerts work (if configured)

## Support

If you encounter issues:

1. Check the log file: `/Users/zachbeaudoin/disability-wiki/backups/backup.log`
2. Verify Docker containers are running: `docker ps`
3. Test manually: `./backup_agent.sh`
4. Check disk space: `df -h`

---

**Next Steps**: After setting up the backup agent, proceed to implement the monitoring agents for proactive alerts.
