"""INTENTIONALLY VULNERABLE demo app -- FOR AUTHORIZED SECURITY TESTING ONLY.

================================================================================
  🚨 DO NOT DEPLOY. DO NOT ADD REAL DATA. This is a deliberately-broken test
  fixture for a sandboxed pentest agent. Every vulnerability below is planted on
  purpose. All data is fake. Run it only inside an isolated sandbox / localhost.
================================================================================

Planted vulnerabilities:
  1. Leaked key   -- fake Supabase service_role JWT embedded in /static/app.js
  2. Open DB      -- /rest/v1/<table> returns rows for ANY key (RLS "disabled")
  3. Missing auth -- /api/admin returns sensitive data with no authentication
  4. IDOR         -- /api/orders/<id> returns any order, no ownership check

Run:  python app.py [port]      (default 8000)
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

# Obviously-fake service_role key (JWT shape). PLANTED BUG: never ship this to a
# browser in real code. This value is not a real credential.
FAKE_SERVICE_ROLE_JWT = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJyb2xlIjoic2VydmljZV9yb2xlIiwiaXNzIjoic3VwYWJhc2UiLCJyZWYiOiJkZW1vLWZha2UifQ."
    "FAKEdemoSIGNATUREvalue0123456789abcdefXYZ"
)

INDEX_HTML = """<!doctype html>
<html><head><title>Demo Shop (INTENTIONALLY VULNERABLE — TEST ONLY)</title></head>
<body style="font-family:sans-serif">
  <div style="background:#B00020;color:#fff;padding:10px;font-weight:bold">
    ⚠️ INTENTIONALLY VULNERABLE TEST APP — NOT A REAL SERVICE — DO NOT USE REAL DATA
  </div>
  <h1>Demo Shop</h1>
  <p>A deliberately-insecure practice target for authorized security testing.</p>
  <script src="/static/app.js"></script>
</body></html>
"""

APP_JS = f"""// demo client bundle -- INTENTIONALLY VULNERABLE TEST APP
const SUPABASE_URL = window.location.origin;
// PLANTED BUG #1: a service_role key must NEVER live in a client bundle.
const SUPABASE_SERVICE_ROLE_KEY = "{FAKE_SERVICE_ROLE_JWT}";
const API = {{
  profiles: SUPABASE_URL + "/rest/v1/profiles",
  admin:    SUPABASE_URL + "/api/admin",
  order:    (id) => SUPABASE_URL + "/api/orders/" + id,
}};
console.log("demo shop (vulnerable test app) booted");
"""

# All data below is FAKE. No real people, emails, phones, or cards.
PROFILES = [
    {"id": 1, "email": "alice@example.test", "phone": "+1-415-555-0001", "role": "user"},
    {"id": 2, "email": "bob@example.test", "phone": "+1-415-555-0002", "role": "user"},
    {"id": 3, "email": "carol@example.test", "phone": "+1-415-555-0003", "role": "admin"},
]
ORDERS = {
    "1001": {"id": "1001", "user_id": 1, "total": 42.0, "card_last4": "4242"},
    "1002": {"id": "1002", "user_id": 2, "total": 99.5, "card_last4": "1881"},
}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type="application/json", extra=None):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_):
        pass

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            return self._send(200, INDEX_HTML, "text/html")
        if path == "/static/app.js":
            return self._send(200, APP_JS, "application/javascript")
        # PLANTED BUG #2: open "Supabase" REST -- rows for ANY/no key.
        if path.startswith("/rest/v1/"):
            table = path[len("/rest/v1/"):]
            rows = PROFILES if table == "profiles" else []
            total = len(rows)
            return self._send(
                200, json.dumps(rows),
                extra={"content-range": f"0-{max(total - 1, 0)}/{total}"},
            )
        # PLANTED BUG #3: missing auth on admin data.
        if path == "/api/admin":
            return self._send(200, json.dumps({"secret": "all users", "profiles": PROFILES}))
        # PLANTED BUG #4: IDOR on orders.
        if path.startswith("/api/orders/"):
            order = ORDERS.get(path[len("/api/orders/"):])
            if order:
                return self._send(200, json.dumps(order))
            return self._send(404, json.dumps({"error": "not found"}))
        return self._send(404, json.dumps({"error": "not found"}))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"INTENTIONALLY VULNERABLE demo target on http://127.0.0.1:{port} (test only)")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
