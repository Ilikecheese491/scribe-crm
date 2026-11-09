# SMB CRM Measurement Specification

**Primary Metric:** Qualified trial starts  
**Definition:** A `trial_start` event with a matching `activation` event within 72 hours (Lens's day-30 gate: 150+ qualified trials AND ≥25% activation)  
**Status:** Lin's scaffold (`api/app.py`, `schema.sql`) implements this with 16/16 tests passing

---

## Event Taxonomy (from scaffold)

| Event | Trigger | Required Fields | Notes |
|-------|---------|-----------------|-------|
| `session_start` | Page load via `trial.js` | `session_id`, `device`, `event_id`, `ts` | Fires automatically |
| `cta_click` | CTA button click | `channel`, `event` (label) | Client helper: `scribeTrack(label)` |
| `trial_start` | Sign-up form submit | `email`, `business_size` (optional) | Client helper: `scribeStartTrial(email, size)` |
| `activation` | User completes core action | `method` (what they activated) | Client-guarded: fires once per session via `scribeActivate(method)` |

All events POST to `/track` with JSON body:
```json
{
  "event_id": "uid()",
  "session_id": "uid()",
  "ts": Unix timestamp,
  "event": "session_start|cta_click|trial_start|activation",
  "email": "user@example.com",
  "device": "device_id",
  "channel": "web",
  "utm_source": "...", "utm_medium": "...", "utm_campaign": "...",
  "business_size": "1-5|6-20|21-100",
  "method": "email_import|automation_turned_on|team_added"
}
```

**Note:** Field names in schema are `event`, `email`, `device`, `channel`, `utm_source`, `utm_medium`, `utm_campaign`, `business_size`, `method`. Earlier docs incorrectly used `event_id` as `event_type`, `email_domain`, `timestamp`.

---

## Qualification Logic (v_trial_activation view)

A trial qualifies if:
1. A `trial_start` event exists for the session
2. An `activation` event exists for the same `session_id`
3. `activation.ts - trial_start.ts ≤ 72 hours`

```sql
SELECT ...
FROM events WHERE event='trial_start' t
LEFT JOIN events WHERE event='activation' a ON a.session_id = t.session_id
WHERE (a.ts - t.ts) BETWEEN 0 AND 72*3600
```

---

## Baseline & Decision Thresholds

| Milestone | Trials Needed | Qualified Trials | Activation Rate | Decision |
|-----------|---------------|------------------|-----------------|----------|
| Day 7 | 50 | 12+ | ≥25% | Early signals — verify channel quality |
| Day 30 | 150 | 38+ | ≥25% | **Day-30 gate** — greenlight paid spend |
| Day 60 | 400 | 100+ | ≥25% | Scale paid spend 2x |
| Day 90 | 1,000 | 250+ | ≥25% | Scale expansion — add channels |

**Threshold note:** The "≥25% activation" is the *qualified rate* (qualified trials ÷ total trials). At Day 30, this means the `/summary` endpoint should return:
```json
{
  "trials": 150,
  "qualified": 38,
  "activation_rate": 0.253,
  "avg_hours_to_activate": <30
}
```

---

## Reporting Cadence

| Cadence | Owner | Metric | Target | Alert |
|---------|-------|--------|--------|-------|
| **Daily** | Growth Analyst | `v_daily.trials_started` | Track volume | <10/day after Day 14 |
| **Weekly** | Growth Analyst | Qualified rate, mean time-to-activate | Compare to baseline | Rate <20% OR avg_hours >36 |
| **Bi-weekly** | Growth Lead | Channel mix (by `utm_source`) | Cost-per-qualified | Paid channels not contributing ≥50% |

---

## Tracking Endpoints (Dev → Wire)

| Endpoint | Method | Auth | Authored by | Purpose |
|----------|--------|------|-------------|---------|
| `POST /track` | JSON | `TRACK_PUBLIC_KEY` (optional) | Lin's scaffold | Ingest all events |
| `GET /health` | N/A | N/A | Lin's scaffold | Liveness probe |
| `GET /summary` | N/A | `Bearer «redacted 14 chars»` | Lin's scaffold | Dashboard: trials, qualified, rate, avg_hours |

**Wire checklist (per test-plan.md launch gate):**
- [ ] Frontend Engineer: inject `trial.js` in landing hero, CTA, sign-up (replace `API_URL`, `PUBLIC_KEY`)
- [ ] Tech Lead: verify Render DB persists across deploys (`/data/track.db`)
- [ ] QA: 10 sessions via `test-harness.html`, zero dropped events

---

## Rollout Checkpoints

- **Week 1:** Endpoint health check (500 OK, `/health` returns 200)
- **Week 2:** Data integrity (no duplicate `event_id`s, 10-session smoke test)
- **Week 3:** Attribution mapping (UTM → `channel` field populates)
- **Week 4:** Baseline locked (Day-30 metric ready for paid decision)

---

## What This Is NOT

- Not a product analytics tool — no funnel steps beyond trial→activation
- Not a replacement for product-level event tracking (feature usage, retention by week)
- Does NOT include SOC-2 or PII compliance — email stored in plain text in SQLite

---

## References

- Event schema: `api/schema.sql`
- HTTP handler: `api/app.py`
- Client snippet: `landing/trial.js`
- Views: `v_trial_activation`, `v_daily`
- Tests: `api/test_app.py` (16/16 passing)
