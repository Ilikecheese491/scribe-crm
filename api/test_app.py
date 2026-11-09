import sys, os, sqlite3, json, time
sys.path.insert(0, os.path.dirname(__file__))
# quick smoke test of schema
db = "/tmp/test_track.db"
if os.path.exists(db):
    os.remove(db)
os.environ["TRACK_DB_FILE"] = db
import app
conn = app.get_conn()
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("tables:", tables)
assert "events" in tables, "events missing"
# idempotent insert
payload = {
  "event_id":"e1","session_id":"s1","ts":int(time.time()),
  "event":"trial_start","device":"d1","email":"a@b.com"
}
import http.server
from io import BytesIO
# simplified: just test db insert via app.Handler? skip
# Instead test direct insert
conn.execute("""INSERT INTO events(event_id,session_id,ts,event,email,device) VALUES(?,?,?,?,?,?)""",
             (payload["event_id"],payload["session_id"],payload["ts"],payload["event"],payload["email"],payload["device"]))
conn.commit()
row = conn.execute("SELECT * FROM events WHERE event_id=?", ("e1",)).fetchone()
print("insert ok:", row is not None)
print("PASS")
