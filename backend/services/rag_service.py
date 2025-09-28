import json
import logging
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import or_ 
logger = logging.getLogger(__name__)

class RAGService:
    """Retrieval-Augmented Generation service for herbal knowledge"""
    
    def __init__(self, plant_model, remedy_model=None):
        self.Plant = plant_model
        self.Remedy = remedy_model
        self.model = None
        self.plant_embeddings = {}
        self.remedy_templates = self._load_remedy_templates()

    def _uses_list(self, val):
        """Return uses as a clean list no matter the source type."""
        if not val:
            return []
        if isinstance(val, list):
            return val
        if isinstance(val, str):
            # try JSON first
            try:
                j = json.loads(val)
                if isinstance(j, list):
                    return j
            except Exception:
                pass
            # fallback: split by '|' or ','
            return [p.strip() for p in val.replace("|", ",").split(",") if p.strip()]
        return []

    def _properties_dict(self, val):
        if not val:
            return {}
        if isinstance(val, dict):
            return val
        if isinstance(val, str):
            try:
                j = json.loads(val)
                return j if isinstance(j, dict) else {}
            except Exception:
                return {}
        return {}

    def _to_view(self, p):
        """
        Accepts either a SQLAlchemy Plant instance or a dict,
        returns a normalized dict with consistent keys.
        """
        if isinstance(p, dict):
            name = p.get("name")
            sci = p.get("scientific_name")
            return {
                "id": p.get("id"),
                "name": name or "",
                "scientific_name": sci or "",
                "ayush_system": p.get("ayush_system") or "",
                "category": p.get("category") or "",
                "uses": self._uses_list(p.get("uses")),
                "description": p.get("description") or "",
                "preparation": p.get("preparation") or "",
                "contraindications": p.get("contraindications") or "",
                "properties": self._properties_dict(p.get("properties")),
                "image_path": p.get("image_path") or "",
            }
        # assume model
        return {
            "id": getattr(p, "id", None),
            "name": getattr(p, "name", "") or "",
            "scientific_name": getattr(p, "scientific_name", "") or "",
            "ayush_system": getattr(p, "ayush_system", "") or "",
            "category": getattr(p, "category", "") or "",
            "uses": self._uses_list(getattr(p, "uses", None)),
            "description": getattr(p, "description", "") or "",
            "preparation": getattr(p, "preparation", "") or "",
            "contraindications": getattr(p, "contraindications", "") or "",
            "properties": self._properties_dict(getattr(p, "properties", None)),
            "image_path": getattr(p, "image_path", "") or "",
        }

    # ------------- MAIN RETRIEVAL -------------
    def get_relevant_plants(self, processed_query: Dict, limit: int = 5) -> List:
        """
        Return SQLAlchemy Plant model instances (NOT dicts).
        """
        try:
            Plant = self.Plant
            symptoms = processed_query.get('symptoms', []) or []
            herbs = processed_query.get('herbs', []) or []
            ayush_system = processed_query.get('ayush_system')
            key_phrases = processed_query.get('key_phrases', []) or []

            query = Plant.query
            if ayush_system:
                query = query.filter(Plant.ayush_system.ilike(f"%{ayush_system}%"))

            terms = symptoms + herbs + key_phrases
            if terms:
                conds = []
                for t in terms:
                    conds.extend([
                        Plant.name.ilike(f"%{t}%"),
                        Plant.scientific_name.ilike(f"%{t}%"),
                        Plant.description.ilike(f"%{t}%"),
                        Plant.category.ilike(f"%{t}%"),
                        Plant.uses.ilike(f"%{t}%"),
                    ])
                query = query.filter(or_(*conds))

            candidates = query.limit(limit * 2).all()

            # (Optional) semantic ranking if you wired an embedding model
            if getattr(self, "model", None) and candidates:
                return self._rank_plants_semantically(
                    processed_query.get("cleaned_query") or "",
                    candidates
                )[:limit]

            return candidates[:limit]

        except Exception as e:
            logger.error(f"Error retrieving relevant plants: {str(e)}")
            return []

    def get_relevant_remedies(self, processed_query: dict, limit: int = 3):
        """Return a list of Remedy model instances best matching symptom/phrases."""
        try:
            Remedy = self.Remedy
            if Remedy is None:
                return []
            terms = (processed_query.get("symptoms") or []) + (processed_query.get("key_phrases") or [])
            q = Remedy.query
            if terms:
                conds = [Remedy.symptom.ilike(f"%{t}%") for t in terms]
                q = q.filter(or_(*conds))
            return q.order_by(Remedy.id.desc()).limit(limit).all()
        except Exception as e:
            import logging; logging.getLogger(__name__).error(f"get_relevant_remedies failed: {e}")
            return []

    def _rank_plants_semantically(self, query: str, plants: List) -> List:
        try:
            if not getattr(self, "model", None) or not plants:
                return plants
            texts = []
            for p in plants:
                v = self._to_view(p)
                texts.append(f"{v['name']} {v['description']} {' '.join(v['uses'])} {v['category']}")
            q_emb = self.model.encode([query])
            p_emb = self.model.encode(texts)
            sims = cosine_similarity(q_emb, p_emb)[0]
            order = np.argsort(sims)[::-1]
            return [plants[i] for i in order]
        except Exception as e:
            logger.error(f"Error in semantic ranking: {str(e)}")
            return plants
   
    # ------------- RESPONSE GENERATION -------------
    def generate_response(self, query: str, relevant_plants: list, remedies: list | None = None) -> str:
        """Accepts models (preferred) or dicts; normalizes internally."""
        try:
            remedies = remedies or []
            if not relevant_plants:
                return self._generate_fallback_response(query)
            
            intent = self._classify_query_intent(query)
            if remedies and (intent == "treatment" or (not relevant_plants)):
                return self._generate_from_remedies(query, remedies)

            intent = self._classify_query_intent(query)
            if intent == "information" and len(relevant_plants) == 1:
                return self._generate_plant_info_response(relevant_plants[0])
            elif intent == 'treatment':
                return self._generate_treatment_response(query, relevant_plants)
            else:
                return self._generate_general_response(query, relevant_plants)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return self._generate_fallback_response(query)
    
    def _generate_from_remedies(self, query: str, remedies: list) -> str:
        """Format a remedy-driven answer."""
        try:
            Plant = self.Plant
            lines = []
            for r in remedies[:3]:
                # plant_ids are stored as comma-separated ints (e.g., "1,3,7")
                ids = []
                if isinstance(r.plant_ids, str):
                    ids = [int(x) for x in r.plant_ids.replace(" ", "").split(",") if x.isdigit()]
                # look up plant names
                plants = Plant.query.filter(Plant.id.in_(ids)).all() if ids else []
                plant_names = ", ".join([p.name for p in plants]) if plants else "—"
                lines.append(
                    "\n".join(filter(None, [
                        f"**Symptom:** {r.symptom}",
                        f"**Suggested Plants:** {plant_names}",
                        f"**Dosage/Usage:** {r.dosage or '—'}",
                        f"**Preparation:** {r.preparation_method or '—'}",
                        f"**Lifestyle:** {r.lifestyle_recommendations or '—'}",
                        f"**System:** {r.ayush_system or '—'}",
                    ]))
                )
            safety = "\n".join([
                "• Educational use only — not medical advice.",
                "• Check allergies, interactions and contraindications.",
                "• Consult a qualified practitioner for dosing."
            ])
            return "\n\n".join([
                f"Here are traditional recommendations related to **{query}**:",
                "\n\n---\n\n".join(lines) if lines else "—",
                "\n**Safety Notes:**\n" + safety
            ]).strip()
        except Exception as e:
            import logging; logging.getLogger(__name__).error(f"_generate_from_remedies failed: {e}")
            return "I found relevant traditional remedies, but couldn’t format them safely."


    def _generate_plant_info_response(self, plant) -> str:
        try:
            v = self._to_view(plant)
            uses = v["uses"]
            props = v["properties"]
            return "\n".join([
                f"**{v['name']}** ({v['scientific_name']})",
                f"**Traditional System:** {v['ayush_system']}",
                f"**Category:** {v['category']}",
                "",
                "**Description:**",
                v["description"] or "—",
                "",
                "**Traditional Uses:**",
                ("• " + "\n• ".join(uses)) if uses else "—",
                "",
                f"**Properties:** {', '.join(f'{k}: {val}' for k, val in props.items())}" if props else "**Properties:** —",
                "",
                "**Preparation Methods:**",
                v["preparation"] or "—",
                "",
                "**Safety Notes:**",
                (v["contraindications"] or "—") + "\n• Educational use only — not medical advice."
            ])
        except Exception as e:
            logger.error(f"Error generating plant info response: {str(e)}")
            return "I found information on this plant, but couldn't format details safely."

    def _generate_treatment_response(self, query: str, plants: List) -> str:
        try:
            def line(p):
                v = self._to_view(p)
                uses = v["uses"]
                return (
                    f"**{v['name']}** ({v['scientific_name']}) — "
                    f"Uses: {', '.join(uses[:3]) if uses else '—'}; "
                    f"{(v['description'][:100] + '...') if v['description'] else ''}"
                )
            body = "\n".join(f"{i+1}. {line(p)}" for i, p in enumerate(plants[:3]))
            return "\n".join([
                f"For **{query}**, consider these traditional options:",
                body or "—",
                "",
                "**Preparation Examples:**",
                "\n".join([f"• {self._to_view(p)['name']}: {self._to_view(p)['preparation'][:100]}..." for p in plants[:3] if self._to_view(p)['preparation']]) or "—",
                "",
                "**Safety Notes:**",
                "• Educational use only — not medical advice.",
                "• Check allergies and drug interactions.",
                "• Consult a qualified practitioner for dosing."
            ])
        except Exception as e:
            logger.error(f"Error generating treatment response: {str(e)}")
            return "Please consult a qualified practitioner for personalized treatment guidance."

    def _generate_general_response(self, query: str, plants: List) -> str:
        try:
            bullets = []
            for p in plants[:3]:
                v = self._to_view(p)
                bullets.append(
                    f"• **{v['name']}** — {(v['description'][:110] + '...') if v['description'] else ''} "
                    f"{'(uses: ' + ', '.join(v['uses'][:2]) + ')' if v['uses'] else ''}"
                )
            return "\n".join([
                f"Here’s what I found related to **{query}**:",
                *(bullets or ["—"]),
                "",
                "**Safety Notes:**",
                "• Educational use only — not medical advice.",
                "• Consult a qualified practitioner."
            ])
        except Exception as e:
            logger.error(f"Error generating general response: {str(e)}")
            return "I found some relevant herbal information, but please consult with a qualified practitioner."

    ###############################################################################################################

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
            Plant = self.Plant  # <-- take from constructor

            # Extract search criteria
            symptoms = processed_query.get('symptoms', []) or []
            herbs = processed_query.get('herbs', []) or []
            ayush_system = processed_query.get('ayush_system')
            key_phrases = processed_query.get('key_phrases', []) or []

            # Build query
            query = Plant.query

            # Filter by AYUSH system if specified
            if ayush_system:
                query = query.filter(Plant.ayush_system.ilike(f'%{ayush_system}%'))

            # Text-based search across columns
            search_terms = (symptoms + herbs + key_phrases)
            if search_terms:
                conditions = []
                for term in search_terms:
                    conditions.extend([
                        Plant.name.ilike(f'%{term}%'),
                        Plant.scientific_name.ilike(f'%{term}%'),
                        Plant.description.ilike(f'%{term}%'),
                        Plant.uses.ilike(f'%{term}%'),
                        Plant.category.ilike(f'%{term}%')
                    ])
                if conditions:
                    query = query.filter(or_(*conditions))  # <-- not db.or_

            # Limit
            results = query.limit(limit).all()
            return [p.to_dict() for p in results]

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