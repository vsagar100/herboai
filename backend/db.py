import sqlite3
import sqlite_vec
from sqlite_vec import load as load_sqlite_vec
from flask import current_app, g, Flask
from typing import Optional, List, Dict

PRAGMAS = [
    ("PRAGMA foreign_keys = ON", ()),
    ("PRAGMA journal_mode = WAL", ()),
    ("PRAGMA synchronous = NORMAL", ()),
]

# -----------------------------------------------------------------------------
# sqlite-vec: per-language vector tables (strict retrieval in user language)
# -----------------------------------------------------------------------------

_LANGS = ("en", "hi", "mr")

def _vec_table_sql() -> tuple[str, ...]:
    # Keep 384-dim to match existing embedding function used in your codebase
    stmts: list[str] = []
    for lang in _LANGS:
        stmts.append(f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS disease_vec_{lang} USING vec0(
            disease_id INTEGER PRIMARY KEY,
            name TEXT,
            embedding FLOAT[384]
        )
        """)
        stmts.append(f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS plant_vec_{lang} USING vec0(
            plant_id INTEGER PRIMARY KEY,
            name TEXT,
            embedding FLOAT[384]
        )
        """)
        stmts.append(f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS prep_vec_{lang} USING vec0(
            preparation_id INTEGER PRIMARY KEY,
            name TEXT,
            embedding FLOAT[384]
        )
        """)
    return tuple(stmts)

_VEC_TABLE_SQL = _vec_table_sql()

_VEC_BASE_TABLES = tuple(
    f"{base}_vec_{lang}"
    for lang in _LANGS
    for base in ("disease", "plant", "prep")
)


_vec_tables_ready = False
_vec_cleanup_done = False


def _ensure_vec_tables(conn: sqlite3.Connection) -> None:
    """
    Lazily create the vec0-backed virtual tables so vector search
    never fails with "no such table" when the app boots with a
    fresh database.
    """
    global _vec_tables_ready
    if _vec_tables_ready:
        return

    cur = conn.cursor()
    for statement in _VEC_TABLE_SQL:
        cur.execute(statement)
    cur.close()
    conn.commit()
    _vec_tables_ready = True


def _cleanup_legacy_vec_tables(conn: sqlite3.Connection) -> None:
    """
    Remove sqlite-vec shadow tables that may have been imported
    from SQL dumps without the actual virtual table definitions.
    These stale tables prevent sqlite-vec from loading.
    """
    global _vec_cleanup_done
    if _vec_cleanup_done:
        return

    cur = conn.cursor()
    changed = False

    for base in _VEC_BASE_TABLES:
        sql_row = cur.execute(
            "SELECT sql FROM sqlite_master WHERE name = ?", (base,)
        ).fetchone()
        if sql_row and sql_row[0]:
            sql_def = sql_row[0].upper()
            if "USING VEC0" in sql_def:
                # Looks like a valid vec0 virtual table definition.
                continue

        suffixes = (
            "",
            "_info",
            "_chunks",
            "_rowids",
            "_vector_chunks00",
            "_metadatachunks00",
            "_metadatatext00",
        )
        for suffix in suffixes:
            table_name = f"{base}{suffix}"
            try:
                cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            except sqlite3.OperationalError as drop_err:
                if "no such module: vec0" in str(drop_err).lower():
                    # Dropping an existing vec0 virtual table requires the module,
                    # so skip in that case.
                    continue
                raise
        changed = True

    if changed:
        conn.commit()
    _vec_cleanup_done = True


def resolve_disease_id(conn: sqlite3.Connection, disease_text_en: str) -> Optional[int]:
    q = (disease_text_en or "").strip().lower()
    if not q:
        return None

    row = conn.execute(
        "SELECT id FROM diseases WHERE LOWER(name_en)=? LIMIT 1",
        (q,),
    ).fetchone()
    if row:
        return int(row["id"])

    row = conn.execute(
        "SELECT disease_id FROM disease_synonyms WHERE LOWER(synonym)=? LIMIT 1",
        (q,),
    ).fetchone()
    if row:
        return int(row["disease_id"])

    like = f"%{q}%"
    row = conn.execute(
        "SELECT id FROM diseases WHERE LOWER(name_en) LIKE ? ORDER BY id LIMIT 1",
        (like,),
    ).fetchone()
    if row:
        return int(row["id"])

    row = conn.execute(
        "SELECT disease_id FROM disease_synonyms WHERE LOWER(synonym) LIKE ? ORDER BY disease_id LIMIT 1",
        (like,),
    ).fetchone()
    if row:
        return int(row["disease_id"])

    return None


def fetch_preparations_for_disease(conn: sqlite3.Connection, disease_id: int, limit: int = 6) -> List[Dict]:
    sql = """
    WITH pd AS (
      SELECT plant_id, efficacy_level, evidence_type
      FROM plant_disease_mapping
      WHERE disease_id = ?
    )
    SELECT
      pr.id,
      pr.name_en, pr.name_hi, pr.name_mr,
      pr.classical_name,
      pr.ayush_system,
      pr.form_type, pr.category,
      pr.preparation_steps, pr.equipment_needed,
      pr.duration, pr.yield, pr.storage, pr.shelf_life,
      pr.dosage_json, pr.timing, pr.anupana, pr.notes,
      p.id AS plant_id,
      p.botanical_name, p.common_name_en, p.common_name_hi, p.common_name_mr,
      pd.efficacy_level, pd.evidence_type,
      CASE WHEN pi.preparation_id IS NULL THEN 0 ELSE 1 END AS explicitly_indicated
    FROM pd
    JOIN plants p ON p.id = pd.plant_id
    JOIN preparations pr ON pr.plant_id = pd.plant_id
    LEFT JOIN preparation_indications pi
      ON pi.preparation_id = pr.id AND pi.disease_id = ?
    ORDER BY explicitly_indicated DESC,
             COALESCE(pd.efficacy_level, 0) DESC,
             pr.id DESC
    LIMIT ?
    """
    rows = conn.execute(sql, (disease_id, disease_id, limit)).fetchall()
    return [dict(r) for r in rows]


def get_db():
    """Simple connection helper used across the app."""
    db_path = current_app.config["DB_PATH"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.enable_load_extension(True)
    try:
        _load_sqlite_vec(conn)
    except Exception as e:
        if _vec_cleanup_done:
            conn.enable_load_extension(False)
            raise
        # Attempt cleanup once for legacy dumps, then retry.
        _cleanup_legacy_vec_tables(conn)
        _load_sqlite_vec(conn)
    finally:
        conn.enable_load_extension(False)
    return conn


def _load_sqlite_vec(conn: sqlite3.Connection) -> None:
    try:
        load_sqlite_vec(conn)  # registers vec0
        print("[DB] sqlite-vec (vec0) loaded")
        _ensure_vec_tables(conn)
    except Exception as exc:
        print(f"[DB] sqlite-vec not loaded: {exc}")
        raise


def get_db1() -> sqlite3.Connection:
    """
    Alternative connection helper with PRAGMAs applied.
    Kept for compatibility; most code should use get_db().
    """
    if "db" not in g:
        db_path = current_app.config["DB_PATH"]
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row

        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)

        if not db_path:
            print("[DB] DB_PATH is not configured!")
        else:
            print(f"[DB] Connecting to DB at {db_path}")

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
