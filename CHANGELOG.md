# Changelog

All notable changes to the Disability Wiki project are documented in this file.

---

## [2.5.310] - 2026-01-06

### Updated
- **Wiki.js Version**: Upgraded from 2.5.309 to 2.5.310
  - Updated local installation (Mac)
  - Updated live production server (DigitalOcean)
- **Repository Organization**: Major cleanup and restructuring
  - Created `scripts/` directory for Python utilities
  - Created `docs/` directory for documentation
  - Created `backups/` directory for archives
  - Moved files to appropriate locations

### Added
- **Documentation**:
  - `claude.md` - Comprehensive technical documentation covering:
    - DigitalOcean server details
    - Wiki.js deployment (local and live)
    - Docker configuration
    - Update procedures
    - Maintenance tasks
    - Troubleshooting guide
  - `QUICK_REFERENCE.md` - Fast command reference guide
  - `scripts/README.md` - Utility scripts documentation
  - `docs/README.md` - Documentation directory guide
  - Updated `README.md` with new structure

- **Scripts**:
  - `scripts/generate_descriptions.py` - SEO meta description generator
    - Updated 232 of 254 files with descriptions
  - `scripts/validate_wiki_links.py` - Internal link validator
    - Validated 1,758 links across 254 files
    - Found 15 broken links

- **Infrastructure**:
  - `.gitignore` improvements (Docker volumes, Python cache, backups)
  - `backups/.gitkeep` to maintain directory structure

### Fixed
- Meta descriptions added to 232 markdown files (155-160 characters each)
- Identified 15 broken internal links for repair
- Repository structure now properly organized

---

## [2.5.309] - 2026-01-06

### Updated
- **Wiki.js Version**: Upgraded live server from 2.5.308 to 2.5.309
  - Backed up configuration: `docker-compose.yml.backup-2.5.309`
  - Successfully pulled and deployed new image
  - Verified startup and database connectivity

### Changed
- Docker Compose configuration updated on live server
- Image version pinned to `requarks/wiki:2.5.309`

---

## [2.5.308] - Initial Deployment

### Added
- Initial Wiki.js installation on DigitalOcean
- PostgreSQL 13 database setup
- Docker Compose configuration
- 254 markdown content files across categories:
  - Benefits & Programs
  - Disability Rights
  - Housing Resources
  - Employment Rights
  - Education
  - Healthcare
  - Legal Resources
  - Assistive Technology
  - Transportation

### Infrastructure
- DigitalOcean Ubuntu 22.04 LTS droplet
- Docker containerization
- Port mapping: 8080:3000
- Database volume persistence

---

## Content Statistics

### Current Content (as of 2026-01-06)
- **Total Pages**: 254 markdown files
- **Total Links**: 1,758 internal links validated
- **SEO Coverage**: 232/254 files have meta descriptions (91%)
- **Link Health**: 15 broken links identified (99% valid)

### Categories
- Benefits (SSDI, SSI, Medicaid, Medicare, VA)
- Rights (ADA, IDEA, Section 504, Fair Housing)
- Housing (Accessible housing, modifications)
- Employment (Accommodations, workplace rights)
- Education (K-12, IEPs, 504 plans, college)
- Healthcare (Conditions, treatments, resources)
- Legal (Disability law, advocacy)
- Technology (Assistive tech, accessibility)
- Transportation (Transit, paratransit)
- Crisis (Emergency resources, hotlines)

---

## Maintenance History

### Database Backups
- None recorded yet - **Action Required**: Set up regular backup schedule

### Security Updates
- Server OS: Ubuntu 22.04.5 LTS (latest updates applied)
- Docker: Version on DigitalOcean v1.29.2
- Wiki.js: Version 2.5.310 (latest stable)

---

## Known Issues

### Broken Links (15 total)
- Listed in: `docs/wiki_link_validation_report.txt`
- **Priority**: Medium
- **Action**: Review and fix broken internal references

### Missing Features
- [ ] Automated backup system
- [ ] Monitoring/alerting for downtime
- [ ] SSL certificate (if not configured via Cloudflare)
- [ ] Email configuration for Wiki.js

---

## Planned Improvements

### Short Term (Next 30 days)
- [ ] Fix 15 broken internal links
- [ ] Set up automated weekly database backups
- [ ] Configure Wiki.js email notifications
- [ ] Add monitoring for server resources

### Medium Term (Next 90 days)
- [ ] Implement automated link checking (CI/CD)
- [ ] Set up staging environment
- [ ] Create content contribution guidelines
- [ ] Add search analytics

### Long Term (6+ months)
- [ ] Multi-language support
- [ ] Enhanced search with Elasticsearch
- [ ] Community contribution system
- [ ] API for programmatic access
- [ ] Mobile app integration

---

## Version Numbering

This project follows Wiki.js version numbers for releases. Additional changes are tracked by date.

**Format**: `[Wiki.js Version] - YYYY-MM-DD`

---

## Contributing

When making changes:
1. Update this CHANGELOG with your changes
2. Include date and version number
3. Categorize changes: Added, Changed, Deprecated, Removed, Fixed, Security
4. Link to related issues or PRs when applicable
5. Be specific and concise

---

*Changelog maintained since January 6, 2026*
