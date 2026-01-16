# utils/security.py
from __future__ import annotations

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required(fn):
    """
    Enforces:
    - a valid JWT is present (Authorization: Bearer <token> OR JWT cookies if configured)
    - token contains claim: {"is_admin": true}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt() or {}
        if not claims.get("is_admin", False):
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)

    return wrapper
