# SMB CRM — 90-Day SEO Roadmap (v1)

**Status:** DRAFT | **Updated:** 2026-11-08  
**Launch gate:** Day-30 = 150+ qualified trials AND ≥25% activation

---

## 1. Cluster Architecture

### Pillar Cluster (Month 1)
```
CRM for Small Business (Pillar)
├── Why CRM Fails Small Business
├── 5 Signs You Need Better CRM
└── How Scribe Runs Itself
```

### Comparison Cluster (Month 2)
```
Scribe vs Competitors
├── Scribe vs HubSpot
├── Scribe vs Zoho
└── Scribe vs Pipedrive
```

### BOFU Cluster (Month 3)
```
Pricing & Free Tier Focus
├── Best Free CRM for Small Business
├── Can Small Businesses Afford a CRM?
└── CRM Under $10/Month
```

---

## 2. Internal Link Map

| Page | Canonical To | Secondary Links | UTM |
|------|--------------|-----------------|-----|
| Pillar | - | /compare/*, /pricing, /blog/* | utm_content=pillar |
| TOFU blog | Pillar, /trial | pillar CTA, internal crosslinks | utm_content=tofu |
| Comparison | Pillar, /pricing | pillar intro links | utm_content=comparison |
| Pricing page | Pillar | pillar value section | utm_content=pricing |

**Cannibalization Guardrails:**
- Pillar owns "CRM for small business" + "best CRM for small business"
- Comparison pages use `rel="canonical"` to pillar for shared concepts
- No two pages target the same high-volume query

---

## 3. Publishing Timeline

### Month 1 — Foundation (Weeks 1-4)
| Week | Deliverable | Channel | Next Action |
|------|-------------|---------|-------------|
| Week 1 | Pillar page live | /blog/best-crm-for-small-business | Internal link update |
| Week 2 | Why CRM Fails | /blog/why-crm-fails | Social preview threads |
| Week 3 | 5 Signs post | /blog/5-signs-you-need-crm | GSC baseline |
| Week 4 | How Scribe Works | /blog/crm-that-runs-itself | Trial CTA test |

### Month 2 — Comparison (Weeks 5-8)
| Week | Deliverable | Channel | Next Action |
|------|-------------|---------|-------------|
| Week 5 | Scribe vs HubSpot | /compare/scribe-vs-hubspot | GSC monitor |
| Week 6 | Scribe vs Zoho | /compare/scribe-vs-zoho | GSC monitor |
| Week 7 | Scribe vs Pipedrive | /compare/scribe-vs-pipedrive | GSC monitor |
| Week 8 | Free CRM guide | /blog/best-free-crm | Pricing CTA test |

### Month 3 — Optimization (Weeks 9-12)
| Week | Deliverable | Metric | Decision Point |
|------|-------------|--------|----------------|
| Week 9 | GSC query gap analysis | Top queries | Update focus |
| Week 10 | Internal linking audit | Crawl errors | Fix 404s |
| Week 11 | Page speed optimization | LCP < 2.5s | Deploy fixes |
| Week 12 | Day-30 gate review | 150+ trials, 25%+ act | Scale or pivot |

---

## 4. Dependencies

**Prerequisite from Technical SEO Auditor:** competitor-crawl.csv populated (status: ✅ complete, 25 rows)

**Prerequisite from Watcher:** pricing data validated (status: ✅ complete)

**Prerequisite from Keyword Researcher:** SERP observations captured (status: ✅ complete)

---

## 5. Measurement

- **Primary:** Qualified trial starts (trial start + activation within 72h)
- **Baseline:** Set at end of Week 4
- **Gate:** ≥150 trials AND ≥25% activation by Day 30
- **Reporting:** Weekly GSC + trial dashboard sync
