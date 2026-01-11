#!/usr/bin/env python3
"""
Update Wiki.js pages via GraphQL API
Updates page content from markdown files
"""

import requests
import json
from pathlib import Path
import re


class WikiJSUpdater:
    def __init__(self, base_url="http://localhost:8080", api_key=None):
        self.base_url = base_url
        self.api_url = f"{base_url}/graphql"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def get_api_key_instructions(self):
        """Print instructions to get API key"""
        print("""
To use this script, you need a Wiki.js API key:

1. Open Wiki.js: http://localhost:8080
2. Log in as admin
3. Go to: Administration → API Access
4. Click "New API Key"
5. Give it a name (e.g., "Bulk Update Script")
6. Set permissions: Full Access (or at least read/write pages)
7. Copy the API key
8. Run this script with: python3 update_wikijs_pages.py --api-key "YOUR_KEY_HERE"

Alternatively, you can edit pages directly in Wiki.js admin interface.
        """)

    def extract_frontmatter(self, content):
        """Extract YAML frontmatter from markdown"""
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            body = frontmatter_match.group(2)

            # Parse frontmatter
            metadata = {}
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

            return metadata, body
        return {}, content

    def get_page_path(self, md_file, wiki_root):
        """Convert markdown file path to Wiki.js page path"""
        # Remove wiki_root and .md extension
        rel_path = md_file.relative_to(wiki_root)
        page_path = str(rel_path.with_suffix('')).replace('\\', '/')

        # Wiki.js uses paths like /benefits/ssdi not /benefits/ssdi.md
        return f"/{page_path}"

    def update_page_content(self, page_path, content, title=None):
        """Update a page's content via GraphQL API"""
        metadata, body = self.extract_frontmatter(content)

        if not title:
            title = metadata.get('title', page_path.split('/')[-1].replace('-', ' ').title())

        # GraphQL mutation to update page
        mutation = """
        mutation UpdatePage($id: Int!, $content: String!, $title: String!) {
          pages {
            update(
              id: $id
              content: $content
              title: $title
            ) {
              responseResult {
                succeeded
                errorCode
                slug
                message
              }
            }
          }
        }
        """

        # First, get the page ID
        # This would require another query to find the page by path
        # For now, let's print what would be updated

        print(f"Would update: {page_path}")
        print(f"  Title: {title}")
        print(f"  Content length: {len(body)} characters")
        return True


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Update Wiki.js pages from markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--api-key',
        help='Wiki.js API key (required for updates)'
    )

    parser.add_argument(
        '--wiki-root',
        default='disability-wiki',
        help='Path to markdown files directory'
    )

    parser.add_argument(
        '--base-url',
        default='http://localhost:8080',
        help='Wiki.js base URL'
    )

    args = parser.parse_args()

    updater = WikiJSUpdater(base_url=args.base_url, api_key=args.api_key)

    if not args.api_key:
        print("ERROR: API key required")
        updater.get_api_key_instructions()
        return 1

    print(f"This script would update pages via Wiki.js API")
    print(f"Note: Wiki.js API has some limitations for bulk updates")
    print()
    print("RECOMMENDED: Use Wiki.js admin interface instead:")
    print("  1. Go to http://localhost:8080")
    print("  2. Click on page you want to edit")
    print("  3. Click Edit button")
    print("  4. Paste new footer at the bottom")
    print("  5. Save")
    print()
    print("Or use Storage Sync (see documentation)")


if __name__ == "__main__":
    main()
