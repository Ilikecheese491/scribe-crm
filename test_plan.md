# SMB CRM Test Plan & Acceptance Criteria
**Version:** 1.0 | **Last Updated:** 2026-11-08 | **Author:** QA & Release Engineer

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Acceptance Criteria Framework](#acceptance-criteria-framework)
   - [Content Readiness](#content-readiness)
   - [Launch Readiness](#launch-readiness)
3. [Risk-Based Test Strategy](#risk-based-test-strategy)
4. [Test Matrix by Component](#test-matrix-by-component)
5. [Launch Gates & Go/No-Go Criteria](#launch-gates--go-no-go-criteria)
6. [Rollback Plan](#rollback-plan)
7. [Post-Launch Monitoring](#post-launch-monitoring)

---

## Executive Summary

This document defines the acceptance criteria for the SMB CRM product launch, organized as risk-based test phases. Success is measured against two primary states:

- **Content Ready to Publish:** All marketing assets and the landing experience are technically sound and SEO-optimized
- **Launch Ready:** All tracking, measurement, and safety mechanisms are verified and operational

**References:**
- Lin's tracking scaffold: `crm-tracker/` (16/16 tests passing)
- Rigel's launch gate implementation integrates auth/rate-limiting/retention
- Measurement spec: `/home/user/workspace/smb-crm/measurement-spec.md`

---

## Acceptance Criteria Framework

### Content Readiness

**Definition:** Pages render correctly, links resolve, no 404s exist, load times meet thresholds, and SEO crawlers pass cleanly.

| Criterion | Threshold | Verification Method | Status |
|-----------|-----------|---------------------|--------|
| **Page Renders** | HTML validates, no console errors | Manual QA + Lighthouse | ⬜ |
| **Internal Links** | 0 broken links | Link checker (broken-link-checker) | ⬜ |
| **External Links** | 0 broken external links | External link validator | ⬜ |
| **Load Time (3G)** | < 3 seconds | Lighthouse Performance score ≥ 90 | ⬜ |
| **Core Web Vitals** | LCP < 2.5s, FID < 100ms, CLS < 0.1 | PageSpeed Insights | ⬜ |
| **SEO Crawl** | No robots.txt blocks, valid meta tags | Screaming Frog / SiteCrawler | ⬜ |
| **Mobile Responsiveness** | No horizontal scroll at 360px | Chrome DevTools viewport test | ⬜ |
| **Accessibility** | WCAG 2.1 AA minimum | axe-core automated scan | ⬜ |
| **Favicon & Meta** | All platforms covered (Twitter, Facebook) | Manual inspection | ⬜ |

### Launch Readiness

**Definition:** Tracking is wired end-to-end, measurement baseline is live and accurate, and rollback plan is documented and tested.

| Criterion | Threshold | Verification Method | Status |
|-----------|-----------|---------------------|--------|
| **Tracking Endpoint** | `/track` receives events with valid structure | 10 test sessions via `test-harness.html` | ⬜ |
| **Event Fidelity** | Events not dropped during rate limits | Load test: 100 concurrent sessions | ⬜ |
| **Measurement Baseline** | 0 qualified trials reported (Day 0 state) | Verify `/summary` endpoint shows empty state | ⬜ |
| **Auth Integration** | Invalid keys rejected, valid keys accepted | 2 test API keys | ⬜ |
| **Rate Limiting** | >100 requests/min from single IP returns 429 | 150 req burst test | ⬜ |
| **Data Retention** | Events older than 90 days auto-deleted | Verify DELETE policy in schema | ⬜ |
| **Rollback Plan** | Documented with <5 min RTO | Review `rollback-plan.md` | ⬜ |
| **Monitoring Alerts** | PagerDuty alerts fire for >5% error rate | Simulate error condition | ⬜ |

---

## Risk-Based Test Strategy

### Phase 1: Pre-Launch (Content Foundation)
**Priority: Critical** | **Risk: High** | **Impact: Blocking**

| Test Area | Risk Owner | Pre-conditions | Pass Criteria |
|-----------|------------|----------------|---------------|
| Landing page conversion | Growth Lead | Copy approved | ≥ 40% viewport height for hero CTA |
| Pricing page accuracy | Finance | Prices final | All prices render in USD |
| Trial flow completion | Frontend Engineer | API keys configured | 100% success rate (10/10) |
| SEO technical audit | SEO Strategist | Pages live on staging | 0 critical SEO issues |

### Phase 2: Tracking & Measurement (Launch Gate)
**Priority: Critical** | **Risk: High** | **Impact: Blocking**

| Test Area | Risk Owner | Pre-conditions | Pass Criteria |
|-----------|------------|----------------|---------------|
| Event pipeline | Growth Analyst | Tracker scaffold built | All 16 tests pass |
| Activation event | Tech Lead | `trial.js` integrated | 10 sessions produce 14+ events |
| Rate limiting | Backend Engineer | Load test tool ready | 101st request returns 429 |
| Database persistence | Dev | Render DB mounted | Events persist after deploy |

### Phase 3: Launch Gate Verification (Go/No-Go)
**Priority: Critical** | **Risk: Medium** | **Impact: Blocking**

| Gate | Threshold | Verification | Owner |
|------|-----------|--------------|-------|
| Qualified Trials (Day 30) | ≥ 150 total, ≥ 25% qualified | `/summary` endpoint | Growth Lead |
| Activation Rate | ≥ 25% of trials complete activation | Measure event `activation_start` | Growth Lead |
| Technical Health | Error rate < 5%, 99% uptime | Datadog/PagerDuty | Tech Lead |
| Business Health | CAC payback ≤ 30 days | Financial model | Finance |

---

## Test Matrix by Component

### Landing Experience
| Component | Test Case | Expected Result | Tool |
|-----------|-----------|-----------------|------|
| Hero section | Headline renders correctly | "CRM that runs itself" visible | Manual |
| CTA button | Navigation to signup | `/signup.html` loads | Cypress |
| Pricing display | All prices visible | $0, $9/seat, $19/seat | Lighthouse |
| Form validation | Invalid email rejected | Inline error message | Cypress |

### Tracking Endpoint (`/track`)
| Component | Test Case | Expected Result | Tool |
|-----------|-----------|-----------------|------|
| CORS headers | Preflight succeeds | `Access-Control-Allow-Origin: *` | curl |
| Rate limit | 101 requests/min | HTTP 429 response | locust |
| Auth validation | Invalid key rejected | HTTP 401 | Postman |
| Data storage | Event persisted | Query returns event | SQLite CLI |

### API Endpoints
| Endpoint | Test Case | Expected Result |
|----------|-----------|-----------------|
| `/track` | POST with valid event | HTTP 200, event stored |
| `/track` | POST over rate limit | HTTP 429 |
| `/track` | POST invalid API key | HTTP 401 |
| `/summary` | GET after qualifying trial | Returns qualified count |
| `/health` | GET | HTTP 200, health status |

---

## Launch Gates & Go/No-Go Criteria

### Gate 1: Content Freeze (Day 0)
**Pass when:**
- ✅ All landing pages static content complete
- ✅ All internal links verified
- ✅ SEO audit passes with 0 critical issues
- ✅ Mobile viewport tests pass

**Fail condition:** Any broken link, SEO issue severity ≥ 3, or mobile layout bug

### Gate 2: Tracking Verification (Day 0)
**Pass when (per Lin's scaffold):**
- ✅ 16/16 tests passing in `crm-tracker/test_app.py`
- ✅ `test-harness.html` produces events for 10 sessions
- ✅ `/summary` returns accurate counts
- ✅ Rate limiting active and configured

**Fail condition:** Any tracking test failure, or events not appearing in `/summary`

### Gate 3: Launch (Day 30)
**Pass when (per Rigel's gate):**
- ✅ ≥ 150 qualified trials recorded
- ✅ ≥ 25% of trials completed activation workflow
- ✅ 99%+ API availability (error rate < 1%)
- ✅ No data leaks or security incidents

**Fail condition:** Any threshold unmet for 3 consecutive days → no paid spend

---

## Rollback Plan

### Scenario 1: Landing Page Error
**Detection:** 404 rate > 1% or CTA click-through < 10%
**Action:**
1. Revert DNS to previous snapshot (TTL: 5 min)
2. Notify: `@Growth Lead`, `@Tech Lead`
3. RTO: < 15 minutes

### Scenario 2: Tracking Failure
**Detection:** Event rate drops > 50% or `/health` returns unhealthy
**Action:**
1. Deploy previous working version (via Render manual rollback)
2. Disable tracking beacon in frontend
3. RTO: < 10 minutes

### Scenario 3: Database Corruption
**Detection:** `/summary` returns errors or inconsistent counts
**Action:**
1. Restore from last PostgreSQL backup (daily at 00:00 UTC)
2. Re-import events from S3 archive (7-day retention)
3. RTO: < 1 hour

---

## Post-Launch Monitoring

### Daily Checks (Automated)
- [ ] Event volume ≥ 5x baseline (Day 1-7) or alert
- [ ] Error rate < 1%
- [ ] `/health` endpoint returns healthy

### Weekly Checks (Manual)
- [ ] Data accuracy audit (compare `/summary` counts to raw events)
- [ ] Activation funnel conversion rates
- [ ] CAC calculation based on actual spend

### Communication Plan
| Stakeholder | On Issue | Template |
|-------------|----------|----------|
| CEO | Any launch gate failure | `@you Launch gate [tracking/content] failed: [issue]. Rollback initiated.` |
| Growth Lead | Traffic or conversion drop | `Traffic down [X]%, investigating. Monitoring.` |
| Tech Lead | Infrastructure alert | `Alert: [component] experiencing [error]. [action] taken.` |

---

## Appendices

### Appendix A: Test Environment URLs
- Staging: `https://smb-crm-staging.netlify.app`
- Tracking Endpoint: `https://crm-tracker.onrender.com`
- Health Check: `https://crm-tracker.onrender.com/health`

### Appendix B: Contact List
- **Tech Lead:** @Tech Lead (primary), @Dev (secondary)
- **Growth:** @Growth Lead (primary), @SEO Strategist (secondary)
- **QA:** @QA and Release Engineer (primary)
- **Business:** CEO (emergency escalation only)

### Appendix C: Test Completion Sign-Off
| Phase | Performed By | Date | Status |
|-------|--------------|------|--------|
| Content Readiness | QA | 2026-11-08 | ⬜ |
| Tracking Verification | QA + Growth | 2026-11-08 | ⬜ |
| Launch Gate Review | Growth Lead | TBD | ⬜ |

---

*Document follows the "CRM for Small Business" positioning and aligns with the 90-day SEO roadmap.*
