#!/usr/bin/env python3
"""Content-level accessibility audit for disability-wiki markdown.

Checks the .md SOURCE (not the rendered site) for the accessibility defects that
live in content: image alt text, heading hierarchy, link text, table headers, and
emoji-as-information. Reports `file:line — issue — fix`; it does NOT auto-fix
(alt text and link text need human judgement). See the disability-wiki-accessibility
skill for how to act on findings.

USAGE
-----
    python3 scripts/check_accessibility.py                 # all tracked content .md
    python3 scripts/check_accessibility.py media/books.md  # specific files/dirs
    python3 scripts/check_accessibility.py --summary        # counts only

Scans English + es content; skips frontmatter, fenced code, and non-content trees.
"""
import os, re, subprocess, sys

args = [a for a in sys.argv[1:] if not a.startswith('--')]
SUMMARY = '--summary' in sys.argv
SKIP = ('backups/', '.claude/', 'docs/', 'node_modules/', 'archetypes/', 'content/',
        'page-review-2026-06-05/', 'scripts/')

def target_files():
    if args:
        out = []
        for a in args:
            if os.path.isdir(a):
                for root, _, fs in os.walk(a):
                    out += [os.path.join(root, f) for f in fs if f.endswith('.md')]
            elif a.endswith('.md'):
                out.append(a)
        return out
    tracked = subprocess.check_output("git ls-files '*.md'", shell=True, text=True).split()
    return [f for f in tracked if not f.startswith(SKIP) and '/' in f]

# real emoji/pictographs (NOT typographic arrows like → ←, which are fine)
EMOJI = re.compile('[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]️?')
VAGUE_LINK = {'click here', 'here', 'read more', 'more', 'link', 'this', 'this page',
              'learn more', 'see here', 'click', 'read this'}

def body_lines(path):
    """Yield (lineno, text) for prose lines: skip frontmatter + fenced code."""
    raw = open(path, encoding='utf-8').read().split('\n')
    out, in_fm, in_code, started = [], False, False, False
    for i, ln in enumerate(raw, 1):
        if i == 1 and ln.strip() == '---':
            in_fm = True; continue
        if in_fm:
            if ln.strip() == '---':
                in_fm = False
            continue
        if ln.lstrip().startswith('```'):
            in_code = not in_code; continue
        if in_code:
            continue
        out.append((i, ln))
    return out

def check(path):
    findings = []
    lines = body_lines(path)
    heads = []  # (lineno, level)
    for ln, t in lines:
        # images
        for m in re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)', t):
            alt, src = m.group(1).strip(), m.group(2)
            base = re.sub(r'[#?].*$', '', src).rsplit('/', 1)[-1].lower()
            if alt == '':
                findings.append((ln, 'image', f'empty alt text on image ({base})', 'add descriptive alt, or confirm decorative'))
            elif alt.lower() in ('image', 'img', 'photo', 'picture', 'logo', 'icon', 'screenshot') or alt.lower() == base:
                findings.append((ln, 'image', f'unhelpful alt text "{alt}"', 'describe what the image conveys'))
        # links (skip image links already handled; markdown link not preceded by !)
        for m in re.finditer(r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)', t):
            txt = m.group(1).strip().lower()
            if txt in VAGUE_LINK:
                findings.append((ln, 'link-text', f'non-descriptive link text "{m.group(1).strip()}"', 'use text that describes the destination'))
            elif txt.startswith(('http://', 'https://', 'www.')):
                findings.append((ln, 'link-text', 'bare URL as link text', 'use a human-readable label'))
        # headings
        hm = re.match(r'^(#{1,6})\s', t)
        if hm:
            heads.append((ln, len(hm.group(1))))
        # emoji as information
        if EMOJI.search(t):
            ems = ''.join(set(EMOJI.findall(t)))
            findings.append((ln, 'emoji', f'emoji in content ({ems})', 'use plain-text label; emoji read poorly on screen readers'))
    # heading hierarchy. House convention: body opens with `# Title`, then ## sections.
    # So a leading H1 is expected — only flag SKIPPED levels (e.g. ## -> ####).
    prev = None
    for ln, lv in heads:
        if prev is not None and lv > prev + 1:
            findings.append((ln, 'heading', f'heading level jumps from h{prev} to h{lv}', "don't skip levels"))
        prev = lv
    # tables: a |row| block needs a |---| separator on line 2
    for idx, (ln, t) in enumerate(lines):
        if t.lstrip().startswith('|') and t.count('|') >= 2:
            nxt = lines[idx + 1][1] if idx + 1 < len(lines) else ''
            prv = lines[idx - 1][1] if idx > 0 else ''
            is_sep = bool(re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', t))
            after_sep = bool(re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', prv))
            before_sep = bool(re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', nxt))
            # flag a header-looking first row with no separator following
            if not is_sep and not after_sep and not before_sep:
                # only flag once per table (first data row not part of a separated table)
                if not (prv.lstrip().startswith('|')):
                    findings.append((ln, 'table', 'table row without a header separator (|---|) row', 'add a header row + |---| separator'))
    return findings

files = target_files()
total = {}
flagged_files = 0
for f in sorted(files):
    fs = check(f)
    if not fs:
        continue
    flagged_files += 1
    for _, cat, _, _ in fs:
        total[cat] = total.get(cat, 0) + 1
    if not SUMMARY:
        print(f'\n### {f}')
        for ln, cat, issue, fix in fs:
            print(f'  {f}:{ln} — [{cat}] {issue} → {fix}')

print('\n=== accessibility summary ===')
print(f'files with findings: {flagged_files} / {len(files)} scanned')
for cat in sorted(total):
    print(f'  {cat}: {total[cat]}')
if not total:
    print('  clean — no content-level a11y issues found.')
