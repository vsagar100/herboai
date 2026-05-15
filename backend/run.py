from init import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Enable multithreaded dev server so long LLM requests
    # don't block health checks and static/file routes.
    host = os.environ.get("HERBOAI_HOST", "127.0.0.1")
    port = int(os.environ.get("HERBOAI_PORT", os.environ.get("PORT", "5000")))
    app.run(host=host, port=port, debug=False, threaded=True)
