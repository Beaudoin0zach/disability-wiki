#!/usr/bin/env python3
"""Sweep non-content pages that leaked into the live wiki and unpublish them.

WHY THIS EXISTS
---------------
Wiki.js v2 git storage imports EVERY markdown/HTML file in the repo as a page
(it skips only `.git`). There is no import-exclude config, no `.wikignore`, and
`.gitignore` is honored only when *committing*, never when *importing*. Dot-dirs
are imported with the leading dot stripped (`.claude/foo.md` -> page `claude/foo`).
Frontmatter `published: false` is IGNORED on import — the page lands published.

So repo-internal docs (`.claude/**`, `docs/**`, root `README`/`AUDIT_*`/..., Hugo
`archetypes/**`, vestigial `content/**`) get published as public pages, and they
re-publish whenever the file CHANGES (a later sync re-imports it). Python/shell/yml
files do NOT leak (not a page content-type) — only `.md`/`.html`.

This script lists pages via the API and unpublishes any PUBLISHED page under a
known non-content path. Unpublish (not delete) — reversible, and safe in pull mode
(a *modify* write-back, never a delete/rebase conflict). Run it after syncing if
you touched any non-content `.md`. Dry-run by default; pass --apply to act.

USAGE
-----
    python3 scripts/sweep_noncontent_pages.py           # report only
    python3 scripts/sweep_noncontent_pages.py --apply    # unpublish the leaks

Token: $WIKIJS_TOKEN, else /tmp/wjs.txt. See the disability-wiki-edit skill.
"""
import json, os, re, sys, urllib.request

API = 'https://disabilitywiki.org/graphql'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36'
APPLY = '--apply' in sys.argv

# Path prefixes that are NEVER public content (dot stripped by Wiki.js on import).
NONCONTENT_PREFIXES = ('claude/', 'docs/', 'archetypes/', 'content/', 'page-review', 'site/')
# Exact root-level page paths that are repo meta, not content.
NONCONTENT_EXACT = {
    'README', 'SECURITY', 'SETUP', 'PROJECT_STATUS', 'BACKUP_AGENT_SETUP',
    'FOOTER_UPDATE_GUIDE', 'LINK_VALIDATOR_SETUP', 'QUICK_REFERENCE', 'CHANGELOG',
    'claude', 'robots',
}
# Dated root meta-docs (AUDIT_*, CONTENT_GAPS_*, PAGE_REVIEW_*, *_SCOPE_*).
NONCONTENT_RE = re.compile(r'^(AUDIT_|CONTENT_GAPS_|PAGE_REVIEW_)', re.I)

def is_noncontent(path):
    return (path.startswith(NONCONTENT_PREFIXES)
            or path in NONCONTENT_EXACT
            or bool(NONCONTENT_RE.match(path)))

def token():
    t = os.environ.get('WIKIJS_TOKEN')
    if t:
        return t.strip()
    with open('/tmp/wjs.txt') as f:
        return f.read().strip()

def gql(q, v=None):
    body = json.dumps({'query': q, 'variables': v or {}}).encode()
    req = urllib.request.Request(API, body, {
        'Authorization': 'Bearer ' + token(),
        'Content-Type': 'application/json', 'User-Agent': UA})
    return json.load(urllib.request.urlopen(req))

SINGLE = '''query($id:Int!){ pages{ single(id:$id){
  path title description content editor isPublished isPrivate locale
  tags{tag} scriptCss scriptJs } } }'''
UPDATE = '''mutation($id:Int!,$content:String!,$description:String!,$editor:String!,
  $isPublished:Boolean!,$isPrivate:Boolean!,$locale:String!,$path:String!,
  $tags:[String]!,$title:String!,$scriptCss:String,$scriptJs:String){
  pages{ update(id:$id,content:$content,description:$description,editor:$editor,
    isPublished:$isPublished,isPrivate:$isPrivate,locale:$locale,path:$path,
    tags:$tags,title:$title,scriptCss:$scriptCss,scriptJs:$scriptJs){
    responseResult{ succeeded message } }}}'''

def main():
    pages = gql('{ pages { list { id path locale isPublished } } }')['data']['pages']['list']
    leaks = [p for p in pages if p['isPublished'] and is_noncontent(p['path'])]
    print(f"published non-content pages: {len(leaks)}")
    for p in sorted(leaks, key=lambda x: x['path']):
        print(f"   id{p['id']:>4} [{p['locale']}] {p['path']}")
    if not leaks:
        print("clean — nothing to unpublish.")
        return
    if not APPLY:
        print("\n(dry-run) re-run with --apply to unpublish these.")
        return
    for p in leaks:
        pg = gql(SINGLE, {'id': p['id']})['data']['pages']['single']
        v = {'id': p['id'], 'content': pg['content'], 'description': pg['description'] or '',
             'editor': pg['editor'] or 'markdown', 'isPublished': False, 'isPrivate': pg['isPrivate'],
             'locale': pg['locale'], 'path': pg['path'], 'tags': [t['tag'] for t in (pg['tags'] or [])],
             'title': pg['title'] or pg['path'], 'scriptCss': pg['scriptCss'], 'scriptJs': pg['scriptJs']}
        r = gql(UPDATE, v)['data']['pages']['update']['responseResult']
        print(f"  {'OK  ' if r['succeeded'] else 'FAIL'} id{p['id']} {p['path']}")

if __name__ == '__main__':
    main()
