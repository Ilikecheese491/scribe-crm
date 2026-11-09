import json, os, sqlite3, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

BASE = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.environ.get("TRACK_DB_FILE", os.path.join(BASE,"data/track.db"))
RATE_LIMIT = int(os.environ.get("TRACK_RATE_LIMIT","300"))
PUBLIC_KEY = os.environ.get("TRACK_PUBLIC_KEY","")
SUMMARY_SECRET = os.environ.get("SUMMARY_SECRET","")

def get_conn():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL")
    with open(os.path.join(BASE,"schema.sql"),"r") as f:
        conn.executescript(f.read())
    conn.commit()
    return conn

def check_rate(ip, conn):
    if RATE_LIMIT <= 0:
        return True
    window = int(time.time()//3600)
    cur = conn.execute("SELECT n FROM rate_limits WHERE ip=? AND window_start=?", (ip, window))
    row = cur.fetchone()
    if row:
        n = row[0]+1
        if n > RATE_LIMIT:
            return False
        conn.execute("UPDATE rate_limits SET n=? WHERE ip=? AND window_start=?", (n, ip, window))
    else:
        conn.execute("INSERT INTO rate_limits(ip,window_start,n) VALUES(?,?,1)", (ip, window))
    conn.commit()
    return True

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self._json(200, {"ok":True})
            return
        if path == "/summary":
            auth = self.headers.get("Authorization","")
            if SUMMARY_SECRET and auth != f"Bearer {SUMMARY_SECRET}":
                self._json(401, {"error":"unauthorized"})
                return
            conn = get_conn()
            cur = conn.execute("SELECT COUNT(*) FROM events WHERE event='trial_start'")
            trials = cur.fetchone()[0]
            cur = conn.execute("SELECT COUNT(*) FROM v_trial_activation WHERE qualified=1")
            qualified = cur.fetchone()[0]
            rate = qualified/trials if trials else 0
            cur = conn.execute("SELECT AVG(hours_to_activate) FROM v_trial_activation WHERE activation_event_id IS NOT NULL")
            avg_h = cur.fetchone()[0]
            self._json(200, {"trials":trials,"qualified":qualified,"activation_rate":rate,"avg_hours_to_activate":avg_h})
            return
        self._json(404, {"error":"not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/track":
            self._json(404, {"error":"not found"})
            return
        ip = self.client_address[0]
        conn = get_conn()
        if not check_rate(ip, conn):
            self._json(429, {"error":"rate limited"})
            return
        try:
            length = int(self.headers.get("Content-Length",0))
            data = json.loads(self.rfile.read(length))
        except Exception:
            self._json(400, {"error":"invalid json"})
            return
        if PUBLIC_KEY and data.get("key") != PUBLIC_KEY:
            self._json(401, {"error":"unauthorized"})
            return
        for k in ("event_id","session_id","event","ts"):
            if k not in data:
                self._json(400, {"error":f"missing {k}"})
                return
        device = data.get("device","")
        if not device:
            self._json(400, {"error":"device required"})
            return
        try:
            conn.execute("""INSERT INTO events(event_id,session_id,ts,event,email,device,channel,utm_source,utm_medium,utm_campaign,business_size,method)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            (data["event_id"], data["session_id"], int(data["ts"]), data["event"],
             data.get("email"), device, data.get("channel"), data.get("utm_source"), data.get("utm_medium"), data.get("utm_campaign"), data.get("business_size"), data.get("method")))
            conn.commit()
            self._json(202, {"ok":True})
        except sqlite3.IntegrityError:
            self._json(202, {"ok":True,"deduped":True})
        except Exception as e:
            self._json(500, {"error":str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT","8000"))
    HTTPServer(("0.0.0.0",port), Handler).serve_forever()
