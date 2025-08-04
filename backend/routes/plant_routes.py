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
        
        # First, get plants from database
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
            # Use AI to provide a helpful response even when no plants are found
            ai_prompt = f"""As a herbal medicine expert, provide a helpful response for the query: '{args['q']}'.
            If you don't have specific plant recommendations, suggest general wellness advice or recommend consulting an Ayurvedic practitioner."""
            
            ai_response = ai_service.generate_response(ai_prompt)
            return {
                "message": f"No exact matches found for '{args['q']}'",
                "ai_suggestion": ai_response
            }, 404
            
        # Enhance plant information with AI insights
        plant_list = [{
            "id": plant[0],
            "name": plant[1],
            "ayush_system": plant[2],
            "uses": plant[3].split(','),
            "remedies": plant[4].split(','),
            "precautions": plant[5]
        } for plant in plants]
        
        # Generate AI-enhanced insights
        ai_prompt = f"""As an Ayurvedic expert, provide additional insights about these plants: {[p['name'] for p in plant_list]}.
        Focus on traditional usage, combinations, and modern research if available. Keep it concise."""
        
        ai_insights = ai_service.generate_response(ai_prompt)
        
        return {
            "plants": plant_list,
            "ai_insights": ai_insights
        }, 200