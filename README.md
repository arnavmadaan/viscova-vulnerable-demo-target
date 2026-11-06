# ⚠️ INTENTIONALLY VULNERABLE — FOR SECURITY TESTING ONLY ⚠️

> **🚨 DO NOT DEPLOY THIS. DO NOT PUT REAL DATA IN IT. 🚨**
>
> This repository is a **deliberately insecure demo application**. Every
> vulnerability in it is **planted on purpose** as a test fixture for an
> authorized, sandboxed penetration-testing agent (Viscova). It exists only so
> that automated testing can find known bugs in a system nobody will be harmed by.
>
> It contains **no real users, no real secrets, and no real data** — only
> obviously-fake placeholder values. It is meant to be cloned and run **inside an
> isolated sandbox**, never on a public server or anywhere reachable from the
> internet.

---

## What this is

A tiny "demo shop" web app that intentionally ships several common web
vulnerabilities, so a security tool can be demonstrated finding them with
reproducible evidence. Think of it like a miniature, single-file OWASP Juice
Shop / DVWA — a **practice target**, not a product.

## Planted vulnerabilities (on purpose!)

| # | Class | Where |
|---|-------|-------|
| 1 | **Leaked secret key** | A fake Supabase `service_role` key is embedded in the client JS bundle (`/static/app.js`). |
| 2 | **Open database / broken access control** | `/rest/v1/<table>` returns rows for *any* key (as if Row-Level Security were disabled). |
| 3 | **Missing authentication** | `/api/admin` returns sensitive data with no auth. |
| 4 | **IDOR** | `/api/orders/<id>` returns any order with no ownership check. |

All "sensitive" data (emails, phone numbers, card digits) is **made up**.

## Run it (sandbox / localhost only)

```bash
python app.py 8000
# or
docker build -t vuln-demo . && docker run --rm -p 8000:8000 vuln-demo
```

Then browse to `http://localhost:8000`.

## Safety / legal

- This code is published **solely** as an authorized test target. Running it
  against anyone, or deploying it where others can reach it, is **not** its
  intended use and could expose the (fake) app to abuse.
- Do not add real credentials, real personal data, or real payment details.
- If you fork or reuse this, **keep these warnings**.

_Published for authorized security testing and education only._
