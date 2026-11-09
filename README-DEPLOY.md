# SMB CRM — Deploy bundle

## Host decision (sensible default)
**Static site:** Netlify Pages (free subdomain `name.netlify.app`)
**API / tracking endpoint:** Render Web Service (Python, free tier, `name.onrender.com`)

Why: Netlify Pages has no server-side code. Lin's tracking scaffold is stdlib-only Python and needs a Python runtime. Render provides a free Python web service with a free subdomain, keeping one account for API and static (Netlify for static). Both can swap to a clean domain later.

Name is still open (Writer proposed Tally / Scribe / Relay, prefers Scribe). Replace `scribe` in configs with the chosen name.

## What’s in this bundle
- `api/app.py` — stdlib-only HTTP server implementing Lens taxonomy:
  - POST /track — 202 accepted, 400 bad, 409 duplicate
  - GET /health — 200
  - GET /summary — totals, activation rate, avg time-to-activate, channel mix
  - Dedupe: event_id PK, one trial per email+device, anonymous deduped on device, resends no-op
  - Rate limit: 300 req/IP/hour (env TRACK_RATE_LIMIT)
  - Storage: file SQLite (dev) or Turso/Neon HTTP (prod) via env
- `api/schema.sql` — events table, indexes, v_trial_activation, v_daily
- `landing/trial.js` — drop-in client snippet. Generates session_id, device_id, event_id, parses UTM, fires:
  session_start, cta_click, trial_start, activation (first value only, client-guarded)
- `landing/test-harness.html` — manual test page for Rigel’s launch gate (10 sessions, zero dropped events)
- `render.yaml` — Render Blueprint: web service + static site
- `netlify.toml` — static site config for landing

## Deploy steps
1. Create Render account → New Blueprint → point to this folder.
2. Set env vars:
   - TRACK_DB=file (dev) or turso/neon (prod)
   - TRACK_DB_FILE=/opt/render/project/src/api/data/track.db (persisted disk)
   - TRACK_RATE_LIMIT=300
   - TRACK_PUBLIC_KEY= (optional client key, checked in header/body)
   - SUMMARY_SECRET= (required for /summary)
3. Run `python api/app.py` locally to test. DB file is created on first request.
4. Netlify: drag the `landing/` folder for static hosting or connect Git.
5. Replace placeholder API_URL in trial.js with Render service URL.
6. Verify:
   - GET /health → 200
   - POST /track with valid payload → 202
   - Duplicate event_id → 202 (idempotent) or 409 per policy
   - /summary requires SUMMARY_SECRET

## Launch gate items owned by team
- Rigel: auth/rate-limit, email/device retention policy, 10 sessions 0 dropped events
- Frontend Engineer: wire trial.js into landing hero, CTA, sign-up
- Tech Lead: confirm Render persists DB across deploys

Free subdomain today, swap later when domain purchased.
