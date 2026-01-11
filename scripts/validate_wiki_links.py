#!/usr/bin/env python3
"""
Internal Link Validator for Disability Wiki (Wiki.js exports)
Checks all 254 markdown files for broken internal links and suggests improvements
"""

import re
from pathlib import Path
from collections import defaultdict

# Base directory
BASE_DIR = Path(__file__).parent / 'disability-wiki'

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown (simple parsing)"""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    # Simple YAML parsing - extract description field
    frontmatter_text = parts[1]
    body = parts[2]

    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, body

def extract_links(content):
    """Extract all markdown links from content"""
    # Pattern for [text](url) and [text](/path)
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    return re.findall(pattern, content)

def is_internal_link(url):
    """Check if a link is internal (Wiki.js path)"""
    return url.startswith('/') and not url.startswith(('http://', 'https://', 'mailto:'))

def normalize_wiki_path(link_url):
    """Normalize a Wiki.js link URL to file path"""
    # Remove leading slash
    path = link_url.lstrip('/')

    # Wiki.js uses URL paths like /benefits/us/ssdi
    # Map to disability-wiki/benefits/us/ssdi.md
    return BASE_DIR / f"{path}.md"

def check_link_exists(link_path):
    """Check if a Wiki.js link target exists"""
    if link_path.exists():
        return True

    # Check parent as index (e.g., /benefits/ -> benefits.md)
    parent_md = link_path.parent.with_suffix('.md')
    if parent_md.name != '.md' and parent_md.exists():
        return True

    return False

def find_potential_links(content, all_pages):
    """Find potential internal links based on content keywords"""
    suggestions = []
    content_lower = content.lower()

    # Common disability wiki topics that should be linked
    topic_keywords = {
        'ssdi': '/benefits/us/ssdi',
        'social security': '/benefits/us',
        'disability rights': '/rights',
        'ada': '/rights/us/ada',
        'medicaid': '/benefits/us/medicaid',
        'medicare': '/benefits/us/medicare',
        'housing': '/housing',
        'employment': '/employment',
        'education': '/education',
        'crisis': '/crisis',
        'mental health': '/conditions',
    }

    for keyword, suggested_link in topic_keywords.items():
        # Check if keyword appears but link doesn't
        if keyword in content_lower and suggested_link not in content:
            suggestions.append(f"Consider linking '{keyword}' to {suggested_link}")

    return suggestions

def main():
    print("=" * 80)
    print("DISABILITY WIKI - INTERNAL LINK VALIDATOR")
    print("=" * 80)
    print()

    # Find all markdown files
    md_files = list(BASE_DIR.glob('**/*.md'))
    print(f"Found {len(md_files)} markdown files\n")

    broken_links = []
    all_links = []
    files_without_description = []
    suggestions_by_file = defaultdict(list)

    # Check each file
    for md_file in md_files:
        rel_path = md_file.relative_to(BASE_DIR)
        content = md_file.read_text(encoding='utf-8')

        # Parse frontmatter
        frontmatter, body = extract_frontmatter(content)

        # Check for missing description
        if not frontmatter.get('description') or frontmatter.get('description').strip() == '':
            files_without_description.append(str(rel_path))

        # Extract links from body
        links = extract_links(body)

        for text, url in links:
            if is_internal_link(url):
                all_links.append((str(rel_path), text, url))

                # Normalize and check
                target = normalize_wiki_path(url)

                if not check_link_exists(target):
                    broken_links.append({
                        'file': str(rel_path),
                        'text': text,
                        'url': url,
                        'target': str(target.relative_to(BASE_DIR.parent))
                    })

        # Find suggestions
        suggestions = find_potential_links(body, md_files)
        if suggestions:
            suggestions_by_file[str(rel_path)] = suggestions

    # Report results
    print("=" * 80)
    print("LINK VALIDATION RESULTS")
    print("=" * 80)

    if broken_links:
        print(f"\n❌ {len(broken_links)} BROKEN INTERNAL LINKS FOUND:\n")
        for link in broken_links[:10]:  # Show first 10
            print(f"File: {link['file']}")
            print(f"  Text: '{link['text']}'")
            print(f"  URL: {link['url']}")
            print(f"  Target not found: {link['target']}\n")

        if len(broken_links) > 10:
            print(f"  ... and {len(broken_links) - 10} more (see report file)\n")
    else:
        print("\n✓ No broken internal links found!\n")

    # Report missing descriptions
    print("=" * 80)
    print("FRONTMATTER ANALYSIS")
    print("=" * 80)
    print(f"\n📝 {len(files_without_description)} files missing descriptions\n")

    if files_without_description:
        print("Files without descriptions (first 10):")
        for file_path in files_without_description[:10]:
            print(f"  • {file_path}")
        if len(files_without_description) > 10:
            print(f"  ... and {len(files_without_description) - 10} more\n")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total markdown files: {len(md_files)}")
    print(f"Total internal links: {len(all_links)}")
    print(f"Broken links: {len(broken_links)}")
    print(f"Files missing descriptions: {len(files_without_description)}")
    print(f"Files with link suggestions: {len(suggestions_by_file)}")

    # Suggestions sample
    if suggestions_by_file:
        print("\n" + "=" * 80)
        print("SUGGESTED INTERNAL LINKS (Sample)")
        print("=" * 80)
        sample_files = list(suggestions_by_file.items())[:5]
        for file_path, suggestions in sample_files:
            print(f"\n{file_path}:")
            for suggestion in suggestions[:3]:  # Max 3 per file
                print(f"  • {suggestion}")

    # Save detailed report
    report_file = BASE_DIR.parent / 'wiki_link_validation_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("DISABILITY WIKI - INTERNAL LINK VALIDATION REPORT\n")
        f.write("=" * 80 + "\n\n")

        if broken_links:
            f.write(f"BROKEN LINKS ({len(broken_links)} found):\n")
            f.write("-" * 80 + "\n")
            for link in broken_links:
                f.write(f"\nFile: {link['file']}\n")
                f.write(f"  Text: '{link['text']}'\n")
                f.write(f"  URL: {link['url']}\n")
                f.write(f"  Target: {link['target']}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write(f"FILES MISSING DESCRIPTIONS ({len(files_without_description)}):\n")
        f.write("-" * 80 + "\n")
        for file_path in files_without_description:
            f.write(f"{file_path}\n")

        if suggestions_by_file:
            f.write("\n" + "=" * 80 + "\n")
            f.write("SUGGESTED INTERNAL LINKS\n")
            f.write("=" * 80 + "\n")
            for file_path, suggestions in suggestions_by_file.items():
                f.write(f"\n{file_path}:\n")
                for suggestion in suggestions:
                    f.write(f"  • {suggestion}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total files: {len(md_files)}\n")
        f.write(f"Total internal links: {len(all_links)}\n")
        f.write(f"Broken links: {len(broken_links)}\n")
        f.write(f"Files missing descriptions: {len(files_without_description)}\n")

    print(f"\n✓ Detailed report saved to: {report_file}")
    print()

if __name__ == '__main__':
    main()
