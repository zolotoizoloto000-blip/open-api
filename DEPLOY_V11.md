# AYTAN ECO AI Manager V11 CLEAN

Render:
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`

Environment:
- `OPENAI_API_KEY` = secret API key
- `ADMIN_USERNAME` = admin login
- `ADMIN_PASSWORD` = strong password
- `SESSION_SECRET` = long random secret
- optional `OPENAI_MODEL` (default in app: gpt-4.1-mini)

URLs:
- `/` client demo chat
- `/admin` separate CRM/admin panel
- `/api/health` connection status

V11 removes the legacy owner CRM/token UI from the public page and uses one chat form handler only. The chat form is intercepted with `preventDefault()` through `addEventListener`, so sending a message must not reload the page.
