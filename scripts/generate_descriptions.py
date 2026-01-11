#!/usr/bin/env python3
"""
Meta Description Generator for Disability Wiki
Generates SEO-friendly descriptions for all markdown files missing them
"""

import re
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent / 'disability-wiki'

def extract_frontmatter_and_content(file_path):
    """Extract frontmatter and content from markdown file"""
    content = file_path.read_text(encoding='utf-8')

    if not content.startswith('---'):
        return {}, content, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content, content

    frontmatter_text = parts[1]
    body = parts[2]

    # Parse frontmatter
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, frontmatter_text, body

def generate_description(title, body, max_length=158):
    """Generate a meta description from content"""
    # Clean the body
    body = body.strip()

    # Remove headers
    body = re.sub(r'^#+\s+.*$', '', body, flags=re.MULTILINE)

    # Remove links but keep text
    body = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', body)

    # Remove images
    body = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', body)

    # Remove bold/italic
    body = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', body)

    # Remove bullet points
    body = re.sub(r'^[-*]\s+', '', body, flags=re.MULTILINE)

    # Get paragraphs
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and len(p.strip()) > 30]

    if not paragraphs:
        # Fallback to title-based description
        return f"Comprehensive guide to {title.lower()} for the disability community. Resources, rights, and support information."

    # Combine first 2-3 sentences from first paragraphs to get better context
    combined_text = ' '.join(paragraphs[:2])

    # Clean up whitespace
    combined_text = ' '.join(combined_text.split())

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', combined_text)

    # Build description from sentences
    description = ''
    for sentence in sentences:
        if len(description) + len(sentence) + 1 <= max_length:
            description += sentence + ' '
        else:
            break

    description = description.strip()

    # If still too short, just use first paragraph truncated
    if len(description) < 100 and len(combined_text) > 100:
        description = combined_text[:max_length].rsplit(' ', 1)[0]
        if not description.endswith(('.', '!', '?')):
            description += '...'

    # Ensure it ends properly
    if description and not description.endswith(('.', '!', '?', '...')):
        description += '.'

    # Fallback if still empty or too short
    if not description or len(description) < 50:
        description = f"Comprehensive guide to {title.lower()} for the disability community. Resources, rights, and support information."

    return description

def update_file_with_description(file_path, description):
    """Add description to frontmatter"""
    content = file_path.read_text(encoding='utf-8')

    if not content.startswith('---'):
        # No frontmatter, add it
        new_content = f"""---
title: {file_path.stem.replace('-', ' ').title()}
description: {description}
---

{content}"""
        file_path.write_text(new_content, encoding='utf-8')
        return True

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    frontmatter_text = parts[1]
    body = parts[2]

    # Update or add description line
    lines = frontmatter_text.split('\n')
    new_lines = []
    description_updated = False

    for line in lines:
        if line.strip().startswith('description:'):
            # Replace empty or existing description
            new_lines.append(f'description: {description}')
            description_updated = True
        else:
            new_lines.append(line)
            # Add after title if description wasn't found yet
            if line.strip().startswith('title:') and not description_updated:
                new_lines.append(f'description: {description}')
                description_updated = True

    # If still not added, append at end
    if not description_updated:
        new_lines.append(f'description: {description}')

    new_frontmatter = '\n'.join(new_lines)
    new_content = f"---{new_frontmatter}---{body}"
    file_path.write_text(new_content, encoding='utf-8')
    return True

def main():
    print("=" * 80)
    print("DISABILITY WIKI - META DESCRIPTION GENERATOR")
    print("=" * 80)
    print()

    # Find all markdown files
    md_files = list(BASE_DIR.glob('**/*.md'))
    print(f"Found {len(md_files)} markdown files\n")

    files_to_update = []
    files_updated = 0
    files_skipped = 0

    # Check each file
    for md_file in md_files:
        rel_path = md_file.relative_to(BASE_DIR)

        frontmatter, fm_text, body = extract_frontmatter_and_content(md_file)

        # Check if description exists and is not empty
        description = frontmatter.get('description', '').strip()

        if not description or description == '':
            # Get title
            title = frontmatter.get('title', md_file.stem.replace('-', ' ').title())

            # Generate description
            generated_desc = generate_description(title, body)

            files_to_update.append({
                'path': md_file,
                'rel_path': str(rel_path),
                'title': title,
                'description': generated_desc
            })

    print(f"Found {len(files_to_update)} files needing descriptions\n")

    # Ask for confirmation
    if files_to_update:
        print("Sample descriptions (first 5):")
        print("-" * 80)
        for item in files_to_update[:5]:
            print(f"\n{item['rel_path']}:")
            print(f"  Title: {item['title']}")
            print(f"  Description: {item['description']}")

        print("\n" + "=" * 80)
        response = input(f"\nUpdate {len(files_to_update)} files with generated descriptions? (yes/no): ")

        if response.lower() in ['yes', 'y']:
            print("\nUpdating files...")
            for item in files_to_update:
                try:
                    if update_file_with_description(item['path'], item['description']):
                        files_updated += 1
                        if files_updated % 20 == 0:
                            print(f"  Updated {files_updated}/{len(files_to_update)} files...")
                    else:
                        files_skipped += 1
                except Exception as e:
                    print(f"  Error updating {item['rel_path']}: {e}")
                    files_skipped += 1

            print(f"\n✓ Updated {files_updated} files")
            if files_skipped > 0:
                print(f"  ⚠ Skipped {files_skipped} files (errors or already had descriptions)")
        else:
            print("\nCancelled. No files were modified.")

    else:
        print("✓ All files already have descriptions!")

    print()

if __name__ == '__main__':
    main()
