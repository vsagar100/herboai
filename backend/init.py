import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from db import init_app as init_db
from api.routes import bp as api_bp
from api.files import files_bp
from api.admin_auth import admin_auth_bp
from api.admin_plants import admin_plants_bp

def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    jwt = JWTManager(app)
    app.config["JWT_SECRET_KEY"] = "supersecret-change-this"
    app.config["FILE_ROOT"] = app.config.get("MEDIA_ROOT")

    CORS(app,
         resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173", "*"]}},
         supports_credentials=True,  # no cookies needed for /api/query
         allow_headers=["Content-Type", "Authorization", "x-session-id"],
         expose_headers=["Content-Type", "Authorization"],
         methods=["GET","POST","PUT","DELETE","OPTIONS"])

    # DB init (connection factory + teardown)
    init_db(app)

    # Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(files_bp, url_prefix="/files/static/plant_images") 
    app.register_blueprint(admin_auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_plants_bp, url_prefix="/api/admin")

    @app.get("/api/health")
    def health():
        return {"status": "ok", "service": "herboai-backend"}, 200

    return app
