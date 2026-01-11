# Quick Reference Guide

Fast reference for common Disability Wiki operations.

---

## 🚀 Quick Start

### Start Local Wiki
```bash
cd /Users/zachbeaudoin/disability-wiki
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
docker compose up -d
open http://localhost:8080
```

### SSH to Live Server
```bash
ssh root@167.71.97.167
cd /opt/wiki
```

---

## 📦 Docker Commands

### Local (Mac)
```bash
# Start containers
docker compose up -d

# Stop containers
docker compose down

# View logs
docker compose logs -f wiki

# Restart Wiki.js
docker compose restart wiki

# Check status
docker compose ps

# Pull new image
docker compose pull wiki
```

### Live Server
```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f wiki

# Restart Wiki.js
docker-compose restart wiki

# Check status
docker-compose ps

# Pull new image
docker-compose pull wiki
```

**Note**: Live server uses `docker-compose` (hyphen), local uses `docker compose` (space)

---

## 🔄 Update Wiki.js

### Local
```bash
# Edit docker-compose.yml, change version number
# image: requarks/wiki:2.5.XXX

export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
docker compose down
docker compose pull wiki
docker compose up -d
docker compose logs -f wiki
```

### Live
```bash
ssh root@167.71.97.167
cd /opt/wiki

# Backup config
cp docker-compose.yml docker-compose.yml.backup-$(date +%Y%m%d)

# Edit docker-compose.yml, change version number
# image: requarks/wiki:2.5.XXX

docker-compose down
docker-compose pull wiki
docker-compose up -d
docker-compose logs -f wiki
```

---

## 💾 Database Backup

### Create Backup (Live)
```bash
ssh root@167.71.97.167
mkdir -p /opt/wiki/backups
docker exec wiki_db_1 pg_dump -U wiki wiki > /opt/wiki/backups/wiki-backup-$(date +%Y%m%d).sql
```

### Download Backup
```bash
scp root@167.71.97.167:/opt/wiki/backups/wiki-backup-*.sql ~/Downloads/
```

### Restore Backup
```bash
ssh root@167.71.97.167
cat /opt/wiki/backups/wiki-backup-YYYYMMDD.sql | docker exec -i wiki_db_1 psql -U wiki wiki
```

---

## 🔧 Utility Scripts

### Generate Meta Descriptions
```bash
cd /Users/zachbeaudoin/disability-wiki
python3 scripts/generate_descriptions.py
```

### Validate Links
```bash
cd /Users/zachbeaudoin/disability-wiki
python3 scripts/validate_wiki_links.py
cat docs/wiki_link_validation_report.txt
```

---

## 🔍 Monitoring

### Check Wiki.js Status (Live)
```bash
ssh root@167.71.97.167 "cd /opt/wiki && docker-compose ps"
```

### Check Server Resources
```bash
ssh root@167.71.97.167 "df -h / && free -h"
```

### View Recent Logs (Live)
```bash
ssh root@167.71.97.167 "cd /opt/wiki && docker-compose logs --tail=100 wiki"
```

### Follow Logs in Real-Time
```bash
ssh root@167.71.97.167 "cd /opt/wiki && docker-compose logs -f wiki"
```

---

## 🐛 Troubleshooting

### Docker Not Found (Mac)
```bash
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
```

### Make It Permanent
```bash
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Database Won't Connect
```bash
docker compose logs db
docker compose restart db
```

### Port 8080 Already in Use
```bash
lsof -i :8080
kill -9 <PID>
```

### Container Won't Start
```bash
# Check logs for errors
docker compose logs wiki

# Full restart
docker compose down
docker compose up -d
```

### Wiki.js Shows Error Page
```bash
# Check database is healthy
docker compose ps

# Restart both containers
docker compose restart
```

---

## 📝 Git Operations

### Check Status
```bash
git status
```

### Commit Changes
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### View Recent Commits
```bash
git log --oneline -10
```

### Create Branch
```bash
git checkout -b feature-name
```

---

## 🌐 URLs

| Environment | URL |
|-------------|-----|
| **Live Wiki** | http://disabilitywiki.org |
| **Local Wiki** | http://localhost:8080 |
| **GitHub Repo** | https://github.com/Beaudoin0zach/disability-wiki |

---

## 📊 File Locations

| Item | Location |
|------|----------|
| **Local repo** | `/Users/zachbeaudoin/disability-wiki/` |
| **Live Wiki.js** | `/opt/wiki/` (on 167.71.97.167) |
| **Docker config (local)** | `/Users/zachbeaudoin/disability-wiki/docker-compose.yml` |
| **Docker config (live)** | `/opt/wiki/docker-compose.yml` |
| **Content files** | `/Users/zachbeaudoin/disability-wiki/disability-wiki/` |
| **Scripts** | `/Users/zachbeaudoin/disability-wiki/scripts/` |
| **Backups (live)** | `/opt/wiki/backups/` |

---

## 🔑 Server Info

| Detail | Value |
|--------|-------|
| **IP Address** | 167.71.97.167 |
| **OS** | Ubuntu 22.04.5 LTS |
| **RAM** | 2GB |
| **Disk** | 25GB SSD |
| **SSH** | `ssh root@167.71.97.167` |

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Project overview and quick start |
| **claude.md** | Complete technical documentation |
| **QUICK_REFERENCE.md** | This file - command cheatsheet |
| **scripts/README.md** | Utility scripts documentation |
| **docs/** | Additional documentation and reports |

---

## ⚡ One-Liners

```bash
# Check if Wiki.js is running (live)
ssh root@167.71.97.167 "docker ps | grep wiki"

# Get Wiki.js version (local)
docker compose logs wiki 2>&1 | grep "Wiki.js" | head -1

# Count markdown files
find disability-wiki -name "*.md" | wc -l

# Check disk usage (live)
ssh root@167.71.97.167 "du -sh /opt/wiki/*"

# Test if site is accessible
curl -I http://disabilitywiki.org

# Find broken links in reports
grep "Target not found" docs/wiki_link_validation_report.txt

# List recent backups (live)
ssh root@167.71.97.167 "ls -lth /opt/wiki/backups/"
```

---

*Quick Reference v1.0 - January 6, 2026*
