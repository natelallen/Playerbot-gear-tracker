import sqlite3
from pathlib import Path

DB_PATH = Path("data/database.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DB_PATH)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.close()
