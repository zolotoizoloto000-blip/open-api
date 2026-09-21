# Render deployment

1. Upload only the contents of this folder to the repository root.
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:app`
4. Set `OPENAI_API_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `SESSION_SECRET` in Render Environment.
5. Deploy and open `/` for the demo and `/admin` for CRM.
6. Open `/api/openai/check` to diagnose the OpenAI connection.
