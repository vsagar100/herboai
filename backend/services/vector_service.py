import numpy as np
import logging
from typing import List, Dict, Tuple
import json
import os
from sentence_transformers import SentenceTransformer
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class VectorService:
    """Vector database service for semantic search"""
    
    def __init__(self):
        self.model = None
        self.embedding_dim = 384  # for all-MiniLM-L6-v2
        self.vectors_db_path = './data/vectors.db'
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize embedding model and vector database"""
        try:
            # Initialize embedding model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Loaded SentenceTransformer model")
            
            # Initialize vector database (SQLite for simplicity)
            self._init_vector_db()
            logger.info("Initialized vector database")
            
        except Exception as e:
            logger.error(f"Error initializing vector services: {str(e)}")
            # Continue without vector search functionality
            self.model = None
    
    def _init_vector_db(self):
        """Initialize SQLite database for vector storage"""
        try:
            os.makedirs('./data', exist_ok=True)
            
            conn = sqlite3.connect(self.vectors_db_path)
            cursor = conn.cursor()
            
            # Create vectors table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS plant_vectors (
                    plant_id INTEGER PRIMARY KEY,
                    embedding BLOB,
                    text_content TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error initializing vector database: {str(e)}")
    
    def add_plant_vector(self, plant_id: int, plant_data: Dict) -> bool:
        """Add plant embedding to vector database"""
        try:
            if not self.model:
                logger.warning("Embedding model not available")
                return False
            
            # Create text representation
            text = self._create_plant_text(plant_data)
            
            # Generate embedding
            embedding = self.model.encode(text)
            
            # Store in database
            conn = sqlite3.connect(self.vectors_db_path)
            cursor = conn.cursor()
            
            metadata = {
                "name": plant_data.get('name', ''),
                "scientific_name": plant_data.get('scientific_name', ''),
                "category": plant_data.get('category', ''),
                "system": plant_data.get('ayush_system', '')
            }
            
            cursor.execute('''
                INSERT OR REPLACE INTO plant_vectors 
                (plant_id, embedding, text_content, metadata)
                VALUES (?, ?, ?, ?)
            ''', (
                plant_id,
                embedding.tobytes(),
                text,
                json.dumps(metadata)
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added vector for plant {plant_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding plant vector: {str(e)}")
            return False
    
    def semantic_search(self, query: str, limit: int = 10) -> List[Dict]:
        """Perform semantic search for plants"""
        try:
            if not self.model:
                logger.warning("Embedding model not available for semantic search")
                return []
            
            # Generate query embedding
            query_embedding = self.model.encode(query)
            
            # Get all vectors from database
            conn = sqlite3.connect(self.vectors_db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT plant_id, embedding, metadata FROM plant_vectors')
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                logger.info("No vectors found in database")
                return []
            
            # Calculate similarities
            similarities = []
            for plant_id, embedding_bytes, metadata_json in rows:
                try:
                    # Convert bytes back to numpy array
                    stored_embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
                    
                    # Calculate cosine similarity
                    similarity = cosine_similarity(
                        query_embedding.reshape(1, -1),
                        stored_embedding.reshape(1, -1)
                    )[0][0]
                    
                    metadata = json.loads(metadata_json)
                    
                    similarities.append({
                        'plant_id': plant_id,
                        'similarity': float(similarity),
                        'name': metadata.get('name', ''),
                        'scientific_name': metadata.get('scientific_name', ''),
                        'category': metadata.get('category', ''),
                        'system': metadata.get('system', '')
                    })
                    
                except Exception as e:
                    logger.warning(f"Error processing vector for plant {plant_id}: {str(e)}")
                    continue
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:limit]
                
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []
    
    def _create_plant_text(self, plant_data: Dict) -> str:
        """Create searchable text representation of plant"""
        parts = []
        
        # Basic info
        if plant_data.get('name'):
            parts.append(plant_data['name'])
        if plant_data.get('scientific_name'):
            parts.append(plant_data['scientific_name'])
        
        # Category and system
        if plant_data.get('category'):
            parts.append(f"Category: {plant_data['category']}")
        if plant_data.get('ayush_system'):
            parts.append(f"System: {plant_data['ayush_system']}")
        
        # Uses
        if plant_data.get('uses'):
            if isinstance(plant_data['uses'], str):
                try:
                    uses = json.loads(plant_data['uses'])
                except:
                    uses = [plant_data['uses']]
            else:
                uses = plant_data['uses']
            
            if uses:
                parts.append(f"Uses: {', '.join(uses)}")
        
        # Description
        if plant_data.get('description'):
            parts.append(plant_data['description'])
        
        # Properties
        if plant_data.get('properties'):
            if isinstance(plant_data['properties'], str):
                try:
                    props = json.loads(plant_data['properties'])
                except:
                    props = {}
            else:
                props = plant_data['properties']
            
            if props:
                prop_text = ' '.join([f"{k}: {v}" for k, v in props.items()])
                parts.append(prop_text)
        
        return ' '.join(parts)
    
    def get_similar_plants(self, plant_id: int, limit: int = 5) -> List[Dict]:
        """Find plants similar to a given plant"""
        try:
            if not self.model:
                return []
            
            # Get the plant's embedding
            conn = sqlite3.connect(self.vectors_db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT embedding FROM plant_vectors WHERE plant_id = ?', (plant_id,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return []
            
            query_embedding = np.frombuffer(result[0], dtype=np.float32)
            
            # Get all other plants
            cursor.execute('SELECT plant_id, embedding, metadata FROM plant_vectors WHERE plant_id != ?', (plant_id,))
            rows = cursor.fetchall()
            conn.close()
            
            # Calculate similarities
            similarities = []
            for other_plant_id, embedding_bytes, metadata_json in rows:
                try:
                    stored_embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
                    
                    similarity = cosine_similarity(
                        query_embedding.reshape(1, -1),
                        stored_embedding.reshape(1, -1)
                    )[0][0]
                    
                    metadata = json.loads(metadata_json)
                    
                    similarities.append({
                        'plant_id': other_plant_id,
                        'similarity': float(similarity),
                        'name': metadata.get('name', '')
                    })
                    
                except Exception as e:
                    logger.warning(f"Error calculating similarity for plant {other_plant_id}: {str(e)}")
                    continue
            
            # Sort and return top results
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:limit]
            
        except Exception as e:
            logger.error(f"Error finding similar plants: {str(e)}")
            return []
    
    def update_plant_vector(self, plant_id: int, plant_data: Dict) -> bool:
        """Update existing plant vector"""
        try:
            # Simply replace the existing vector
            return self.add_plant_vector(plant_id, plant_data)
            
        except Exception as e:
            logger.error(f"Error updating plant vector: {str(e)}")
            return False
    
    def delete_plant_vector(self, plant_id: int) -> bool:
        """Delete plant vector"""
        try:
            conn = sqlite3.connect(self.vectors_db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM plant_vectors WHERE plant_id = ?', (plant_id,))
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting plant vector: {str(e)}")
            return False
    
    def get_collection_stats(self) -> Dict:
        """Get vector database statistics"""
        try:
            conn = sqlite3.connect(self.vectors_db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM plant_vectors')
            count = cursor.fetchone()[0]
            conn.close()
            
            return {
                'total_vectors': count,
                'embedding_dimension': self.embedding_dim,
                'model_name': 'all-MiniLM-L6-v2',
                'database_path': self.vectors_db_path
            }
                
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {'total_vectors': 0, 'embedding_dimension': 0}
    
    def rebuild_all_vectors(self) -> int:
        """Rebuild all plant vectors from database"""
        try:
            # Import here to avoid circular imports
            from app import Plant
            
            plants = Plant.query.all()
            success_count = 0
            
            for plant in plants:
                plant_data = {
                    'name': plant.name,
                    'scientific_name': plant.scientific_name,
                    'ayush_system': plant.ayush_system,
                    'category': plant.category,
                    'uses': plant.uses,
                    'description': plant.description,
                    'properties': plant.properties
                }
                
                if self.add_plant_vector(plant.id, plant_data):
                    success_count += 1
            
            logger.info(f"Rebuilt vectors for {success_count}/{len(plants)} plants")
            return success_count
            
        except Exception as e:
            logger.error(f"Error rebuilding vectors: {str(e)}")
            return 0
    
    def clear_all_vectors(self) -> bool:
        """Clear all vectors from database"""
        try:
            conn = sqlite3.connect(self.vectors_db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM plant_vectors')
            conn.commit()
            conn.close()
            
            logger.info("Cleared all vectors from database")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing vectors: {str(e)}")
            return False