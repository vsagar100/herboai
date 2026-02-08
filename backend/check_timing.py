import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))
from init import create_app
app = create_app()
with app.app_context():
    from db import get_db
    db = get_db()
    rows = db.execute("SELECT DISTINCT timing FROM preparations WHERE timing IS NOT NULL AND timing != ''").fetchall()
    print("=== DISTINCT TIMING VALUES ===")
    for r in rows:
        print(f"  [{r[0]}]")
    print(f"Total: {len(rows)}")
    rows2 = db.execute("SELECT DISTINCT anupana FROM preparations WHERE anupana IS NOT NULL AND anupana != ''").fetchall()
    print("\n=== DISTINCT ANUPANA VALUES ===")
    for r in rows2:
        print(f"  [{r[0]}]")
    print(f"Total: {len(rows2)}")
