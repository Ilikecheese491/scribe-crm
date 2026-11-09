PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS events (
  event_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  ts INTEGER NOT NULL,
  event TEXT NOT NULL CHECK(event IN ('session_start','cta_click','trial_start','activation')),
  email TEXT,
  device TEXT NOT NULL,
  channel TEXT,
  utm_source TEXT,
  utm_medium TEXT,
  utm_campaign TEXT,
  business_size TEXT,
  method TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_email_device ON events(email,device,event);
CREATE INDEX IF NOT EXISTS idx_events_event_ts ON events(event,ts);
CREATE TABLE IF NOT EXISTS rate_limits (
  ip TEXT NOT NULL,
  window_start INTEGER NOT NULL,
  n INTEGER NOT NULL,
  PRIMARY KEY(ip,window_start)
);
CREATE VIEW IF NOT EXISTS v_trial_activation AS
SELECT t.session_id, t.event_id AS trial_event_id, t.ts AS trial_ts,
       a.event_id AS activation_event_id, a.ts AS activation_ts,
       (a.ts - t.ts)/3600.0 AS hours_to_activate,
       CASE WHEN a.ts IS NOT NULL AND (a.ts - t.ts) BETWEEN 0 AND 72*3600 THEN 1 ELSE 0 END AS qualified
FROM (SELECT * FROM events WHERE event='trial_start') t
LEFT JOIN (SELECT * FROM events WHERE event='activation') a
  ON a.session_id = t.session_id
ORDER BY t.ts DESC;
CREATE VIEW IF NOT EXISTS v_daily AS
SELECT date(ts,'unixepoch') AS day,
       COUNT(DISTINCT CASE WHEN event='trial_start' THEN session_id END) AS trials_started,
       COUNT(DISTINCT CASE WHEN event='activation' THEN session_id END) AS activations,
       COUNT(*) AS total_events
FROM events
GROUP BY day;
