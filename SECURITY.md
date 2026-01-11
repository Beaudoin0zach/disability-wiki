# Security Hardening Guide

This document outlines security best practices and hardening procedures for the Disability Wiki deployment.

## Table of Contents

- [Credential Management](#credential-management)
- [TLS/HTTPS Configuration](#tlshttps-configuration)
- [Reverse Proxy Setup](#reverse-proxy-setup)
- [Rate Limiting](#rate-limiting)
- [Backup Verification](#backup-verification)
- [Security Checklist](#security-checklist)

---

## Credential Management

### Environment Variables

**Never commit credentials to the repository.** Use environment variables for all secrets.

#### Local Development

```bash
# Copy the template
cp .env.example .env

# Generate a strong password
openssl rand -base64 32

# Edit .env with your credentials
```

#### Production Server

Create `/opt/wiki/.env` on the server:

```bash
# /opt/wiki/.env
POSTGRES_DB=wiki
POSTGRES_USER=wiki
POSTGRES_PASSWORD=<STRONG_RANDOM_PASSWORD>
DB_TYPE=postgres
DB_HOST=db
DB_PORT=5432
DB_USER=wiki
DB_PASS=<STRONG_RANDOM_PASSWORD>
DB_NAME=wiki
```

Update the production `docker-compose.yml` to use environment variables:

```yaml
services:
  db:
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  wiki:
    environment:
      DB_PASS: ${DB_PASS}
```

### Credential Rotation

Rotate database passwords quarterly:

1. Generate new password: `openssl rand -base64 32`
2. Update `.env` file on server
3. Restart containers: `docker-compose down && docker-compose up -d`
4. Verify Wiki.js connects successfully
5. Store old password securely for rollback if needed

### SSH Key Management

- Use SSH keys instead of passwords for server access
- Disable password authentication in `/etc/ssh/sshd_config`:
  ```
  PasswordAuthentication no
  PermitRootLogin prohibit-password
  ```
- Use a non-root user with sudo privileges when possible

---

## TLS/HTTPS Configuration

### Option 1: Nginx Reverse Proxy with Let's Encrypt (Recommended)

Install Certbot and Nginx on the server:

```bash
apt update
apt install nginx certbot python3-certbot-nginx
```

Create Nginx configuration `/etc/nginx/sites-available/wiki`:

```nginx
server {
    listen 80;
    server_name disabilitywiki.org www.disabilitywiki.org;

    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name disabilitywiki.org www.disabilitywiki.org;

    # SSL configuration (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/disabilitywiki.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/disabilitywiki.org/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # Modern TLS configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS (uncomment after testing)
    # add_header Strict-Transport-Security "max-age=63072000" always;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Enable the site and obtain certificate:

```bash
ln -s /etc/nginx/sites-available/wiki /etc/nginx/sites-enabled/
nginx -t
certbot --nginx -d disabilitywiki.org -d www.disabilitywiki.org
systemctl reload nginx
```

### Option 2: Traefik Reverse Proxy

Add Traefik to `docker-compose.yml`:

```yaml
services:
  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=false"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.letsencrypt.acme.email=your-email@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik_letsencrypt:/letsencrypt

  wiki:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.wiki.rule=Host(`disabilitywiki.org`)"
      - "traefik.http.routers.wiki.entrypoints=websecure"
      - "traefik.http.routers.wiki.tls.certresolver=letsencrypt"
      - "traefik.http.routers.wiki-http.rule=Host(`disabilitywiki.org`)"
      - "traefik.http.routers.wiki-http.entrypoints=web"
      - "traefik.http.routers.wiki-http.middlewares=https-redirect"
      - "traefik.http.middlewares.https-redirect.redirectscheme.scheme=https"
    # Remove ports section - Traefik handles external access

volumes:
  traefik_letsencrypt:
```

---

## Rate Limiting

### Nginx Rate Limiting

Add to `/etc/nginx/nginx.conf` in the `http` block:

```nginx
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=addr:10m;
```

Add to the server block:

```nginx
# General rate limiting
limit_req zone=general burst=20 nodelay;
limit_conn addr 10;

# Stricter rate limiting for login/admin paths
location ~ ^/(login|admin|graphql) {
    limit_req zone=login burst=5 nodelay;
    proxy_pass http://127.0.0.1:8080;
    # ... other proxy settings
}
```

### Fail2Ban Integration

Install and configure fail2ban:

```bash
apt install fail2ban
```

Create `/etc/fail2ban/jail.local`:

```ini
[wiki-login]
enabled = true
port = http,https
filter = wiki-login
logpath = /var/log/nginx/access.log
maxretry = 5
bantime = 3600
findtime = 600

[nginx-req-limit]
enabled = true
port = http,https
filter = nginx-req-limit
logpath = /var/log/nginx/error.log
maxretry = 10
bantime = 7200
findtime = 600
```

Create `/etc/fail2ban/filter.d/wiki-login.conf`:

```ini
[Definition]
failregex = ^<HOST> .* "(POST|GET) /(login|graphql).* 401
ignoreregex =
```

---

## Backup Verification

### Automated Backup Script

Create `/opt/wiki/backup.sh`:

```bash
#!/bin/bash
set -e

BACKUP_DIR="/opt/wiki/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
docker exec wiki_db_1 pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_DIR/wiki-$DATE.sql.gz"

# Verify backup is not empty
if [ ! -s "$BACKUP_DIR/wiki-$DATE.sql.gz" ]; then
    echo "ERROR: Backup file is empty!"
    exit 1
fi

# Test backup integrity
gunzip -t "$BACKUP_DIR/wiki-$DATE.sql.gz"
echo "Backup verified: wiki-$DATE.sql.gz"

# Remove old backups
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Sync to off-site storage (configure your backup destination)
# rsync -avz "$BACKUP_DIR/" backup-server:/backups/wiki/
# or
# aws s3 sync "$BACKUP_DIR/" s3://your-bucket/wiki-backups/
```

### Backup Verification Procedure

**Monthly verification checklist:**

1. Download a recent backup to a test environment
2. Start a fresh PostgreSQL container
3. Restore the backup:
   ```bash
   gunzip -c wiki-backup.sql.gz | docker exec -i test_db psql -U wiki wiki
   ```
4. Start Wiki.js connected to the test database
5. Verify content is accessible and complete
6. Document the test results

### Cron Schedule

Add to crontab (`crontab -e`):

```cron
# Daily backup at 3 AM
0 3 * * * /opt/wiki/backup.sh >> /var/log/wiki-backup.log 2>&1

# Weekly backup verification reminder (sends email)
0 9 * * 1 echo "Weekly reminder: Verify Wiki.js backup integrity" | mail -s "Backup Verification Reminder" admin@example.com
```

---

## Security Checklist

### Initial Setup

- [ ] Generate strong, unique passwords for all services
- [ ] Configure environment variables (never commit secrets)
- [ ] Set up TLS/HTTPS with valid certificates
- [ ] Configure HTTP to HTTPS redirect
- [ ] Enable HSTS header
- [ ] Set up reverse proxy (Nginx or Traefik)
- [ ] Configure rate limiting
- [ ] Set up fail2ban or similar

### Server Hardening

- [ ] Disable root SSH login (use sudo user)
- [ ] Configure SSH key authentication only
- [ ] Enable UFW firewall (allow only 80, 443, 22)
- [ ] Keep system packages updated
- [ ] Configure automatic security updates
- [ ] Set up monitoring/alerting

### Application Security

- [ ] Use strong admin password for Wiki.js
- [ ] Enable 2FA for admin accounts if available
- [ ] Review Wiki.js access permissions
- [ ] Limit admin panel access by IP if possible
- [ ] Configure CORS appropriately

### Ongoing Maintenance

- [ ] Rotate credentials quarterly
- [ ] Verify backups monthly
- [ ] Review access logs weekly
- [ ] Apply security updates promptly
- [ ] Review fail2ban bans weekly
- [ ] Test disaster recovery annually

### Monitoring

- [ ] Set up uptime monitoring (e.g., UptimeRobot, Healthchecks.io)
- [ ] Configure log aggregation
- [ ] Set up alerts for failed login attempts
- [ ] Monitor disk space and resource usage

---

## Incident Response

### If Credentials Are Compromised

1. **Immediately** rotate all passwords
2. Review access logs for unauthorized access
3. Check for unauthorized content changes
4. Restore from known-good backup if needed
5. Review and revoke any suspicious API keys or tokens
6. Document the incident and improve security measures

### If Server Is Compromised

1. Take the server offline immediately
2. Preserve logs and evidence
3. Provision a new server
4. Restore from known-good backup
5. Rotate all credentials
6. Review and fix the attack vector
7. Document lessons learned

---

## Resources

- [Wiki.js Security Documentation](https://docs.requarks.io/security)
- [OWASP Security Guidelines](https://owasp.org/www-project-web-security-testing-guide/)
- [DigitalOcean Security Best Practices](https://docs.digitalocean.com/products/droplets/how-to/secure/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx Security Hardening](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)

---

*Last Updated: January 11, 2026*
