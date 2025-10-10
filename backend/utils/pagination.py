# utils/pagination.py
from flask import request

def parse_pagination(default_limit=20, max_limit=100):
    try:
        page = max(1, int(request.args.get("page", 1)))
        limit = min(max_limit, max(1, int(request.args.get("limit", default_limit))))
    except Exception:
        page, limit = 1, default_limit
    offset = (page - 1) * limit
    return page, limit, offset
