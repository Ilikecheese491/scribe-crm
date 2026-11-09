# Scribe — Keyword & Content Calendar (v1)

Source: Keyword Researcher SERP observation pass (DuckDuckGo + Forbes live page, 2026-11-08, US English).
Honest caveats: NO volume/difficulty/CPC data was observed (no tool access). Volume tiers are inferred
from SERP landscape (query breadth + authority of ranking pages). No GSC baseline exists yet — re-rank
this calendar against real impressions at day 30 post-launch.

## Publish order (matches Rigel's launch gate: pillar first, then cluster, then comparisons)

### Phase 1 — Pillar (must be live before comparisons link in)
| Query (observed SERP phrasing) | Intent | Stage | URL | Angle |
|---|---|---|---|---|
| "best crm for small business (2026)" — consolidate variant "best small business crm software" | Commercial investigation | MOFU | /blog/best-crm-for-small-business | One canonical pillar (cannibalization flag: both phrasings are the same intent). Forbes/Agiled/SaaSworthy listicles dominate; differentiate with an automation-first pick section ("runs itself") |

### Phase 2 — TOFU cluster (AI/automation — the whitespace)
| Query | Intent | Stage | URL | Angle |
|---|---|---|---|---|
| "crm that runs itself" (no one observed ranking — whitespace, own the language) | Informational → commercial | TOFU | /blog/crm-that-runs-itself | Positioning page; the differentiator named in the pillar |
| "ai crm for small business (2026)" (guides observed) | Commercial | MOFU | /blog/ai-crm-for-small-business | Category definition; link to pillar |
| "automate sales follow-up / ai sales automation small business" (observed, incl. monday.com ad copy only) | Informational | TOFU | /blog/automate-sales-follow-up | Problem-space entry; no observed owner of an AI-native SMB narrative — whitespace |

### Phase 3 — BOFU (comparisons + pricing/free tier)
| Query | Intent | Stage | URL | Angle |
|---|---|---|---|---|
| "Scribe vs HubSpot" (SERPs: hubspot vs zoho/pipedrive/freshsales) | Decision | BOFU | /compare/scribe-vs-hubspot | Pipeline vs automation; canonical-links to pillar |
| "Scribe vs Zoho CRM" (price anchor observed: Free + $20/user) | Decision | BOFU | /compare/scribe-vs-zoho | Cost + manual-data-entry wedge |
| "Scribe vs Pipedrive" (SERP: monday vs pipedrive) | Decision | BOFU | /compare/scribe-vs-pipedrive | Same wedge; keep one "best" intro on pillar only (cannibalization rule) |
| "best free crm small business" + "can small businesses afford a crm" (observed on Forbes FAQ) | Transactional | BOFU | /pricing + /blog/best-free-crm | Free-tier activation; observed anchors: Zoho $20/user, Bigin $9, Freshsales $11 |

## Internal link map
- Every comparison → pillar (canonical context) + /pricing
- TOFU cluster → pillar → trial CTA
- /pricing → trial CTA (activation goal)
- UTM per page on the trial CTA so the tracking stack (trial.js) attributes content source

## Vertical variants (phase 4, later)
Generalize: best-of pillar, comparison pages, /pricing (same buyer across verticals).
Vertical-specific skeleton: "crm that runs itself for retail / services / healthcare / real estate" —
same TOFU template, swap vertical proof points. Don't build until a vertical shows intent in GSC data.

## Gaps (cannot assert)
- No keyword volume, difficulty, CPC, or rank positions — SERP-observed only.
- No demand trend / date range.
- Geography: US only (SERPs observed; unconfirmed beyond US).
