# app.py
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import text
from config import Settings
from database import Base, engine
from blueprints.health import bp as health_bp
from blueprints.files import bp as files_bp
from blueprints.auth import bp as auth_bp
from blueprints.plants import bp as plants_bp
from blueprints.remedies import bp as remedies_bp
from blueprints.chat import bp as chat_bp
from blueprints.admin import bp as admin_bp
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # DB init
    Base.metadata.create_all(bind=engine)

    try:
        from services import semantic
        semantic.load_indexes()  # safe: silently does nothing if files missing
    except Exception as e:
        print("Semantic indexes not loaded:", e)


    # CORS for your React client
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"], "supports_credentials": True},
                         r"/files/*": {"origins": app.config["CORS_ORIGINS"]}})

    JWTManager(app)

    # blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(plants_bp)
    app.register_blueprint(remedies_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)

    @app.get("/")
    def root():
        return {"message": "HerboAI backend is running."}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
