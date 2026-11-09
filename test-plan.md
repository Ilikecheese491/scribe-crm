# SMB CRM Test Plan & Acceptance Criteria

**Launch Gate:** Rigel owns auth/rate-limiting/retention (pending)  
**Content Ready:** Lin's scaffold complete (16/16 tests passing)

---

## Content Readiness Check

| Criterion | Pass Condition |
|-----------|----------------|
| Pages render | HTML valid, no console errors |
| Links resolve | 0 404s, 301s valid |
| Meta tags | Title < 60 chars, desc < 155 chars |
| Load time | Core Web Vitals: LCP < 2.5s, CLS < 0.1 |
| Crawler pass | clean crawl, no indexation issues |

---

## Launch-Ready Gates

| Gate | Status Owner | Trigger Condition |
|------|--------------|-------------------|
| Tracking wired | Lin | `/track/*` endpoints return 200 |
| Baseline live | Growth Analyst | Day-7 measurement dashboard |
| Rollback plan | Rigel | One-click revert to snapshot state |

---

## Pre-Launch Checklist

- [ ] Pillar page SEO validated (Technical SEO Auditor)
- [ ] Keyword calendar synced (Keyword Researcher)
- [ ] Competitor gap analysis complete (Technical SEO Auditor)
- [ ] Messaging framework approved (Strategy Analyst)
- [ ] Measurement taxonomy aligned (Lin)
- [ ] Channel plan gated (Distribution Lead)

---

## Post-Launch Monitoring

| Metric | Alert Threshold | Owner |
|--------|-----------------|-------|
| 404 errors | >5/day | Frontend |
| Trial conversion | <20% Day 7 | Growth |
| Page speed | LCP > 3s | Tech Lead |
