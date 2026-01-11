# Disability Wiki - Technical Documentation

## Project Overview

This repository contains the infrastructure and content for **disabilitywiki.org**, a comprehensive Wiki.js-powered knowledge base for disability rights, resources, and support information.

**Live Site**: https://disabilitywiki.org
**Repository**: https://github.com/Beaudoin0zach/disability-wiki
**Current Version**: Wiki.js 2.5.310

---

## Server Information

### Production Server
- **Provider**: DigitalOcean
- **OS**: Ubuntu 22.04.5 LTS (Jammy Jellyfish)
- **RAM**: 2GB
- **Storage**: 25GB SSD

> **Note**: Server IP and SSH credentials are stored securely outside this repository. See your password manager or infrastructure documentation for access details.

---

## Wiki.js Deployment

### Live Production Setup

**Location**: `/opt/wiki/`
**Version**: Wiki.js 2.5.310
**Database**: PostgreSQL 13
**Port Mapping**: 8080:3000 (external:internal)

> **Security Note**: Production credentials are managed via environment variables on the server. Never commit credentials to this repository.

#### Container Names
- **Wiki App**: `wiki_wiki_1`
- **Database**: `wiki_db_1`
- **Network**: `wiki_default`

### Local Development Setup

**Location**: Project root directory
**Version**: Wiki.js 2.5.310
**Database**: PostgreSQL 15
**Port Mapping**: 8080:3000 (localhost:8080)

#### Setup Instructions

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with secure credentials:
   ```bash
   # Generate a strong password
   openssl rand -base64 32
   ```

3. Start the containers:
   ```bash
   export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
   docker compose up -d
   ```

4. Access locally at http://localhost:8080

#### Container Names
- **Wiki App**: `wiki-app`
- **Database**: `wiki-db`
- **Network**: `disability-wiki_default`

#### Management Commands
```bash
# View logs
docker compose logs -f wiki

# Stop containers
docker compose down

# Restart
docker compose restart
```

---

## Deployment Commands

### Update Local Wiki.js

```bash
cd /path/to/disability-wiki

# Edit docker-compose.yml to update version number
# Change: image: requarks/wiki:2.5.XXX

# Apply update
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
docker compose down
docker compose pull wiki
docker compose up -d
docker compose logs -f wiki
```

### Update Live Wiki.js

```bash
# SSH into server (use your secure access method)
ssh user@your-server

# Navigate to Wiki.js directory
cd /opt/wiki

# Backup current configuration
cp docker-compose.yml docker-compose.yml.backup-$(date +%Y%m%d)

# Edit docker-compose.yml to update version
# Change: image: requarks/wiki:2.5.XXX

# Apply update
docker-compose down
docker-compose pull wiki
docker-compose up -d
docker-compose logs -f wiki
```

### Database Backup (Live Server)

```bash
# SSH into server
ssh user@your-server

# Create backup directory
mkdir -p /opt/wiki/backups

# Backup database (use your actual DB user)
docker exec wiki_db_1 pg_dump -U $DB_USER $DB_NAME > /opt/wiki/backups/wiki-backup-$(date +%Y%m%d).sql

# Verify backup
ls -lh /opt/wiki/backups/
```

### Database Restore (if needed)

```bash
# Restore from backup
cat /opt/wiki/backups/wiki-backup-YYYYMMDD.sql | docker exec -i wiki_db_1 psql -U $DB_USER $DB_NAME
```

---

## Repository Structure

```
disability-wiki/
├── .claude/                      # Claude Code configuration
├── .git/                         # Git repository
├── .github/                      # GitHub workflows
│   └── workflows/
│       └── hugo.yml             # Auto-deploy workflow (if used)
├── archetypes/                   # Hugo archetypes (legacy)
├── backups/                      # Archive storage (not tracked)
├── content/                      # Hugo content (legacy - mixed project)
├── disability-wiki/              # Wiki.js markdown exports (254 files)
│   ├── benefits/
│   ├── rights/
│   ├── housing/
│   ├── employment/
│   ├── education/
│   ├── conditions/
│   └── ...                      # Additional categories
├── docs/                         # Project documentation
├── editorial-theme/              # Custom Hugo theme (legacy)
├── scripts/                      # Python utilities
│   ├── generate_descriptions.py # SEO meta description generator
│   └── validate_wiki_links.py   # Internal link validator
├── static/                       # Static assets
├── themes/                       # Hugo themes (legacy)
├── .env.example                  # Environment variable template
├── .gitignore                    # Git ignore rules
├── CNAME                         # Domain configuration
├── README.md                     # Project README
├── SECURITY.md                   # Security hardening guide
├── claude.md                     # This file
├── docker-compose.yml            # Local Wiki.js configuration
├── hugo.toml                     # Hugo configuration (legacy)
└── install_wikijs.sh             # Automated Wiki.js installer

TOTAL FILES: 254 markdown files in disability-wiki/
```

### Content Organization

The `disability-wiki/` directory contains 254 markdown files exported from Wiki.js:

**Main Categories**:
- **Benefits** (SSDI, SSI, Medicaid, Medicare, VA benefits)
- **Rights** (ADA, IDEA, Section 504, Fair Housing)
- **Housing** (Accessible housing, modifications, support)
- **Employment** (Workplace accommodations, rights, resources)
- **Education** (K-12, college, IEPs, 504 plans)
- **Healthcare** (Conditions, treatments, resources)
- **Crisis** (Emergency resources, hotlines)
- **Legal** (Disability law, advocacy)
- **Technology** (Assistive tech, accessibility)
- **Transportation** (Accessible transit, paratransit)

---

## Utility Scripts

### 1. Meta Description Generator

**Location**: `scripts/generate_descriptions.py`

Automatically generates SEO-friendly meta descriptions (155-160 characters) for all markdown files missing descriptions.

```bash
# Run the generator
python3 scripts/generate_descriptions.py
```

**Features**:
- Extracts first 1-2 paragraphs from content
- Removes markdown formatting
- Truncates to 158 characters maximum
- Updates YAML frontmatter automatically
- Shows preview before applying changes

### 2. Internal Link Validator

**Location**: `scripts/validate_wiki_links.py`

Validates all internal Wiki.js links across markdown files.

```bash
# Run the validator
python3 scripts/validate_wiki_links.py
```

**Features**:
- Validates all `[text](/path)` internal links
- Checks frontmatter for missing descriptions
- Suggests potential cross-links
- Generates detailed report

### 3. Wiki.js Installer

**Location**: `install_wikijs.sh`

Automated installation script for local Wiki.js development.

```bash
chmod +x install_wikijs.sh
./install_wikijs.sh
```

**Features**:
- Checks for Docker installation
- Offers Homebrew installation option
- Verifies Docker is running
- Pulls Wiki.js image
- Starts containers automatically
- Shows access URL and management commands

---

## Maintenance Tasks

### Weekly
- [ ] Check Wiki.js logs for errors
- [ ] Monitor disk usage on server
- [ ] Verify site accessibility

### Monthly
- [ ] Backup database from live server
- [ ] Check for Wiki.js updates: https://github.com/Requarks/wiki/releases
- [ ] Run link validator
- [ ] Review server resource usage

### Quarterly
- [ ] Full database export and download
- [ ] Review and update documentation
- [ ] Clean up old backups
- [ ] Security updates on server

---

## Common Operations

### Check Wiki.js Status (Live)
```bash
ssh user@your-server "cd /opt/wiki && docker-compose ps"
```

### Restart Wiki.js (Live)
```bash
ssh user@your-server "cd /opt/wiki && docker-compose restart wiki"
```

### View Wiki.js Logs (Live)
```bash
ssh user@your-server "cd /opt/wiki && docker-compose logs -f wiki"
```

### Export Content from Wiki.js
1. Log into Wiki.js admin panel
2. Navigate to Administration → Storage
3. Configure Git storage target
4. Sync content to export markdown files

### Add New Content
1. Log into Wiki.js (local or production)
2. Click "Create New Page"
3. Select page category and path
4. Write content using markdown editor
5. Add metadata (title, description, tags)
6. Publish

---

## Docker Notes

### Local (Mac) Docker Setup
- **Docker Desktop**: `/Applications/Docker.app`
- **CLI Path**: `/Applications/Docker.app/Contents/Resources/bin/docker`
- **Add to PATH**: `export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"`

### Server Docker Version
- **Server**: Docker Compose v1.29.2 (uses `docker-compose` with hyphen)
- **Local**: Docker Compose v2.x (uses `docker compose` with space)

---

## Version History

### 2.5.310 (Current)
- Updated: January 6, 2026
- Both local and live installations
- Latest stable release

### 2.5.309
- Previous version

### 2.5.308
- Original live server version
- Initial deployment

---

## Troubleshooting

### Docker Not Found (Mac)
```bash
# Add Docker to PATH
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"

# Or add to .zshrc permanently
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Database Connection Failed
```bash
# Check database container is running
docker compose ps

# View database logs
docker compose logs db

# Restart database
docker compose restart db
```

### Wiki.js Won't Start
```bash
# Check logs for errors
docker compose logs wiki

# Common fixes:
# 1. Ensure database is healthy
docker compose ps

# 2. Restart both containers
docker compose restart

# 3. Full restart
docker compose down
docker compose up -d
```

### Port Already in Use
```bash
# Check what's using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml:
# ports:
#   - "8081:3000"  # Changed from 8080 to 8081
```

---

## Security

See [SECURITY.md](./SECURITY.md) for:
- Production hardening guidelines
- TLS/HTTPS setup with reverse proxy
- Rate limiting configuration
- Backup verification procedures
- Credential rotation procedures

---

## Resources

### Wiki.js Documentation
- **Official Docs**: https://docs.requarks.io/
- **GitHub**: https://github.com/Requarks/wiki
- **Docker Hub**: https://hub.docker.com/r/requarks/wiki

### DigitalOcean
- **Control Panel**: https://cloud.digitalocean.com/
- **Documentation**: https://docs.digitalocean.com/

### Repository
- **GitHub**: https://github.com/Beaudoin0zach/disability-wiki
- **Issues**: https://github.com/Beaudoin0zach/disability-wiki/issues

---

## Contact & Support

**Repository Owner**: Zach Beaudoin
**GitHub**: @Beaudoin0zach

---

*Last Updated: January 11, 2026*
*Wiki.js Version: 2.5.310*
