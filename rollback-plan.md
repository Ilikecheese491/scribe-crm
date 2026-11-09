# Rollback Plan

## Trigger
If launch gate fails (activation rate <25% or >150 trials with no qualified activations), or if tracking is broken.

## One-Click Rollback Steps

### 1. Disable Landing Page
- In Netlify dashboard → site settings → disable site, or point DNS to maintenance page
- Alternative: set `trial.js` `API_URL` to empty string to silently drop events

### 2. Revert Tracking
- Restore previous `trial.js` from git/tag if versioned
- On Render: deploy a no-op version that returns 202 for all `/track` POSTs without writing to DB

### 3. Preserve Data
- Export SQLite: `sqlite3 track.db .dump > backup.sql`
- Download track.db from Render dashboard before any reset

### 4. Analyze Before Re-launch
- Query `/summary` for: trial count, qualified count, activation rate, avg hours to activate
- Check for: high trial_start with zero activation (form bug), high cta_click with zero trial_start (signup friction), all events from single IP (bot traffic)

### 5. Fix & Re-test
- Fix identified issues in landing/signup/trial.js
- Test with `test-harness.html` locally before re-deploying
- Re-enable only after 10 manual tests pass

## Snapshot State
- Current working state: all files in `/home/user/workspace/smb-crm/`
- API tested: `/health` returns 200, `/track` accepts events, `/summary` returns metrics
- No production data yet (fresh SQLite)
