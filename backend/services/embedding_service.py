import logging
import json
import os
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import numpy as np

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating and managing embeddings"""
    
    def __init__(self):
        self.model = None
        self.model_name = 'all-MiniLM-L6-v2'
        self.embedding_cache = {}
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            self.model = None
    
    def generate_text_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a single text"""
        if not self.model:
            logger.error("Embedding model not loaded")
            return None
        
        try:
            # Check cache first
            if text in self.embedding_cache:
                return self.embedding_cache[text]
            
            # Generate embedding
            embedding = self.model.encode(text)
            embedding_list = embedding.tolist()
            
            # Cache the result
            self.embedding_cache[text] = embedding_list
            
            return embedding_list
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None
    
    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if not self.model:
            logger.error("Embedding model not loaded")
            return []
        
        try:
            embeddings = self.model.encode(texts)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            return []
    
    def generate_plant_embeddings(self, plant) -> bool:
        """Generate embeddings for a plant object"""
        try:
            # Create comprehensive text representation
            plant_text = self._create_plant_text(plant)
            
            # Generate embedding
            embedding = self.generate_text_embedding(plant_text)
            
            if embedding:
                # Save embedding (could be stored in database or vector store)
                self._save_plant_embedding(plant.id, embedding, plant_text)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error generating plant embeddings: {str(e)}")
            return False
    
    def _create_plant_text(self, plant) -> str:
        """Create searchable text representation of plant"""
        text_parts = []
        
        # Basic information
        text_parts.append(plant.name)
        text_parts.append(plant.scientific_name)
        
        if plant.description:
            text_parts.append(plant.description)
        
        # Uses
        if plant.uses:
            try:
                uses = json.loads(plant.uses) if isinstance(plant.uses, str) else plant.uses
                if uses:
                    text_parts.append(f"Uses: {', '.join(uses)}")
            except:
                text_parts.append(f"Uses: {plant.uses}")
        
        # Category and system
        if plant.category:
            text_parts.append(f"Category: {plant.category}")
        
        if plant.ayush_system:
            text_parts.append(f"System: {plant.ayush_system}")
        
        # Properties
        if plant.properties:
            try:
                props = json.loads(plant.properties) if isinstance(plant.properties, str) else plant.properties
                if props:
                    prop_text = ' '.join([f"{k}: {v}" for k, v in props.items()])
                    text_parts.append(prop_text)
            except:
                pass
        
        # Preparation and contraindications
        if plant.preparation:
            text_parts.append(f"Preparation: {plant.preparation}")
        
        if plant.contraindications:
            text_parts.append(f"Contraindications: {plant.contraindications}")
        
        return ' '.join(text_parts)
    
    def _save_plant_embedding(self, plant_id: int, embedding: List[float], text: str):
        """Save plant embedding to file system"""
        try:
            # Create embeddings directory if it doesn't exist
            embeddings_dir = './data/embeddings'
            os.makedirs(embeddings_dir, exist_ok=True)
            
            # Save embedding data
            embedding_data = {
                'plant_id': plant_id,
                'embedding': embedding,
                'text': text,
                'model': self.model_name,
                'dimension': len(embedding)
            }
            
            file_path = os.path.join(embeddings_dir, f'plant_{plant_id}.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(embedding_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved embedding for plant {plant_id}")
            
        except Exception as e:
            logger.error(f"Error saving plant embedding: {str(e)}")
    
    def load_plant_embedding(self, plant_id: int) -> Optional[Dict]:
        """Load plant embedding from file system"""
        try:
            file_path = f'./data/embeddings/plant_{plant_id}.json'
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
            
        except Exception as e:
            logger.error(f"Error loading plant embedding: {str(e)}")
            return None
    
    def get_query_embedding(self, query: str, language: str = 'en') -> Optional[List[float]]:
        """Get embedding for search query"""
        # For multilingual support, you could translate query first
        if language != 'en':
            # Import here to avoid circular imports
            from utils.multilingual import MultilingualProcessor
            processor = MultilingualProcessor()
            query = processor.translate_to_english(query, language)
        
        return self.generate_text_embedding(query)
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            # Convert to numpy arrays
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Calculate cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def find_similar_embeddings(self, target_embedding: List[float], 
                              candidate_embeddings: Dict[int, List[float]], 
                              top_k: int = 5) -> List[Dict]:
        """Find most similar embeddings from candidates"""
        similarities = []
        
        for plant_id, embedding in candidate_embeddings.items():
            similarity = self.calculate_similarity(target_embedding, embedding)
            similarities.append({
                'plant_id': plant_id,
                'similarity': similarity
            })
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similarities[:top_k]
    
    def get_embedding_stats(self) -> Dict:
        """Get statistics about embeddings"""
        try:
            embeddings_dir = './data/embeddings'
            
            if not os.path.exists(embeddings_dir):
                return {'total_embeddings': 0, 'model': self.model_name}
            
            embedding_files = [f for f in os.listdir(embeddings_dir) if f.endswith('.json')]
            
            return {
                'total_embeddings': len(embedding_files),
                'model': self.model_name,
                'cache_size': len(self.embedding_cache),
                'embedding_dimension': 384 if self.model else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting embedding stats: {str(e)}")
            return {'total_embeddings': 0, 'error': str(e)}
    
    def clear_cache(self):
        """Clear embedding cache"""
        self.embedding_cache.clear()
        logger.info("Embedding cache cleared")
    
    def precompute_plant_embeddings(self, plants: List) -> int:
        """Precompute embeddings for a list of plants"""
        success_count = 0
        
        for plant in plants:
            try:
                if self.generate_plant_embeddings(plant):
                    success_count += 1
            except Exception as e:
                logger.error(f"Error precomputing embedding for plant {plant.id}: {str(e)}")
        
        logger.info(f"Precomputed embeddings for {success_count}/{len(plants)} plants")
        return success_count