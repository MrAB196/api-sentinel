import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB = Path(__file__).resolve().parent / "data" / "api_sentinel.db"
def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    return c
def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, url TEXT, method TEXT,
        total INTEGER, success_rate REAL, p50_ms REAL, p95_ms REAL, p99_ms REAL, failures INTEGER)""")
def save_run(url, method, s):
    with connect() as c:
        c.execute("INSERT INTO runs (created_at,url,method,total,success_rate,p50_ms,p95_ms,p99_ms,failures) VALUES (?,?,?,?,?,?,?,?,?)",
        (datetime.now(timezone.utc).isoformat(),url,method,s["total"],s["success_rate"],s["p50_ms"],s["p95_ms"],s["p99_ms"],s["failures"]))
def list_runs():
    with connect() as c:
        return [dict(r) for r in c.execute("SELECT * FROM runs ORDER BY id DESC LIMIT 100").fetchall()]
