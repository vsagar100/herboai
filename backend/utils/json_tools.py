import json

def parse_json_field(value):
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except Exception:
        return value  # keep raw if not valid JSON

def to_json_safe(row_or_dict):
    if row_or_dict is None:
        return None
    if isinstance(row_or_dict, dict):
        return {k: try_parse(v) for k, v in row_or_dict.items()}
    # sqlite3.Row
    return {k: try_parse(row_or_dict[k]) for k in row_or_dict.keys()}

def try_parse(v):
    if isinstance(v, (dict, list)) or v is None:
        return v
    if isinstance(v, (int, float, bool)):
        return v
    # try JSON
    parsed = parse_json_field(v)
    return parsed
