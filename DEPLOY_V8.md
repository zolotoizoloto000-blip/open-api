# AYTAN ECO AI Manager V8 — Render

Build Command:
`pip install -r requirements.txt`

Start Command:
`gunicorn app:app`

Required Render environment variables for the demo admin panel:
- `ADMIN_USERNAME=aytanadmin`
- `ADMIN_PASSWORD=<create a strong password>`
- `SESSION_SECRET=<long random secret>`

OpenAI (add after the web demo is confirmed working):
- `OPENAI_API_KEY=<your key>`
- `OPENAI_MODEL=gpt-4.1-mini` (or another model available to the account)

URLs:
- `/` — client AI demo
- `/admin` — owner login / CRM
- `/admin/dashboard`, `/admin/leads`, `/admin/conversations`, `/admin/knowledge`, `/admin/calendar` — admin aliases that open the CRM SPA
- `/api/health` — service status

For Render Free, SQLite data is not durable across redeploys/restarts. For a client production deployment use a persistent disk or PostgreSQL. The demo can use SQLite temporarily.
