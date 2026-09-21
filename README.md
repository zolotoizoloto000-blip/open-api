# AYTAN ECO AI SALES MANAGER

Демонстрационный AI-менеджер продаж AYTAN ECO: профессиональная консультация, мягкая квалификация клиента, автоматический захват лида, CRM, оценка готовности клиента, следующий шаг, аналитика и редактируемая база знаний.

## Render
Build: `pip install -r requirements.txt`
Start: `gunicorn app:app`

Обязательные переменные: `OPENAI_API_KEY`, `ADMIN_PASSWORD`, `SESSION_SECRET`. Рекомендуется задать `ADMIN_USERNAME=aytanadmin`.

Публичный чат: `/`  
CRM: `/admin`
