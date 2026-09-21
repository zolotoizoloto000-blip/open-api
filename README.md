# AYTAN ECO AI Manager — CLEAN FINAL

Clean deployment package for the AYTAN ECO web demo and CRM.

## Public demo
- `/` — AI manager chat
- `/api/chat` — chat API
- `/api/openai/check` — real OpenAI connectivity diagnostic

## Admin / CRM
- `/admin` — admin login / dashboard
- CRM, conversations, knowledge base and calendar are managed from the admin interface.

## Render
Build command:
`pip install -r requirements.txt`

Start command:
`gunicorn app:app`

Required environment variables:
- `OPENAI_API_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `SESSION_SECRET`

Do not commit real secrets to GitHub.
