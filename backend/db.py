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
    """Resolve a disease name (in ANY language) to its disease ID.

    Search order (first match wins):
      1. Exact match on diseases.name_en / name_hi / name_mr
      2. Exact match on disease_synonyms.synonym
      3. Exact match on entity_i18n (disease name field, any lang)
      4. LIKE (contains) on diseases name columns
      5. LIKE on disease_synonyms
      6. LIKE on entity_i18n name field
    """
    q = (disease_text_en or "").strip().lower()
    if not q:
        return None

    # ── 1. Exact match on base table (all language columns) ──
    row = conn.execute(
        """SELECT id FROM diseases
           WHERE LOWER(name_en)=? OR LOWER(name_hi)=? OR LOWER(name_mr)=?
           LIMIT 1""",
        (q, q, q),
    ).fetchone()
    if row:
        return int(row["id"])

    # ── 2. Exact match on disease_synonyms ──
    row = conn.execute(
        "SELECT disease_id FROM disease_synonyms WHERE LOWER(synonym)=? LIMIT 1",
        (q,),
    ).fetchone()
    if row:
        return int(row["disease_id"])

    # ── 3. Exact match on entity_i18n (disease name, any language) ──
    row = conn.execute(
        """SELECT entity_id FROM entity_i18n
           WHERE entity_type='disease' AND field='name' AND LOWER(text)=?
           LIMIT 1""",
        (q,),
    ).fetchone()
    if row:
        return int(row["entity_id"])

    # ── 4. LIKE on base table ──
    like = f"%{q}%"
    row = conn.execute(
        """SELECT id FROM diseases
           WHERE LOWER(name_en) LIKE ? OR LOWER(name_hi) LIKE ? OR LOWER(name_mr) LIKE ?
           ORDER BY id LIMIT 1""",
        (like, like, like),
    ).fetchone()
    if row:
        return int(row["id"])

    # ── 5. LIKE on disease_synonyms ──
    row = conn.execute(
        "SELECT disease_id FROM disease_synonyms WHERE LOWER(synonym) LIKE ? ORDER BY disease_id LIMIT 1",
        (like,),
    ).fetchone()
    if row:
        return int(row["disease_id"])

    # ── 6. LIKE on entity_i18n ──
    row = conn.execute(
        """SELECT entity_id FROM entity_i18n
           WHERE entity_type='disease' AND field='name' AND LOWER(text) LIKE ?
           ORDER BY entity_id LIMIT 1""",
        (like,),
    ).fetchone()
    if row:
        return int(row["entity_id"])

    return None


def fetch_preparations_for_disease(conn: sqlite3.Connection, disease_id: int, limit: int = 10) -> List[Dict]:
    """Fetch a focused, curated list of preparations for a disease.

    Strategy (DB-first, language-agnostic):
      1) Start from plants mapped to this disease (plant_disease_mapping).
      2) Prefer preparations explicitly indicated for the disease
         (preparation_indications.strength), otherwise fall back to the
         plant_disease_mapping.efficacy_level.
      3) Fetch a generous candidate set, then in Python:
            - group by primary plant (pr.plant_id),
            - rank plants by max efficacy/evidence,
            - within each plant keep a small number of top preparations,
            - finally cap overall list to ``limit`` items.

    This ensures that high‑priority plants (e.g. flagship diabetes herbs
    like Gudmar / Jamun / Vijayasar) always contribute at least one
    preparation, instead of being crowded out by many similar lower-tier
    entries.

    NOTE: Uses preparations.plant_id for the primary plant link; the
    preparation_ingredients table may be empty for some rows.
    """

    # Fetch more than we finally return so that we can re-rank/group
    # deterministically in Python without losing potentially important
    # candidates.
    candidate_limit = max(limit * 3, limit + 4)

    sql = """
    SELECT DISTINCT
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
      COALESCE(pi.strength, pdm.efficacy_level, 3) AS efficacy_level,
      CASE WHEN pi.preparation_id IS NOT NULL THEN 1 ELSE 0 END AS explicitly_indicated,
      pdm.evidence_type
    FROM preparations pr
    INNER JOIN plants p ON p.id = pr.plant_id
    INNER JOIN plant_disease_mapping pdm ON pdm.plant_id = p.id AND pdm.disease_id = ?
    LEFT JOIN preparation_indications pi 
      ON pi.preparation_id = pr.id AND pi.disease_id = ?
    ORDER BY explicitly_indicated DESC,
             COALESCE(pi.strength, pdm.efficacy_level, 0) DESC,
             pr.id DESC
    LIMIT ?
    """

    rows = conn.execute(sql, (disease_id, disease_id, candidate_limit)).fetchall()
    candidates: List[Dict] = [dict(r) for r in rows]
    if not candidates:
        return []

    # Group preparations by their primary plant so we can ensure each
    # high‑efficacy plant contributes at least one preparation.
    by_plant: Dict[int, List[Dict]] = {}
    for prep in candidates:
        plant_id = prep.get("plant_id")
        if plant_id is None:
            # Keep orphaned preparations in a special bucket (plant_id = 0)
            plant_id = 0
            prep["plant_id"] = plant_id
        by_plant.setdefault(int(plant_id), []).append(prep)

    def _plant_sort_key(item: tuple[int, List[Dict]]) -> tuple:
        plant_id, preps = item
        # Highest efficacy across this plant's preparations
        max_eff = 0
        best_explicit = 0
        best_evidence = ""
        for p in preps:
            eff = p.get("efficacy_level") or 0
            if isinstance(eff, str):
                try:
                    eff = int(eff)
                except ValueError:
                    eff = 0
            eff = int(eff)
            exp = 1 if p.get("explicitly_indicated") else 0
            ev = (p.get("evidence_type") or "").lower()
            if eff > max_eff or (eff == max_eff and exp > best_explicit):
                max_eff = eff
                best_explicit = exp
                best_evidence = ev
        # Higher efficacy first, then explicit indications, then evidence type, then plant_id
        return (-max_eff, -best_explicit, best_evidence, plant_id)

    def _prep_sort_key(prep: Dict) -> tuple:
        eff = prep.get("efficacy_level") or 0
        if isinstance(eff, str):
            try:
                eff = int(eff)
            except ValueError:
                eff = 0
        eff = int(eff)
        exp = 1 if prep.get("explicitly_indicated") else 0
        # Prefer explicitly indicated, then higher efficacy, then newer IDs
        return (-exp, -eff, -int(prep.get("id") or 0))

    # Sort plants by their best preparation's properties
    plant_items = sorted(by_plant.items(), key=_plant_sort_key)

    # Within each plant, keep at most this many preparations to avoid
    # overwhelming the user with similar options for a single herb.
    max_per_plant = 2

    selected: List[Dict] = []
    for plant_id, preps in plant_items:
        preps_sorted = sorted(preps, key=_prep_sort_key)
        for prep in preps_sorted[:max_per_plant]:
            selected.append(prep)
            if len(selected) >= limit:
                return selected

    return selected


def rank_preparations_by_severity(
    preparations: List[Dict],
    severity_band: str = "normal",
    limit: int = 8,
) -> List[Dict]:
    """
    Apply severity-based intelligence to select and order preparations.

    Strategy:
      - high/emergency  → mostly high-efficacy (≥4), some mid (3), minimal low
      - moderate         → balanced mix of high (≥4) and mid (3)
      - low/normal       → show variety: high, mid, and a few low-efficacy

    Each result is annotated with ``_relevance_tier`` ('high', 'mid', 'low')
    so the response builder can render efficacy indicators.
    """
    if not preparations:
        return []

    def _eff(p: Dict) -> int:
        v = p.get("efficacy_level", 0)
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                v = 0
        return int(v)

    # Classify into tiers
    high = [p for p in preparations if _eff(p) >= 4]
    mid  = [p for p in preparations if _eff(p) == 3]
    low  = [p for p in preparations if _eff(p) < 3]

    # Sort each tier: explicitly indicated first, then efficacy desc
    def _sort_key(p: Dict):
        return (-(1 if p.get("explicitly_indicated") else 0), -_eff(p), -(p.get("id") or 0))

    high.sort(key=_sort_key)
    mid.sort(key=_sort_key)
    low.sort(key=_sort_key)

    # Decide allocations based on severity
    band = (severity_band or "normal").lower()
    if band in ("high", "emergency"):
        # Aggressive: mostly high efficacy
        n_high = min(len(high), max(limit - 1, 4))
        n_mid  = min(len(mid), max(limit - n_high - 0, 1))
        n_low  = min(len(low), max(limit - n_high - n_mid, 0))
    elif band == "moderate":
        # Balanced: good mix
        n_high = min(len(high), max(limit // 2, 3))
        n_mid  = min(len(mid), max(limit - n_high - 1, 2))
        n_low  = min(len(low), max(limit - n_high - n_mid, 0))
    else:
        # Normal/low: show variety
        n_high = min(len(high), max(limit // 3, 2))
        n_mid  = min(len(mid),  max(limit // 3, 2))
        n_low  = min(len(low),  max(limit - n_high - n_mid, 1))

    # Fill remaining slots from any tier
    selected = []
    for p in high[:n_high]:
        p["_relevance_tier"] = "high"
        selected.append(p)
    for p in mid[:n_mid]:
        p["_relevance_tier"] = "mid"
        selected.append(p)
    for p in low[:n_low]:
        p["_relevance_tier"] = "low"
        selected.append(p)

    # If we haven't reached limit, backfill from any remaining
    remaining = limit - len(selected)
    if remaining > 0:
        used_ids = {p.get("id") for p in selected}
        for pool, tier_label in [(high, "high"), (mid, "mid"), (low, "low")]:
            for p in pool:
                if p.get("id") not in used_ids:
                    p["_relevance_tier"] = tier_label
                    selected.append(p)
                    used_ids.add(p.get("id"))
                    if len(selected) >= limit:
                        break
            if len(selected) >= limit:
                break

    return selected[:limit]


def _init_conn(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Reduce SQLITE_BUSY errors under concurrent writes
    conn.execute("PRAGMA busy_timeout = 5000")
    for sql, params in PRAGMAS:
        conn.execute(sql, params)
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


def get_db():
    """Connection helper cached per request via flask.g."""
    db_path = current_app.config["DB_PATH"]
    if "db_main" not in g:
        g.db_main = _init_conn(db_path)
    return g.db_main


def get_db_standalone():
    """Create new connection for background threads/tasks (not request-cached)."""
    db_path = current_app.config["DB_PATH"]
    return _init_conn(db_path)


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
    for key in ("db_main", "db"):
        db = g.pop(key, None)
        if db is not None:
            db.close()


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
