#!/usr/bin/env python3
"""Quick fix for duplicate footers"""
import re
from pathlib import Path

wiki_root = Path("disability-wiki")

# Pattern for old footer
old_footer_pattern = re.compile(
    r'---\n\n'
    r'\*\*Last updated\*\*:.*?\n'
    r'\*\*Maintained by\*\*:.*?\n'
    r'\*\*Questions or feedback\?\*\*.*?\n\n'
    r'(?=---\n\n## Contribute)',
    re.MULTILINE | re.DOTALL
)

count = 0
for md_file in wiki_root.rglob("*.md"):
    content = md_file.read_text(encoding='utf-8')

    # Remove old footer if it appears before new footer
    new_content = old_footer_pattern.sub('', content)

    if content != new_content:
        md_file.write_text(new_content, encoding='utf-8')
        count += 1
        print(f"Fixed: {md_file}")

print(f"\nFixed {count} files with duplicate footers")
