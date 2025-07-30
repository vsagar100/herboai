# models/plant_model.py

from database.db import db

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))
    ayush_system = db.Column(db.String(50))
    uses = db.Column(db.Text)
    remedies = db.Column(db.Text)