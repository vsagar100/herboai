import sys
from flask import Flask, jsonify
from flask import Blueprint
from flask_cors import CORS
from routes.herbs import herbs_bp
from routes.search import search_bp, initialize_ai_system

app = Flask(__name__)
app.config.from_object('config.Config')
#search_bp = Blueprint("search", __name__)
CORS(app)  # Allow frontend to connect
#CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# Register routes
app.register_blueprint(herbs_bp, url_prefix="/api")
app.register_blueprint(search_bp, url_prefix="/api")

@app.route('/api/health_old', methods=["GET"])
def main_health():
    print("Health check requested")
    try:
        return jsonify({
            "status": "healthy",
            "app": "HerboAI Main Server",
            "version": "2.0.0"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

# Initialize AI system before first request
@app.before_request
def startup():
    if not hasattr(app, '_ai_initialized'):
        print("Initializing AI system...")
        if initialize_ai_system():
            app._ai_initialized = True
            #print("AI system ready!")
            print("✅ HerboAI Server ready!")
        else:
            print("Failed to initialize AI system!")


if __name__ == "__main__":

    # Initialize AI system
    if not initialize_ai_system():
        print("❌ Critical: AI system initialization failed!")
        sys.exit(1)
    
    print("\n🚀 Server starting on http://localhost:5000")
    print("📱 Frontend should connect to: http://localhost:5000/api")
    print("🔍 API endpoints:")
    print("   POST /api/query - Main AI query endpoint")
    print("   POST /api/suggestions - AI suggestions")
    print("   GET  /api/health - System health check")
    print("   GET  /api/debug/ai_analysis/<query> - Debug AI analysis")
    print("\n" + "=" * 50)

    print("\n=== Registered Routes ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    print("=========================\n")

    app.run(debug=True)
    #app.run(host="localhost", port=5000, debug=True)
