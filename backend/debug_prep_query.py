"""Debug script for preparation query entity extraction"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))

from db import get_db
from api.nlu_optimized import (
    extract_entities, search_plants_fuzzy, _prioritized_tokens,
    normalize_query_token, classify_intent,
)

def debug_query(query, label=""):
    print(f"\n{'='*60}")
    print(f"QUERY: {query}  [{label}]")
    print(f"{'='*60}")
    
    intent = classify_intent(query)
    print(f"INTENT: {intent}")
    
    # Check if is_preparation_like_query triggers
    try:
        from services.chat import is_preparation_like_query
        prep_like = is_preparation_like_query(query, query)
        print(f"is_preparation_like_query: {prep_like}")
    except Exception as e:
        print(f"is_preparation_like_query: error - {e}")
    
    tokens = _prioritized_tokens(query)
    print(f"TOKENS: {tokens}")
    for t in tokens:
        norms = normalize_query_token(t)
        print(f"  {t!r} -> {norms}")
    
    print(f"\nsearch_plants_fuzzy results:")
    plants = search_plants_fuzzy(query, limit=5)
    for p in plants:
        dist = p.get("_vec_distance", "n/a")
        print(f"  id={p.get('id')} name_en={p.get('common_name_en')!r} name_mr={p.get('common_name_mr')!r} vec_dist={dist}")
    
    if not plants:
        print("  (none)")
    
    print(f"\nextract_entities results:")
    pl, dl = extract_entities(query, query)
    print(f"  plants: {[(p.get('id'), p.get('common_name_en')) for p in pl]}")
    print(f"  diseases: {[(d.get('id'), d.get('name_en')) for d in dl]}")

# Test queries - need app context for DB access
from init import create_app
app = create_app()
with app.app_context():
    debug_query("गुडमारचा काढा कसा बनवायचा?", "Gudmar decoction in Marathi")
    debug_query("हळदीचे दूध बनवण्याची पद्धत", "Turmeric milk in Marathi")
    debug_query("अश्वगंधाबद्दल सांगा", "Tell about Ashwagandha in Marathi")

    # Also check specific token searches
    print(f"\n{'='*60}")
    print("Direct search for 'गुडमार':")
    r = search_plants_fuzzy("गुडमार", limit=3)
    for p in r:
        print(f"  id={p.get('id')} name_en={p.get('common_name_en')!r} name_mr={p.get('common_name_mr')!r}")

    print("\nDirect search for 'हळद':")
    r = search_plants_fuzzy("हळद", limit=3)
    for p in r:
        print(f"  id={p.get('id')} name_en={p.get('common_name_en')!r} name_mr={p.get('common_name_mr')!r}")

    # Check what's in DB for Gudmar
    db = get_db()
    row = db.execute("SELECT id, common_name_en, common_name_mr, common_name_hi FROM plants WHERE common_name_en LIKE '%udmar%' OR common_name_en LIKE '%ymnema%'").fetchall()
    print(f"\nDB lookup for Gudmar/Gymnema:")
    for r in row:
        print(f"  id={r['id']} en={r['common_name_en']!r} mr={r['common_name_mr']!r} hi={r['common_name_hi']!r}")
