#!/bin/bash
# disability-wiki Backup Agent
# Automated backup of Wiki.js database and content
# Schedule: Daily at 3 AM via cron

set -e  # Exit on error

# Configuration
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_BASE_DIR="/Users/zachbeaudoin/disability-wiki/backups"
BACKUP_DIR="$BACKUP_BASE_DIR/$DATE"
PROJECT_DIR="/Users/zachbeaudoin/disability-wiki"
LOG_FILE="$BACKUP_BASE_DIR/backup.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# Create backup directories
mkdir -p "$BACKUP_DIR"
mkdir -p "$BACKUP_BASE_DIR"

log "Starting backup for disability-wiki..."

# 1. Check if Docker containers are running
log "Checking Docker container status..."
if ! docker ps | grep -q wiki-db; then
    log_error "PostgreSQL container (wiki-db) is not running!"
    exit 1
fi

if ! docker ps | grep -q wiki-app; then
    log_warning "Wiki.js container (wiki-app) is not running, but continuing..."
fi

# 2. Backup PostgreSQL database
log "Backing up PostgreSQL database..."
if docker exec wiki-db pg_dump -U wikijs wikijs > "$BACKUP_DIR/wikijs_db.sql" 2>> "$LOG_FILE"; then
    DB_SIZE=$(du -h "$BACKUP_DIR/wikijs_db.sql" | cut -f1)
    log_success "Database backup completed (${DB_SIZE})"
else
    log_error "Database backup failed!"
    exit 1
fi

# 3. Backup docker-compose.yml configuration
log "Backing up docker-compose.yml..."
if [ -f "$PROJECT_DIR/docker-compose.yml" ]; then
    cp "$PROJECT_DIR/docker-compose.yml" "$BACKUP_DIR/"
    log_success "Configuration backup completed"
else
    log_warning "docker-compose.yml not found"
fi

# 4. Backup any custom content/data directories if they exist
if [ -d "$PROJECT_DIR/content" ]; then
    log "Backing up content directory..."
    cp -r "$PROJECT_DIR/content" "$BACKUP_DIR/"
    log_success "Content directory backup completed"
fi

if [ -d "$PROJECT_DIR/data" ]; then
    log "Backing up data directory..."
    cp -r "$PROJECT_DIR/data" "$BACKUP_DIR/"
    log_success "Data directory backup completed"
fi

# 5. Create backup manifest
log "Creating backup manifest..."
cat > "$BACKUP_DIR/MANIFEST.txt" << EOF
Disability-Wiki Backup Manifest
================================
Backup Date: $TIMESTAMP
Hostname: $(hostname)
Wiki.js Version: $(docker exec wiki-app cat package.json 2>/dev/null | grep '"version"' | head -1 || echo "unknown")

Contents:
---------
EOF

ls -lh "$BACKUP_DIR" >> "$BACKUP_DIR/MANIFEST.txt"

# 6. Compress the backup
log "Compressing backup..."
cd "$BACKUP_BASE_DIR"
if tar -czf "${DATE}.tar.gz" "$DATE" 2>> "$LOG_FILE"; then
    COMPRESSED_SIZE=$(du -h "${DATE}.tar.gz" | cut -f1)
    log_success "Backup compressed to ${DATE}.tar.gz (${COMPRESSED_SIZE})"
    rm -rf "$BACKUP_DIR"
else
    log_error "Compression failed!"
    exit 1
fi

# 7. Rotate old backups (keep 7 daily, 4 weekly, 12 monthly)
log "Rotating old backups..."

# Keep daily backups for 7 days
DAILY_COUNT=$(find "$BACKUP_BASE_DIR" -name "*.tar.gz" -mtime -7 | wc -l)
find "$BACKUP_BASE_DIR" -name "*.tar.gz" -mtime +7 -mtime -30 -exec rm {} \; 2>> "$LOG_FILE"

# Keep weekly backups (Sunday) for 4 weeks
# Keep monthly backups (1st of month) for 12 months
MONTHLY_BACKUPS=$(find "$BACKUP_BASE_DIR" -name "*-01.tar.gz" -mtime +365 | wc -l)
find "$BACKUP_BASE_DIR" -name "*-01.tar.gz" -mtime +365 -exec rm {} \; 2>> "$LOG_FILE"

# Delete anything older than 1 year
find "$BACKUP_BASE_DIR" -name "*.tar.gz" -mtime +365 -exec rm {} \; 2>> "$LOG_FILE"

REMAINING_BACKUPS=$(find "$BACKUP_BASE_DIR" -name "*.tar.gz" | wc -l)
log_success "Backup rotation completed. ${REMAINING_BACKUPS} backups retained."

# 8. Calculate total backup size
TOTAL_SIZE=$(du -sh "$BACKUP_BASE_DIR" | cut -f1)
log "Total backup directory size: $TOTAL_SIZE"

# 9. Optional: Upload to cloud storage (uncomment and configure)
# Uncomment ONE of the following options and configure credentials

# Option A: AWS S3
# log "Uploading to AWS S3..."
# if aws s3 cp "$BACKUP_BASE_DIR/${DATE}.tar.gz" s3://your-bucket/disability-wiki-backups/; then
#     log_success "Uploaded to S3"
# else
#     log_error "S3 upload failed"
# fi

# Option B: Backblaze B2 via rclone
# log "Uploading to Backblaze B2..."
# if rclone copy "$BACKUP_BASE_DIR/${DATE}.tar.gz" b2:your-bucket/disability-wiki-backups/; then
#     log_success "Uploaded to Backblaze B2"
# else
#     log_error "B2 upload failed"
# fi

# Option C: DigitalOcean Spaces
# log "Uploading to DigitalOcean Spaces..."
# if aws s3 cp "$BACKUP_BASE_DIR/${DATE}.tar.gz" s3://your-space/disability-wiki-backups/ --endpoint-url=https://nyc3.digitaloceanspaces.com; then
#     log_success "Uploaded to DigitalOcean Spaces"
# else
#     log_error "Spaces upload failed"
# fi

# Option D: Rsync to remote server
# log "Uploading to remote server..."
# if rsync -avz "$BACKUP_BASE_DIR/${DATE}.tar.gz" user@remote-server:/backups/disability-wiki/; then
#     log_success "Uploaded to remote server"
# else
#     log_error "Remote upload failed"
# fi

# 10. Summary
log "=========================================="
log_success "Backup completed successfully!"
log "Backup file: ${DATE}.tar.gz"
log "Backup size: ${COMPRESSED_SIZE}"
log "Total backups: ${REMAINING_BACKUPS}"
log "=========================================="

exit 0
