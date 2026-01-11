# Disability Wiki - Utility Scripts

This directory contains Python utilities for maintaining and optimizing the disability wiki content.

---

## Scripts

### 1. generate_descriptions.py

**Purpose**: Automatically generates SEO-friendly meta descriptions for markdown files missing them.

**Usage**:
```bash
cd /Users/zachbeaudoin/disability-wiki
python3 scripts/generate_descriptions.py
```

**What it does**:
- Scans all markdown files in `disability-wiki/` directory
- Identifies files with empty or missing `description:` fields in frontmatter
- Extracts content from first 1-2 paragraphs
- Cleans markdown formatting (headers, links, bold, bullets)
- Generates descriptions of 155-160 characters (SEO optimal)
- Shows preview of first 5 files before applying
- Updates YAML frontmatter with generated descriptions

**Results**:
- ✅ Updated 232 of 254 files with meta descriptions
- ✅ All descriptions optimized for search engines
- ✅ Preserves existing descriptions (doesn't overwrite)

**Example Output**:
```
disability-wiki/benefits/us/ssdi.md:
  Title: Social Security Disability Insurance (SSDI)
  Description: SSDI provides monthly benefits to people who can't work due to a disability. Learn about eligibility requirements, application process, and benefit amounts.
```

---

### 2. validate_wiki_links.py

**Purpose**: Validates all internal Wiki.js links and identifies broken references.

**Usage**:
```bash
cd /Users/zachbeaudoin/disability-wiki
python3 scripts/validate_wiki_links.py
```

**What it does**:
- Scans all 254 markdown files
- Extracts all internal links (format: `[text](/path)`)
- Validates each link target exists in the file system
- Checks frontmatter for missing descriptions
- Suggests potential cross-links based on content keywords
- Generates detailed report: `docs/wiki_link_validation_report.txt`

**Results**:
- ✅ Checked 1,758 internal links
- ⚠️ Found 15 broken links
- 📝 Identified 232 files missing descriptions (now fixed)
- 💡 Suggested 127 potential internal links to add

**Report Sections**:
1. **Broken Links**: File path, link text, target URL, why it failed
2. **Missing Descriptions**: List of files without frontmatter descriptions
3. **Suggested Links**: Keyword-based link suggestions for better navigation
4. **Summary**: Total files, links checked, issues found

**Example Output**:
```
BROKEN LINKS:
File: benefits/state/california.md
  Text: 'California IHSS Program'
  URL: /benefits/state/california/ihss
  Target not found: disability-wiki/benefits/state/california/ihss.md

SUGGESTIONS:
File: rights/us/ada.md:
  • Consider linking 'employment' to /employment
  • Consider linking 'housing' to /housing
```

---

## Requirements

Both scripts use only Python standard library modules:
- `re` - Regular expressions
- `pathlib` - File path handling
- `collections` - Data structures

**No external dependencies required!**

---

## File Paths

Scripts expect this directory structure:
```
/Users/zachbeaudoin/disability-wiki/
├── scripts/
│   ├── generate_descriptions.py
│   └── validate_wiki_links.py
└── disability-wiki/              # Target markdown files
    ├── benefits/
    ├── rights/
    ├── housing/
    └── ...
```

---

## Best Practices

### When to Run

**generate_descriptions.py**:
- After adding new content without descriptions
- Before deploying content updates
- When improving SEO

**validate_wiki_links.py**:
- After restructuring content directories
- Before major content updates
- Monthly maintenance check
- After importing new content

### Workflow

1. Add new content to Wiki.js
2. Export markdown files to `disability-wiki/` directory
3. Run `validate_wiki_links.py` to check for broken links
4. Fix any broken links identified
5. Run `generate_descriptions.py` to add meta descriptions
6. Review generated descriptions (shown in preview)
7. Approve and apply changes
8. Re-import to Wiki.js or commit to git

---

## Customization

### Modify Description Length

Edit `generate_descriptions.py` line 36:
```python
def generate_description(title, body, max_length=158):  # Change 158 to desired length
```

### Add Custom Link Suggestions

Edit `validate_wiki_links.py` lines 72-84:
```python
topic_keywords = {
    'ssdi': '/benefits/us/ssdi',
    'ada': '/rights/us/ada',
    # Add your own keywords here
    'your-keyword': '/path/to/page',
}
```

---

## Troubleshooting

### Script Can't Find disability-wiki/ Directory

**Error**: `FileNotFoundError: disability-wiki directory not found`

**Fix**: Run scripts from repository root:
```bash
cd /Users/zachbeaudoin/disability-wiki
python3 scripts/generate_descriptions.py
```

### No Files Found

**Error**: `Found 0 markdown files`

**Fix**: Check BASE_DIR in script (line 11):
```python
BASE_DIR = Path(__file__).parent / 'disability-wiki'
```

### Permission Denied

**Error**: `PermissionError: [Errno 13] Permission denied`

**Fix**: Make script executable:
```bash
chmod +x scripts/generate_descriptions.py
chmod +x scripts/validate_wiki_links.py
```

---

## Future Enhancements

Potential improvements for these scripts:

### generate_descriptions.py
- [ ] AI-powered description generation using OpenAI API
- [ ] Keyword extraction for better SEO
- [ ] Multi-language support
- [ ] Character count optimization per search engine

### validate_wiki_links.py
- [ ] Check external links (HTTP status codes)
- [ ] Detect duplicate content
- [ ] Find orphaned pages (no incoming links)
- [ ] Generate sitemap.xml
- [ ] Link graph visualization

---

## Contributing

To add new utility scripts:

1. Create script in `scripts/` directory
2. Add docstring at top explaining purpose
3. Use Python standard library when possible
4. Update this README with usage instructions
5. Add example output
6. Include error handling

---

*Last Updated: January 6, 2026*
