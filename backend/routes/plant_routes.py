# routes/plant_routes.py

from flask import request
from flask_restful import Resource,reqparse
#from backend.models.plant_model import Plant
from database.db import get_db
from sqlalchemy import or_
from services.ai_service import AIService

class PlantList(Resource):
    def get(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM plants')
        plants = cursor.fetchall()
        
        if not plants:
            return {"message": "No plants found"}, 404
            
        return [{
            "id": plant[0],
            "name": plant[1],
            "ayush_system": plant[2],
            "uses": plant[3].split(','),
            "remedies": plant[4].split(','),
            "precautions": plant[5]
        } for plant in plants], 200



ai_service = AIService()

class PlantSearch(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, required=True, help='Search query is required')
        args = parser.parse_args()
        
        db = get_db()
        cursor = db.cursor()
        search_query = f"%{args['q']}%"
        
        cursor.execute('''
            SELECT * FROM plants 
            WHERE name LIKE ? 
            OR ayush_system LIKE ? 
            OR uses LIKE ?
        ''', (search_query, search_query, search_query))
        
        plants = cursor.fetchall()
        
        if not plants:
            ai_prompt = f"As an Ayurvedic expert, what general advice would you give for someone asking about: '{args['q']}'?"
            ai_response = ai_service.generate_response(ai_prompt)
            return {
                "message": f"No exact matches found for '{args['q']}'",
                "ai_suggestion": ai_response
            }, 404

        plant_list = [{
            "id": plant[0],
            "name": plant[1],
            "ayush_system": plant[2],
            "uses": plant[3].split(','),
            "remedies": plant[4].split(','),
            "precautions": plant[5]
        } for plant in plants]

        # Get detailed AI insights for each plant
        detailed_insights = []
        for plant in plant_list:
            plant_info = ai_service.generate_plant_info(plant['name'])
            if plant_info:
                detailed_insights.append(plant_info)

        return {
            "plants": plant_list,
            "detailed_insights": detailed_insights
        }, 200