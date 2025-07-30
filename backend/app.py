# app.py

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from database.db import init_db
from backend.routes.plant_routes import PlantList, PlantSearch
from backend.routes.admin_routes import PlantCreate, PlantEdit, PlantDelete

app = Flask(__name__)
CORS(app)
api = Api(app)

# Database setup
init_db(app)

# Routes
api.add_resource(PlantList, "/api/plants")
api.add_resource(PlantSearch, "/api/plants/search")
api.add_resource(PlantCreate, "/api/admin/plant")
api.add_resource(PlantEdit, "/api/admin/plant/<int:plant_id>")
api.add_resource(PlantDelete, "/api/admin/plant/<int:plant_id>")

if __name__ == "__main__":
    app.run(debug=True)
