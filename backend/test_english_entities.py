"""Debug English entity extraction for 'Neem for acne'"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app
app = create_app()

with app.app_context():
    from api.nlu_optimized import search_plants_fuzzy, search_diseases_fuzzy, _prioritized_tokens, normalize_query_token
    from db import get_db

    # Check tokens
    tokens = _prioritized_tokens("Neem for acne")
    print(f"Tokens: {tokens}")
    
    # Check what "neem" matches in disease_synonyms
    db = get_db()
    cur = db.cursor()
    for tok in tokens:
        variants = normalize_query_token(tok)
        for v in variants[:3]:
            rows = cur.execute("""
                SELECT ds.synonym, d.id, d.name_en
                FROM disease_synonyms ds 
                JOIN diseases d ON d.id = ds.disease_id
                WHERE LOWER(ds.synonym) LIKE ? OR LOWER(ds.synonym) LIKE ?
                LIMIT 5
            """, (f"{v}%", f"%{v}%")).fetchall()
            if rows:
                print(f"  Token '{v}' in disease_synonyms: {[(r[0],r[1],r[2]) for r in rows]}")
            
            rows2 = cur.execute("""
                SELECT * FROM diseases
                WHERE LOWER(name_en) LIKE ? OR LOWER(name_hi) LIKE ? OR LOWER(name_mr) LIKE ?
                LIMIT 3
            """, (f"%{v}%", f"%{v}%", f"%{v}%")).fetchall()
            if rows2:
                print(f"  Token '{v}' in diseases base: {[(dict(r)['id'], dict(r)['name_en']) for r in rows2]}")
    
    print("\n=== Full disease search for 'Neem for acne' ===")
    diseases = search_diseases_fuzzy("Neem for acne", limit=5)
    for d in diseases:
        dd = dict(d) if not isinstance(d, dict) else d
        vec_dist = dd.get("_vec_distance", "N/A")
        print(f"  id={dd.get('id')}, name={dd.get('name_en')}, vec_dist={vec_dist}")
