import re
import json
from typing import Dict, List, Tuple, Any, Optional

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_plant_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate plant data for creation/update"""
    errors = []
    
    # Required fields
    required_fields = ['name', 'scientific_name', 'ayush_system']
    for field in required_fields:
        if not data.get(field) or not str(data[field]).strip():
            errors.append(f"Missing or empty required field: {field}")
    
    # Name validation
    if data.get('name'):
        if len(data['name']) < 2:
            errors.append("Plant name must be at least 2 characters")
        if len(data['name']) > 100:
            errors.append("Plant name must not exceed 100 characters")
    
    # Scientific name validation
    if data.get('scientific_name'):
        if len(data['scientific_name']) < 3:
            errors.append("Scientific name must be at least 3 characters")
        if len(data['scientific_name']) > 100:
            errors.append("Scientific name must not exceed 100 characters")
        # Basic scientific name format check
        if not re.match(r'^[A-Z][a-z]+ [a-z]+', data['scientific_name'].strip()):
            errors.append("Scientific name should follow binomial nomenclature (e.g., 'Genus species')")
    
    # AYUSH system validation
    valid_systems = ['Ayurveda', 'Siddha', 'Unani', 'Homeopathy', 'Yoga', 'Naturopathy']
    if data.get('ayush_system') and data['ayush_system'] not in valid_systems:
        errors.append(f"Invalid AYUSH system. Must be one of: {', '.join(valid_systems)}")
    
    # Category validation
    if data.get('category'):
        valid_categories = [
            'Anti-inflammatory', 'Antibacterial', 'Antiviral', 'Antifungal',
            'Digestive', 'Respiratory', 'Cardiovascular', 'Nervous System',
            'Immune System', 'Skin & Hair', 'Reproductive Health', 'Adaptogen',
            'Detoxification', 'Pain Relief', 'Mental Health', 'Metabolic', 'Antioxidant'
        ]
        if data['category'] not in valid_categories:
            errors.append(f"Invalid category. Must be one of: {', '.join(valid_categories)}")
    
    # Uses validation
    if data.get('uses'):
        if isinstance(data['uses'], str):
            try:
                uses = json.loads(data['uses'])
                if not isinstance(uses, list):
                    errors.append("Uses must be a list when provided as JSON string")
            except json.JSONDecodeError:
                errors.append("Invalid JSON format for uses field")
        elif isinstance(data['uses'], list):
            if len(data['uses']) > 20:
                errors.append("Maximum 20 uses allowed")
            for use in data['uses']:
                if not isinstance(use, str) or len(use.strip()) == 0:
                    errors.append("Each use must be a non-empty string")
        else:
            errors.append("Uses must be a list or JSON string")
    
    # Properties validation
    if data.get('properties'):
        if isinstance(data['properties'], str):
            try:
                props = json.loads(data['properties'])
                if not isinstance(props, dict):
                    errors.append("Properties must be a dictionary when provided as JSON string")
            except json.JSONDecodeError:
                errors.append("Invalid JSON format for properties field")
        elif not isinstance(data['properties'], dict):
            errors.append("Properties must be a dictionary or JSON string")
    
    # Description validation
    if data.get('description') and len(data['description']) > 1000:
        errors.append("Description must not exceed 1000 characters")
    
    # Preparation validation
    if data.get('preparation') and len(data['preparation']) > 500:
        errors.append("Preparation instructions must not exceed 500 characters")
    
    # Contraindications validation
    if data.get('contraindications') and len(data['contraindications']) > 500:
        errors.append("Contraindications must not exceed 500 characters")
    
    return len(errors) == 0, errors

def validate_chat_query(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate chat query data"""
    errors = []
    
    # Query validation
    if not data.get('query') or not str(data['query']).strip():
        errors.append("Query is required and cannot be empty")
    elif len(data['query']) > 1000:
        errors.append("Query must not exceed 1000 characters")
    
    # Language validation
    valid_languages = ['en', 'hi', 'mr']
    if data.get('language') and data['language'] not in valid_languages:
        errors.append(f"Invalid language. Must be one of: {', '.join(valid_languages)}")
    
    # Session ID validation
    if data.get('session_id'):
        if len(data['session_id']) > 100:
            errors.append("Session ID must not exceed 100 characters")
        if not re.match(r'^[a-zA-Z0-9_-]+$', data['session_id']):
            errors.append("Session ID can only contain alphanumeric characters, underscores, and hyphens")
    
    return len(errors) == 0, errors

def validate_search_params(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate search parameters"""
    errors = []
    
    # Query validation
    if not data.get('query') or not str(data['query']).strip():
        errors.append("Search query is required")
    elif len(data['query']) > 200:
        errors.append("Search query must not exceed 200 characters")
    
    # Limit validation
    if data.get('limit'):
        try:
            limit = int(data['limit'])
            if limit < 1 or limit > 50:
                errors.append("Limit must be between 1 and 50")
        except (ValueError, TypeError):
            errors.append("Limit must be a valid integer")
    
    # Language validation
    valid_languages = ['en', 'hi', 'mr']
    if data.get('language') and data['language'] not in valid_languages:
        errors.append(f"Invalid language. Must be one of: {', '.join(valid_languages)}")
    
    return len(errors) == 0, errors

def validate_admin_credentials(username: str, password: str) -> bool:
    """Validate admin credentials"""
    # In production, this should check against hashed passwords in database
    return username == 'admin' and password == 'admin123'

def sanitize_text_input(text: str) -> str:
    """Sanitize text input to prevent XSS and other attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>&"\']', '', text)
    
    # Limit length
    sanitized = sanitized[:1000]
    
    # Strip whitespace
    sanitized = sanitized.strip()
    
    return sanitized

def validate_file_upload(file_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate file upload data"""
    errors = []
    
    # File size validation (max 16MB)
    max_size = 16 * 1024 * 1024
    if file_data.get('size', 0) > max_size:
        errors.append("File size must not exceed 16MB")
    
    # File type validation
    allowed_types = ['application/json', 'text/csv', 'application/vnd.ms-excel', 
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    if file_data.get('type') not in allowed_types:
        errors.append("Invalid file type. Only JSON, CSV, and Excel files are allowed")
    
    # Filename validation
    if file_data.get('filename'):
        if not re.match(r'^[a-zA-Z0-9._-]+$', file_data['filename']):
            errors.append("Filename contains invalid characters")
        if len(file_data['filename']) > 255:
            errors.append("Filename must not exceed 255 characters")
    
    return len(errors) == 0, errors

def validate_pagination_params(page: Optional[int], per_page: Optional[int]) -> Tuple[bool, List[str]]:
    """Validate pagination parameters"""
    errors = []
    
    # Page validation
    if page is not None:
        if page < 1:
            errors.append("Page number must be at least 1")
        if page > 1000:
            errors.append("Page number must not exceed 1000")
    
    # Per page validation
    if per_page is not None:
        if per_page < 1:
            errors.append("Items per page must be at least 1")
        if per_page > 100:
            errors.append("Items per page must not exceed 100")
    
    return len(errors) == 0, errors

def validate_filter_params(filters: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate filter parameters for plant search"""
    errors = []
    
    # Category filter
    if filters.get('category'):
        valid_categories = [
            'Anti-inflammatory', 'Antibacterial', 'Antiviral', 'Antifungal',
            'Digestive', 'Respiratory', 'Cardiovascular', 'Nervous System',
            'Immune System', 'Skin & Hair', 'Reproductive Health', 'Adaptogen',
            'Detoxification', 'Pain Relief', 'Mental Health', 'Metabolic', 'Antioxidant'
        ]
        if filters['category'] not in valid_categories:
            errors.append(f"Invalid category filter: {filters['category']}")
    
    # AYUSH system filter
    if filters.get('ayush_system'):
        valid_systems = ['Ayurveda', 'Siddha', 'Unani', 'Homeopathy', 'Yoga', 'Naturopathy']
        if filters['ayush_system'] not in valid_systems:
            errors.append(f"Invalid AYUSH system filter: {filters['ayush_system']}")
    
    # Search term filter
    if filters.get('search'):
        if len(filters['search']) > 100:
            errors.append("Search term must not exceed 100 characters")
    
    return len(errors) == 0, errors

def validate_remedy_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate remedy data"""
    errors = []
    
    # Required fields
    required_fields = ['symptom', 'plant_ids']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Symptom validation
    if data.get('symptom'):
        if len(data['symptom']) < 2:
            errors.append("Symptom must be at least 2 characters")
        if len(data['symptom']) > 100:
            errors.append("Symptom must not exceed 100 characters")
    
    # Plant IDs validation
    if data.get('plant_ids'):
        if isinstance(data['plant_ids'], str):
            try:
                plant_ids = json.loads(data['plant_ids'])
            except json.JSONDecodeError:
                errors.append("Invalid JSON format for plant_ids")
                plant_ids = []
        else:
            plant_ids = data['plant_ids']
        
        if not isinstance(plant_ids, list):
            errors.append("Plant IDs must be a list")
        elif len(plant_ids) == 0:
            errors.append("At least one plant ID is required")
        elif len(plant_ids) > 10:
            errors.append("Maximum 10 plant IDs allowed")
        else:
            for pid in plant_ids:
                if not isinstance(pid, int) or pid < 1:
                    errors.append("All plant IDs must be positive integers")
                    break
    
    # AYUSH system validation
    if data.get('ayush_system'):
        valid_systems = ['Ayurveda', 'Siddha', 'Unani', 'Homeopathy', 'Yoga', 'Naturopathy']
        if data['ayush_system'] not in valid_systems:
            errors.append(f"Invalid AYUSH system: {data['ayush_system']}")
    
    # Text field length validations
    text_fields = {
        'diagnosis_pattern': 500,
        'dosage': 300,
        'lifestyle_recommendations': 500,
        'preparation_method': 400
    }
    
    for field, max_length in text_fields.items():
        if data.get(field) and len(data[field]) > max_length:
            errors.append(f"{field} must not exceed {max_length} characters")
    
    return len(errors) == 0, errors

def validate_language_code(language: str) -> bool:
    """Validate language code"""
    valid_languages = ['en', 'hi', 'mr']
    return language in valid_languages

def validate_json_string(json_str: str) -> Tuple[bool, Optional[Dict]]:
    """Validate and parse JSON string"""
    try:
        parsed = json.loads(json_str)
        return True, parsed
    except json.JSONDecodeError:
        return False, None

def validate_numeric_range(value: Any, min_val: float, max_val: float) -> bool:
    """Validate numeric value is within range"""
    try:
        num_val = float(value)
        return min_val <= num_val <= max_val
    except (ValueError, TypeError):
        return False

def validate_date_format(date_str: str) -> bool:
    """Validate date string format (YYYY-MM-DD)"""
    pattern = r'^\d{4}-\d{2}-\d{2}'
    return bool(re.match(pattern, date_str))

def validate_session_id(session_id: str) -> bool:
    """Validate session ID format"""
    if not session_id or len(session_id) > 100:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_-]+, session_id)'))

def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    if not api_key:
        return False
    # API key should be alphanumeric and at least 32 characters
    return bool(re.match(r'^[a-zA-Z0-9]{32,}, api_key)'))

def validate_bulk_import_data(data: List[Dict]) -> Tuple[bool, List[str]]:
    """Validate bulk import data"""
    errors = []
    
    if not isinstance(data, list):
        errors.append("Import data must be a list")
        return False, errors
    
    if len(data) == 0:
        errors.append("Import data cannot be empty")
        return False, errors
    
    if len(data) > 1000:
        errors.append("Maximum 1000 items can be imported at once")
        return False, errors
    
    # Validate each item
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"Item {i+1}: Must be a dictionary")
            continue
        
        # Validate plant data
        is_valid, item_errors = validate_plant_data(item)
        if not is_valid:
            for error in item_errors:
                errors.append(f"Item {i+1}: {error}")
    
    return len(errors) == 0, errors

class InputSanitizer:
    """Class for sanitizing various types of input"""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Remove HTML tags and dangerous characters"""
        if not text:
            return ""
        
        # Remove HTML tags
        clean = re.sub(r'<[^>]*>', '', text)
        
        # Remove potentially dangerous characters
        clean = re.sub(r'[<>&"\']', '', clean)
        
        return clean.strip()
    
    @staticmethod
    def sanitize_sql(text: str) -> str:
        """Sanitize input to prevent SQL injection"""
        if not text:
            return ""
        
        # Remove SQL keywords and dangerous characters
        dangerous_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)',
            r'[;\'\"\\]',
            r'--',
            r'/\*',
            r'\*/'
        ]
        
        clean = text
        for pattern in dangerous_patterns:
            clean = re.sub(pattern, '', clean, flags=re.IGNORECASE)
        
        return clean.strip()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe storage"""
        if not filename:
            return "unnamed_file"
        
        # Remove path traversal attempts
        clean = os.path.basename(filename)
        
        # Remove dangerous characters
        clean = re.sub(r'[^a-zA-Z0-9._-]', '_', clean)
        
        # Limit length
        if len(clean) > 255:
            name, ext = os.path.splitext(clean)
            clean = name[:250] + ext
        
        return clean or "unnamed_file"
    
    @staticmethod
    def sanitize_search_query(query: str) -> str:
        """Sanitize search query"""
        if not query:
            return ""
        
        # Remove special search operators that might be dangerous
        clean = re.sub(r'[*+\-(){}[\]^"~?:\\]', ' ', query)
        
        # Normalize whitespace
        clean = re.sub(r'\s+', ' ', clean)
        
        return clean.strip()[:200]  # Limit length

def get_validation_rules() -> Dict[str, Dict]:
    """Get all validation rules for reference"""
    return {
        'plant': {
            'required_fields': ['name', 'scientific_name', 'ayush_system'],
            'max_lengths': {
                'name': 100,
                'scientific_name': 100,
                'description': 1000,
                'preparation': 500,
                'contraindications': 500
            },
            'valid_systems': ['Ayurveda', 'Siddha', 'Unani', 'Homeopathy', 'Yoga', 'Naturopathy'],
            'valid_categories': [
                'Anti-inflammatory', 'Antibacterial', 'Antiviral', 'Antifungal',
                'Digestive', 'Respiratory', 'Cardiovascular', 'Nervous System',
                'Immune System', 'Skin & Hair', 'Reproductive Health', 'Adaptogen',
                'Detoxification', 'Pain Relief', 'Mental Health', 'Metabolic', 'Antioxidant'
            ]
        },
        'chat': {
            'max_query_length': 1000,
            'max_session_id_length': 100,
            'valid_languages': ['en', 'hi', 'mr']
        },
        'search': {
            'max_query_length': 200,
            'max_limit': 50,
            'min_limit': 1
        },
        'pagination': {
            'max_page': 1000,
            'max_per_page': 100
        },
        'file_upload': {
            'max_size': 16 * 1024 * 1024,  # 16MB
            'allowed_types': ['application/json', 'text/csv', 'application/vnd.ms-excel'],
            'max_filename_length': 255
        }
    }