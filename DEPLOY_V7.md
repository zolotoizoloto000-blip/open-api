# V7 deployment and honest feature status

The public AYTAN ECO site is unchanged. This is a separate Flask service.

## Implemented in source
- Web chat, OpenAI integration when API key is configured, editable knowledge and audit history, CRM and CSV export.
- Owner-controlled appointment creation and cancellation with overlap rejection. Times must be timezone-aware; UI assumes Kazakhstan UTC+05:00. Appointments are NOT automatically offered as available to customers.
- Official Meta WhatsApp Cloud API webhook verification and SHA-256 request signature verification; text messages are stored and replies sent using the configured API. Requires Meta-approved business setup, a valid access token, phone number ID, verify token, app secret, HTTPS URL and applicable WhatsApp messaging rules. No credentials included. This is NOT an unofficial WhatsApp connection.
- Durable notification outbox and admin manual retry (up to five attempts), HTTPS signed owner webhook. It does NOT magically send owner messages without an external receiving endpoint.
- SQLite online backup utility backup.py. Schedule externally with cron and BACKUP_DIR on persistent storage; offsite backups and restore drills are operator responsibilities.

## Setup
1. Install requirements.txt, configure .env.example secrets as host environment variables; do not commit .env.
2. Set DB_PATH to persistent disk. SQLite supports a single service instance; for horizontally scaled production migrate to PostgreSQL and use shared rate limiting.
3. For WhatsApp, configure Meta webhook callback `https://YOUR-HOST/webhooks/whatsapp`, set the verify token, subscribe to `messages`, and supply the remaining WHATSAPP_* environment variables. Send only permitted messages and respect the 24-hour customer service window/template rules.
4. For notifications, configure OWNER_WEBHOOK_URL and OWNER_WEBHOOK_SECRET and use CRM retry button or a trusted scheduled job to retry pending items. Notifications are queued, not automatically retried.
5. For backup schedule `DB_PATH=/persistent/aytan.sqlite3 BACKUP_DIR=/persistent/backups python backup.py` daily and copy encrypted backups offsite. Test restores before live launch.
6. Login `/crm` with configured ADMIN_USERNAME and ADMIN_PASSWORD. Set SESSION_SECRET and COOKIE_SECURE=1 for HTTPS.
7. Configure OPENAI_API_KEY on server, never in HTML or GitHub. Confirm API billing and test answers before using with customers.

## Limitations / remaining acceptance tests
- Flask is not installed in the build environment, so full integration tests and browser tests have NOT passed here; Python syntax checks only.
- WhatsApp live delivery, webhook retries, Meta approval and OpenAI accuracy cannot be certified without real account credentials and a running deployment.
- No staff role permissions, distributed rate limiting, PostgreSQL migration, automatic notification worker, or third-party calendar sync.
- Seeded prices, services, documents and safety statements MUST be verified with the business owner before launch. AI cannot guarantee perfect answers.
