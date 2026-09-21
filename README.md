# AYTAN ECO AI Manager V5 — client demo + owner CRM

This archive is a separate Flask service. It does **not** alter or deploy the existing AYTAN ECO website.

## Ready functions

- RU / KZ / EN manager with constrained AYTAN ECO knowledge base.
- Automatic lead capture from chat/form: phone, service, issue, city, object, area, desired time and urgency.
- SQLite CRM, saved conversation history, compact dialogue memory, duplicate-phone detection, preliminary estimates and audit-event timeline.
- Separate responsive owner panel at `/crm`: works on phones, tablets and desktop; list/search/filter, lead editing, status changes, chat history and CSV export.
- Owner login with `ADMIN_USERNAME` and `ADMIN_PASSWORD`; signed HttpOnly session and CSRF protection.
- Editable knowledge base inside the CRM. Every item has its own category, question and answer fields plus Save, Enable/Disable and Delete actions.
- Expanded knowledge transferred from the AYTAN ECO site: services, apartment/cottage prices, preparation, safety, guarantee, documents, B2B pest control and cautious agribusiness qualification.
- Signed, idempotent generic inbound webhook for a future channel adapter.
- Validation, request size limits, rate limits, session HMAC tokens, owner-token protection and security headers.

## Explicit integration status

WhatsApp Business API is **not connected**. Calendar booking is **not connected**. Owner notifications are **not connected**. A desired time remains a request until an owner confirms it.

## Deploy

1. Use Python 3.11+.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`, fill strong secrets, and do not commit `.env`.
4. Start: `python app.py`
5. Production command: `gunicorn --workers 2 --threads 4 --bind 0.0.0.0:$PORT app:app`

Client interface: `/`. Owner CRM: `/crm`.

Use HTTPS and a persistent disk for `DB_PATH`. SQLite is suitable for a small team on one app instance. For multiple instances, migrate to PostgreSQL and use Redis or proxy rate limiting.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `SESSION_SECRET` | Long random secret for private visitor-session tokens; required in production. |
| `ADMIN_USERNAME` | Owner login; default `aytanadmin`. |
| `ADMIN_PASSWORD` | Strong owner password; required for browser CRM login. |
| `ADMIN_TOKEN` | Optional long token for server-to-server CRM API access. |
| `COOKIE_SECURE` | Use `1` on HTTPS production; use `0` only for local HTTP testing. |
| `OPENAI_API_KEY` | Enables real OpenAI replies and extraction. Without it, safe offline capture and fallback consultation continue working. |
| `OPENAI_MODEL` | Optional; default `gpt-4.1-mini`. |
| `DB_PATH` | Persistent absolute SQLite path. |
| `INBOUND_WEBHOOK_SECRET` | Optional; enables only the generic signed inbound endpoint. |

Generate secrets: `python -c "import secrets; print(secrets.token_urlsafe(48))"`.

## Owner CRM API

The browser CRM logs in with username/password and uses a secure session. Server-to-server owner calls may use `X-Admin-Token: <ADMIN_TOKEN>`.

## Connecting OpenAI for the client demo

Set `OPENAI_API_KEY` in the hosting environment and redeploy. Do not put the key in HTML, GitHub, the ZIP, or a browser field. Open `/api/health`: `real_ai` must be `true`. Then test RU/KZ/EN questions, an unknown question, a price question and a complete order. Without a key the CRM and deterministic lead capture still work, but replies use safe fallback text.

- `GET /api/leads?q=...&status=...`
- `GET /api/leads/<id>`
- `PATCH /api/leads/<id>` — editable CRM fields such as `name`, `phone`, `service`, `notes`.
- `POST /api/leads/<id>/status` with `{"status":"В работе"}`.
- `GET /api/leads/export.csv`

## Future channel webhook — not a messenger integration

After setting `INBOUND_WEBHOOK_SECRET`, send `POST /api/inbound` with:

```json
{"external_id":"unique-message-id","session_id":"32-hex-character-session-id","source":"verified-provider-name","message":"Client message"}
```

Sign the exact raw body with HMAC-SHA256 and pass the lowercase hex digest in `X-Webhook-Signature`. Duplicate `external_id` values are ignored. A real WhatsApp/Telegram/etc. adapter must still be separately built, authenticated and tested before it can deliver messages.

## Verification

Run `python -m unittest -v`. The suite checks transparent integration status, lead capture, session privacy, owner authentication/CRM actions, CSV export and signed inbound webhook idempotency.


## V6 improvements
- SQLite busy timeout and foreign-key enforcement; use a persistent disk for DB_PATH.
- Owner notifications: set OWNER_WEBHOOK_URL to your own HTTPS endpoint and OWNER_WEBHOOK_SECRET. Payloads are HMAC-SHA256 signed using X-Aytan-Signature; do not use an arbitrary third-party URL. Failed notifications are logged; leads remain saved. No WhatsApp delivery is implied.
- Admin-only POST /api/admin/backup downloads a consistent SQLite backup. Store backups off-server and test restoration. This is a manual backup, not automatic scheduling.
- Admin-only GET /api/knowledge/audit returns up to 200 recent knowledge create/update/delete snapshots.
- Rate limits now use the direct peer IP rather than trusting an unvalidated X-Forwarded-For header. In-memory rate limiting remains per process; deploy a shared limiter for scale.
- OpenAI credentials, official WhatsApp API credentials, and an actual calendar provider are NOT included or connected.
- Do not treat seeded prices, service claims or preparation instructions as owner-verified without confirmation.
