# blueprints/files.py
import os
from flask import Blueprint, send_from_directory, abort, current_app

bp = Blueprint("files", __name__, url_prefix="/files")

@bp.get("/<path:filename>")
def serve_file(filename):
    root = current_app.config["UPLOAD_FOLDER"]
    fpath = os.path.join(root, filename)
    print("Serving file:", fpath)
    if not os.path.isfile(fpath):
        abort(404)
    directory, name = os.path.split(fpath)
    return send_from_directory(directory, name, max_age=86400)
