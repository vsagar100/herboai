from flask import Flask
from flask import Blueprint
from flask_cors import CORS
from routes.herbs import herbs_bp
from routes.search import search_bp

app = Flask(__name__)
#search_bp = Blueprint("search", __name__)
CORS(app)  # Allow frontend to connect
#CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# Register routes
app.register_blueprint(herbs_bp, url_prefix="/api")
app.register_blueprint(search_bp, url_prefix="/api")

if __name__ == "__main__":

    print("\n=== Registered Routes ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    print("=========================\n")

    app.run(debug=True)
    #app.run(host="localhost", port=5000, debug=True)
