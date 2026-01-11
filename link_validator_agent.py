#!/usr/bin/env python3
"""
Disability Wiki Link Validator Agent
Scans all markdown files for broken internal and external links
"""

import re
import os
from pathlib import Path
from urllib.parse import urlparse, unquote
from datetime import datetime
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠ Warning: 'requests' module not available. External link checking disabled.")
    print("Install with: pip install requests")


class Colors:
    """ANSI color codes"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'


class LinkValidator:
    def __init__(self, wiki_root=None):
        if wiki_root is None:
            wiki_root = Path(__file__).parent / "disability-wiki"
        else:
            wiki_root = Path(wiki_root)

        self.wiki_root = wiki_root
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "broken_internal_links": [],
            "broken_external_links": [],
            "all_links": [],
            "files_scanned": 0,
            "internal_links_checked": 0,
            "external_links_checked": 0
        }

        # Cache for external URL checks (avoid duplicate requests)
        self.external_url_cache = {}

        # Pattern for markdown links: [text](url)
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')

    def find_markdown_files(self):
        """Find all markdown files in the wiki"""
        md_files = list(self.wiki_root.rglob("*.md"))
        print(f"Found {len(md_files)} markdown files")
        return md_files

    def extract_links(self, file_path):
        """Extract all links from a markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            links = []
            for match in self.link_pattern.finditer(content):
                text = match.group(1)
                url = match.group(2)
                line_num = content[:match.start()].count('\n') + 1

                # Categorize link
                if url.startswith('http://') or url.startswith('https://'):
                    link_type = 'external'
                elif url.startswith('/'):
                    link_type = 'internal'
                elif url.startswith('#'):
                    link_type = 'anchor'
                elif url.startswith('mailto:'):
                    link_type = 'email'
                else:
                    link_type = 'relative'

                links.append({
                    'text': text,
                    'url': url,
                    'type': link_type,
                    'line': line_num,
                    'file': str(file_path.relative_to(self.wiki_root.parent))
                })

            return links

        except Exception as e:
            print(f"{Colors.RED}Error reading {file_path}: {e}{Colors.NC}")
            return []

    def validate_internal_link(self, url, source_file):
        """Check if an internal Wiki.js link exists"""
        # Wiki.js uses paths like /employment/job-searching
        # These correspond to files in the disability-wiki directory

        # Remove leading slash and decode URL encoding
        path = unquote(url.lstrip('/'))

        # Try multiple possible file locations
        possible_paths = [
            self.wiki_root / f"{path}.md",
            self.wiki_root / path / "index.md",
            self.wiki_root / f"{path}/index.md",
        ]

        # Also check if path already ends in .md
        if not path.endswith('.md'):
            possible_paths.insert(0, self.wiki_root / path)

        for candidate in possible_paths:
            if candidate.exists() and candidate.is_file():
                return True, None

        # Link not found
        return False, f"No file found at {path}"

    def validate_external_link(self, url, timeout=10):
        """Check if an external URL is accessible"""
        if not REQUESTS_AVAILABLE:
            return None, "requests module not installed"

        # Check cache first
        if url in self.external_url_cache:
            return self.external_url_cache[url]

        try:
            # Use HEAD request for efficiency
            response = requests.head(
                url,
                timeout=timeout,
                allow_redirects=True,
                headers={'User-Agent': 'Mozilla/5.0 (DisabilityWiki LinkValidator/1.0)'}
            )

            # Some servers don't support HEAD, try GET
            if response.status_code in [405, 501]:
                response = requests.get(
                    url,
                    timeout=timeout,
                    allow_redirects=True,
                    headers={'User-Agent': 'Mozilla/5.0 (DisabilityWiki LinkValidator/1.0)'},
                    stream=True  # Don't download full content
                )

            success = response.status_code < 400
            error = None if success else f"HTTP {response.status_code}"

            # Cache result
            self.external_url_cache[url] = (success, error)

            # Rate limiting - be nice to servers
            time.sleep(0.5)

            return success, error

        except requests.Timeout:
            result = (False, "Timeout")
            self.external_url_cache[url] = result
            return result
        except requests.ConnectionError:
            result = (False, "Connection failed")
            self.external_url_cache[url] = result
            return result
        except Exception as e:
            result = (False, str(e))
            self.external_url_cache[url] = result
            return result

    def validate_links_in_file(self, file_path):
        """Validate all links in a single file"""
        links = self.extract_links(file_path)
        results = {
            'file': str(file_path.relative_to(self.wiki_root.parent)),
            'total_links': len(links),
            'internal_links': [],
            'external_links': [],
            'broken_internal': [],
            'broken_external': []
        }

        for link in links:
            if link['type'] == 'internal':
                valid, error = self.validate_internal_link(link['url'], file_path)
                results['internal_links'].append(link)

                if not valid:
                    results['broken_internal'].append({
                        **link,
                        'error': error
                    })
                    self.results['broken_internal_links'].append({
                        **link,
                        'error': error
                    })

            elif link['type'] == 'external':
                results['external_links'].append(link)
                # External validation happens in batch later

        return results

    def scan_all_files(self):
        """Scan all markdown files for links"""
        print("\n" + "=" * 80)
        print("DISABILITY WIKI - LINK VALIDATOR")
        print("=" * 80)

        md_files = self.find_markdown_files()
        self.results['files_scanned'] = len(md_files)

        print(f"\nScanning {len(md_files)} files for links...")

        all_internal_links = []
        all_external_links = []
        file_results = []

        # Scan all files
        for i, md_file in enumerate(md_files, 1):
            if i % 50 == 0 or i == len(md_files):
                print(f"  Processed {i}/{len(md_files)} files...", end='\r')

            file_result = self.validate_links_in_file(md_file)
            file_results.append(file_result)

            all_internal_links.extend(file_result['internal_links'])
            all_external_links.extend(file_result['external_links'])

        print(f"  Processed {len(md_files)}/{len(md_files)} files... Done!")

        self.results['internal_links_checked'] = len(all_internal_links)
        self.results['external_links_checked'] = len(all_external_links)

        print(f"\n{Colors.CYAN}Links Found:{Colors.NC}")
        print(f"  Internal: {len(all_internal_links)}")
        print(f"  External: {len(all_external_links)}")

        # Validate external links (batch with threading)
        if all_external_links and REQUESTS_AVAILABLE:
            print(f"\n{Colors.CYAN}Validating external links...{Colors.NC}")
            self.validate_external_links_batch(all_external_links)

        return file_results

    def validate_external_links_batch(self, external_links):
        """Validate external links in parallel"""
        # Get unique URLs
        unique_urls = list(set(link['url'] for link in external_links))

        print(f"  Checking {len(unique_urls)} unique external URLs...")

        # Use thread pool for parallel requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {
                executor.submit(self.validate_external_link, url): url
                for url in unique_urls
            }

            completed = 0
            for future in as_completed(future_to_url):
                completed += 1
                if completed % 10 == 0 or completed == len(unique_urls):
                    print(f"    Checked {completed}/{len(unique_urls)} URLs...", end='\r')

        print(f"    Checked {len(unique_urls)}/{len(unique_urls)} URLs... Done!")

        # Now categorize broken links
        for link in external_links:
            url = link['url']
            if url in self.external_url_cache:
                valid, error = self.external_url_cache[url]
                if not valid:
                    self.results['broken_external_links'].append({
                        **link,
                        'error': error
                    })

    def generate_report(self):
        """Generate and print validation report"""
        broken_internal = len(self.results['broken_internal_links'])
        broken_external = len(self.results['broken_external_links'])
        total_broken = broken_internal + broken_external

        print("\n" + "=" * 80)
        print(f"{Colors.WHITE}VALIDATION REPORT{Colors.NC}")
        print("=" * 80)

        # Summary
        print(f"\n{Colors.CYAN}Summary:{Colors.NC}")
        print(f"  Files scanned: {self.results['files_scanned']}")
        print(f"  Internal links: {self.results['internal_links_checked']}")
        print(f"  External links: {self.results['external_links_checked']}")
        print()

        if total_broken == 0:
            print(f"{Colors.GREEN}✓ All links are valid!{Colors.NC}")
        else:
            if broken_internal > 0:
                print(f"{Colors.RED}✗ Broken internal links: {broken_internal}{Colors.NC}")
            if broken_external > 0:
                print(f"{Colors.YELLOW}⚠ Broken external links: {broken_external}{Colors.NC}")

        # Broken internal links (high priority)
        if broken_internal > 0:
            print(f"\n{Colors.RED}Broken Internal Links:{Colors.NC}")
            print("-" * 80)

            # Group by file
            by_file = {}
            for link in self.results['broken_internal_links']:
                file = link['file']
                if file not in by_file:
                    by_file[file] = []
                by_file[file].append(link)

            for file, links in sorted(by_file.items()):
                print(f"\n{Colors.CYAN}{file}{Colors.NC}")
                for link in links:
                    print(f"  Line {link['line']}: [{link['text']}]({link['url']})")
                    print(f"    {Colors.RED}✗ {link['error']}{Colors.NC}")

        # Broken external links (medium priority)
        if broken_external > 0:
            print(f"\n{Colors.YELLOW}Broken External Links:{Colors.NC}")
            print("-" * 80)

            # Group by error type
            by_error = {}
            for link in self.results['broken_external_links']:
                error = link['error']
                if error not in by_error:
                    by_error[error] = []
                by_error[error].append(link)

            for error, links in sorted(by_error.items()):
                print(f"\n{Colors.YELLOW}{error} ({len(links)} links){Colors.NC}")
                for link in links[:10]:  # Show first 10 per error type
                    print(f"  {link['file']}:{link['line']}")
                    print(f"    [{link['text']}]({link['url']})")

                if len(links) > 10:
                    print(f"  ... and {len(links) - 10} more")

        print("\n" + "=" * 80)

        # Save summary
        self.results['summary'] = {
            'total_files': self.results['files_scanned'],
            'total_internal_links': self.results['internal_links_checked'],
            'total_external_links': self.results['external_links_checked'],
            'broken_internal': broken_internal,
            'broken_external': broken_external,
            'total_broken': total_broken,
            'health_score': self._calculate_health_score()
        }

        return total_broken

    def _calculate_health_score(self):
        """Calculate link health score (0-100)"""
        total_links = self.results['internal_links_checked'] + self.results['external_links_checked']
        if total_links == 0:
            return 100

        broken = len(self.results['broken_internal_links']) + len(self.results['broken_external_links'])
        score = ((total_links - broken) / total_links) * 100
        return round(score, 1)

    def save_report(self, output_file=None):
        """Save detailed report to JSON"""
        if output_file is None:
            output_file = Path(__file__).parent / "link_validation_report.json"
        else:
            output_file = Path(output_file)

        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)

            print(f"\n{Colors.GREEN}✓ Detailed report saved: {output_file}{Colors.NC}")

            # Also save text summary
            text_file = output_file.with_suffix('.txt')
            self.save_text_report(text_file)

        except Exception as e:
            print(f"\n{Colors.RED}✗ Failed to save report: {e}{Colors.NC}")

    def save_text_report(self, output_file):
        """Save human-readable text report"""
        try:
            with open(output_file, 'w') as f:
                f.write("DISABILITY WIKI - LINK VALIDATION REPORT\n")
                f.write("=" * 80 + "\n")
                f.write(f"Generated: {self.results['timestamp']}\n")
                f.write("\n")

                # Summary
                f.write("SUMMARY\n")
                f.write("-" * 80 + "\n")
                f.write(f"Files scanned: {self.results['files_scanned']}\n")
                f.write(f"Internal links: {self.results['internal_links_checked']}\n")
                f.write(f"External links: {self.results['external_links_checked']}\n")
                f.write(f"Broken internal: {len(self.results['broken_internal_links'])}\n")
                f.write(f"Broken external: {len(self.results['broken_external_links'])}\n")
                f.write(f"Health score: {self.results['summary']['health_score']}%\n")
                f.write("\n")

                # Broken internal links
                if self.results['broken_internal_links']:
                    f.write("BROKEN INTERNAL LINKS\n")
                    f.write("-" * 80 + "\n")
                    for link in self.results['broken_internal_links']:
                        f.write(f"\n{link['file']}:{link['line']}\n")
                        f.write(f"  Text: {link['text']}\n")
                        f.write(f"  URL: {link['url']}\n")
                        f.write(f"  Error: {link['error']}\n")

                # Broken external links
                if self.results['broken_external_links']:
                    f.write("\n\nBROKEN EXTERNAL LINKS\n")
                    f.write("-" * 80 + "\n")
                    for link in self.results['broken_external_links']:
                        f.write(f"\n{link['file']}:{link['line']}\n")
                        f.write(f"  Text: {link['text']}\n")
                        f.write(f"  URL: {link['url']}\n")
                        f.write(f"  Error: {link['error']}\n")

            print(f"{Colors.GREEN}✓ Text report saved: {output_file}{Colors.NC}")

        except Exception as e:
            print(f"{Colors.RED}✗ Failed to save text report: {e}{Colors.NC}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate links in Disability Wiki markdown files"
    )
    parser.add_argument(
        '--wiki-root',
        default=None,
        help='Path to wiki root directory (default: ./disability-wiki)'
    )
    parser.add_argument(
        '--skip-external',
        action='store_true',
        help='Skip external link validation (faster)'
    )
    parser.add_argument(
        '--output',
        default=None,
        help='Output file for report (default: ./link_validation_report.json)'
    )

    args = parser.parse_args()

    # Create validator
    validator = LinkValidator(wiki_root=args.wiki_root)

    # Skip external validation if requested
    if args.skip_external:
        global REQUESTS_AVAILABLE
        REQUESTS_AVAILABLE = False
        print(f"{Colors.YELLOW}Skipping external link validation{Colors.NC}")

    # Run validation
    validator.scan_all_files()

    # Generate report
    total_broken = validator.generate_report()

    # Save detailed report
    validator.save_report(output_file=args.output)

    # Exit code: 0 if all links valid, 1 if broken links found
    return 0 if total_broken == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
