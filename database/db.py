# database/db.py
import os
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import g

DATABASE = 'herbal.db'
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database')
os.makedirs(db_path, exist_ok=True)
# Set the full path for the database file
db_file = os.path.join(db_path, DATABASE)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(db_file)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            
            # Create plants table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS plants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    ayush_system TEXT NOT NULL,
                    uses TEXT NOT NULL,
                    remedies TEXT NOT NULL,
                    precautions TEXT
                )
            ''')
            
            # Insert sample data
            sample_data = [
                (
                    "Ashwagandha",
                    "Ayurveda",
                    "Stress relief,Immunity booster,Energy enhancement,Sleep quality",
                    "Mix 1 tsp powder with warm milk,Take 300-500mg extract twice daily,Prepare tea with honey",
                    "Consult doctor if pregnant"
                ),
                (
                    "Tulsi",
                    "Ayurveda",
                    "Respiratory health,Immunity,Stress reduction,Antioxidant",
                    "Chew fresh leaves,Prepare tea,Use in steam inhalation",
                    "May lower blood sugar"
                )
            ]
            
            cursor.executemany('''
                INSERT INTO plants (name, ayush_system, uses, remedies, precautions)
                VALUES (?, ?, ?, ?, ?)
            ''', sample_data)
            
            db.commit()

    app.teardown_appcontext(close_db)