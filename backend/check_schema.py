from flask import Flask
from db import init_app, get_db

app = Flask(__name__)
app.config["DB_PATH"] = "../db/new_herboai.db"
init_app(app)

with app.app_context():
    db = get_db()
    info = db.execute('PRAGMA table_info(disease_synonyms)').fetchall()
    print('disease_synonyms columns:')
    for r in info:
        print(f"  {r['name']} ({r['type']})")
