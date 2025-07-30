# database/db.py
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database')
    os.makedirs(db_path, exist_ok=True)
    
    # Set the full path for the database file
    db_file = os.path.join(db_path, 'herboai.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
