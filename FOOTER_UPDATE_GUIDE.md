# Footer Update Guide

## New Footer Format

The new community-focused footer:

```markdown
---

## Contribute to This Page

Have lived experience or expertise that could strengthen this page? We especially welcome perspectives on models not well represented here, including those from the Global South and Indigenous communities.

[Suggest an edit or addition →](/start/contribute)

---

*This page centers disabled people's expertise and is informed by disabled-led organizing globally. For questions or to suggest additions, see [How to Contribute](/start/contribute).*

*Last updated: January 2026*
```

## Quick Start

### 1. Preview the footer format
```bash
cd /Users/zachbeaudoin/disability-wiki
python3 add_new_footer.py --preview
```

### 2. Dry run (see what will change, no files modified)
```bash
python3 add_new_footer.py
```

This shows:
- `+ Added` - Pages that will get new footer
- `⟳ Replaced` - Pages where old footer will be replaced
- `- Skipped` - Pages that already have the new footer

### 3. Apply to all pages
```bash
python3 add_new_footer.py --apply
```

Will ask for confirmation before making changes.

## Common Use Cases

### Update with specific date
```bash
python3 add_new_footer.py --date "January 2026" --apply
```

### Add footer to specific directory only
```bash
# Only benefits pages
python3 add_new_footer.py --pattern "benefits/**/*.md" --apply

# Only rights pages
python3 add_new_footer.py --pattern "Rights/**/*.md" --apply
```

### Exclude certain pages
```bash
# Exclude drafts and archive folders
python3 add_new_footer.py --exclude "drafts" --exclude "archive" --apply
```

### Update existing footers (force)
```bash
# Replace even pages that already have new footer
python3 add_new_footer.py --force --date "February 2026" --apply
```

## What It Does

1. **Finds existing footers** and removes them:
   - `**Last updated**: [Date]`
   - `**Maintained by**: Team Name`
   - `**Questions or feedback?** Contact us`
   - `*Last updated: Month Year*`

2. **Adds new footer** to the bottom of each markdown file

3. **Cleans up formatting** (removes extra blank lines)

4. **Preserves content** - only changes the footer section at the end

## Safety Features

- ✅ **Dry run by default** - shows preview before any changes
- ✅ **Confirmation prompt** - asks "Are you sure?" when using `--apply`
- ✅ **Shows all changes** - lists every file that will be modified
- ✅ **Skips duplicates** - won't add footer if it already exists (unless `--force`)

## Results

After running with `--apply`, you'll see a summary:
```
Summary:
  Added:    139 files
  Replaced: 115 files  (removed old footer, added new)
  Skipped:  0 files
  Errors:   0 files

254 files were updated
```

## Customization

Want to change the footer text? Edit `add_new_footer.py`:

```python
def create_new_footer(self, last_updated=None):
    """Generate the new footer text"""
    if last_updated is None:
        last_updated = datetime.now().strftime("%B %Y")

    footer = f"""---

## Contribute to This Page

[Your custom text here]

*Last updated: {last_updated}*
"""
    return footer
```

## Troubleshooting

### "Already has new footer" for many files
- Normal! Script skips files that already have the new footer
- Use `--force` to replace existing footers

### Need to undo changes
```bash
# If you committed to git before:
git diff disability-wiki/  # Review changes
git checkout disability-wiki/  # Undo all changes

# Or restore from backup if you made one
```

### Want to test on one file first
```bash
# Just test on one directory
python3 add_new_footer.py --pattern "benefits/us/*.md" --apply
```

## Recommendation

1. **Commit current state to git first**:
   ```bash
   git add disability-wiki/
   git commit -m "Before footer update"
   ```

2. **Run dry run** to see what will change:
   ```bash
   python3 add_new_footer.py
   ```

3. **Apply changes**:
   ```bash
   python3 add_new_footer.py --apply
   ```

4. **Review changes**:
   ```bash
   git diff disability-wiki/ | head -100
   ```

5. **If good, commit**:
   ```bash
   git add disability-wiki/
   git commit -m "Update wiki footers to community-focused format"
   ```

---

**Files will be modified**: All `.md` files in `disability-wiki/` directory
**Backup recommended**: Commit to git or create backup before applying
**Reversible**: Changes can be undone with `git checkout` if needed
