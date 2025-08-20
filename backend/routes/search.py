import json
import os
import re
from flask import Blueprint, request, jsonify
from sentence_transformers import SentenceTransformer, util
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Main API Blueprint - Single entry point for frontend
search_bp = Blueprint("api", __name__)

# Load model and data
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
DATA_FILE = os.path.join(os.path.dirname(__file__), "../../database/data.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    herbs_data = json.load(f)

class RequestAnalyzer:
    """Analyzes incoming requests to determine the best response strategy"""
    
    @staticmethod
    def analyze_query(query, request_context=None):
        """
        Analyze the query and return the appropriate action
        Returns: dict with 'action', 'confidence', and 'metadata'
        """
        if not query or not query.strip():
            return {
                "action": "error",
                "confidence": 1.0,
                "metadata": {"error": "Empty query"}
            }
        
        query = query.strip()
        query_lower = query.lower()
        word_count = len(query.split())
        char_count = len(query)
        
        # Check if it's a suggestion request (partial/incomplete query)
        if RequestAnalyzer._is_suggestion_request(query, request_context):
            return {
                "action": "suggest",
                "confidence": 0.9,
                "metadata": {"query_type": "partial", "word_count": word_count}
            }
        
        # Check if it's a complete search request
        if RequestAnalyzer._is_search_request(query):
            search_strategy = RequestAnalyzer._determine_search_strategy(query)
            return {
                "action": "search",
                "confidence": 0.95,
                "metadata": {
                    "query_type": "complete",
                    "strategy": search_strategy,
                    "word_count": word_count,
                    "char_count": char_count
                }
            }
        
        # Default to search for ambiguous cases
        return {
            "action": "search",
            "confidence": 0.7,
            "metadata": {"query_type": "ambiguous", "word_count": word_count}
        }
    
    @staticmethod
    def _is_suggestion_request(query, context):
        """Determine if this should trigger suggestions"""
        # Short queries (1-2 characters) are typically for suggestions
        if len(query) <= 2:
            return True
        
        # If context indicates user is typing (from frontend)
        if context and context.get("typing", False):
            return True
            
        # Incomplete words or partial matches
        if len(query) <= 4 and len(query.split()) == 1:
            return True
            
        return False
    
    @staticmethod
    def _is_search_request(query):
        """Determine if this is a complete search request"""
        # Complete words, multiple words, or specific patterns
        if len(query) >= 3 and (len(query.split()) > 1 or len(query) > 4):
            return True
        
        # Single complete herb names
        herb_names = [herb.get("name", "").lower() for herb in herbs_data]
        all_alt_names = []
        for herb in herbs_data:
            all_alt_names.extend([name.lower() for name in herb.get("alt_names", [])])
        
        if query.lower() in herb_names or query.lower() in all_alt_names:
            return True
            
        return False
    
    @staticmethod
    def _determine_search_strategy(query):
        """Determine the best search strategy"""
        query_lower = query.lower()
        word_count = len(query.split())
        
        # Check for exact herb names
        herb_names = [herb.get("name", "").lower() for herb in herbs_data]
        if query_lower in herb_names:
            return "exact_match"
        
        # Check for health conditions or symptoms
        health_keywords = [
            "pain", "stress", "immunity", "digestion", "sleep", "skin", "hair",
            "cold", "fever", "headache", "joint", "memory", "energy", "detox"
        ]
        if any(keyword in query_lower for keyword in health_keywords):
            return "symptom_based"
        
        # Single word queries
        if word_count == 1:
            return "single_term"
        
        # Multi-word queries
        if word_count > 3:
            return "semantic"
        
        return "hybrid"

class IntelligentHerbalSearch:
    def __init__(self, herbs_data, model):
        self.herbs_data = herbs_data
        self.model = model
        self.prepare_search_data()
        
    def prepare_search_data(self):
        """Prepare comprehensive search data with multiple indexing strategies"""
        # Create exact match index for names
        self.name_index = {}
        self.alt_name_index = {}
        
        # Prepare semantic search data
        self.semantic_texts = []
        self.keyword_texts = []
        
        for i, herb in enumerate(self.herbs_data):
            # Exact name matching
            herb_name = herb.get("name", "").lower().strip()
            self.name_index[herb_name] = i
            
            # Alternative names
            for alt_name in herb.get("alt_names", []):
                self.alt_name_index[alt_name.lower().strip()] = i
            
            # Semantic search text (comprehensive)
            semantic_parts = [
                herb.get("name", ""),
                herb.get("scientific_name", ""),
                " ".join(herb.get("alt_names", [])),
                " ".join(herb.get("uses", [])),
                " ".join(herb.get("therapies", [])),
                herb.get("ayush_system", "")
            ]
            self.semantic_texts.append(" ".join(filter(None, semantic_parts)))
            
            # Keyword search text (focused)
            keyword_parts = [
                herb.get("name", ""),
                " ".join(herb.get("alt_names", [])),
                " ".join(herb.get("uses", []))
            ]
            self.keyword_texts.append(" ".join(filter(None, keyword_parts)).lower())
        
        # Create embeddings for semantic search
        print("Creating semantic embeddings...")
        self.semantic_embeddings = self.model.encode(
            self.semantic_texts, 
            convert_to_tensor=True, 
            normalize_embeddings=True,
            show_progress_bar=True
        )
        
        # Create TF-IDF vectorizer for keyword search
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            stop_words=None,  # Keep all words for multilingual support
            lowercase=True,
            max_features=5000
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.keyword_texts)
    
    def search(self, query, strategy="hybrid"):
        """Comprehensive search with strategy-based optimization"""
        if not query or not query.strip():
            return []
        
        query = query.strip()
        all_results = []
        seen_herbs = set()
        
        if strategy == "exact_match":
            return self._exact_match_search(query)
        elif strategy == "single_term":
            return self._single_term_search(query)
        elif strategy == "symptom_based":
            return self._symptom_based_search(query)
        elif strategy == "semantic":
            return self._semantic_heavy_search(query)
        else:  # hybrid approach
            return self._hybrid_search(query)
    
    def _exact_match_search(self, query):
        """Optimized for exact herb name searches"""
        query_lower = query.lower().strip()
        results = []
        
        if query_lower in self.name_index:
            results.append({
                "herb": self.herbs_data[self.name_index[query_lower]],
                "score": 1.0,
                "match_type": "exact_name"
            })
            
        if query_lower in self.alt_name_index:
            idx = self.alt_name_index[query_lower]
            if not any(r["herb"]["name"] == self.herbs_data[idx]["name"] for r in results):
                results.append({
                    "herb": self.herbs_data[idx],
                    "score": 0.95,
                    "match_type": "alt_name"
                })
        
        return results
    
    def _single_term_search(self, query):
        """Optimized for single word searches"""
        results = []
        seen_herbs = set()
        
        # First try exact matches
        exact_results = self._exact_match_search(query)
        for result in exact_results:
            results.append(result)
            seen_herbs.add(result["herb"]["name"])
        
        # Then try partial matches if no exact match
        if not exact_results:
            query_lower = query.lower()
            for herb in self.herbs_data:
                if herb["name"] in seen_herbs:
                    continue
                    
                # Check main name
                if query_lower in herb.get("name", "").lower():
                    results.append({
                        "herb": herb,
                        "score": 0.8,
                        "match_type": "partial_name"
                    })
                    seen_herbs.add(herb["name"])
                    continue
                
                # Check alternative names
                for alt_name in herb.get("alt_names", []):
                    if query_lower in alt_name.lower():
                        results.append({
                            "herb": herb,
                            "score": 0.75,
                            "match_type": "partial_alt_name"
                        })
                        seen_herbs.add(herb["name"])
                        break
        
        return sorted(results, key=lambda x: x["score"], reverse=True)[:5]
    
    def _symptom_based_search(self, query):
        """Optimized for health condition/symptom searches"""
        query_embedding = self.model.encode(
            query,
            convert_to_tensor=True,
            normalize_embeddings=True
        )
        
        cosine_scores = util.cos_sim(query_embedding, self.semantic_embeddings)[0]
        
        results = []
        threshold = 0.2  # Lower threshold for symptom matching
        
        for i, score in enumerate(cosine_scores):
            if float(score) >= threshold:
                results.append({
                    "herb": self.herbs_data[i],
                    "score": float(score),
                    "match_type": "symptom_match"
                })
        
        return sorted(results, key=lambda x: x["score"], reverse=True)[:5]
    
    def _semantic_heavy_search(self, query):
        """Optimized for complex, multi-word semantic searches"""
        return self._symptom_based_search(query)  # Similar approach
    
    def _hybrid_search(self, query):
        """The original comprehensive hybrid approach"""
        all_results = []
        seen_herbs = set()
        
        # 1. Exact match search (highest priority)
        exact_results = self._exact_match_search(query)
        for result in exact_results:
            herb_name = result["herb"]["name"]
            if herb_name not in seen_herbs:
                all_results.append(result)
                seen_herbs.add(herb_name)
        
        # 2. Semantic search
        if len(all_results) < 3:  # Only if we need more results
            semantic_results = self._symptom_based_search(query)
            for result in semantic_results:
                herb_name = result["herb"]["name"]
                if herb_name not in seen_herbs and len(all_results) < 5:
                    all_results.append(result)
                    seen_herbs.add(herb_name)
        
        return sorted(all_results, key=lambda x: x["score"], reverse=True)[:5]
    
    def get_suggestions(self, partial_query):
        """Get suggestions for partial queries"""
        if len(partial_query) < 2:
            return []
        
        partial_query = partial_query.lower()
        suggestions = []
        
        for herb in self.herbs_data:
            # Check main name
            if partial_query in herb.get("name", "").lower():
                suggestions.append({
                    "text": herb.get("name"),
                    "type": "herb_name"
                })
            
            # Check alternative names
            for alt_name in herb.get("alt_names", []):
                if partial_query in alt_name.lower():
                    suggestions.append({
                        "text": alt_name,
                        "type": "alt_name",
                        "herb": herb.get("name")
                    })
            
            # Check uses for context
            for use in herb.get("uses", []):
                if partial_query in use.lower():
                    suggestions.append({
                        "text": f"{use} ({herb.get('name')})",
                        "type": "use_case",
                        "herb": herb.get("name")
                    })
        
        # Remove duplicates and limit
        seen = set()
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion["text"] not in seen:
                unique_suggestions.append(suggestion)
                seen.add(suggestion["text"])
        
        return unique_suggestions[:8]

# Initialize the system
print("Initializing AYUSH Herbal Search System...")
search_system = IntelligentHerbalSearch(herbs_data, model)
print("Search system ready!")

# SINGLE ENTRY POINT - This is what frontend calls
@search_bp.route("/query", methods=["POST"])
def handle_query():
    """
    Single entry point for all frontend requests
    Intelligently routes to appropriate handler based on query analysis
    """
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        context = data.get("context", {})  # Frontend can send additional context
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Query is required"
            }), 400
        
        # Analyze the request
        analysis = RequestAnalyzer.analyze_query(query, context)
        
        if analysis["action"] == "error":
            return jsonify({
                "success": False,
                "error": analysis["metadata"]["error"]
            }), 400
        
        elif analysis["action"] == "suggest":
            # Handle suggestion request
            suggestions = search_system.get_suggestions(query)
            return jsonify({
                "success": True,
                "action": "suggest",
                "query": query,
                "suggestions": suggestions,
                "analysis": analysis
            })
        
        elif analysis["action"] == "search":
            # Handle search request
            strategy = analysis["metadata"].get("strategy", "hybrid")
            results = search_system.search(query, strategy)
            
            return jsonify({
                "success": True,
                "action": "search",
                "query": query,
                "total_results": len(results),
                "results": results,
                "analysis": analysis
            })
        
        else:
            return jsonify({
                "success": False,
                "error": "Unknown action"
            }), 400

    except Exception as e:
        print(f"API Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@search_bp.route("/health", methods=["GET"])
def health_check():
    """System health check"""
    return jsonify({
        "status": "healthy",
        "model": "paraphrase-multilingual-mpnet-base-v2",
        "total_herbs": len(herbs_data),
        "endpoints": {
            "main": "/api/query",
            "health": "/api/health"
        }
    })

# Optional: Direct endpoints for advanced users (but frontend should use /query)
@search_bp.route("/search", methods=["POST"])
def direct_search():
    """Direct search endpoint (legacy/advanced use)"""
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        strategy = data.get("strategy", "hybrid")
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        results = search_system.search(query, strategy)
        return jsonify({
            "query": query,
            "strategy": strategy,
            "total_results": len(results),
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@search_bp.route("/suggest", methods=["POST"])
def direct_suggest():
    """Direct suggestion endpoint (legacy/advanced use)"""
    try:
        data = request.get_json(force=True)
        partial_query = data.get("query", "").strip()
        
        suggestions = search_system.get_suggestions(partial_query)
        return jsonify({
            "query": partial_query,
            "suggestions": suggestions
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500