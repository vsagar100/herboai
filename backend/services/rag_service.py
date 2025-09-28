import json
import logging
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class RAGService:
    """Retrieval-Augmented Generation service for herbal knowledge"""
    
    def __init__(self):
        self.model = None
        self.plant_embeddings = {}
        self.remedy_templates = self._load_remedy_templates()
        self.safety_guidelines = self._load_safety_guidelines()
        self._load_embedding_model()
    
    def _load_embedding_model(self):
        """Load sentence transformer model for embeddings"""
        try:
            # Use lightweight model for CPU inference
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Loaded SentenceTransformer model: all-MiniLM-L6-v2")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            self.model = None
    
    def _load_remedy_templates(self) -> Dict[str, str]:
        """Load remedy response templates"""
        return {
            'treatment': """
Based on traditional {system} medicine, here are some herbal recommendations for {symptom}:

{plant_info}

**Preparation and Usage:**
{preparation}

**Important Notes:**
- Always consult with a qualified healthcare provider before starting any herbal treatment
- Start with small doses to test for allergic reactions
- Discontinue use if you experience any adverse effects

**Disclaimer:** This information is for educational purposes only and should not replace professional medical advice.
            """,
            
            'information': """
Here's what I found about {plant_name}:

**Scientific Name:** {scientific_name}
**Traditional System:** {system}
**Category:** {category}

**Description:**
{description}

**Traditional Uses:**
{uses}

**Properties:** {properties}

**Preparation Methods:**
{preparation}

**Safety Information:**
{contraindications}
            """,
            
            'general': """
Based on your query about "{query}", here's what traditional medicine systems suggest:

{relevant_info}

**Key Recommendations:**
{recommendations}

**Safety Notes:**
{safety_notes}

Would you like more specific information about any of these herbs or their preparation methods?
            """
        }
    
    def _load_safety_guidelines(self) -> Dict[str, List[str]]:
        """Load safety guidelines for different conditions"""
        return {
            'pregnancy': [
                'Avoid herbs with strong uterine stimulant properties',
                'Consult healthcare provider before using any herbs',
                'Some herbs may cause miscarriage or birth defects'
            ],
            'children': [
                'Use reduced dosages for children',
                'Some herbs are not suitable for children under 12',
                'Always consult pediatrician before giving herbs to children'
            ],
            'elderly': [
                'May require adjusted dosages due to slower metabolism',
                'Be cautious with herbs affecting blood pressure',
                'Monitor for drug interactions with medications'
            ],
            'chronic_conditions': [
                'Monitor blood sugar levels if diabetic',
                'Check blood pressure regularly if hypertensive',
                'Be aware of potential drug interactions'
            ]
        }
    
    def get_relevant_plants(self, processed_query: Dict, limit: int = 5) -> List:
        """Retrieve relevant plants based on processed query"""
        try:
            # Import here to avoid circular imports
            from flask import current_app
            from app import Plant, db
            
            # Extract search criteria
            symptoms = processed_query.get('symptoms', [])
            herbs = processed_query.get('herbs', [])
            ayush_system = processed_query.get('ayush_system')
            key_phrases = processed_query.get('key_phrases', [])
            
            # Build query
            query = Plant.query
            
            # Filter by AYUSH system if specified
            if ayush_system:
                query = query.filter(Plant.ayush_system.ilike(f'%{ayush_system}%'))
            
            # Text-based search
            search_terms = symptoms + herbs + key_phrases
            if search_terms:
                conditions = []
                for term in search_terms:
                    conditions.extend([
                        Plant.name.ilike(f'%{term}%'),
                        Plant.description.ilike(f'%{term}%'),
                        Plant.uses.ilike(f'%{term}%'),
                        Plant.category.ilike(f'%{term}%')
                    ])
                
                if conditions:
                    query = query.filter(db.or_(*conditions))
            
            plants = query.limit(limit * 2).all()  # Get more for semantic filtering
            
            # Apply semantic ranking if embedding model is available
            if self.model and plants:
                ranked_plants = self._rank_plants_semantically(
                    processed_query['cleaned_query'], 
                    plants
                )
                return ranked_plants[:limit]
            
            return plants[:limit]
            
        except Exception as e:
            logger.error(f"Error retrieving relevant plants: {str(e)}")
            return []
    
    def _rank_plants_semantically(self, query: str, plants: List) -> List:
        """Rank plants using semantic similarity"""
        try:
            # Create plant descriptions for embedding
            plant_texts = []
            for plant in plants:
                uses = json.loads(plant.uses) if plant.uses else []
                text = f"{plant.name} {plant.description} {' '.join(uses)} {plant.category}"
                plant_texts.append(text)
            
            # Generate embeddings
            query_embedding = self.model.encode([query])
            plant_embeddings = self.model.encode(plant_texts)
            
            # Calculate similarities
            similarities = cosine_similarity(query_embedding, plant_embeddings)[0]
            
            # Rank plants by similarity
            ranked_indices = np.argsort(similarities)[::-1]
            ranked_plants = [plants[i] for i in ranked_indices]
            
            return ranked_plants
            
        except Exception as e:
            logger.error(f"Error in semantic ranking: {str(e)}")
            return plants
    
    def generate_response(self, query: str, relevant_plants: List) -> str:
        """Generate comprehensive response using retrieved plants"""
        try:
            if not relevant_plants:
                return self._generate_fallback_response(query)
            
            # Determine response type based on query
            intent = self._classify_query_intent(query)
            
            if intent == 'information' and len(relevant_plants) == 1:
                return self._generate_plant_info_response(relevant_plants[0])
            elif intent == 'treatment':
                return self._generate_treatment_response(query, relevant_plants)
            else:
                return self._generate_general_response(query, relevant_plants)
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return self._generate_fallback_response(query)
    
    def _classify_query_intent(self, query: str) -> str:
        """Classify the intent of the query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['what is', 'tell me about', 'information about']):
            return 'information'
        elif any(word in query_lower for word in ['cure', 'treatment', 'remedy', 'heal', 'help with']):
            return 'treatment'
        elif any(word in query_lower for word in ['how to use', 'dosage', 'preparation']):
            return 'usage'
        else:
            return 'general'
    
    def _generate_plant_info_response(self, plant) -> str:
        """Generate detailed information response for a specific plant"""
        try:
            uses = json.loads(plant.uses) if plant.uses else []
            properties = json.loads(plant.properties) if plant.properties else {}
            
            template = self.remedy_templates['information']
            response = template.format(
                plant_name=plant.name,
                scientific_name=plant.scientific_name,
                system=plant.ayush_system,
                category=plant.category or 'General',
                description=plant.description or 'Traditional medicinal plant',
                uses=self._format_uses(uses),
                properties=self._format_properties(properties),
                preparation=plant.preparation or 'Consult with qualified practitioner for preparation methods',
                contraindications=plant.contraindications or 'Generally safe when used appropriately'
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating plant info response: {str(e)}")
            return f"Information about {plant.name} from {plant.ayush_system} tradition."
    
    def _generate_treatment_response(self, query: str, plants: List) -> str:
        """Generate treatment-focused response"""
        try:
            # Extract symptom from query
            symptom = self._extract_main_symptom(query)
            
            # Get primary system
            system = plants[0].ayush_system if plants else 'traditional medicine'
            
            # Build plant information
            plant_info = []
            for i, plant in enumerate(plants[:3]):  # Top 3 plants
                uses = json.loads(plant.uses) if plant.uses else []
                plant_info.append(f"**{i+1}. {plant.name}** ({plant.scientific_name})\n"
                                f"   - Uses: {', '.join(uses[:3])}\n"
                                f"   - {plant.description[:100]}...")
            
            # Combine preparation methods
            preparations = []
            for plant in plants[:3]:
                if plant.preparation:
                    preparations.append(f"• {plant.name}: {plant.preparation[:100]}...")
            
            template = self.remedy_templates['treatment']
            response = template.format(
                system=system,
                symptom=symptom,
                plant_info='\n\n'.join(plant_info),
                preparation='\n'.join(preparations) if preparations else 'Consult qualified practitioner for preparation methods'
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating treatment response: {str(e)}")
            return "Please consult with a qualified healthcare provider for treatment advice."
    
    def _generate_general_response(self, query: str, plants: List) -> str:
        """Generate general informational response"""
        try:
            # Build relevant information
            relevant_info = []
            for plant in plants[:3]:
                uses = json.loads(plant.uses) if plant.uses else []
                relevant_info.append(f"**{plant.name}**: {plant.description[:100]}... "
                                   f"Traditional uses include {', '.join(uses[:2])}.")
            
            # Build recommendations
            recommendations = []
            for plant in plants[:2]:
                recommendations.append(f"• Consider {plant.name} for its traditional benefits")
            
            # Add safety notes
            safety_notes = [
                "• Always consult healthcare provider before use",
                "• Start with small doses to test tolerance",
                "• Be aware of potential interactions with medications"
            ]
            
            template = self.remedy_templates['general']
            response = template.format(
                query=query,
                relevant_info='\n\n'.join(relevant_info),
                recommendations='\n'.join(recommendations),
                safety_notes='\n'.join(safety_notes)
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating general response: {str(e)}")
            return "I found some relevant herbal information, but please consult with a qualified practitioner."
    
    def _generate_fallback_response(self, query: str) -> str:
        """Generate fallback response when no relevant plants found"""
        return f"""I understand you're asking about "{query}". While I don't have specific information in my current database, I recommend:

• Consulting with a qualified Ayurvedic, Unani, or other traditional medicine practitioner
• Visiting a local herbal medicine expert
• Checking with certified herbalists in your area

Traditional medicine systems have extensive knowledge that may help with your query. Always ensure you're working with qualified practitioners for safe and effective treatment.

Would you like to try rephrasing your question or asking about a specific herb or condition?"""
    
    def _extract_main_symptom(self, query: str) -> str:
        """Extract the main symptom from query"""
        query_lower = query.lower()
        
        # Common symptom patterns
        symptoms = {
            'pain': ['pain', 'ache', 'hurt'],
            'digestive issues': ['stomach', 'digestion', 'gastric', 'acidity'],
            'respiratory problems': ['cough', 'cold', 'breathing'],
            'skin conditions': ['skin', 'rash', 'eczema'],
            'stress': ['stress', 'anxiety', 'tension'],
            'inflammation': ['inflammation', 'swelling']
        }
        
        for symptom, keywords in symptoms.items():
            if any(keyword in query_lower for keyword in keywords):
                return symptom
        
        return 'general health concerns'
    
    def _format_uses(self, uses: List[str]) -> str:
        """Format uses list for display"""
        if not uses:
            return "Various traditional applications"
        return "• " + "\n• ".join(uses[:5])  # Show first 5 uses
    
    def _format_properties(self, properties: Dict) -> str:
        """Format properties for display"""
        if not properties:
            return "Traditional properties not specified"
        
        formatted = []
        for key, value in properties.items():
            formatted.append(f"**{key.title()}:** {value}")
        
        return "\n".join(formatted)