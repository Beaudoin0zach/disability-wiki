#!/usr/bin/env python3
"""
Bulk Update Wiki Footer Script
Updates the footer section on multiple wiki pages
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
    NC = '\033[0m'


class FooterUpdater:
    def __init__(self, wiki_root):
        self.wiki_root = Path(wiki_root)

        # Pattern to match the existing footer
        self.footer_pattern = re.compile(
            r'\*\*Last updated\*\*:.*?\n'
            r'\*\*Maintained by\*\*:.*?\n'
            r'\*\*Questions or feedback\?\*\*.*?\n',
            re.MULTILINE | re.DOTALL
        )

        # Alternative patterns for different footer styles
        self.alt_patterns = [
            # Style 1: *Last updated: Month Year*
            re.compile(r'\*Last updated:.*?\*\s*$', re.MULTILINE),
            # Style 2: **Last updated:** Date
            re.compile(r'\*\*Last updated:\*\*.*?\n', re.MULTILINE),
        ]

    def find_files_with_footer(self):
        """Find all markdown files with footer sections"""
        files_with_footer = []

        for md_file in self.wiki_root.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')

                # Check for main footer pattern
                if self.footer_pattern.search(content):
                    files_with_footer.append({
                        'file': md_file,
                        'type': 'full_footer'
                    })
                # Check for alternative patterns
                else:
                    for pattern in self.alt_patterns:
                        if pattern.search(content):
                            files_with_footer.append({
                                'file': md_file,
                                'type': 'simple_footer'
                            })
                            break

            except Exception as e:
                print(f"Error reading {md_file}: {e}")

        return files_with_footer

    def preview_changes(self, action='remove'):
        """Preview what will be changed"""
        files = self.find_files_with_footer()

        print(f"\n{Colors.CYAN}Found {len(files)} files with footer sections:{Colors.NC}\n")

        for item in files:
            file_path = item['file'].relative_to(self.wiki_root.parent)
            print(f"  {file_path} ({item['type']})")

        return files

    def remove_footer(self, dry_run=True):
        """Remove footer sections from files"""
        files = self.find_files_with_footer()
        updated_count = 0

        print(f"\n{Colors.CYAN}{'DRY RUN - ' if dry_run else ''}Removing footers...{Colors.NC}\n")

        for item in files:
            md_file = item['file']

            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content

                # Remove full footer
                if item['type'] == 'full_footer':
                    content = self.footer_pattern.sub('', content)
                # Remove simple footer
                else:
                    for pattern in self.alt_patterns:
                        content = pattern.sub('', content)

                # Clean up extra blank lines (max 2 consecutive)
                content = re.sub(r'\n{3,}', '\n\n', content)
                content = content.rstrip() + '\n'

                if content != original_content:
                    if not dry_run:
                        md_file.write_text(content, encoding='utf-8')

                    updated_count += 1
                    relative_path = md_file.relative_to(self.wiki_root.parent)
                    print(f"  {Colors.GREEN}✓{Colors.NC} {relative_path}")

            except Exception as e:
                print(f"  {Colors.YELLOW}✗{Colors.NC} Error updating {md_file}: {e}")

        print(f"\n{Colors.GREEN}{updated_count} files {'would be' if dry_run else ''} updated{Colors.NC}")
        return updated_count

    def update_footer(self, new_date=None, new_team=None, dry_run=True):
        """Update footer sections with new information"""
        files = self.find_files_with_footer()
        updated_count = 0

        # Use current date if not provided
        if new_date is None:
            new_date = datetime.now().strftime("%B %Y")

        if new_team is None:
            new_team = "DisabilityWiki Benefits & Financial Support Team"

        new_footer = (
            f"**Last updated**: {new_date}\n"
            f"**Maintained by**: {new_team}\n"
            f"**Questions or feedback?** [Contact us →](/about/contact)\n"
        )

        print(f"\n{Colors.CYAN}{'DRY RUN - ' if dry_run else ''}Updating footers...{Colors.NC}\n")
        print(f"New footer will be:\n{new_footer}")

        for item in files:
            md_file = item['file']

            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content

                # Replace full footer
                if item['type'] == 'full_footer':
                    content = self.footer_pattern.sub(new_footer, content)
                # Replace simple footer with full footer
                else:
                    for pattern in self.alt_patterns:
                        if pattern.search(content):
                            content = pattern.sub(new_footer, content)
                            break

                if content != original_content:
                    if not dry_run:
                        md_file.write_text(content, encoding='utf-8')

                    updated_count += 1
                    relative_path = md_file.relative_to(self.wiki_root.parent)
                    print(f"  {Colors.GREEN}✓{Colors.NC} {relative_path}")

            except Exception as e:
                print(f"  {Colors.YELLOW}✗{Colors.NC} Error updating {md_file}: {e}")

        print(f"\n{Colors.GREEN}{updated_count} files {'would be' if dry_run else ''} updated{Colors.NC}")
        return updated_count

    def replace_footer(self, old_text, new_text, dry_run=True):
        """Replace specific text in footer sections"""
        files = self.find_files_with_footer()
        updated_count = 0

        print(f"\n{Colors.CYAN}{'DRY RUN - ' if dry_run else ''}Replacing '{old_text}' with '{new_text}'...{Colors.NC}\n")

        for item in files:
            md_file = item['file']

            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content

                # Replace text
                content = content.replace(old_text, new_text)

                if content != original_content:
                    if not dry_run:
                        md_file.write_text(content, encoding='utf-8')

                    updated_count += 1
                    relative_path = md_file.relative_to(self.wiki_root.parent)
                    print(f"  {Colors.GREEN}✓{Colors.NC} {relative_path}")

            except Exception as e:
                print(f"  {Colors.YELLOW}✗{Colors.NC} Error updating {md_file}: {e}")

        print(f"\n{Colors.GREEN}{updated_count} files {'would be' if dry_run else ''} updated{Colors.NC}")
        return updated_count


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Bulk update wiki footer sections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview what will be changed
  python3 bulk_update_footer.py --preview

  # Remove all footers (dry run first)
  python3 bulk_update_footer.py --remove

  # Remove all footers (actually do it)
  python3 bulk_update_footer.py --remove --apply

  # Update date to January 2026
  python3 bulk_update_footer.py --update-date "January 2026" --apply

  # Update team name
  python3 bulk_update_footer.py --update-team "DisabilityWiki Content Team" --apply

  # Replace [Date] placeholder with actual date
  python3 bulk_update_footer.py --replace "[Date]" "January 2026" --apply

  # Replace specific team name
  python3 bulk_update_footer.py --replace "Benefits & Financial Support Team" "Community Team" --apply
        """
    )

    parser.add_argument(
        '--wiki-root',
        default='disability-wiki',
        help='Path to wiki root directory (default: disability-wiki)'
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview files that have footer sections'
    )

    parser.add_argument(
        '--remove',
        action='store_true',
        help='Remove footer sections completely'
    )

    parser.add_argument(
        '--update-date',
        metavar='DATE',
        help='Update date in footer (e.g., "January 2026")'
    )

    parser.add_argument(
        '--update-team',
        metavar='TEAM',
        help='Update team name in footer'
    )

    parser.add_argument(
        '--replace',
        nargs=2,
        metavar=('OLD', 'NEW'),
        help='Replace OLD text with NEW text in footers'
    )

    parser.add_argument(
        '--apply',
        action='store_true',
        help='Actually apply changes (default is dry run)'
    )

    args = parser.parse_args()

    # Create updater
    updater = FooterUpdater(args.wiki_root)

    # Preview mode
    if args.preview or not any([args.remove, args.update_date, args.update_team, args.replace]):
        updater.preview_changes()
        print(f"\n{Colors.YELLOW}Use --remove, --update-date, --update-team, or --replace to make changes{Colors.NC}")
        print(f"{Colors.YELLOW}Add --apply to actually apply changes (default is dry run){Colors.NC}\n")
        return

    # Confirmation for apply mode
    if args.apply:
        print(f"\n{Colors.YELLOW}⚠ WARNING: This will modify files!{Colors.NC}")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return
    else:
        print(f"\n{Colors.BLUE}DRY RUN MODE - No files will be modified{Colors.NC}")
        print(f"{Colors.BLUE}Add --apply to actually make changes{Colors.NC}")

    # Execute action
    if args.remove:
        updater.remove_footer(dry_run=not args.apply)

    elif args.update_date or args.update_team:
        updater.update_footer(
            new_date=args.update_date,
            new_team=args.update_team,
            dry_run=not args.apply
        )

    elif args.replace:
        old_text, new_text = args.replace
        updater.replace_footer(old_text, new_text, dry_run=not args.apply)

    if not args.apply:
        print(f"\n{Colors.BLUE}This was a dry run. Add --apply to actually make changes.{Colors.NC}")


if __name__ == "__main__":
    main()
