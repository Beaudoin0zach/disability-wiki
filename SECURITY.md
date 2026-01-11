# Security Hardening Guide

This document outlines security best practices and the current security configuration for the Disability Wiki deployment.

## Current Security Status

| Feature | Status | Details |
|---------|--------|---------|
| TLS/HTTPS | **Implemented** | Let's Encrypt, auto-renewal enabled |
| HTTP to HTTPS redirect | **Implemented** | 301 redirect on all HTTP requests |
| HSTS | **Implemented** | 1 year max-age with includeSubDomains |
| Security headers | **Implemented** | X-Frame-Options, CSP, XSS protection |
| Rate limiting | **Implemented** | 10r/s general, 1r/s login paths |
| Automated backups | **Implemented** | Daily at 3 AM UTC, 7/4/3 retention |
| Environment variables | **Implemented** | Credentials in .env, not in repo |
| Git history scrubbed | **Implemented** | Sensitive data removed from history |

---

## Table of Contents

- [Credential Management](#credential-management)
- [TLS/HTTPS Configuration](#tlshttps-configuration)
- [Rate Limiting](#rate-limiting)
- [Automated Backups](#automated-backups)
- [Security Checklist](#security-checklist)
- [Incident Response](#incident-response)

---

## Credential Management

### Environment Variables

**Never commit credentials to the repository.** All secrets are managed via environment variables.

#### Local Development

```bash
# Copy the template
cp .env.example .env

# Generate a strong password
openssl rand -base64 32

# Edit .env with your credentials
```

#### Production Server

Credentials are stored in `/opt/wiki/.env`:

```bash
# /opt/wiki/.env (actual file on server)
POSTGRES_PASSWORD=<32-character-random-password>
DB_PASS=<32-character-random-password>
```

The `docker-compose.yml` references these via `${VARIABLE}` syntax.

### Credential Rotation

Rotate database passwords quarterly:

```bash
# SSH into server
ssh user@your-server
cd /opt/wiki

# Generate new password
NEW_PASS=$(openssl rand -base64 32 | tr -d '/+=' | head -c 32)

# Update .env file
sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$NEW_PASS/" .env
sed -i "s/DB_PASS=.*/DB_PASS=$NEW_PASS/" .env

# Update PostgreSQL password
source .env
docker exec wiki_db_1 psql -U wiki -d wiki -c "ALTER USER wiki WITH PASSWORD '$DB_PASS';"

# Restart Wiki.js
docker-compose down && docker-compose up -d

# Verify
docker-compose logs wiki | tail -20
```

### SSH Key Management

- Use SSH keys instead of passwords for server access
- Disable password authentication in `/etc/ssh/sshd_config`:
  ```
  PasswordAuthentication no
  PermitRootLogin prohibit-password
  ```

---

## TLS/HTTPS Configuration

### Current Production Setup (Implemented)

TLS is configured via Nginx reverse proxy at `/etc/nginx/sites-available/disabilitywiki.org`.

**Certificate Details**:
- **Issuer**: Let's Encrypt
- **Domains**: disabilitywiki.org, www.disabilitywiki.org
- **Auto-renewal**: certbot timer (runs twice daily)
- **Expiry check**: `ssh user@your-server "certbot certificates"`

### Active Security Headers

```nginx
# Currently deployed on production
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

### Verify TLS Configuration

```bash
# Check certificate status
ssh user@your-server "certbot certificates"

# Test renewal
ssh user@your-server "certbot renew --dry-run"

# Check headers (from local machine)
curl -I https://disabilitywiki.org
```

---

## Rate Limiting

### Current Configuration (Implemented)

Rate limiting is configured in the Nginx site configuration.

```nginx
# Rate limiting zones (in nginx config)
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=addr:10m;
```

**Applied Limits**:
- **General requests**: 10 requests/second with burst of 20
- **Login/Admin paths** (`/login`, `/a`, `/graphql`): 1 request/second with burst of 5
- **Connection limit**: 10 concurrent connections per IP

### Fail2Ban (Optional Enhancement)

If additional protection is needed, install fail2ban:

```bash
apt install fail2ban

# Create /etc/fail2ban/jail.local
[wiki-login]
enabled = true
port = http,https
filter = wiki-login
logpath = /var/log/nginx/access.log
maxretry = 5
bantime = 3600
findtime = 600
```

---

## Automated Backups

### Current Configuration (Implemented)

Backups run automatically via cron at 3 AM UTC daily.

**Backup Script**: `/opt/wiki/backup.sh`
**Restore Script**: `/opt/wiki/restore.sh`
**Log File**: `/var/log/wiki-backup.log`

### Retention Policy

| Type | Retention | Created |
|------|-----------|---------|
| Daily | 7 backups | Every day |
| Weekly | 4 backups | Sundays |
| Monthly | 3 backups | 1st of month |

### Backup Location

```
/opt/wiki/backups/
├── daily/      # wiki-YYYYMMDD_HHMMSS.sql.gz
├── weekly/     # wiki-weekly-YYYYMMDD_HHMMSS.sql.gz
└── monthly/    # wiki-monthly-YYYYMMDD_HHMMSS.sql.gz
```

### Manual Backup

```bash
ssh user@your-server "/opt/wiki/backup.sh"
```

### Restore Procedure

```bash
ssh user@your-server

# Interactive restore (shows available backups)
/opt/wiki/restore.sh

# Or specify backup directly
/opt/wiki/restore.sh /opt/wiki/backups/daily/wiki-20260111_030000.sql.gz
```

### Backup Verification

Monthly verification checklist:

1. Download a recent backup to a test environment
2. Start a fresh PostgreSQL container
3. Restore the backup:
   ```bash
   gunzip -c wiki-backup.sql.gz | docker exec -i test_db psql -U wiki wiki
   ```
4. Start Wiki.js connected to the test database
5. Verify content is accessible and complete
6. Document the test results

---

## Security Checklist

### Initial Setup - COMPLETED

- [x] Generate strong, unique passwords for all services
- [x] Configure environment variables (never commit secrets)
- [x] Set up TLS/HTTPS with valid certificates
- [x] Configure HTTP to HTTPS redirect
- [x] Enable HSTS header
- [x] Set up reverse proxy (Nginx)
- [x] Configure rate limiting
- [x] Scrub git history of sensitive data
- [x] Set up automated backups

### Server Hardening - RECOMMENDED

- [ ] Disable root SSH login (use sudo user)
- [ ] Configure SSH key authentication only
- [ ] Enable UFW firewall (allow only 80, 443, 22)
- [ ] Configure automatic security updates
- [ ] Set up fail2ban

### Application Security

- [ ] Use strong admin password for Wiki.js
- [ ] Enable 2FA for admin accounts if available
- [ ] Review Wiki.js access permissions
- [ ] Configure CORS appropriately

### Ongoing Maintenance

- [x] Automated daily backups
- [ ] Rotate credentials quarterly
- [ ] Verify backups monthly
- [ ] Review access logs weekly
- [ ] Apply security updates promptly

### Monitoring - RECOMMENDED

- [ ] Set up uptime monitoring (e.g., UptimeRobot, Healthchecks.io)
- [ ] Configure log aggregation
- [ ] Set up alerts for failed login attempts
- [ ] Monitor disk space and resource usage

---

## Incident Response

### If Credentials Are Compromised

1. **Immediately** rotate all passwords (see Credential Rotation above)
2. Review access logs: `ssh user@your-server "tail -1000 /var/log/nginx/access.log | grep -i 'POST\|admin'"`
3. Check for unauthorized content changes in Wiki.js
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

### Backup Recovery

If you need to recover from a disaster:

```bash
# 1. Provision new server with Docker

# 2. Copy backup from off-site storage or old server

# 3. Set up Wiki.js with docker-compose

# 4. Restore database
gunzip -c backup.sql.gz | docker exec -i wiki_db_1 psql -U wiki wiki

# 5. Restart Wiki.js
docker-compose restart wiki
```

---

## Resources

- [Wiki.js Security Documentation](https://docs.requarks.io/security)
- [OWASP Security Guidelines](https://owasp.org/www-project-web-security-testing-guide/)
- [DigitalOcean Security Best Practices](https://docs.digitalocean.com/products/droplets/how-to/secure/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx Security Hardening](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)

---

*Last Updated: January 11, 2026*
