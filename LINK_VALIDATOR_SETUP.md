# Link Validator Agent Setup Guide

## Overview

The link validator agent scans all 284 markdown files in the Disability Wiki for broken links:
- **Internal links**: Validates Wiki.js paths (e.g., `/employment/job-searching`)
- **External links**: Checks HTTP status of external URLs
- **Health scoring**: Calculates overall link health (0-100%)
- **Detailed reporting**: JSON and text reports with broken link locations

## Quick Start

### 1. Install Dependencies (Optional)

For external link validation, install `requests`:

```bash
pip3 install requests
```

**Note**: Internal link validation works without dependencies.

### 2. Run the Validator

```bash
cd /Users/zachbeaudoin/disability-wiki
python3 link_validator_agent.py
```

### 3. View Results

```bash
# View JSON report
cat link_validation_report.json | python3 -m json.tool

# View text report
cat link_validation_report.txt
```

## Command Options

### Basic Usage

```bash
# Full validation (internal + external)
python3 link_validator_agent.py

# Internal links only (faster, no dependencies)
python3 link_validator_agent.py --skip-external

# Custom wiki root
python3 link_validator_agent.py --wiki-root /path/to/disability-wiki

# Custom output file
python3 link_validator_agent.py --output my_report.json
```

## What Gets Validated

### Internal Links ✅

**Format**: `[text](/path/to/page)`

**Examples**:
- `[Job Searching](/employment/job-searching-with-a-disability)`
- `[SSDI](/benefits/ssdi)`
- `[ADA Rights](/rights/ada)`

**Validation**:
- Checks if target file exists in `disability-wiki/` directory
- Tries multiple file locations:
  - `disability-wiki/path/to/page.md`
  - `disability-wiki/path/to/page/index.md`
- Reports missing targets with file and line number

### External Links ✅

**Format**: `[text](https://example.com)`

**Examples**:
- `[Social Security Administration](https://www.ssa.gov)`
- `[ADA.gov](https://www.ada.gov)`
- `[CDC Disability](https://www.cdc.gov/disability)`

**Validation**:
- Checks HTTP status code (< 400 = valid)
- Uses HEAD requests (efficient, doesn't download content)
- Falls back to GET if server doesn't support HEAD
- 10-second timeout per URL
- Parallel validation (10 concurrent requests)
- Rate limiting (0.5s delay between requests)
- Caches results to avoid duplicate checks

**Common Errors**:
- `HTTP 404`: Page not found
- `HTTP 403`: Forbidden
- `Timeout`: Server didn't respond in 10 seconds
- `Connection failed`: DNS or network error

### Anchor Links 🔗

**Format**: `[text](#section)`

Currently not validated (on roadmap).

### Email Links 📧

**Format**: `[text](mailto:email@example.com)`

Currently not validated (on roadmap).

## Output Reports

### JSON Report (`link_validation_report.json`)

```json
{
  "timestamp": "2026-01-06T15:30:00",
  "summary": {
    "total_files": 284,
    "total_internal_links": 1758,
    "total_external_links": 423,
    "broken_internal": 15,
    "broken_external": 8,
    "total_broken": 23,
    "health_score": 98.5
  },
  "broken_internal_links": [
    {
      "text": "Missing Page",
      "url": "/path/to/missing",
      "type": "internal",
      "line": 45,
      "file": "disability-wiki/employment.md",
      "error": "No file found at path/to/missing"
    }
  ],
  "broken_external_links": [
    {
      "text": "Dead Link",
      "url": "https://example.com/404",
      "type": "external",
      "line": 67,
      "file": "disability-wiki/benefits/ssdi.md",
      "error": "HTTP 404"
    }
  ]
}
```

### Text Report (`link_validation_report.txt`)

Human-readable format with:
- Summary statistics
- Broken internal links (grouped by file)
- Broken external links (grouped by error type)
- File and line numbers for easy fixing

## Scheduling

### Weekly Validation (Recommended)

```bash
crontab -e
```

Add:
```cron
# Run weekly on Sundays at 10 AM
0 10 * * 0 cd /Users/zachbeaudoin/disability-wiki && python3 link_validator_agent.py >> link_validator.log 2>&1
```

### Monthly Validation with Email

```bash
# Run monthly on 1st day at 9 AM, email results
0 9 1 * * cd /Users/zachbeaudoin/disability-wiki && python3 link_validator_agent.py && cat link_validation_report.txt | mail -s "Wiki Link Validation Report" your@email.com
```

## Integration with CI/CD

### GitHub Actions

Create `.github/workflows/link-validator.yml`:

```yaml
name: Link Validation

on:
  schedule:
    - cron: '0 10 * * 0'  # Weekly on Sunday
  workflow_dispatch:  # Manual trigger
  pull_request:  # On PRs

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install requests

      - name: Run link validator
        run: |
          cd disability-wiki
          python3 link_validator_agent.py

      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: link-reports
          path: |
            link_validation_report.json
            link_validation_report.txt

      - name: Comment on PR
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '⚠️ Link validation failed. Check the artifacts for details.'
            })
```

## Interpreting Results

### Health Score

- **95-100%**: Excellent - minimal broken links
- **90-94%**: Good - a few broken links to fix
- **80-89%**: Fair - moderate number of broken links
- **< 80%**: Poor - significant link maintenance needed

### Priority Levels

1. **High Priority**: Broken internal links
   - Users can't navigate wiki
   - Fix immediately

2. **Medium Priority**: Broken external links with HTTP errors
   - External resources moved/deleted
   - Find replacement URLs or remove

3. **Low Priority**: External links with timeouts
   - May be temporary server issues
   - Re-check before removing

## Common Issues & Fixes

### Broken Internal Links

**Problem**: Wiki.js page path changed or file moved

**Fix**:
```bash
# Find the correct path
find disability-wiki -name "*keyword*.md"

# Update the link in the source file
# Old: [Text](/old/path)
# New: [Text](/new/path)
```

### External Link HTTP 404

**Problem**: External website page removed

**Fix Options**:
1. Find new URL on same site
2. Use archive.org backup: `https://web.archive.org/web/*/ORIGINAL_URL`
3. Find alternative resource
4. Remove link if no longer relevant

### External Link Timeout

**Problem**: Server slow or temporarily down

**Action**:
1. Wait and re-run validator (may be temporary)
2. Test link manually in browser
3. If consistently timing out, consider removing

### External Link Connection Failed

**Problem**: Domain no longer exists or DNS issues

**Fix**:
1. Verify domain in browser
2. Search for organization's new website
3. Use archive.org if organization defunct
4. Remove if truly gone

## Performance

### Expected Runtime

- **Internal only** (--skip-external): ~10-30 seconds for 284 files
- **Full validation**: ~3-8 minutes depending on:
  - Number of external URLs
  - Network speed
  - Server response times

### Optimization Tips

1. **Run internal-only during development**:
   ```bash
   python3 link_validator_agent.py --skip-external
   ```

2. **Cache is automatic**: Duplicate URLs only checked once per run

3. **Parallel validation**: 10 concurrent external requests (configurable in code)

## Fixing Broken Links

### Batch Fix Template

Create `fix_links.sh`:

```bash
#!/bin/bash
# Fix common broken links

# Example: Update moved page path
find disability-wiki -name "*.md" -exec sed -i '' 's|/old/path|/new/path|g' {} +

# Example: Update changed external URL
find disability-wiki -name "*.md" -exec sed -i '' 's|https://old-url.com|https://new-url.com|g' {} +
```

### Manual Fix Process

1. Open `link_validation_report.txt`
2. For each broken link:
   ```bash
   # Find the file
   vim disability-wiki/path/to/file.md:LINE_NUMBER

   # Update the link
   # Save and exit
   ```
3. Re-run validator to verify fixes

## Maintenance

### Weekly Tasks

- [ ] Run link validator
- [ ] Review broken internal links (fix immediately)
- [ ] Review broken external links (research and update)
- [ ] Update link validation report

### Monthly Tasks

- [ ] Full external link validation
- [ ] Check health score trend
- [ ] Update documentation with common broken patterns
- [ ] Clean up consistently failing external links

### Quarterly Tasks

- [ ] Review validator configuration
- [ ] Update timeout values if needed
- [ ] Check for new link patterns to validate (anchors, emails)

## Troubleshooting

### "requests module not available"

```bash
# Install requests
pip3 install requests

# Or use system Python
python3 -m pip install requests

# Or skip external validation
python3 link_validator_agent.py --skip-external
```

### Validator runs too slow

```bash
# Skip external links for faster validation
python3 link_validator_agent.py --skip-external

# Or increase parallel workers (edit link_validator_agent.py):
# Change: ThreadPoolExecutor(max_workers=10)
# To: ThreadPoolExecutor(max_workers=20)
```

### False positives on external links

Some servers block automated requests. Options:

1. Test link manually in browser
2. Ignore specific errors in report
3. Add URL to allowlist (edit code to skip validation)

### Too many timeout errors

```bash
# Increase timeout (edit link_validator_agent.py):
# Change: timeout=10
# To: timeout=30
```

## Advanced Usage

### Custom Link Patterns

Edit `link_validator_agent.py` to add custom patterns:

```python
# Add pattern for wiki templates
self.template_pattern = re.compile(r'\{\{([^\}]+)\}\}')

# Add validation logic
def validate_template_link(self, template_name):
    # Custom validation
    pass
```

### Integration with Wiki.js API

Future enhancement: Validate against live Wiki.js API instead of file system.

### Archive.org Auto-Backup

Future enhancement: Automatically create archive.org backups for broken external links.

## Best Practices

1. **Run before major releases**: Ensure all links work
2. **Validate after bulk edits**: Catch broken links early
3. **Track health score**: Monitor trend over time
4. **Fix internal links immediately**: Critical for navigation
5. **Batch fix external links**: More efficient than one-by-one
6. **Document common fixes**: Build a fix playbook
7. **Use archive.org**: Preserve external content

## Next Steps

After setting up the link validator:

1. Run initial validation
2. Fix high-priority broken internal links
3. Research broken external links
4. Schedule weekly automated runs
5. Track health score trend
6. Consider GitHub Actions integration

---

## Support

### Check Validator Status

```bash
# Run with verbose output
python3 link_validator_agent.py

# Check specific file
python3 -c "from link_validator_agent import LinkValidator; v = LinkValidator(); print(v.extract_links('disability-wiki/employment.md'))"
```

### Common Questions

**Q: Why are some external links marked as broken when they work in my browser?**
A: Some servers block automated requests. Try testing with curl or updating the User-Agent in the code.

**Q: How often should I run the validator?**
A: Weekly for active wikis, monthly for stable content.

**Q: Can I validate just one file?**
A: Not currently, but you can filter results in the JSON report.

**Q: Does this work with other Wiki.js instances?**
A: Yes! Just point `--wiki-root` to your wiki's markdown export directory.

---

**Estimated Time**: 4-6 hours for full implementation and documentation
**Value**: Maintains wiki quality, ensures user navigation works
**Health Score Target**: > 95%

*Last Updated: January 6, 2026*
