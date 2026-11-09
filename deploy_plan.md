# Deploy Plan: Tracking Endpoint

## Deploy Target: **Render Free Python Web Service**

### Recommendation
Deploy Lin's tracking endpoint on Render (free tier, `scribe.onrender.com`) paired with Netlify Pages for the static landing site.

### Why Render vs Alternatives

| Platform | Pros | Cons |
|----------|------|------|
| **Render** | Free Python runtime, auto HTTPS, free subdomain, persistent disk option | Cold starts on free tier |
| **Netlify Functions** | Good for static sites, integrated | Requires Node.js, not Python, no persistent disk |
| **Cloudflare Workers** | Low latency | No Python runtime (Workers are JS/TS only) |
| **Railway** | Good free tier | More complex setup |

**Decision**: Render is the only option that hosts a Python stdlib-only server without build steps or custom runtimes.

### Endpoint URL
`https://scribe.onrender.com` (already updated in landing/trial.js)

---

## Auth + Rate Limit Plan

### Current State
- Rate limit: 300 requests/IP/hour (configurable via `TRACK_RATE_LIMIT`)
- Public key: Optional, checked in header and body
- Summary endpoint: Requires `SUMMARY_SECRET` Bearer token

### Pre-Launch Auth Enhancements

**1. Public Key Authentication (Client-Side)**

Set `TRACK_PUBLIC_KEY` env var. Clients must include it in request body (key field). This prevents:
- Bot scraping of the endpoint
- Anonymous spam from curl/script

```env
TRACK_PUBLIC_KEY=<your-generated-key>
```

**2. Rate Limit: Recommended Settings**

| Environment | Limit | Rationale |
|-------------|-------|-----------|
| Dev / Internal | Unlimited (0) | For testing, skip rate limits |
| Staging | 500/hour/IP | Catch abuse before prod |
| Production | 300/hour/IP | Protects service, enough for 100 trials/day |

Set via `TRACK_RATE_LIMIT=300`

**3. IP-Based Throttling**

The endpoint already implements IP-based hourly throttling. Combined with public key auth:
- Legitimate users: 300+ events/hour allowed
- Bots: Blocked after 300 requests from same IP
- Spoofed IPs: Rate limit still effective (even if distributed)

### Launch Gate Checklist

- [ ] Create Render account and connect at https://dashboard.render.com
- [ ] Set `TRACK_PUBLIC_KEY` in Render environment
- [ ] Set `TRACK_RATE_LIMIT=300` (or 0 for dev)
- [ ] Set `TRACK_DB_FILE=/opt/render/project/src/api/data/track.db` for persistence
- [ ] Set `TRACK_DB=sqlite` for simple file-based storage
- [ ] Set `SUMMARY_SECRET` for dashboard access
- [ ] Verify POST /track returns 202
- [ ] Verify GET /health returns 200
- [ ] Verify duplicate event_id deduplicates (202 response)
- [ ] Verify `/summary` requires `Authorization: Bearer {SUMMARY_SECRET}`

---

## Publishing the Landing Page

1. **Deploy to Netlify:**
   - Create Netlify account (if not exists)
   - Drag the `landing/` folder to Netlify Drop: https://app.netlify.com/drop
   - Get URL: `https://scribe.netlify.app` (or similar)

2. **Verify trial.js is updated:**
   - API_URL is already set to `https://scribe.onrender.com`
   - PUBLIC_KEY placeholder remains (set when you have a key)

3. **Test the integration:**
   - Open landing page in browser
   - Check browser console for `session_start` events
   - Click "Start Free Trial" - should fire `cta_click` then redirect to signup
   - On signup, complete form - should see two events: `trial_start` and `activation`

---

## Files Ready to Deploy

### API Files (for Render)
- `api/app.py` — 107 lines of Python stdlib-only HTTP server
- `api/schema.sql` — Database schema with events table and views
- `api/data/` — Directory for SQLite database

### Landing Page Files (for Netlify)
- `landing/index.html` — Main landing page with hero, problem, market reality sections
- `landing/signup.html` — Signup form with tracking and activation
- `landing/trial.js` — Client tracking snippet (updated with Render URL)
- `landing/test-harness.html` — Manual test page for launch gate verification

### Configuration Files
- `render.yaml` — Render Blueprint (web service + static site)
- `netlify.toml` — Static site config for landing

---

## Automated Deployment Steps

```bash
# 1. Deploy API to Render (requires account connection)
# Visit: https://dashboard.render.com
# Create New → Web Service → Connect Git or use Blueprint
# Or drag api/ folder contents if manual

# 2. Deploy landing to Netlify
curl -X POST -F "file=@landing.zip" https://app.netlify.com/api/v1/sites

# 3. Set environment variables on Render
# TRACK_PUBLIC_KEY=your-key-here
# TRACK_RATE_LIMIT=300
# SUMMARY_SECRET=your-secret-here
# TRACK_DB_FILE=/opt/render/project/src/api/data/track.db

# 4. Update trial.js URL (already done)
API_URL = "https://scribe.onrender.com"
```

## Next Steps After Launch

1. Monitor `/summary` endpoint for trial activation metrics
2. Set up monitoring alerts for rate limiting
3. Migrate to custom domain once purchased
4. Scale to managed PostgreSQL when data volume grows

