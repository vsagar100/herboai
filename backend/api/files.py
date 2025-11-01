# files.py
import os
from flask import Blueprint, current_app, send_from_directory, abort, make_response

files_bp = Blueprint("files", __name__)

@files_bp.get("/<path:filename>")
def serve_file(filename: str):
    root = current_app.config.get("MEDIA_ROOT")
    print("MEDIA_ROOT:", root)
    if not root:
        abort(404)
    # Security: no path traversal
    safe_path = os.path.normpath(filename).lstrip(os.sep)
    full = os.path.join(root, safe_path)
    print("Serving file:", full)
    if not os.path.isfile(full):
        abort(404)
    resp = make_response(send_from_directory(root, safe_path))
    # Cache for a week; tweak as needed
    resp.headers["Cache-Control"] = "public, max-age=604800"
    return resp
