import logging
import json
import re
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from functools import wraps
from flask import jsonify, request

logger = logging.getLogger(__name__)

def format_api_response(data: Any = None, message: str = "Success", 
                       status_code: int = 200, errors: List[str] = None) -> Dict:
    """Format standardized API response"""
    response = {
        'status': 'success' if status_code < 400 else 'error',
        'message': message,
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if errors:
        response['errors'] = errors
    
    return response

def safe_json_loads(json_str: Union[str, None], default: Any = None) -> Any:
    """Safely parse JSON string with fallback"""
    if not json_str:
        return default
    
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Failed to parse JSON: {str(e)}")
        return default

def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """Safely convert data to JSON string"""
    try:
        return json.dumps(data, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        logger.warning(f"Failed to serialize to JSON: {str(e)}")
        return default

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix"""
    if not text or len(text) <= max_length:
        return text or ""
    
    return text[:max_length - len(suffix)] + suffix

def clean_whitespace(text: str) -> str:
    """Clean and normalize whitespace in text"""
    if not text:
        return ""
    
    # Replace multiple whitespace with single space
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()

def extract_numbers(text: str) -> List[float]:
    """Extract all numbers from text"""
    if not text:
        return []
    
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    
    numbers = []
    for match in matches:
        try:
            numbers.append(float(match))
        except ValueError:
            continue
    
    return numbers

def generate_session_id() -> str:
    """Generate unique session ID"""
    import uuid
    return str(uuid.uuid4())

def validate_required_fields(data: Dict, required_fields: List[str]) -> List[str]:
    """Validate that required fields are present and not empty"""
    errors = []
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            errors.append(f"Field '{field}' cannot be empty")
    
    return errors

def paginate_query(query, page: int = 1, per_page: int = 20, max_per_page: int = 100):
    """Paginate SQLAlchemy query with validation"""
    # Validate pagination parameters
    page = max(1, page)
    per_page = min(max(1, per_page), max_per_page)
    
    try:
        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    except Exception as e:
        logger.error(f"Pagination error: {str(e)}")
        return None

def format_pagination_response(pagination_obj, data_key: str = 'items') -> Dict:
    """Format paginated response"""
    if not pagination_obj:
        return {
            data_key: [],
            'pagination': {
                'page': 1,
                'pages': 0,
                'per_page': 20,
                'total': 0,
                'has_next': False,
                'has_prev': False
            }
        }
    
    return {
        data_key: [item.to_dict() if hasattr(item, 'to_dict') else item 
                   for item in pagination_obj.items],
        'pagination': {
            'page': pagination_obj.page,
            'pages': pagination_obj.pages,
            'per_page': pagination_obj.per_page,
            'total': pagination_obj.total,
            'has_next': pagination_obj.has_next,
            'has_prev': pagination_obj.has_prev
        }
    }

def handle_file_upload(file_obj, allowed_extensions: List[str], 
                      max_size: int = 16 * 1024 * 1024) -> Dict:
    """Handle file upload with validation"""
    if not file_obj:
        return {'success': False, 'error': 'No file provided'}
    
    # Check file size
    file_obj.seek(0, os.SEEK_END)
    file_size = file_obj.tell()
    file_obj.seek(0)
    
    if file_size > max_size:
        return {'success': False, 'error': f'File size exceeds {max_size} bytes'}
    
    # Check file extension
    filename = file_obj.filename or ''
    if '.' not in filename:
        return {'success': False, 'error': 'File must have an extension'}
    
    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in allowed_extensions:
        return {'success': False, 'error': f'File type .{extension} not allowed'}
    
    return {
        'success': True,
        'filename': filename,
        'size': file_size,
        'extension': extension
    }

def log_api_request(endpoint: str = None):
    """Decorator to log API requests"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            
            # Log request
            logger.info(f"API Request: {request.method} {request.path}")
            
            try:
                result = func(*args, **kwargs)
                
                # Log successful response
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.info(f"API Response: {request.path} completed in {duration:.3f}s")
                
                return result
                
            except Exception as e:
                # Log error
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.error(f"API Error: {request.path} failed in {duration:.3f}s - {str(e)}")
                raise
                
        return wrapper
    return decorator

def handle_database_error(e: Exception) -> tuple:
    """Handle database errors consistently"""
    logger.error(f"Database error: {str(e)}")
    
    error_message = "Database operation failed"
    status_code = 500
    
    # Handle specific database errors
    error_str = str(e).lower()
    if 'unique constraint' in error_str or 'duplicate' in error_str:
        error_message = "Record already exists"
        status_code = 409
    elif 'foreign key' in error_str:
        error_message = "Invalid reference to related record"
        status_code = 400
    elif 'not null' in error_str:
        error_message = "Required field is missing"
        status_code = 400
    
    return jsonify(format_api_response(
        message=error_message,
        status_code=status_code
    )), status_code

def calculate_similarity_score(text1: str, text2: str) -> float:
    """Calculate simple text similarity score"""
    if not text1 or not text2:
        return 0.0
    
    # Convert to lowercase and split into words
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0

def format_duration(start_time: datetime, end_time: datetime = None) -> str:
    """Format duration between two datetimes"""
    if not end_time:
        end_time = datetime.utcnow()
    
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    
    if total_seconds < 60:
        return f"{total_seconds} seconds"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"
    else:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def create_safe_filename(filename: str) -> str:
    """Create safe filename for storage"""
    if not filename:
        return f"file_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    
    # Remove path components
    filename = os.path.basename(filename)
    
    # Replace unsafe characters
    safe_chars = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    
    # Limit length
    if len(safe_chars) > 255:
        name, ext = os.path.splitext(safe_chars)
        safe_chars = name[:250] + ext
    
    return safe_chars

def merge_dicts(*dicts: Dict) -> Dict:
    """Merge multiple dictionaries, with later ones taking precedence"""
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result

def get_client_ip() -> str:
    """Get client IP address from request"""
    # Check for forwarded IP first (from proxy/load balancer)
    forwarded_ips = request.headers.get('X-Forwarded-For', '').split(',')
    if forwarded_ips and forwarded_ips[0].strip():
        return forwarded_ips[0].strip()
    
    # Check other proxy headers
    proxy_headers = [
        'X-Real-IP',
        'X-Forwarded-For',
        'CF-Connecting-IP',  # Cloudflare
        'True-Client-IP'     # Cloudflare Enterprise
    ]
    
    for header in proxy_headers:
        ip = request.headers.get(header)
        if ip:
            return ip.split(',')[0].strip()
    
    # Fall back to remote address
    return request.remote_addr or 'unknown'

def is_development() -> bool:
    """Check if running in development mode"""
    return os.getenv('FLASK_ENV') == 'development'

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"

def rate_limit_key(identifier: str = None) -> str:
    """Generate rate limiting key"""
    if not identifier:
        identifier = get_client_ip()
    
    return f"rate_limit:{identifier}:{datetime.utcnow().strftime('%H:%M')}"