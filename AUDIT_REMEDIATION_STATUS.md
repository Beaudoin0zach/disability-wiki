---
title: Audit Remediation Status
description: Internal tracker — progress against AUDIT_RESULTS_2026-06-06.md. Not for publication.
published: false
tags:
editor: markdown
---

# Audit Remediation Status (2026-06-07)

Tracks fixes against the Codex audit (`AUDIT_RESULTS_2026-06-06.md`). Site is Wiki.js pull-mode: edit the `.md`, merge to `main`, Wiki.js pulls (force-sync via API for immediate publish).

## ✅ DONE & LIVE

### 🚑 Tier A — life-safety crisis pages (commit fix(crisis), all verified vs official sources)
- `north-america/mexico` — lead was a **US** number → **Línea de la Vida 800-911-2000** (CONASAMA)
- `north-america/united-states` — Trans Lifeline M–F (not 24/7); 988 emergency-policy wording; demoted 1-800-273-8255
- `north-america/canada` — removed nonexistent 988 chat + "100+ languages"; emergency wording
- `asian-pacific/india` — added national **Tele-MANAS 14416**; iCall M–Sat (not 24/7); dropped AASRA WhatsApp claim
- `asian-pacific/indonesia` — lead → **Healing119.id / 119 ext 8** (Kemenkes)
- `asian-pacific/philippines` — lead → **NCMH 1553**; updated old Hopeline landlines
- `asian-pacific/thailand` — **1300 → 1323** (Dept of Mental Health)
- `asian-pacific/australia` — Lifeline "free" (not "local call rate"); QLife not 24/7
- `europe/united-kingdom` + `crisis/abuse/abuse-resources` — Rape Crisis **0808 802 9999 → 0808 500 2222**
- Softened "all free/confidential/24-7" + false "verified" footers site-wide

### 🔴 Tier B — High content
- `benefits/us/ssi` — SSI not taxable; gifts DO count; in-kind food rule (Sept 2024); resource exclusions (one vehicle any value, household goods); SGA = application test; noncitizen rules
- `rights/us/ada` — punitive damages NOT vs government (Barnes v. Gorman); LGBTQ+ exclusion rewritten (LGB "not impairments"; people with a disability protected; gender dysphoria can qualify — Williams v. Kincaid)

### 🟠 Tier C — Medium content
- `rights/us/section-504` — July 2026 equipment = one accessible unit per type (not all)
- `rights/us/state-disability-rights-laws` — CA DFEH→CRD (2 leftover spots); NY 4+ → all employers (1+)
- `benefits/us/medicare` — removed donut-hole leftover; qualified MA copay/referral; removed unsourced copay/Medigap ranges; bathroom equipment not covered
- `benefits/us/veterans-benefits` — caregiver stipend varies (GS-4 locality/level); clothing allowance not automatic; TDRP not a fixed 5-year term
- `rights/us/air-carrier-access-act` — DOT's actual 45-day / 6-month wording

### 🔧 Tier E — structural blocker
- Restored missing canonical `foundations/disability-models.md` (was stubbed-to but absent from repo → broke a redirect + 17 references). Exported from the Wiki.js DB.

---

## ✅ DONE & LIVE — 2026-06-09 session

### 🚑 Tier A — Mexico/Argentina crisis verification flags (PR #11, verified in DB)
Closed the open Mexico/Argentina flags from `docs/translation-source-accuracy-flags.md`, verified vs primary sources (argentina.gob.ar, ANDIS, gob.mx CONASAMA/CNDH/CONAPRED). EN + es:
- `south-america/argentina` — **emergency block corrected: 100 = Bomberos (firefighters), NOT police** (es literally said "Llama al 100 para la policía"); added 911 (integrated), 107 (SAME). **ANDIS** name fixed (Agencia/Secretaría Nacional de Discapacidad; es had "Asociación Nacional de Discapacitados") + unverifiable **4303-9088 → official 0800-555-3472** + Deaf/HoH video line. Added verified suicide lines CAS (135 / 0800-345-1435) + Salud Mental Responde (0800-333-1665).
- `north-america/mexico` — **deleted unverifiable 01-800-526-2345** (was "CONADIS / CNDH", conflated two orgs); split into **CNDH 800-715-2000**, **CONAPRED 800-543-0033**, CONADIS (site/email). "CONADIC 01-800-911-2000" (dup of Línea de la Vida, outdated operator) → **Línea de la Vida (CONASAMA)**.

### 🔴/🟠 Tier D — the 4 live "fix-in-place" essays (PR #12, verified in DB) — EN + es
- `race-and-disability` — AI/AN rate **~31% → ~39%** (CDC DHDS, 2022 BRFSS, 2024); sterilization estimate now attributed to historians (Lawrence 2000) + GAO HRD-77-3 cited separately.
- `lgbtq-and-disability` — conversion therapy: named AMA/APA×2/AAP, suicide stat sourced (Trevor Project, AJPH 2020); dead **rad.org → deafrad.org**.
- `poverty-and-class` — intent-as-fact removed ("designed to keep" → structural framing; heading + body).
- `disability-and-homelessness` — "~half / 2–3×" rescoped (HUD ~40% sheltered; chronic = disabling by definition); CRPD Art. 19 "violation" → advocates' interpretation.

---

## ⏳ REMAINING (after 2026-06-09)

### Tier D — the remaining 6 intersectionality essays

**✅ RESOLVED 2026-06-09 — PR #5 closed (stale branch, 3 days behind main; merging would have deleted skills/audit docs). The 6 essays' content is settled:**
- ✅ **LIVE on main** — `rural-disability`, `immigration-and-refugees`, `incarceration-and-criminalization`, `gender-and-disability`: the branch's fixes are already on `main` (0 diff; re-verified 2026-06-09 — e.g. gender 31 states + DC / 2.27× OR; incarceration BJS 2011–12 + 2016=38% + FCC 24-75; rural UNC Sheps 108/88, "sharing medication" gone).
- ✅ **LIVE on main** — `religion-and-disability`: deep-linked the RespectAbility/Disability Belongs 2021 Jewish-survey page (commit `b488059`, verified in DB). The AAPD IDAC dead-link concern does not exist on the current page (IDAC is plain text).
- ⏸️ **HELD — `indigenous-disability-perspectives`**: the fact-verified draft fill (GAO HRD-77-3 sterilization framing corrected; orgs verified) is preserved in **draft PR #13** (`hold/indigenous-disability-review`, rebased clean onto current main). **DO NOT MERGE until an Indigenous disabled reviewer approves** — a publication-quality prerequisite AI cannot satisfy. The live page intentionally remains a stub until then.

### Spanish (`es/`) translation sync — ⚠️ added 2026-06-07
All English pages fixed this session have `es/` counterparts that are **now stale** and still carry the old/incorrect content (including wrong crisis numbers). See `docs/translation-source-accuracy-flags.md` for the full list and the ES-sync priority order (crisis pages first — life-safety). That file also tracks additional English-source issues the translator flagged (some already fixed this session; `benefits/index.md` + `poverty-and-benefits-trap.md` 2024-figure refresh and the 1972/1989 asset-limit contradiction remain open).

### Tier E — structural (rest)
- ✅ **internal links — RESOLVED 2026-06-07.** Repo now at **0 broken internal links** (`validate_wiki_links.py`, 2,335 links). All the recurring targets above (`/community/online-communities`, `/community/disability-specific-peer-groups`, `/foundations/language-terminology-identity`, etc.) were repointed or created. See `docs/broken-links-triage-2026-06-07.md`.
- ✅ **auto-generated descriptions — RESOLVED 2026-06-07** (commit `9d0b700`). New `scripts/fix_descriptions.py` regenerated 224 published English pages: 0 colon-endings, 0 duplicates, 0 missing; condition pages (POTS/EDS/MCAS) and laws (ADA/IDEA) now named; 18 graceful `…` truncations remain (single-long-sentence intros), down from 187 mid-word cuts. *(es/ descriptions not yet swept — separate task.)*
- ✅ `scripts/validate_wiki_links.py` — base-dir bug fixed (commit `8020984`); now scans the repo correctly.
- ✅ `benefits/index.md` + `benefits/poverty-and-benefits-trap.md` 2024→2026 figure refresh + 1972/1989 asset-limit reconciliation — **DONE** (EN earlier; es/ synced 2026-06-07, commit `7739db4`).
