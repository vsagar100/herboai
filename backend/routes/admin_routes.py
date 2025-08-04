# routes/admin_routes.py

from flask import request
from flask_restful import Resource
#from backend.models.plant_model import Plant
from database.db import get_db

class PlantCreate(Resource):
    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data.get("name"),
            image_url=data.get("image_url"),
            ayush_system=data.get("ayush_system"),
            uses='|'.join(data.get("uses", [])),
            remedies='|'.join(data.get("remedies", []))
        )
        db.session.add(new_plant)
        db.session.commit()
        return {"message": "Plant added successfully."}, 201

class PlantEdit(Resource):
    def put(self, plant_id):
        plant = Plant.query.get(plant_id)
        if not plant:
            return {"message": "Plant not found."}, 404
        data = request.get_json()
        plant.name = data.get("name", plant.name)
        plant.image_url = data.get("image_url", plant.image_url)
        plant.ayush_system = data.get("ayush_system", plant.ayush_system)
        plant.uses = '|'.join(data.get("uses", plant.uses.split('|')))
        plant.remedies = '|'.join(data.get("remedies", plant.remedies.split('|')))
        db.session.commit()
        return {"message": "Plant updated successfully."}, 200

class PlantDelete(Resource):
    def delete(self, plant_id):
        plant = Plant.query.get(plant_id)
        if not plant:
            return {"message": "Plant not found."}, 404
        db.session.delete(plant)
        db.session.commit()
        return {"message": "Plant deleted successfully."}, 200
