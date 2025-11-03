import sqlite3
import sqlite_vec
from sqlite_vec import load as load_sqlite_vec
from flask import current_app, g, Flask

PRAGMAS = [
    ("PRAGMA foreign_keys = ON", ()),
    ("PRAGMA journal_mode = WAL", ()),
    ("PRAGMA synchronous = NORMAL", ()),
]

def get_db():
    db_path = current_app.config["DB_PATH"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.enable_load_extension(True)
    try:
        load_sqlite_vec(conn)  # ← registers vec0
        print("✅ sqlite-vec (vec0) loaded")
    except Exception as e:
        print("⚠️ sqlite-vec not loaded:", e)
    conn.enable_load_extension(False)
    return conn

def get_db1() -> sqlite3.Connection:
    if "db" not in g:
        db_path = current_app.config["DB_PATH"]
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)   # loads the extension
        conn.enable_load_extension(False)
        if not db_path:
            print("DB_PATH is not configured!")
        else:
            print("DB path found.")

        print(f"Connecting to DB at {db_path}")
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        # Apply pragmas
        cur = conn.cursor()
        for sql, params in PRAGMAS:
            cur.execute(sql)
        cur.close()
        g.db = conn
    return g.db

def close_db(_=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app: Flask):
    app.teardown_appcontext(close_db)
