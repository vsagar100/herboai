from init import create_app

app = create_app()

if __name__ == "__main__":
    # Enable multithreaded dev server so long LLM requests
    # don't block health checks and static/file routes.
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
