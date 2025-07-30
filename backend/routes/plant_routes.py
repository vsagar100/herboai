# routes/plant_routes.py

from flask import request
from flask_restful import Resource
from backend.models.plant_model import Plant
from database.db import db
from sqlalchemy import or_

class PlantList(Resource):
    def get(self):
        plants = Plant.query.all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "image_url": p.image_url,
                "ayush_system": p.ayush_system,
                "uses": p.uses.split('|'),
                "remedies": p.remedies.split('|')
            } for p in plants
        ], 200

class PlantSearch(Resource):
    def get(self):
        q = request.args.get('q', '')
        if not q:
            return {"message": "Query param 'q' required."}, 400
        plants = Plant.query.filter(
            or_(
                Plant.name.ilike(f"%{q}%"),
                Plant.uses.ilike(f"%{q}%"),
                Plant.remedies.ilike(f"%{q}%")
            )
        ).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "image_url": p.image_url,
                "ayush_system": p.ayush_system,
                "uses": p.uses.split('|'),
                "remedies": p.remedies.split('|')
            } for p in plants
        ], 200
