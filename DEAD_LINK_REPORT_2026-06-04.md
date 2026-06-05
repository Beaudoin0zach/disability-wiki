# Dead-Link Report — disabilitywiki.org

**Generated:** 2026-06-04
**Method:** Live crawl of disabilitywiki.org (208 pages), HEAD/GET status checks, then single-threaded re-verification to remove rate-limit / bot-block false positives.
**Note:** All wiki content lives in the Wiki.js database on the host — the git repo holds no page content. Fixes below must be applied in the **Wiki.js editor** (content links) or **Wiki.js Admin → Navigation** (sidebar links), not in this repo.

---

## ✅ RESOLVED 2026-06-04 — Internal stale-slug links (71 fixes across 22 pages)

Diagnosis corrected: the Benefits/contact/federal-rights pages **were never missing** — they exist at hierarchical paths (`/benefits/us/ssi`), but in-content links used flat slugs (`/benefits/us-ssi`). Fixed all 71 occurrences via the Wiki.js GraphQL API. Verified: 0 stale slugs remain; all targets return HTTP 200. Originals backed up to `backups/linkfix-2026-06-04/` (one JSON per page — restore via `pages.update` to roll back).

Slug corrections applied: `/benefits/us-*` → `/benefits/us/*`; `/benefits/uk-benefits` → `/benefits/united-kingdom/benefits`; `/benefits/eu-benefits` → `/benefits/european-union/benefits`; `/benefits/canada-benefits` → `/benefits/canada/benefits`; `/benefits/australia-benefits` → `/benefits/australia/benefits`; `/benefits/international-benefits-overview` → `/benefits/international/benefits-overview`; `/about/contact` → `/start/contact`; `/rights/us-federal-rights` → `/rights/us/federal-rights`.

### ✅ RESOLVED 2026-06-04 — External placeholders + moved links (34 pages)
- `https://forms.gle/DisabilityWikiContribution` and `https://forms.gle/YourGoogleFormLink` (placeholders) → `/start/contribute` (existing internal page), across 33 pages.
- `https://www2.ed.gov/about/offices/list/ocr/index.html` → `https://www.ed.gov/ocr` (verified 200).
- `http://medicaid.gov/medicaid/hcbs` → `https://www.medicaid.gov/medicaid/hcbs` (live, normalized).
- `https://access-board.gov` → `https://www.access-board.gov` (verified 200).
- Verified: 0 occurrences of any of the above remain. Backups: `backups/linkfix-2026-06-04/EXT_*.json`.

### ✅ RESOLVED 2026-06-04 (round 2) — Dead external domains researched & replaced (46 fixes / 21 pages)

Each dead domain was researched (web search + live verification of the replacement). Backups: `backups/linkfix-2026-06-04/RES_*.json`. Verified: 0 occurrences of any old token remain.

**Clean same-org migrations:**
| Old | New (verified 200) |
|---|---|
| disabilityinternational.org | driadvocacy.org (Disability Rights Intl rebrand) |
| sabeint.org | sabeusa.com (SABE) |
| ilcan.ca | ilc-vac.ca (Independent Living Canada) |
| lawhelp.org | www.lawhelp.org (normalized) |
| drlcenter.org | thedrlc.org ⚠️ org winding down — re-check periodically |
| ombudsman.org.uk | housing-ombudsman.org.uk (correct UK housing body) |
| nccsdlearningcenter.org | nccsd.ici.umn.edu (moved to U. Minnesota ICI) |
| thesqueakywheelchair.com | thesqueakywheelchairblog.com (active blog) |
| rollingrains.org | rollingrains.com (.com; frozen archive, author d. 2017) |
| bellvrs.ca | srvcanadavrs.ca/en/ (national SRV Canada VRS) |
| nda.ie/publications/nda-ethics-guidance… | nda.ie/publications/ethical-guidance-for-research-with-people-with-disabilities-report |
| butyoudontlooksick.com | www.butyoudontlooksick.com (normalized) |

**Judgment-call substitutions (not identical entity — approved):**
| Old | New |
|---|---|
| disabilityrightsaustralia.org.au ("Disability Rights Australia") | pwd.org.au + label changed to "People with Disability Australia (PWDA)" |
| drdl.law.syr.edu (Disability Rights Digital Library — defunct) | researchguides.library.syr.edu/disabilitystudies |
| disabledtravelers.com (defunct, domain repurposed) | wheelchairtravel.org/resources |

**Left unchanged (false positives — live domains, only blocked our scraper):**
- `otc-cta.gc.ca` (Canadian Transportation Agency) — live; bare-text reference, no change needed.
- `equalityadvisoryservice.com` (EASS UK) — live; bare-text reference, no change needed.
- `ilru.org/projects/cil-net/cil-center-and-association-directory` — the actual link returns **200**; earlier flag was a truncated-path artifact. No change.

**Note:** Most of these were bare-text domain mentions (not clickable links), so the fix updates the displayed domain text to the current one.

---

## 🔴 (HISTORICAL) Priority 1 — Benefits links appeared as 404 (now resolved above)

Every `/benefits/*` page is linked but returns 404. Even the section root `/en/benefits` 404s, and there is no `sitemap.xml`. These links are **site-wide** (not on any single content page), so they are almost certainly in the **Wiki.js navigation sidebar** (Admin → Navigation). The footer-management scripts in this repo (`add_new_footer.py`, `FOOTER_UPDATE_GUIDE.md`) reference a `benefits/**` section and a "Benefits & Financial Support Team", confirming the section was planned but never published.

Missing pages:

| Path (404) |
|---|
| /benefits/us-benefits-overview |
| /benefits/us-ssi |
| /benefits/us-ssdi |
| /benefits/us-medicaid |
| /benefits/us-medicare |
| /benefits/us-snap |
| /benefits/us-tanf |
| /benefits/us-able-accounts |
| /benefits/us-veterans-benefits |
| /benefits/us-family-caregiver-pay |
| /benefits/us-state-benefits |
| /benefits/international-benefits-overview |
| /benefits/uk-benefits |
| /benefits/eu-benefits |
| /benefits/canada-benefits |
| /benefits/australia-benefits |

**Fix options:** (a) create/publish the Benefits pages, or (b) remove the Benefits links from the nav sidebar until the content exists.

---

## 🟠 Priority 2 — Other broken internal links

| Broken path | Linked from |
|---|---|
| /about/contact | /en/community/index, /en/glossary/index |
| /rights/us-federal-rights | /en/get-involved/policy-advocacy, /en/rights/index |
| /history | site-wide (home + 10+ pages incl. all /en/get-involved/*, /en/rights/*) |

`/history` is linked nearly site-wide (likely also nav/footer) — same fix pattern as Benefits: create the page or remove the link.

---

## 🟠 Priority 3 — Placeholder / dead external links

### Placeholder links never replaced (404)
| URL | Linked from |
|---|---|
| https://forms.gle/DisabilityWikiContribution | /en/housing/housing-rights, /en/housing/independent-living-philosophy-and-centers, /en/housing/international-housing-rights |
| https://forms.gle/YourGoogleFormLink | /en/education/early-intervention, /en/education/higher-education, /en/education/k12-education, /en/education/transition-to-adulthood, /en/employment/employment-rights-by-country, /en/healthcare/mental-health, /en/rights/us-state-rights, /en/rights/us/fair-housing-act |

→ Replace both with the real Google Form URL, or remove.

### Confirmed dead / moved (fix or remove)
| URL | Status | Linked from |
|---|---|---|
| https://www2.ed.gov/about/offices/list/ocr/index.html | 404 (moved to ed.gov/about/.../ocr) | /en/glossary/bibliography, /en/rights/us/section-504 |
| http://ilru.org/projects/cil-net | 404 | /en/glossary/bibliography, /en/housing/independent-living-philosophy-and-centers |
| https://nda.ie/publications/nda-ethics-guidance-for-research-with-people-with-disabilities | 404 | /en/glossary/bibliography |
| https://access-board.gov | TLS/SSL error | (bibliography/rights pages) |

### Dead domains — connection failures, likely defunct (verify in browser, then remove)
disabilityinternational.org, sabeint.org, disabilityrightsaustralia.org.au, ilcan.ca, lawhelp.org, rollingrains.org, drlcenter.org, ombudsman.org.uk, otc-cta.gc.ca, equalityadvisoryservice.com, nccsdlearningcenter.org, thesqueakywheelchair.com, butyoudontlooksick.com, disabledtravelers.com, drdl.law.syr.edu, bellvrs.ca

Known source pages: most appear in /en/housing/* and /en/glossary/bibliography.

---

## 🟢 False positives — live, do NOT touch

These return 403/timeout to scripted requests (WAF / bot-blocking) but work fine in a browser:

ssa.gov, bls.gov, hhs.gov/ocr, transportation.gov, regulations.gov (200), social.desa.un.org CRPD (200), medicaid.gov, canada.ca, and `/cdn-cgi/l/email-protection` (Cloudflare email obfuscation, not a real link).

---

## Summary

- **22 broken internal** links → 17 are the missing Benefits section + /history + /about/contact + /rights/us-federal-rights (all nav/footer-level).
- **~25 genuinely broken external** links (2 placeholders, 4 moved/404, ~16 dead domains).
- **~18 false positives** (government/UN sites that bot-block) — ignore.
- **Biggest action:** publish or de-link the Benefits section in Wiki.js Admin → Navigation.
