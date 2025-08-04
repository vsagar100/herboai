from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.db import init_db
from routes.plant_routes import PlantList, PlantSearch

app = Flask(__name__)
CORS(app)
api = Api(app)

# Database setup
init_db(app)

# Routes
api.add_resource(PlantList, "/api/plants")
api.add_resource(PlantSearch, "/api/plants/search")

if __name__ == "__main__":
    app.run(debug=True)