import sqlite3
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from contextlib import contextmanager

@contextmanager
def database_connection(db_path: str):
    """Context manager for database connections"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    try:
        yield conn
    finally:
        conn.close()

class HerbalDataFetcher:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_herb_basic_info(self, conn, herb_id: int) -> Dict:
        """Fetch basic herb information"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM herbs WHERE id = ?
        """, (herb_id,))
        return dict(cursor.fetchone())

    def get_common_names(self, conn, herb_id: int) -> List[str]:
        """Fetch common names for a herb"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM common_names WHERE herb_id = ?
        """, (herb_id,))
        return [row['name'] for row in cursor.fetchall()]

    def get_remedies(self, conn, herb_id: int) -> List[Dict]:
        """Fetch remedies for a herb"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT condition_name, preparation, form 
            FROM remedies WHERE herb_id = ?
        """, (herb_id,))
        return [
            {
                "condition": row['condition_name'],
                "preparation": row['preparation'],
                "form": row['form']
            }
            for row in cursor.fetchall()
        ]

    def get_languages(self, conn, herb_id: int) -> Dict[str, str]:
        """Fetch language translations for a herb"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT language_code, translation 
            FROM herb_languages WHERE herb_id = ?
        """, (herb_id,))
        return {row['language_code']: row['translation'] for row in cursor.fetchall()}

    def process_herb_data(self, herb_basic: Dict, common_names: List[str], 
                         remedies: List[Dict], languages: Dict) -> Dict:
        """Process and format herb data into required JSON structure"""
        return {
            "id": herb_basic['id'],
            "name": herb_basic['name'],
            "scientific_name": herb_basic['scientific_name'],
            "common_names": common_names,
            "ayush_system": herb_basic['ayush_system'],
            "uses": herb_basic['uses'],
            "remedies": remedies,
            "parts_used": herb_basic['parts_used'].split(',') if herb_basic['parts_used'] else [],
            "phytochemicals": herb_basic['phytochemicals'].split(',') if herb_basic['phytochemicals'] else [],
            "contraindications": herb_basic['contraindications'],
            "languages": languages
        }

    def fetch_all_herbs(self) -> List[Dict]:
        """Fetch all herbs data and convert to JSON format"""
        with database_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM herbs")
            herb_ids = [row['id'] for row in cursor.fetchall()]
            
            herbs_data = []
            for herb_id in herb_ids:
                herb_basic = self.get_herb_basic_info(conn, herb_id)
                common_names = self.get_common_names(conn, herb_id)
                remedies = self.get_remedies(conn, herb_id)
                languages = self.get_languages(conn, herb_id)
                
                herb_json = self.process_herb_data(
                    herb_basic, common_names, remedies, languages
                )
                herbs_data.append(herb_json)
            
            return herbs_data

# def main():
#     """Main function to execute the data fetch and JSON conversion"""
#     try:
#         fetcher = HerbalDataFetcher('herbal.db')
#         herbs_data = fetcher.fetch_all_herbs()
        
#         # Write to JSON file
#         output_path = 'herbs_data.json'
#         with open(output_path, 'w', encoding='utf-8') as f:
#             json.dump(herbs_data, f, ensure_ascii=False, indent=2)
            
#         print(f"Successfully exported data to {output_path}")
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")

# if __name__ == "__main__":
#     main()