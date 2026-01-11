#!/usr/bin/env python3
"""
Add New Footer to Wiki Pages
Adds the community-focused footer to wiki pages
"""

import re
from pathlib import Path
from datetime import datetime
import sys


class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'


class NewFooterAdder:
    def __init__(self, wiki_root):
        self.wiki_root = Path(wiki_root)

        # Pattern to match existing footer sections
        self.old_footer_patterns = [
            # Full footer
            re.compile(
                r'\*\*Last updated\*\*:.*?\n'
                r'\*\*Maintained by\*\*:.*?\n'
                r'\*\*Questions or feedback\?\*\*.*?\n',
                re.MULTILINE | re.DOTALL
            ),
            # Simple footer: *Last updated: Month Year*
            re.compile(r'\*Last updated:.*?\*\s*$', re.MULTILINE),
            # Simple footer: **Last updated:** Date
            re.compile(r'\*\*Last updated:\*\*.*?$', re.MULTILINE),
        ]

    def create_new_footer(self, last_updated=None):
        """Generate the new footer text"""
        if last_updated is None:
            last_updated = datetime.now().strftime("%B %Y")

        footer = f"""---

## Contribute to This Page

Have lived experience or expertise that could strengthen this page? We especially welcome perspectives on models not well represented here, including those from the Global South and Indigenous communities.

[Suggest an edit or addition →](/start/contribute)

---

*This page centers disabled people's expertise and is informed by disabled-led organizing globally. For questions or to suggest additions, see [How to Contribute](/start/contribute).*

*Last updated: {last_updated}*
"""
        return footer

    def has_old_footer(self, content):
        """Check if content has old footer"""
        for pattern in self.old_footer_patterns:
            if pattern.search(content):
                return True
        return False

    def has_new_footer(self, content):
        """Check if content already has new footer"""
        return "## Contribute to This Page" in content

    def remove_old_footer(self, content):
        """Remove old footer sections"""
        for pattern in self.old_footer_patterns:
            content = pattern.sub('', content)
        return content

    def add_footer(self, md_file, last_updated=None, dry_run=True, force=False):
        """Add new footer to a file"""
        try:
            content = md_file.read_text(encoding='utf-8')
            original_content = content

            # Skip if already has new footer (unless force)
            if self.has_new_footer(content) and not force:
                return 'skipped', 'Already has new footer'

            # Remove old footer if present
            if self.has_old_footer(content):
                content = self.remove_old_footer(content)
                action = 'replaced'
            else:
                action = 'added'

            # Clean up trailing whitespace
            content = content.rstrip() + '\n\n'

            # Add new footer
            new_footer = self.create_new_footer(last_updated)
            content += new_footer

            if content != original_content:
                if not dry_run:
                    md_file.write_text(content, encoding='utf-8')
                return action, None
            else:
                return 'skipped', 'No changes needed'

        except Exception as e:
            return 'error', str(e)

    def process_files(self, pattern='**/*.md', last_updated=None, dry_run=True, force=False, exclude_patterns=None):
        """Process all matching files"""
        if exclude_patterns is None:
            exclude_patterns = []

        files = list(self.wiki_root.glob(pattern))

        # Filter out excluded patterns
        filtered_files = []
        for f in files:
            should_exclude = False
            for exclude in exclude_patterns:
                if exclude in str(f):
                    should_exclude = True
                    break
            if not should_exclude:
                filtered_files.append(f)

        results = {
            'added': [],
            'replaced': [],
            'skipped': [],
            'errors': []
        }

        print(f"\n{Colors.CYAN}{'DRY RUN - ' if dry_run else ''}Processing {len(filtered_files)} files...{Colors.NC}\n")

        for md_file in filtered_files:
            action, error = self.add_footer(md_file, last_updated, dry_run, force)
            relative_path = md_file.relative_to(self.wiki_root.parent)

            if action == 'added':
                results['added'].append(relative_path)
                print(f"  {Colors.GREEN}+ Added{Colors.NC}     {relative_path}")
            elif action == 'replaced':
                results['replaced'].append(relative_path)
                print(f"  {Colors.YELLOW}⟳ Replaced{Colors.NC}  {relative_path}")
            elif action == 'skipped':
                results['skipped'].append((relative_path, error))
                if not dry_run:  # Only show skipped in apply mode
                    print(f"  {Colors.BLUE}- Skipped{Colors.NC}   {relative_path} ({error})")
            elif action == 'error':
                results['errors'].append((relative_path, error))
                print(f"  {Colors.RED}✗ Error{Colors.NC}     {relative_path}: {error}")

        return results

    def print_summary(self, results, dry_run=True):
        """Print summary of changes"""
        print(f"\n{Colors.CYAN}Summary:{Colors.NC}")
        print(f"  Added:    {len(results['added'])}")
        print(f"  Replaced: {len(results['replaced'])}")
        print(f"  Skipped:  {len(results['skipped'])}")
        print(f"  Errors:   {len(results['errors'])}")

        if results['errors']:
            print(f"\n{Colors.RED}Errors:{Colors.NC}")
            for file, error in results['errors']:
                print(f"  {file}: {error}")

        total_changes = len(results['added']) + len(results['replaced'])
        if total_changes > 0:
            print(f"\n{Colors.GREEN}{total_changes} files {'would be' if dry_run else 'were'} updated{Colors.NC}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Add new community-focused footer to wiki pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes on all pages
  python3 add_new_footer.py --preview

  # Add footer to all pages (dry run)
  python3 add_new_footer.py

  # Actually add footer to all pages
  python3 add_new_footer.py --apply

  # Add footer with specific date
  python3 add_new_footer.py --date "January 2026" --apply

  # Add footer to specific directory only
  python3 add_new_footer.py --pattern "benefits/**/*.md" --apply

  # Replace existing new footers (force update)
  python3 add_new_footer.py --force --apply

  # Exclude certain directories
  python3 add_new_footer.py --exclude "drafts" --exclude "archive" --apply

New footer format:
---
## Contribute to This Page
Have lived experience or expertise that could strengthen this page?
We especially welcome perspectives from the Global South and
Indigenous communities.

[Suggest an edit or addition →](/start/contribute)
---
*This page centers disabled people's expertise and is informed by
disabled-led organizing globally.*

*Last updated: [Date]*
        """
    )

    parser.add_argument(
        '--wiki-root',
        default='disability-wiki',
        help='Path to wiki root directory (default: disability-wiki)'
    )

    parser.add_argument(
        '--date',
        metavar='DATE',
        help='Last updated date (default: current month/year, e.g., "January 2026")'
    )

    parser.add_argument(
        '--pattern',
        default='**/*.md',
        help='File pattern to match (default: **/*.md for all markdown files)'
    )

    parser.add_argument(
        '--exclude',
        action='append',
        default=[],
        help='Exclude files matching pattern (can specify multiple times)'
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview what footer will look like'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Replace footer even if page already has new footer'
    )

    parser.add_argument(
        '--apply',
        action='store_true',
        help='Actually apply changes (default is dry run)'
    )

    args = parser.parse_args()

    # Create adder
    adder = NewFooterAdder(args.wiki_root)

    # Preview mode
    if args.preview:
        print(f"\n{Colors.CYAN}New footer format:{Colors.NC}")
        print(adder.create_new_footer(args.date or "January 2026"))
        print(f"\n{Colors.YELLOW}Run without --preview to add this footer to pages{Colors.NC}")
        print(f"{Colors.YELLOW}Add --apply to actually apply changes (default is dry run){Colors.NC}\n")
        return

    # Confirmation for apply mode
    if args.apply:
        print(f"\n{Colors.YELLOW}⚠ WARNING: This will modify files!{Colors.NC}")
        print(f"\nNew footer format:")
        print(adder.create_new_footer(args.date or datetime.now().strftime("%B %Y")))
        print()
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return
    else:
        print(f"\n{Colors.BLUE}DRY RUN MODE - No files will be modified{Colors.NC}")
        print(f"{Colors.BLUE}Add --apply to actually make changes{Colors.NC}")

    # Process files
    results = adder.process_files(
        pattern=args.pattern,
        last_updated=args.date,
        dry_run=not args.apply,
        force=args.force,
        exclude_patterns=args.exclude
    )

    # Print summary
    adder.print_summary(results, dry_run=not args.apply)

    if not args.apply:
        print(f"\n{Colors.BLUE}This was a dry run. Add --apply to actually make changes.{Colors.NC}")


if __name__ == "__main__":
    main()
