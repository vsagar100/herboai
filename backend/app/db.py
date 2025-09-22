import sqlite3
import json
from typing import List, Dict, Optional
from .settings import settings
from loguru import logger

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(settings.DB_PATH)

def dict_factory(cursor, row):
    """Convert sqlite rows to dictionaries"""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def list_herbs(limit: int = 50, offset: int = 0) -> List[Dict]:
    """List herbs with pagination"""
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, scientific_name, uses, ayush_system, parts_used
            FROM herbs 
            ORDER BY name 
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Error listing herbs: {e}")
        return []

def fetch_herb(herb_id: str) -> Optional[Dict]:
    """Fetch detailed herb information by ID"""
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM herbs WHERE id = ?
        """, (herb_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Error fetching herb {herb_id}: {e}")
        return None

def fetch_herbs_by_ids(herb_ids: List[str]) -> List[Dict]:
    """Fetch multiple herbs by their IDs"""
    if not herb_ids:
        return []
    
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        placeholders = ','.join('?' for _ in herb_ids)
        cursor.execute(f"""
            SELECT * FROM herbs WHERE id IN ({placeholders})
        """, herb_ids)
        
        results = cursor.fetchall()
        conn.close()
        
        # Return results in the same order as herb_ids
        result_dict = {herb['id']: herb for herb in results}
        return [result_dict[herb_id] for herb_id in herb_ids if herb_id in result_dict]
        
    except Exception as e:
        logger.error(f"Error fetching herbs by IDs: {e}")
        return []

def search_herbs_by_condition(condition: str, limit: int = 10) -> List[Dict]:
    """Search herbs by health condition"""
    try:
        conn = get_db_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM herbs 
            WHERE uses LIKE ? OR contraindications LIKE ?
            ORDER BY name 
            LIMIT ?
        """, (f"%{condition}%", f"%{condition}%", limit))
        
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Error searching herbs by condition: {e}")
        return []

def upsert_herb(herb_data: Dict):
    """Insert or update herb data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS herbs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                scientific_name TEXT,
                uses TEXT,
                contraindications TEXT,
                dosage TEXT,
                ayush_system TEXT DEFAULT 'Ayurveda',
                parts_used TEXT,
                languages_json TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Prepare languages JSON
        languages_json = json.dumps(herb_data.get('languages', {}))
        
        # Upsert herb data
        cursor.execute("""
            INSERT OR REPLACE INTO herbs (
                id, name, scientific_name, uses, contraindications, 
                dosage, ayush_system, parts_used, languages_json,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            herb_data.get('id'),
            herb_data.get('name'),
            herb_data.get('scientific_name', ''),
            herb_data.get('uses', ''),
            herb_data.get('contraindications', ''),
            herb_data.get('dosage', ''),
            herb_data.get('ayush_system', 'Ayurveda'),
            herb_data.get('parts_used', ''),
            languages_json
        ))
        
        conn.commit()
        conn.close()
        logger.info(f"Upserted herb: {herb_data.get('id')}")
        
    except Exception as e:
        logger.error(f"Error upserting herb: {e}")
        raise

def get_herb_stats() -> Dict:
    """Get database statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total_herbs FROM herbs")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT ayush_system, COUNT(*) as count 
            FROM herbs 
            GROUP BY ayush_system
        """)
        by_system = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            "total_herbs": total,
            "by_ayush_system": by_system
        }
    except Exception as e:
        logger.error(f"Error getting herb stats: {e}")
        return {"total_herbs": 0, "by_ayush_system": {}}