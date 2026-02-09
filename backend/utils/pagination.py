from flask import request, current_app

def get_pagination():
    try:
        page = int(request.args.get("page", "1"))
        # Accept both "size" and "per_page" for backwards compatibility
        raw = request.args.get("size") or request.args.get("per_page") or str(current_app.config["DEFAULT_PAGE_SIZE"])
        size = int(raw)
    except ValueError:
        page = 1
        size = current_app.config["DEFAULT_PAGE_SIZE"]

    size = max(1, min(size, current_app.config["MAX_PAGE_SIZE"]))
    offset = (page - 1) * size
    return page, size, offset

def absolute_file_url(rel_path: str | None) -> str | None:
    if not rel_path:
        return None
    return rel_path
    # Ensure no leading slash duplication
    rel = rel_path[1:] if rel_path.startswith("/") else rel_path
    base = f"{request.scheme}://{request.host}"
    return f"{base}/files/{rel}"