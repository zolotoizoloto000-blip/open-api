# V10 CHAT FIX
- Quick-question chips now send immediately instead of only filling the input.
- Chat form never reloads the page on submit.
- User message is rendered immediately.
- Visible "AI печатает…" state while waiting.
- 35-second timeout and readable server/JSON errors.
- Existing V9 Admin Pro CRM retained.

Render commands:
Build: pip install -r requirements.txt
Start: gunicorn app:app

Environment: OPENAI_API_KEY, ADMIN_USERNAME, ADMIN_PASSWORD, SESSION_SECRET.
