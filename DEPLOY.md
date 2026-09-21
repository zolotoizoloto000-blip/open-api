# Deploy
1. Загрузить содержимое архива в корень GitHub-репозитория.
2. Render Web Service: Build `pip install -r requirements.txt`; Start `gunicorn app:app`.
3. Environment: `OPENAI_API_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `SESSION_SECRET`.
4. Deploy, затем проверить `/api/openai/check`, публичный чат `/` и CRM `/admin`.
5. Не хранить API-ключи в GitHub.
