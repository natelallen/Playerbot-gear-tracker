import sqlite3
from pathlib import Path
import shutil

DB_PATH = Path("data/database.db")
DEFAULT_DB = Path("/app/defaults/database.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists():
        shutil.copy(DEFAULT_DB, DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.close()
