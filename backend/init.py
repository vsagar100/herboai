import os
import time
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from db import init_app as init_db
from api.routes import bp as api_bp
from api.files import files_bp
from api.admin_auth import admin_auth_bp
from api.admin_plants import admin_plants_bp
from api.admin_diseases import admin_diseases_bp
from api.admin_preparations import admin_prep_bp
from api.vec_health import bp as vec_bp 
from api.mt_health import bp as mt_bp
import threading

# === MODEL PRELOADING FUNCTION (must be defined before create_app) ===
def preload_models():
    """Eagerly load translation models at startup"""
    print("[Startup] Beginning model preload...")
    start = time.time()
    
    try:
        # 1. Load async translator (kickstarts background loading)
        from services.async_translator import get_async_translator
        async_tx = get_async_translator()
        async_tx.warmup()
        print("[Startup] Async translator warmup initiated")
        
        # 2. Wait for it to finish loading (blocking in startup thread is OK)
        max_wait = 120  # 2 minutes max wait
        waited = 0
        while not async_tx.is_ready() and waited < max_wait:
            time.sleep(2)
            waited += 2
            if waited % 10 == 0:
                print(f"[Startup] Still loading models... ({waited}s)")
        
        if async_tx.is_ready():
            elapsed = time.time() - start
            if elapsed < 1:
                print(f"[Startup] ✓ Translation models loaded in {elapsed*1000:.0f}ms")
            else:
                print(f"[Startup] ✓ Translation models loaded in {elapsed:.2f}s")
            
            # 3. Test translation to ensure it works
            try:
                test_result = async_tx.translate_async("Hello", "mr", timeout=10)
                if test_result:
                    print(f"[Startup] ✓ Translation test passed: {test_result}")
                else:
                    print("[Startup] ⚠️  Translation test returned None")
            except Exception as e:
                print(f"[Startup] ⚠️  Translation test failed: {e}")
        else:
            print(f"[Startup] ⚠️  Models did not load within {max_wait}s")
            
    except Exception as exc:
        print(f"[Startup] Model preload error: {exc}")
        import traceback
        traceback.print_exc()


def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    jwt = JWTManager(app)
    app.config["JWT_SECRET_KEY"] = "supersecret-change-this"
    app.config["FILE_ROOT"] = app.config.get("MEDIA_ROOT")
    app.json.ensure_ascii = False

    CORS(app,
         resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173", "*"]}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "x-session-id"],
         expose_headers=["Content-Type", "Authorization"],
         methods=["GET","POST","PUT","DELETE","OPTIONS"])

    # DB init (connection factory + teardown)
    init_db(app)

    # Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(vec_bp, url_prefix="/api") 
    app.register_blueprint(mt_bp, url_prefix="/api")
    app.register_blueprint(files_bp, url_prefix="/files") 
    app.register_blueprint(admin_auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_plants_bp, url_prefix="/api/admin")
    app.register_blueprint(admin_diseases_bp, url_prefix="/api/admin")
    app.register_blueprint(admin_prep_bp, url_prefix="/api/admin")

    # Health check endpoint (with translator status)
    @app.get("/api/health")
    def health():
        try:
            from services.async_translator import get_async_translator
            tx = get_async_translator()
            translator_ready = tx.is_ready()
            has_translator = tx.translator is not None
        except Exception:
            translator_ready = False
            has_translator = False
        
        return {
            "status": "ok",
            "service": "herboai-backend",
            "translator_ready": translator_ready,
             "translator_loaded": has_translator
        }, 200

    # Start model preloading in background thread
    # daemon=False ensures thread completes even during shutdown
    preload_thread = threading.Thread(target=preload_models, daemon=False)
    preload_thread.start()

    def _vector_bootstrapper():
        with app.app_context():
            from services.vector_bootstrap import ensure_vector_indexes
            try:
                stats = ensure_vector_indexes()
                print(f"[Startup] Vector indexes ready: {stats}")
            except Exception as exc:
                print(f"[Startup] Vector index bootstrap failed: {exc}")

    vector_thread = threading.Thread(target=_vector_bootstrapper, daemon=False)
    vector_thread.start()

    print("[Startup] Model preload started in background")
    print("[Startup] Vector indexing started in background")
    print("[Startup] Server will be responsive immediately, translations ready after preload completes")

    return app
