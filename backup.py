"""Run with cron on a persistent disk; retain last 14 backups."""
import os,sqlite3,datetime
from pathlib import Path
source=Path(os.environ['DB_PATH']);dest=Path(os.environ['BACKUP_DIR']);dest.mkdir(parents=True,exist_ok=True)
if not source.is_file():raise SystemExit('Database missing; refusing empty backup')
name=dest/('aytan-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.sqlite3')
with sqlite3.connect(source) as a,sqlite3.connect(name) as b:a.backup(b)
with sqlite3.connect(name) as c:
 if c.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise RuntimeError('Backup integrity check failed')
for old in sorted(dest.glob('aytan-*.sqlite3'),reverse=True)[14:]:old.unlink()
print('Backup verified:',name)
