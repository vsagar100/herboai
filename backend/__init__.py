from flask import Flask
from flask_cors import CORS
from .config import Config
from .db import init_app as init_db
from .api.routes import bp as api_bp

def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    init_db(app)

    # Allow the Vite dev origin (adjust if different)
    CORS(app,
         resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
         supports_credentials=False,  # no cookies needed for /api/query
         allow_headers=["Content-Type", "x-session-id"],
         methods=["GET","POST","PUT","DELETE","OPTIONS"])

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "herboai-backend"}, 200

    return app
